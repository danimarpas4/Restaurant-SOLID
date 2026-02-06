def aplicar_descuento(pedido, porcentaje_descuento):
    """
    Applies a governance rule (Discount) to modify the transaction state.
    
    Args:
        pedido (Pedido): The transaction object to be mutated.
        porcentaje_descuento (float): The factor to adjust the total valuation.
        
    Returns:
        float: The updated total value after state transition.
    """
    descuento = pedido.total * (porcentaje_descuento / 100)
    
    # Mutation of the state object
    pedido.total -= descuento
    
    return pedido.total