from typing import List, Optional
from fastapi import HTTPException
from mysql.connector import Error
from .cycle_models import CycleResponse, CycleWithTransactionsResponse
import json

class CycleHandler:
    def __init__(self, db):
        self.db = db

    async def get_all_cycles(self) -> List[CycleResponse]:
        """Obtener todos los ciclos con progreso calculado"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT 
                    id, name, start_date, end_date, target_usdt, 
                    purchased_usdt, sold_usdt, total_invested, 
                    total_returned, total_profit, status,
                    CASE 
                        WHEN target_usdt > 0 THEN (purchased_usdt / target_usdt * 100)
                        ELSE 0 
                    END as purchase_progress,
                    CASE 
                        WHEN purchased_usdt > 0 THEN (sold_usdt / purchased_usdt * 100)
                        ELSE 0 
                    END as sell_progress
                FROM cycles 
                ORDER BY created_at DESC
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [
                CycleResponse(
                    id=row['id'],
                    name=row['name'],
                    start_date=row['start_date'],
                    end_date=row['end_date'],
                    target_usdt=float(row['target_usdt']),
                    purchased_usdt=float(row['purchased_usdt']),
                    sold_usdt=float(row['sold_usdt']),
                    total_invested=float(row['total_invested']),
                    total_returned=float(row['total_returned']),
                    total_profit=float(row['total_profit']),
                    status=row['status'],
                    purchase_progress=float(row['purchase_progress']),
                    sell_progress=float(row['sell_progress'])
                )
                for row in rows
            ]
            
        except Error as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener los ciclos: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()

    async def get_active_cycles(self) -> List[CycleResponse]:
        """Obtener solo ciclos activos"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT 
                    id, name, start_date, end_date, target_usdt, 
                    purchased_usdt, sold_usdt, total_invested, 
                    total_returned, total_profit, status,
                    CASE 
                        WHEN target_usdt > 0 THEN (purchased_usdt / target_usdt * 100)
                        ELSE 0 
                    END as purchase_progress,
                    CASE 
                        WHEN purchased_usdt > 0 THEN (sold_usdt / purchased_usdt * 100)
                        ELSE 0 
                    END as sell_progress
                FROM cycles 
                WHERE status = 'activo' 
                ORDER BY created_at DESC
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            return [
                CycleResponse(
                    id=row['id'],
                    name=row['name'],
                    start_date=row['start_date'],
                    end_date=row['end_date'],
                    target_usdt=float(row['target_usdt']),
                    purchased_usdt=float(row['purchased_usdt']),
                    sold_usdt=float(row['sold_usdt']),
                    total_invested=float(row['total_invested']),
                    total_returned=float(row['total_returned']),
                    total_profit=float(row['total_profit']),
                    status=row['status'],
                    purchase_progress=float(row['purchase_progress']),
                    sell_progress=float(row['sell_progress'])
                )
                for row in rows
            ]
            
        except Error as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener los ciclos activos: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()

    async def get_cycle_by_id(self, cycle_id: int) -> CycleWithTransactionsResponse:
        """Obtener un ciclo específico con sus transacciones"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Obtener información del ciclo
            cycle_query = "SELECT * FROM cycles WHERE id = %s"
            cursor.execute(cycle_query, (cycle_id,))
            cycle_row = cursor.fetchone()
            
            if not cycle_row:
                raise HTTPException(
                    status_code=404,
                    detail="Ciclo no encontrado"
                )
            
            # Obtener transacciones del ciclo
            transactions_query = """
                SELECT 
                    t.*,
                    (
                        SELECT JSON_ARRAYAGG(
                            JSON_OBJECT(
                                'buy_id', tl.buy_transaction_id,
                                'amount', tl.linked_amount,
                                'buy_price', tl.buy_price
                            )
                        )
                        FROM transaction_links tl 
                        WHERE tl.sell_transaction_id = t.id
                    ) as linked_buys
                FROM transactions t
                WHERE t.cycle_id = %s
                ORDER BY t.transaction_date
            """
            
            cursor.execute(transactions_query, (cycle_id,))
            transactions_rows = cursor.fetchall()
            
            # Convertir JSON strings a dicts
            for row in transactions_rows:
                if row['linked_buys']:
                    row['linked_buys'] = json.loads(row['linked_buys'])
                else:
                    row['linked_buys'] = []
            
            # Construir respuesta
            cycle = CycleWithTransactionsResponse(
                id=cycle_row['id'],
                name=cycle_row['name'],
                start_date=cycle_row['start_date'],
                end_date=cycle_row['end_date'],
                target_usdt=float(cycle_row['target_usdt']),
                purchased_usdt=float(cycle_row['purchased_usdt']),
                sold_usdt=float(cycle_row['sold_usdt']),
                total_invested=float(cycle_row['total_invested']),
                total_returned=float(cycle_row['total_returned']),
                total_profit=float(cycle_row['total_profit']),
                status=cycle_row['status'],
                transactions=transactions_rows
            )
            
            return cycle
            
        except HTTPException:
            raise
        except Error as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al obtener el ciclo: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()

    async def create_cycle(self, target_usdt: float) -> CycleResponse:
        """Crear un nuevo ciclo"""
        cursor = None
        try:
            if target_usdt <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="El objetivo de USDT debe ser un número positivo"
                )
            
            cursor = self.db.cursor(dictionary=True)
            
            # Contar ciclos existentes para generar el nombre
            count_query = "SELECT COUNT(*) FROM cycles"
            cursor.execute(count_query)
            count_result = cursor.fetchone()
            cycle_number = count_result['COUNT(*)'] + 1
            cycle_name = f"Ciclo {cycle_number}"
            
            # Insertar nuevo ciclo
            insert_query = """
                INSERT INTO cycles (name, target_usdt) 
                VALUES (%s, %s)
            """
            
            cursor.execute(insert_query, (cycle_name, target_usdt))
            self.db.commit()
            
            # Obtener el ciclo recién creado
            get_query = "SELECT * FROM cycles WHERE id = LAST_INSERT_ID()"
            cursor.execute(get_query)
            row = cursor.fetchone()
            
            return CycleResponse(
                id=row['id'],
                name=row['name'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                target_usdt=float(row['target_usdt']),
                purchased_usdt=float(row['purchased_usdt'] or 0),
                sold_usdt=float(row['sold_usdt'] or 0),
                total_invested=float(row['total_invested'] or 0),
                total_returned=float(row['total_returned'] or 0),
                total_profit=float(row['total_profit'] or 0),
                status=row['status'],
                purchase_progress=0.0,
                sell_progress=0.0
            )
            
        except HTTPException:
            raise
        except Error as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear el ciclo: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()

    async def finish_cycle(self, cycle_id: int) -> CycleResponse:
        """Finalizar un ciclo"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            
            update_query = """
                UPDATE cycles 
                SET status = 'completado', end_date = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND status = 'activo'
            """
            
            cursor.execute(update_query, (cycle_id,))
            self.db.commit()
            
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Ciclo no encontrado o ya está completado"
                )
            
            # Obtener el ciclo actualizado
            get_query = "SELECT * FROM cycles WHERE id = %s"
            cursor.execute(get_query, (cycle_id,))
            row = cursor.fetchone()
            
            # Calcular progreso
            purchase_progress = 0.0
            sell_progress = 0.0
            
            if row['target_usdt'] and float(row['target_usdt']) > 0:
                purchase_progress = (float(row['purchased_usdt'] or 0) / float(row['target_usdt'])) * 100
                
            if row['purchased_usdt'] and float(row['purchased_usdt']) > 0:
                sell_progress = (float(row['sold_usdt'] or 0) / float(row['purchased_usdt'])) * 100
            
            return CycleResponse(
                id=row['id'],
                name=row['name'],
                start_date=row['start_date'],
                end_date=row['end_date'],
                target_usdt=float(row['target_usdt']),
                purchased_usdt=float(row['purchased_usdt'] or 0),
                sold_usdt=float(row['sold_usdt'] or 0),
                total_invested=float(row['total_invested'] or 0),
                total_returned=float(row['total_returned'] or 0),
                total_profit=float(row['total_profit'] or 0),
                status=row['status'],
                purchase_progress=purchase_progress,
                sell_progress=sell_progress
            )
            
        except HTTPException:
            raise
        except Error as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al finalizar el ciclo: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()

    async def delete_cycle(self, cycle_id: int) -> None:
        """Eliminar un ciclo"""
        cursor = None
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Verificar si el ciclo existe
            check_query = "SELECT id FROM cycles WHERE id = %s"
            cursor.execute(check_query, (cycle_id,))
            exists = cursor.fetchone()
            
            if not exists:
                raise HTTPException(
                    status_code=404,
                    detail="Ciclo no encontrado"
                )
            
            # Eliminar el ciclo (las transacciones se eliminan en cascada)
            delete_query = "DELETE FROM cycles WHERE id = %s"
            cursor.execute(delete_query, (cycle_id,))
            self.db.commit()
            
        except HTTPException:
            raise
        except Error as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al eliminar el ciclo: {str(e)}"
            )
        finally:
            if cursor:
                cursor.close()