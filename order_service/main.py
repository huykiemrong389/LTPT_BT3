from flask import Flask
from Controllers.OrderController import order_controller
from Infrastructure.Database import init_db

# Khởi tạo Flask app
app = Flask(__name__)

# Khởi tạo cơ sở dữ liệu
init_db()

# Đăng ký blueprint
app.register_blueprint(order_controller, url_prefix="/api")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
