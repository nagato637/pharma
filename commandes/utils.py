def create_cart_snapshot(cart):
    return {
        'created_at': cart.created_at.isoformat(),
        'items': [
            {
                'product': item.product.get_snapshot_data(),
                'quantity': item.quantity,
                'added_at': item.product.added_at.isoformat(),
            }
            for item in cart.items.all()
        ],
    }