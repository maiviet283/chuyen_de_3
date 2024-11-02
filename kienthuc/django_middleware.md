### Django
Django là một **web framework** mạnh mẽ và linh hoạt của Python, giúp phát triển các ứng dụng web một cách nhanh chóng và dễ dàng. Được xây dựng với triết lý "Don't Repeat Yourself" (DRY), Django cung cấp các công cụ và tính năng để lập trình viên dễ dàng xử lý các tác vụ phổ biến, từ **quản lý cơ sở dữ liệu**, **tạo API** đến **xử lý biểu mẫu** và **xác thực người dùng**. 

Trong dự án, Django đóng vai trò là **backend server** chính, chịu trách nhiệm:
- **Quản lý cơ sở dữ liệu**: Django ORM giúp truy xuất và thao tác dữ liệu từ database.
- **Xử lý logic nghiệp vụ**: Các luồng nghiệp vụ được xử lý tại đây.
- **Quản lý và xử lý API**: Django Rest Framework giúp dễ dàng tạo các API phục vụ cho frontend.
  
### Middleware
**Middleware** là các lớp trung gian trong Django, nằm giữa **web server** (như Nginx) và **Django** để xử lý các request và response trước khi chúng đến hoặc rời khỏi ứng dụng. Middleware hoạt động như một chuỗi các lớp xử lý, qua đó **mỗi request và response** đều được chuyển qua từng lớp để thực hiện các tác vụ nhất định.

**Tác dụng của Middleware trong dự án**:
1. **Bảo mật**: Middleware có thể chặn các request từ các IP xấu hoặc phát hiện các request đáng ngờ để ngăn chặn tấn công.
2. **Xử lý dữ liệu request và response**: Chẳng hạn, có thể kiểm tra tính hợp lệ của dữ liệu request trước khi vào Django.
3. **Lưu cache và giảm tải server**: Một số middleware có thể lưu lại các response thường xuyên được gọi để giảm tải việc truy cập cơ sở dữ liệu.

### Ứng dụng của Django và Middleware trong dự án
Trong dự án này:
- **Django** là nơi xử lý logic chính của ứng dụng và cung cấp API cho frontend.
- **Middleware** được cấu hình để phát hiện và ngăn chặn các cuộc tấn công **fuzzing** và **IDOR** bằng cách kiểm tra request trước khi chúng đến Django. Middleware này sẽ ghi log lại các hành vi bất thường, như việc thay đổi `id` không hợp lệ, để chặn truy cập trái phép.

Với sự kết hợp của Django và Middleware, dự án có khả năng xử lý các tác vụ nghiệp vụ và bảo mật một cách chặt chẽ và hiệu quả.