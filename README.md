# LTPT_BT3 - Order and Inventory Management System


## Mô tả dự án
Hệ thống quản lý đơn hàng và tồn kho bao gồm hai dịch vụ chính:

1. **Order Service**: Quản lý việc tạo đơn hàng và gửi thông báo tới Inventory Service thông qua RabbitMQ.
2. **Inventory Service**: Quản lý tồn kho, bao gồm thêm sản phẩm, cập nhật số lượng sản phẩm, và xử lý thông báo từ Order Service.

## Kiến trúc hệ thống
- **Message Bus**: RabbitMQ được sử dụng để kết nối Order Service và Inventory Service.
- **Docker Compose**: Để container hóa các dịch vụ.
- **Kubernetes (tùy chọn)**: Hỗ trợ triển khai trên cụm Kubernetes cho hệ thống lớn hơn.
- **Flask**: Dùng cho ứng dụng demo giao diện web.

---

## Yêu cầu hệ thống
- **Docker**: [https://www.docker.com/](https://www.docker.com/)
- **Python 3.9+**
- **RabbitMQ**: Được quản lý thông qua Docker Compose.

---

## Hướng dẫn cài đặt

### **Chạy bằng Docker Compose**

1. **Clone repository:**
   ```bash
   git clone https://github.com/huykiemrong389/LTPT_BT3.git
   cd LTPT_BT3
   ```

2. **Chạy Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Dịch vụ:**
   - **Order Service:** [http://localhost:5002](http://localhost:5002)
   - **Inventory Service:** [http://localhost:5001](http://localhost:5001)
   - **RabbitMQ Management UI:** [http://localhost:15672](http://localhost:15672) (Username: `guest`, Password: `guest`)

4. **Chạy ứng dụng demo web:**
   ```bash
   python app.py
   ```
   - Truy cập: [http://localhost:8000](http://localhost:8000)

---

## API Documentation

### **Order Service**
#### **POST `/api/orders`**
- Tạo đơn hàng mới.
- **Yêu cầu:**
  ```json
  {
    "product_id": "product_1",
    "quantity": 10
  }
  ```
- **Phản hồi:**
  ```json
  {
    "message": "Order created",
    "order": {
      "id": 1,
      "product_id": "product_1",
      "quantity": 10
    }
  }
  ```

### **Inventory Service**
#### **POST `/api/inventory`**
- Thêm hoặc cập nhật sản phẩm trong kho.
- **Yêu cầu:**
  ```json
  {
    "product_id": "product_1",
    "quantity": 100
  }
  ```
- **Phản hồi:**
  ```json
  {
    "message": "Product added or updated",
    "product": {
      "product_id": "product_1",
      "quantity": 100
    }
  }
  ```

#### **PUT `/api/inventory/<product_id>`**
- Cập nhật số lượng sản phẩm hiện có.
- **Yêu cầu:**
  ```json
  {
    "quantity_change": -10
  }
  ```
- **Phản hồi:**
  ```json
  {
    "message": "Inventory updated",
    "product": {
      "product_id": "product_1",
      "quantity": 90
    }
  }
  ```

#### **GET `/api/inventory`**
- Lấy danh sách toàn bộ tồn kho.
- **Phản hồi:**
  ```json
  [
    {
      "product_id": "product_1",
      "quantity": 90
    }
  ]
  ```

---

## Các tính năng chính
1. Quản lý tồn kho:
   - Thêm sản phẩm mới.
   - Cập nhật số lượng sản phẩm hiện có.
   - Kiểm tra danh sách tồn kho.
2. Quản lý đơn hàng:
   - Tạo đơn hàng.
   - Giảm số lượng tồn kho dựa trên đơn hàng.
3. Kết nối dịch vụ qua RabbitMQ.

---

## Tích hợp Kubernetes (tùy chọn)

1. **Deploy RabbitMQ:**
   ```bash
   kubectl apply -f rabbitmq-deployment.yaml
   ```

2. **Deploy Inventory Service:**
   ```bash
   kubectl apply -f inventory-service-deployment.yaml
   ```

3. **Deploy Order Service:**
   ```bash
   kubectl apply -f order-service-deployment.yaml
   ```

4. **Port-forward các dịch vụ:**
   - RabbitMQ: `kubectl port-forward svc/rabbitmq 15672:15672`
   - Order Service: `kubectl port-forward svc/order-service 5002:5000`
   - Inventory Service: `kubectl port-forward svc/inventory-service 5001:5001`

---

## Hướng phát triển trong tương lai
- Thêm tính năng xử lý thanh toán (Payment Service).
- Tích hợp giám sát hiệu suất bằng Prometheus và Grafana.
- Thực hiện CI/CD để tự động triển khai trên môi trường cloud.

---

## Đóng góp
Nếu bạn muốn đóng góp, hãy tạo pull request hoặc liên hệ trực tiếp qua [huybbicute@gmail.com](mailto:huybbicute@gmail.com).
