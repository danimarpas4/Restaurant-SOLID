from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from producto import Base, engine

class Pedido(Base):
    """
    Represents a 'Transaction' entity capturing the exchange between a client and the system.
    Manages the lifecycle of an order and its associated state.
    """
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    cliente = Column(String(255), nullable=False)
    
    # Timestamp for auditability and historical tracking
    fecha = Column(DateTime, default=datetime.utcnow)
    
    # Relational mapping to associated assets (Many-to-Many via Association Object)
    productos = relationship("PedidoProducto", back_populates="pedido")
    
    # Stored calculated value to prevent re-computation overhead (Caching strategy)
    total = Column(Float, nullable=False, default=0.0)

    def calcularTotal(self):
        """
        Executes the logic to aggregate the total value of the transaction.
        Iterates through linked assets to compute the final state of 'total'.
        """
        self.total = sum(pp.producto.precio * pp.cantidad for pp in self.productos)


class PedidoProducto(Base):
    """
    Association Entity (Junction Table) handling the Many-to-Many relationship 
    between Orders (Transactions) and Products (Assets).
    Includes metadata specific to the relationship, such as quantity.
    """
    __tablename__ = "pedido_producto"

    id = Column(Integer, primary_key=True)
    
    # Foreign Keys linking to the parent entities
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    
    cantidad = Column(Integer, nullable=False, default=1)

    # ORM Relationships for traversal
    pedido = relationship("Pedido", back_populates="productos")
    producto = relationship("Producto")

# Ensure schema consistency across all defined models
Base.metadata.create_all(engine)