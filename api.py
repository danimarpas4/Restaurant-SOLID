from producto import Session
from pedido import Pedido

def consultar_pedido(cliente):
    """
    API Endpoint to fetch transaction status from the persistence layer.
    
    Args:
        cliente (str): The unique identifier (name) of the client to query.
        
    Returns:
        dict: A JSON-compatible representation of the transaction state or an error payload.
    """
    # Instantiate a temporary session for this read operation (Unit of Work)
    session = Session()
    
    # Query the ledger for the most recent transaction matching the criteria
    pedido = session.query(Pedido).filter_by(cliente=cliente).first()
    
    if pedido:
        # Serialize the entity into a data transfer object (DTO)
        return {
            "cliente": pedido.cliente,
            "productos": [pp.producto.nombre for pp in pedido.productos],
            "Total": pedido.total,
        }
        
    return {"error": "Transaction not found for the specified client."}