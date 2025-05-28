from sqlalchemy.orm import Session

def add_to_cart(user_id: int, drug_id: int, quantity: int, db: Session):
    cart_item = db.query(CartItem).filter_by(user_id=user_id, drug_id=drug_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=user_id, drug_id=drug_id, quantity=quantity)
        db.add(cart_item)
    db.commit()
    return cart_item


def place_order(user_id: int, db: Session):
    cart_items = db.query(CartItem).filter_by(user_id=user_id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = Order(user_id=user_id)
    db.add(order)
    db.flush()  # Get order.id

    for item in cart_items:
        drug = db.query(Drug).filter(Drug.id == item.drug_id).first()
        if drug:
            price = 0  # You can define a price attribute later
            order_item = OrderItem(
                order_id=order.id,
                drug_id=drug.id,
                quantity=item.quantity,
                price=price
            )
            order.items.append(order_item)

            # ✅ Update sales count here
            drug.sales_count += item.quantity
            db.add(drug)

    # Clean up cart
    db.query(CartItem).filter_by(user_id=user_id).delete()
    db.commit()
    return order
