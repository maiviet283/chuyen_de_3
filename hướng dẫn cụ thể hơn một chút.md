Dưới đây là tóm tắt các bước đẩy dự án Django lên Nginx thông qua Gunicorn, bao gồm giải thích từng phần của mã lệnh:

### 1. Tạo User `rakesh`
```bash
sudo adduser rakesh
```
- **Giải thích:** Lệnh này tạo một user mới có tên là `rakesh`. Người dùng này sẽ được sử dụng để quản lý ứng dụng Django.

### 2. Cấp Quyền `sudo` cho User Mới Tạo
```bash
sudo usermod -aG sudo rakesh
```
- **Giải thích:** Lệnh này thêm user `rakesh` vào nhóm `sudo`, cho phép user này thực hiện các lệnh yêu cầu quyền quản trị.

### 3. Đăng Nhập vào User `rakesh`
```bash
su - rakesh
```
- **Giải thích:** Lệnh này chuyển sang user `rakesh`. Bạn sẽ thực hiện các thao tác dưới quyền user này.

### 4. Tải Các Công Cụ và Ngôn Ngữ Cần Thiết
```bash
sudo apt install python3-venv python3-dev libpq-dev nginx curl
```
- **Giải thích:** Cài đặt các gói cần thiết:
  - `python3-venv`: Để tạo môi trường ảo.
  - `python3-dev`: Cần thiết cho việc cài đặt một số thư viện Python.
  - `libpq-dev`: Thư viện cần thiết cho PostgreSQL.
  - `nginx`: Web server.
  - `curl`: Công cụ dùng để gửi các yêu cầu HTTP.

### 5. Tạo Môi Trường Ảo
```bash
python3 -m venv envtestdjango
```
- **Giải thích:** Tạo một môi trường ảo có tên `envtestdjango`, giúp quản lý các thư viện Python một cách riêng biệt.

### 6. Khởi Tạo Môi Trường Ảo và Tải Thư Viện Django
```bash
source envtestdjango/bin/activate
pip install django
```
- **Giải thích:**
  - `source envtestdjango/bin/activate`: Kích hoạt môi trường ảo.
  - `pip install django`: Cài đặt Django trong môi trường ảo.

### 7. Tạo Dự Án Django
```bash
django-admin startproject chuyende
```
- **Giải thích:** Tạo một dự án Django mới có tên `chuyende`.

### 8. Khởi Tạo Database SQLite cho Django
```bash
cd chuyende/
python3 manage.py migrate
```
- **Giải thích:**
  - `cd chuyende/`: Chuyển vào thư mục dự án.
  - `python3 manage.py migrate`: Chạy các migration để khởi tạo cơ sở dữ liệu SQLite.

### 9. Tạo Thư Mục Static
```bash
mkdir static
```
- **Giải thích:** Tạo thư mục `static` để lưu trữ các file tĩnh (CSS, JS, hình ảnh).

### 10. Cấu Hình `settings.py`
```bash
sudo nano chuyende/settings.py
```
- **Giải thích:** Mở file `settings.py` để cấu hình. Thêm dòng:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```
- **Giải thích:** `STATIC_ROOT` xác định đường dẫn nơi Django sẽ lưu trữ các file tĩnh.

### 11. Sao Chép Các File Tĩnh Sang Thư Mục Static
```bash
python3 manage.py collectstatic
```
- **Giải thích:** Sao chép tất cả các file tĩnh từ dự án vào thư mục `static`.

### 12. Chạy Thử Server
```bash
python3 manage.py runserver
```
- **Giải thích:** Khởi động server phát triển của Django. Bạn có thể truy cập vào `http://127.0.0.1:8000/` để kiểm tra.

### 13. Cập Nhật `ALLOWED_HOSTS`
```python
ALLOWED_HOSTS = ['*']
```
- **Giải thích:** Thay đổi `ALLOWED_HOSTS` để cho phép nhiều IP truy cập vào server.

### 14. Tải Gunicorn
```bash
pip install gunicorn
```
- **Giải thích:** Cài đặt Gunicorn, một WSGI HTTP server cho Python, sẽ được sử dụng để phục vụ ứng dụng Django.

### 15. Chạy Django Bằng Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 chuyende.wsgi
```
- **Giải thích:** Khởi động ứng dụng Django bằng Gunicorn, lắng nghe trên tất cả các địa chỉ IP tại cổng 8000.

### 16. Tạo File `gunicorn.socket`
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
- **Giải thích:** Tạo file socket cho Gunicorn với nội dung sau:
```ini
[Unit]
Description=test django

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```
- **Giải thích:** Cấu hình này cho phép Gunicorn lắng nghe trên một socket UNIX.

### 17. Tạo File `gunicorn.service`
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
- **Giải thích:** Tạo file service cho Gunicorn với nội dung sau:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=rakesh
Group=www-data
WorkingDirectory=/home/rakesh/chuyende  
ExecStart=/home/rakesh/envtestdjango/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          chuyende.wsgi:application

[Install]
WantedBy=multi-user.target
```
- **Giải thích:** Cấu hình này xác định cách Gunicorn sẽ chạy và thông tin người dùng, nhóm, thư mục làm việc.

### 18. Tải Lại và Khởi Động Gunicorn
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn.service
sudo systemctl status gunicorn.service
```
- **Giải thích:** Tải lại cấu hình hệ thống và khởi động service Gunicorn. Lệnh `status` cho phép kiểm tra trạng thái service.

### 19. Gửi Lệnh đến Gunicorn
```bash
curl --unix-socket /run/gunicorn.sock localhost
```
- **Giải thích:** Gửi yêu cầu HTTP đến Gunicorn thông qua socket UNIX và nhận lại phản hồi HTML.

### 20. Cấu Hình Nginx
```bash
sudo nano /etc/nginx/sites-available/chuyende
```
- **Giải thích:** Tạo file cấu hình cho Nginx với nội dung:
```nginx
server {
    listen 80;
    server_name 192.168.226.130;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/rakesh/chuyende/static/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
```
- **Giải thích:** Cấu hình Nginx để lắng nghe trên cổng 80, quản lý các file tĩnh và chuyển tiếp các yêu cầu đến Gunicorn qua socket UNIX.