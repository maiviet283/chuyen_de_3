Dưới đây là hướng dẫn từng bước để thực hiện việc cập nhật sinh viên trong Django. Tất cả mã nguồn sẽ được đưa vào trong một file duy nhất, sử dụng cấu trúc views.py.

### Bước 1: Cấu hình môi trường

Trước tiên, bạn cần đảm bảo rằng bạn đã cài đặt Django. Nếu chưa, hãy cài đặt Django bằng lệnh:

```bash
pip install django
```

### Bước 2: Tạo Project và App

Tạo một project Django và một app mới:

```bash
django-admin startproject myproject
cd myproject
django-admin startapp students
```

### Bước 3: Cấu hình Models

Mở file `students/models.py` và thêm model cho sinh viên:

```python
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Bạn có thể mã hóa mật khẩu ở đây

    def __str__(self):
        return self.name
```

###