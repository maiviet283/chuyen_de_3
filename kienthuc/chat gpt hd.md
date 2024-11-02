Để đẩy dự án Django lên Nginx thông qua Gunicorn, dưới đây là các bước cần thực hiện, đã được bạn chia sẻ từ video hướng dẫn. Mình sẽ bổ sung phần cấu hình Nginx để hoàn thiện quy trình này.

### 1. Tạo user `rakesh` và cấp quyền sudo
```bash
sudo adduser rakesh
sudo usermod -aG sudo rakesh
```

### 2. Đăng nhập vào user `rakesh`
```bash
su - rakesh
```

### 3. Tải các công cụ và ngôn ngữ (Python)
```bash
sudo apt install python3-venv python3-dev libpq-dev nginx curl
```

### 4. Tạo môi trường ảo
```bash
python3 -m venv envtestdjango
```

### 5. Khởi tạo môi trường ảo và tải thư viện Django
```bash
source envtestdjango/bin/activate
pip install django
pip install django-redis
```

### 6. Tạo dự án Django có tên là `chuyende`
```bash
django-admin startproject chuyende
```

### 7. Khởi tạo Database SQLite cho Django
```bash
cd chuyende/
python3 manage.py migrate
```

### 8. Tạo một thư mục static
```bash
mkdir static
```

### 9. Cập nhật `settings.py`
Mở file `settings.py` và thêm dòng sau:
```python
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
```
Cũng cần import thư viện `os`:
```python
import os
```

### 10. Sao chép toàn bộ file tĩnh sang thư mục static
```bash
python3 manage.py collectstatic
```

### 11. Chạy thử server
```bash
python3 manage.py runserver
```
Truy cập vào đường dẫn: `http://127.0.0.1:8000/`

### 12. Cập nhật `ALLOWED_HOSTS`
Trong `settings.py`, thêm:
```python
ALLOWED_HOSTS = ['*']
```

### 13. Tải Gunicorn
```bash
pip install gunicorn
```

### 14. Thử chạy Django bằng Gunicorn
```bash
gunicorn --bind 0.0.0.0:8000 chuyende.wsgi
```

### 15. Tạo file `gunicorn.socket`
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```
Nội dung:
```ini
[Unit]
Description=test django

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### 16. Tạo file `gunicorn.service`
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Nội dung:
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

### 17. Tải lại và cập nhật lại cấu hình
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn.service
sudo systemctl status gunicorn.service
```

### 18. Kiểm tra Gunicorn
```bash
curl --unix-socket /run/gunicorn.sock localhost
```

### 19. Cấu hình Nginx
Mở file cấu hình Nginx:
```bash
sudo nano /etc/nginx/sites-available/chuyende
```
Nội dung:
```nginx
server {
    listen 80;
    server_name 192.168.226.130;  # Thay bằng tên miền hoặc IP của server

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /home/rakesh/chuyende/static/;  # Đường dẫn đến thư mục static
    }

    location / {
        proxy_pass http://unix:/run/gunicorn.sock;  # Đường dẫn đến Gunicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 20. Kích hoạt cấu hình Nginx
Liên kết file cấu hình trong thư mục `sites-available` với thư mục `sites-enabled`:
```bash
sudo ln -s /etc/nginx/sites-available/chuyende /etc/nginx/sites-enabled
```

### 21. Kiểm tra lỗi Nginx
```bash
sudo nginx -t
```

### 22. Khởi động lại Nginx
```bash
sudo systemctl restart nginx
```

Bây giờ bạn có thể truy cập ứng dụng Django của mình qua địa chỉ IP hoặc tên miền của server mà không cần thông qua cổng 8000 nữa. Nếu bạn có thêm câu hỏi nào khác, cứ thoải mái hỏi nhé!




Để giải quyết vấn đề không có giao diện đẹp (CSS) khi truy cập vào `http://192.168.226.130/admin`, bạn có thể thực hiện các bước dưới đây:

### Cấp quyền cho thư mục static

1. **Thay đổi quyền cho thư mục chứa file static**:
    ```bash
    sudo chmod 755 /home/rakesh
    sudo find /home/rakesh/chuyende/static/ -type f -exec chmod 644 {} \;
    sudo find /home/rakesh/chuyende/static/ -type d -exec chmod 755 {} \;
    sudo systemctl restart nginx
    ```

2. **Cấp quyền cho thư mục static khác (nếu cần)**:
    ```bash
    sudo chmod -R 755 /home/vietmau/chuyen_de_3/static/
    sudo chown -R www-data:www-data /home/vietmau/chuyen_de_3/static/
    ```

3. **Kiểm tra log lỗi của Nginx để xác định nguyên nhân nếu vẫn gặp vấn đề**:
    ```bash
    sudo tail -f /var/log/nginx/error.log
    ```

### Tải và cài đặt Redis Cache

1. **Cập nhật danh sách gói**:
    ```bash
    sudo apt update
    ```

2. **Cài đặt Redis server**:
    ```bash
    sudo apt install redis-server
    ```

3. **Bắt đầu dịch vụ Redis**:
    ```bash
    sudo systemctl start redis
    ```

4. **Kích hoạt dịch vụ Redis tự động khởi động khi hệ thống khởi động**:
    ```bash
    sudo systemctl enable redis-server
    ```

5. **Kiểm tra trạng thái của Redis**:
    ```bash
    sudo systemctl status redis
    ```

### Cấu hình Django sử dụng Redis

Nếu bạn muốn cấu hình Django sử dụng Redis để cache, hãy thêm vào `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Kiểm tra

Sau khi thực hiện các bước trên, hãy thử truy cập lại vào `http://192.168.226.130/admin` để kiểm tra xem giao diện đã được hiển thị đúng chưa. Nếu bạn vẫn gặp vấn đề, hãy kiểm tra lại các log để tìm ra nguyên nhân cụ thể.