from typing import List, Dict, Any
from fastapi import HTTPException
from mysql.connector import Error
from apps.arbitrage_engine.transaction_models import (
    CreateBuyTransactionRequest,
    CreateSellTransactionRequest,
    BuyTransactionResponse,
    SellTransactionResponse,
    PendingBuysResponse,
    CycleTransactionsResponse,
    LinkedBuy
)

class TransactionHandler:
    def __init__(self, db):
        self.db = db

    async def create_buy_transaction(
        self, 
        cycle_id: int, 
        transaction_data: CreateBuyTransactionRequest
    ) -> BuyTransactionResponse:
        """Registrar una compra"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Iniciar transacción
            self.db.start_transaction()
            
            # Verificar que el ciclo existe y está activo
            cycle_query = """
                SELECT * FROM cycles WHERE id = %s AND status = 'activo'
            """
            cursor.execute(cycle_query, (cycle_id,))
            cycle_row = cursor.fetchone()
            
            if not cycle_row:
                raise HTTPException(
                    status_code=404,
                    detail="Ciclo no encontrado o no está activo"
                )
            
            # Verificar que no exceda el objetivo del ciclo
            current_purchased = float(cycle_row['purchased_usdt'] or 0)
            target_usdt = float(cycle_row['target_usdt'])
            
            if current_purchased + transaction_data.usdt_desired > target_usdt:
                max_available = target_usdt - current_purchased
                raise HTTPException(
                    status_code=400,
                    detail=f"Esta compra excedería el objetivo del ciclo ({target_usdt} USDT). "
                           f"Máximo disponible: {max_available:.2f} USDT"
                )
            
            # Insertar la transacción de compra
            insert_query = """
                INSERT INTO transactions (
                    cycle_id, transaction_type, usdt_desired, commission_rate,
                    purchase_price, usdt_to_pay, total_investment_bs, 
                    real_purchase_price, buy_status
                ) VALUES (%s, 'compra', %s, %s, %s, %s, %s, %s, 'pendiente')
            """
            
            cursor.execute(
                insert_query,
                (
                    cycle_id,
                    transaction_data.usdt_desired,
                    transaction_data.commission_rate,
                    transaction_data.purchase_price,
                    transaction_data.usdt_to_pay,
                    transaction_data.total_investment_bs,
                    transaction_data.real_purchase_price
                )
            )
            
            # Obtener la transacción recién creada
            get_query = "SELECT * FROM transactions WHERE id = LAST_INSERT_ID()"
            cursor.execute(get_query)
            row = cursor.fetchone()
            
            self.db.commit()
            
            return BuyTransactionResponse(
                id=row['id'],
                cycle_id=row['cycle_id'],
                transaction_type=row['transaction_type'],
                usdt_desired=float(row['usdt_desired']),
                commission_rate=float(row['commission_rate']),
                purchase_price=float(row['purchase_price']),
                usdt_to_pay=float(row['usdt_to_pay']),
                total_investment_bs=float(row['total_investment_bs']),
                real_purchase_price=float(row['real_purchase_price']),
                buy_status=row['buy_status'],
                transaction_date=row['transaction_date']
            )
            
        except HTTPException:
            self.db.rollback()
            raise
        except Error as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al registrar la compra: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()

    async def create_sell_transaction(
        self, 
        cycle_id: int, 
        transaction_data: CreateSellTransactionRequest
    ) -> SellTransactionResponse:
        """Registrar una venta"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Iniciar transacción
            self.db.start_transaction()
            
            # Obtener compras pendientes del ciclo (FIFO)
            pending_buys_query = """
                SELECT * FROM transactions 
                WHERE cycle_id = %s AND transaction_type = 'compra' AND buy_status = 'pendiente'
                ORDER BY transaction_date ASC
            """
            cursor.execute(pending_buys_query, (cycle_id,))
            pending_buys_rows = cursor.fetchall()
            
            if not pending_buys_rows:
                raise HTTPException(
                    status_code=400,
                    detail="No hay compras pendientes para vender"
                )
            
            # Distribuir la venta entre las compras pendientes (FIFO)
            remaining_to_sell = transaction_data.usdt_sold
            linked_buys = []
            
            for buy_row in pending_buys_rows:
                if remaining_to_sell <= 0:
                    break
                
                sell_from_this_buy = min(remaining_to_sell, float(buy_row['usdt_desired']))
                linked_buys.append({
                    'buy_id': buy_row['id'],
                    'amount': sell_from_this_buy,
                    'buy_price': float(buy_row['real_purchase_price'])
                })
                
                remaining_to_sell -= sell_from_this_buy
            
            if remaining_to_sell > 0:
                raise HTTPException(
                    status_code=400,
                    detail="No hay suficientes USDT disponibles para vender"
                )
            
            # Insertar la transacción de venta
            sell_insert_query = """
                INSERT INTO transactions (
                    cycle_id, transaction_type, market_best_price, competitive_adjustment,
                    sale_price, usdt_sold, profit_bs, profit_percentage
                ) VALUES (%s, 'venta', %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(
                sell_insert_query,
                (
                    cycle_id,
                    transaction_data.market_best_price,
                    transaction_data.competitive_adjustment,
                    transaction_data.sale_price,
                    transaction_data.usdt_sold,
                    transaction_data.profit_bs,
                    transaction_data.profit_percentage
                )
            )
            
            # Obtener ID de la venta recién creada
            sell_transaction_id = cursor.lastrowid
            
            # Crear los vínculos y actualizar las compras
            for link in linked_buys:
                # Insertar el vínculo
                link_insert_query = """
                    INSERT INTO transaction_links 
                    (sell_transaction_id, buy_transaction_id, linked_amount, buy_price)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(
                    link_insert_query,
                    (
                        sell_transaction_id,
                        link['buy_id'],
                        link['amount'],
                        link['buy_price']
                    )
                )
                
                # Actualizar la compra
                buy_transaction = next(b for b in pending_buys_rows if b['id'] == link['buy_id'])
                new_usdt_desired = float(buy_transaction['usdt_desired']) - link['amount']
                
                if new_usdt_desired <= 0.00001:  # Considerando decimales
                    # Marcar como completada
                    cursor.execute(
                        """UPDATE transactions 
                           SET buy_status = 'completado', updated_at = CURRENT_TIMESTAMP
                           WHERE id = %s""",
                        (link['buy_id'],)
                    )
                else:
                    # Actualizar cantidades pendientes
                    original_usdt = float(buy_transaction['usdt_desired'])
                    ratio = new_usdt_desired / original_usdt
                    
                    new_investment = float(buy_transaction['total_investment_bs']) * ratio
                    new_usdt_to_pay = float(buy_transaction['usdt_to_pay']) * ratio
                    
                    cursor.execute(
                        """UPDATE transactions 
                           SET usdt_desired = %s, total_investment_bs = %s, 
                               usdt_to_pay = %s, updated_at = CURRENT_TIMESTAMP
                           WHERE id = %s""",
                        (new_usdt_desired, new_investment, new_usdt_to_pay, link['buy_id'])
                    )
            
            # Obtener la venta completa para la respuesta
            get_sell_query = "SELECT * FROM transactions WHERE id = %s"
            cursor.execute(get_sell_query, (sell_transaction_id,))
            sell_row = cursor.fetchone()
            
            self.db.commit()
            
            # Preparar linked_buys para respuesta
            linked_buys_response = [
                LinkedBuy(
                    buy_id=link['buy_id'],
                    amount=link['amount'],
                    buy_price=link['buy_price']
                )
                for link in linked_buys
            ]
            
            return SellTransactionResponse(
                id=sell_row['id'],
                cycle_id=sell_row['cycle_id'],
                transaction_type=sell_row['transaction_type'],
                market_best_price=float(sell_row['market_best_price']),
                competitive_adjustment=float(sell_row['competitive_adjustment']) if sell_row['competitive_adjustment'] else None,
                sale_price=float(sell_row['sale_price']),
                usdt_sold=float(sell_row['usdt_sold']),
                profit_bs=float(sell_row['profit_bs']) if sell_row['profit_bs'] else None,
                profit_percentage=float(sell_row['profit_percentage']) if sell_row['profit_percentage'] else None,
                transaction_date=sell_row['transaction_date'],
                linked_buys=linked_buys_response
            )
            
        except HTTPException:
            self.db.rollback()
            raise
        except Error as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al registrar la venta: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()

    async def get_pending_buys(self, cycle_id: int) -> PendingBuysResponse:
        """Obtener compras pendientes de un ciclo"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            
            query = """
                SELECT * FROM transactions 
                WHERE cycle_id = %s AND transaction_type = 'compra' AND buy_status = 'pendiente'
                ORDER BY transaction_date ASC
            """
            
            cursor.execute(query, (cycle_id,))
            rows = cursor.fetchall()
            
            pending_buys = [
                BuyTransactionResponse(
                    id=row['id'],
                    cycle_id=row['cycle_id'],
                    transaction_type=row['transaction_type'],
                    usdt_desired=float(row['usdt_desired']),
                    commission_rate=float(row['commission_rate']),
                    purchase_price=float(row['purchase_price']),
                    usdt_to_pay=float(row['usdt_to_pay']),
                    total_investment_bs=float(row['total_investment_bs']),
                    real_purchase_price=float(row['real_purchase_price']),
                    buy_status=row['buy_status'],
                    transaction_date=row['transaction_date']
                )
                for row in rows
            ]
            
            total_available = sum(buy.usdt_desired for buy in pending_buys)
            
            return PendingBuysResponse(
                pending_buys=pending_buys,
                total_available_usdt=total_available
            )
            
        except Error as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener las compras pendientes: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()
    
    async def get_cycle_transactions(self, cycle_id: int) -> CycleTransactionsResponse:
        """Obtener todas las transacciones de un ciclo"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Obtener todas las transacciones del ciclo
            query = """
                SELECT * FROM transactions 
                WHERE cycle_id = %s 
                ORDER BY transaction_date ASC
            """
            
            cursor.execute(query, (cycle_id,))
            rows = cursor.fetchall()
            
            transactions = []
            
            for row in rows:
                if row['transaction_type'] == 'compra':
                    # Transacción de compra
                    transaction = {
                        "id": row['id'],
                        "cycle_id": row['cycle_id'],
                        "type": "compra",
                        "date": row['transaction_date'].strftime("%Y-%m-%d %H:%M:%S"),
                        "usdtDeseados": float(row['usdt_desired']),
                        "comision": float(row['commission_rate']),
                        "precioCompra": float(row['purchase_price']),
                        "usdtAPagar": float(row['usdt_to_pay']),
                        "inversionTotalBs": float(row['total_investment_bs']),
                        "precioRealCompra": float(row['real_purchase_price']),
                        "status": row['buy_status']
                    }
                else:
                    # Transacción de venta
                    # Obtener las compras vinculadas
                    link_query = """
                        SELECT tl.linked_amount, tl.buy_price, tl.buy_transaction_id
                        FROM transaction_links tl
                        WHERE tl.sell_transaction_id = %s
                    """
                    cursor.execute(link_query, (row['id'],))
                    links = cursor.fetchall()
                    
                    linked_buys = [
                        {
                            "buyId": link['buy_transaction_id'],
                            "amount": float(link['linked_amount']),
                            "buyPrice": float(link['buy_price'])
                        }
                        for link in links
                    ]
                    
                    transaction = {
                        "id": row['id'],
                        "cycle_id": row['cycle_id'],
                        "type": "venta",
                        "date": row['transaction_date'].strftime("%Y-%m-%d %H:%M:%S"),
                        "mejorPrecioMercado": float(row['market_best_price']),
                        "ajusteCompetitivo": float(row['competitive_adjustment']),
                        "precioVenta": float(row['sale_price']),
                        "usdtVendidos": float(row['usdt_sold']),
                        "gananciaBs": float(row['profit_bs']),
                        "gananciaPorcentaje": float(row['profit_percentage']),
                        "linkedBuys": linked_buys
                    }
                
                transactions.append(transaction)
            
            return CycleTransactionsResponse(
                cycle_id=cycle_id,
                transactions=transactions,
                total_transactions=len(transactions)
            )
            
        except Error as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener las transacciones del ciclo: {str(e)}"
            )
        finally:
            if cursor:  
                cursor.close()

        