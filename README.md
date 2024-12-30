# LTPT_BT3 - Order and Inventory Management System

## Mô tả dự án
Hệ thống gồm 2 dịch vụ chính:
1. **Order Service**: Xử lý tạo đơn hàng và gửi thông báo tới Inventory Service thông qua RabbitMQ.
2. **Inventory Service**: Quản lý tồn kho và xử lý các thông báo từ RabbitMQ.

## Hướng dẫn chạy

### Chạy bằng Docker Compose
1. Clone repository:
   ```bash
   git clone https://github.com/huykiemrong389/LTPT_BT3.git
   cd LTPT_BT3
2. Chạy Docker Compose:
   ```bash
   docker-compose up --build
3. Chạy bằng Kubernetes
Đẩy Docker image lên DockerHub.

Deploy các dịch vụ:

bash
Copy code
kubectl apply -f rabbitmq-deployment.yaml
kubectl apply -f inventory-service-deployment.yaml
kubectl apply -f order-service-deployment.yaml
Truy cập các dịch vụ qua port-forward:

bash
Copy code
kubectl port-forward svc/order-service 5000:5000
kubectl port-forward svc/inventory-service 5001:5001
