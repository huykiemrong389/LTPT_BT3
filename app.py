from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Thêm secret key để sử dụng flash messages

# URL của các services
ORDER_SERVICE_URL = "http://localhost:5002/api/orders"
INVENTORY_SERVICE_URL = "http://localhost:5001/api/inventory"

@app.route("/")
def index():
    """
    Trang chính hiển thị danh sách tồn kho.
    """
    inventory = []
    try:
        response = requests.get(INVENTORY_SERVICE_URL)
        if response.status_code == 200:
            inventory = response.json()
        else:
            flash("Failed to fetch inventory data.", "danger")
    except Exception as e:
        flash(f"Error fetching inventory: {e}", "danger")
    return render_template("index.html", inventory=inventory)

@app.route("/create_order", methods=["POST"])
def create_order():
    """
    API để tạo đơn hàng mới.
    """
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]
    try:
        response = requests.post(ORDER_SERVICE_URL, json={
            "product_id": product_id,
            "quantity": int(quantity)
        })
        if response.status_code == 201:
            flash("Order created successfully!", "success")
        else:
            flash(f"Failed to create order: {response.json().get('error', 'Unknown error')}", "danger")
    except Exception as e:
        flash(f"Error creating order: {e}", "danger")
    return redirect(url_for("index"))

@app.route("/add_product", methods=["POST"])
def add_product():
    """
    API để thêm sản phẩm mới hoặc cập nhật số lượng sản phẩm hiện có.
    """
    product_id = request.form["product_id"]
    quantity = request.form["quantity"]
    try:
        response = requests.post(f"{INVENTORY_SERVICE_URL}", json={
            "product_id": product_id,
            "quantity": int(quantity)
        })
        if response.status_code == 201:
            flash("Product added or updated successfully!", "success")
        else:
            flash(f"Failed to add/update product: {response.json().get('error', 'Unknown error')}", "danger")
    except Exception as e:
        flash(f"Error adding/updating product: {e}", "danger")
    return redirect(url_for("index"))

@app.route("/update_product/<product_id>", methods=["POST"])
def update_product(product_id):
    """
    API để cập nhật số lượng sản phẩm.
    """
    quantity_change = request.form["quantity_change"]
    try:
        response = requests.put(f"{INVENTORY_SERVICE_URL}/{product_id}", json={
            "quantity_change": int(quantity_change)
        })
        if response.status_code == 200:
            flash("Product quantity updated successfully!", "success")
        else:
            flash(f"Failed to update product quantity: {response.json().get('error', 'Unknown error')}", "danger")
    except Exception as e:
        flash(f"Error updating product quantity: {e}", "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
