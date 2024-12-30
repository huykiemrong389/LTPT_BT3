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
   docker-compose up --build