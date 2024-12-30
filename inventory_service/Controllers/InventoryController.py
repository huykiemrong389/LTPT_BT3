from flask import Blueprint, request, jsonify
from Infrastructure.Database import SessionLocal
from Entities.Product import Product

inventory_controller = Blueprint('inventory_controller', __name__)

@inventory_controller.route('/inventory', methods=['POST'])
def add_or_update_product():
    """
    API để thêm sản phẩm mới vào kho hoặc cập nhật số lượng sản phẩm hiện có.
    """
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Kiểm tra đầu vào
    if not product_id or quantity is None:
        return jsonify({"error": "Missing product_id or quantity"}), 400
    if quantity < 0:
        return jsonify({"error": "Quantity must be positive"}), 400

    db = SessionLocal()
    try:
        # Kiểm tra xem sản phẩm đã tồn tại hay chưa
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product:
            # Nếu sản phẩm đã tồn tại, cập nhật số lượng
            product.quantity += quantity
        else:
            # Nếu sản phẩm chưa tồn tại, thêm sản phẩm mới
            product = Product(product_id=product_id, quantity=quantity)
            db.add(product)

        db.commit()
        db.refresh(product)

        return jsonify({
            "message": "Product added or updated",
            "product": {
                "product_id": product.product_id,
                "quantity": product.quantity
            }
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@inventory_controller.route('/inventory/<product_id>', methods=['PUT'])
def update_inventory_quantity(product_id):
    """
    API để cập nhật số lượng sản phẩm trong kho (thêm hoặc giảm).
    """
    data = request.json
    quantity_change = data.get('quantity_change')

    # Kiểm tra đầu vào
    if quantity_change is None:
        return jsonify({"error": "Missing quantity_change"}), 400

    db = SessionLocal()
    try:
        # Kiểm tra xem sản phẩm có tồn tại không
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Ngăn tồn kho về âm
        if product.quantity + quantity_change < 0:
            return jsonify({"error": "Insufficient stock"}), 400

        # Cập nhật tồn kho
        product.quantity += quantity_change
        db.commit()
        db.refresh(product)

        return jsonify({
            "message": "Inventory updated",
            "product": {
                "product_id": product.product_id,
                "quantity": product.quantity
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@inventory_controller.route('/inventory/<product_id>', methods=['GET'])
def get_inventory_by_product(product_id):
    """
    API để lấy thông tin tồn kho của một sản phẩm cụ thể.
    """
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            return jsonify({"error": "Product not found"}), 404

        return jsonify({
            "product_id": product.product_id,
            "quantity": product.quantity
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@inventory_controller.route('/inventory', methods=['GET'])
def get_inventory():
    """
    API để lấy danh sách tất cả sản phẩm trong kho.
    """
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        result = [{"product_id": product.product_id, "quantity": product.quantity} for product in products]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

