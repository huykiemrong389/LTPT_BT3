from flask import Flask
from Controllers.InventoryController import inventory_controller
from Infrastructure.Database import init_db
from Infrastructure.MessageBus import MessageBus
import threading

# Khởi tạo Flask app
app = Flask(__name__)

# Khởi tạo cơ sở dữ liệu
init_db()

# Đăng ký blueprint
app.register_blueprint(inventory_controller, url_prefix="/api")

# Hàm chạy Message Bus
def run_message_bus():
    message_bus = MessageBus()
    message_bus.start_listening()

if __name__ == '__main__':
    # Chạy Message Bus trong một thread riêng
    threading.Thread(target=run_message_bus, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5001)
