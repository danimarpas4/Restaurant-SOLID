from producto import Producto, Session
from pedido import Pedido, PedidoProducto
from descuento import aplicar_descuento
from factura import generar_factura
from api import consultar_pedido
from reporte import generar_reporte

def main():
    """
    Main entry point for the application.
    Orchestrates the lifecycle of asset creation, transaction processing, 
    and reporting services.
    """
    
    # Initialize the transaction session (Connection to the persistence layer)
    session = Session()

    print("[INFO] Initializing Genesis Assets...")
    # Instantiate Asset objects (Genesis Block simulation)
    producto1 = Producto(nombre="Pizza margarita", tipo="plato", precio=8.5)
    producto2 = Producto(nombre="Coca Cola", tipo="bebida", precio=1.5)

    # Batch insert of assets into the staging area
    session.add_all([producto1, producto2])
    # Atomic Commit: Persist assets to the database
    session.commit()

    print("[INFO] Processing New Transaction...")
    # Initialize a new Order (Transaction)
    pedido = Pedido(cliente="Raquel Martinez")
    session.add(pedido)
    session.commit()

    # Link Assets to the Transaction (Graph construction)
    pedido_producto1 = PedidoProducto(
        pedido_id=pedido.id, producto_id=producto1.id, cantidad=1
    )
    pedido_producto2 = PedidoProducto(
        pedido_id=pedido.id, producto_id=producto2.id, cantidad=2
    )
    session.add_all([pedido_producto1, pedido_producto2])
    
    # Calculate state aggregation
    pedido.calcularTotal()
    session.commit()

    print("[INFO] Applying Governance Rules (Discounts)...")
    # Apply business logic modifications
    aplicar_descuento(pedido, 10)
    session.commit()

    # Generate Output Views
    print(generar_factura(pedido))

    # Test API Interface
    print("[INFO] Querying API Gateway...")
    print(consultar_pedido("Raquel Martinez"))

    # Trigger Off-chain Reporting
    print("[INFO] Generating Audit Report...")
    generar_reporte("reporte_pedidos.pdf")
    print("[SUCCESS] Report generated successfully.")

if __name__ == "__main__":
    main()