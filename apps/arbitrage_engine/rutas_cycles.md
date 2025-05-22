Obtener todos los ciclos
GET http://localhost:8000/api/cycles/
Obtener ciclos activos
GET http://localhost:8000/api/cycles/active
Obtener un ciclo específico
GET http://localhost:8000/api/cycles/1

crear un nuevo ciclo
POST http://localhost:8000/api/cycles/
Content-Type: application/json

{
  "target_usdt": 1000.00
}

Finalizar un ciclo
PUT http://localhost:8000/api/cycles/1/finish
Eliminar un ciclo
DELETE http://localhost:8000/api/cycles/1

Registrar una compra
POST http://localhost:8000/api/cycles/1/transactions/buy
Content-Type: application/json

{
  "usdt_desired": 100.00,
  "commission_rate": 0.5,
  "purchase_price": 35.50
}
Registrar una venta
POST http://localhost:8000/api/cycles/1/transactions/sell
Content-Type: application/json

{
  "market_best_price": 36.20,
  "competitive_adjustment": 0.10,
  "usdt_sold": 100.00
}
Obtener compras pendientes
GET http://localhost:8000/api/cycles/1/pending-buys