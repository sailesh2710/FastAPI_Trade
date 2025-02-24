from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from app.database.db import get_db_connection
from app.models.order import OrderCreate, OrderResponse
from typing import List
import json

router = APIRouter()

# Store active WebSocket connections
active_connections = set()

@router.websocket("/ws/orders")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time order updates.

    - Clients can connect to this WebSocket at `/ws/orders`
    - Whenever a new order is placed, all connected clients receive real-time updates.
    """
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)

# Function to broadcast order updates
async def broadcast_order_update(order_data):
    """Broadcasts a new order to all WebSocket clients."""
    disconnected_clients = []
    for connection in active_connections:
        try:
            await connection.send_text(json.dumps(order_data))
        except:
            disconnected_clients.append(connection)

    # Remove disconnected clients
    for client in disconnected_clients:
        active_connections.remove(client)

# Create order (POST /orders) with WebSocket Notification
@router.post(
    "/orders",
    response_model=OrderResponse,
    summary="Create a new trade order",
    description="""
    Places a new trade order in the system.

    - **symbol**: Stock symbol (e.g., AAPL, TSLA)
    - **price**: Order price
    - **quantity**: Number of shares
    - **order_type**: "buy" or "sell"
    
    **WebSocket Broadcast:** The new order will be broadcasted in real-time to all connected WebSocket clients.
    """
)
async def create_order(order: OrderCreate):
    """Handles new order creation and broadcasts updates via WebSocket."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO orders (symbol, price, quantity, order_type) VALUES (%s, %s, %s, %s) RETURNING id",
            (order.symbol, order.price, order.quantity, order.order_type),
        )
        order_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        order_data = OrderResponse(id=order_id, **order.dict())

        # Broadcast new order to WebSocket clients
        await broadcast_order_update(order_data.dict())

        return order_data
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# Get all orders (GET /orders)
@router.get(
    "/orders",
    response_model=List[OrderResponse],
    summary="Retrieve all trade orders",
    description="""
    Fetches all trade orders stored in the system.

    - Returns a list of all trade orders, including order ID, stock symbol, price, quantity, and order type.
    """
)
def get_orders():
    """Fetches all orders from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, symbol, price, quantity, order_type FROM orders")
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        return [OrderResponse(id=row[0], symbol=row[1], price=row[2], quantity=row[3], order_type=row[4]) for row in orders]
    except Exception as e:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))