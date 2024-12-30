from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

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
    except Exception as e:
        print(f"Error fetching inventory: {e}")
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
        if response.status_code != 201:
            return f"Failed to create order: {response.json()}"
    except Exception as e:
        return f"Error: {e}"
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
        if response.status_code != 201:
            return f"Failed to add or update product: {response.json()}"
    except Exception as e:
        return f"Error: {e}"
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
        if response.status_code != 200:
            return f"Failed to update product quantity: {response.json()}"
    except Exception as e:
        return f"Error: {e}"
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
