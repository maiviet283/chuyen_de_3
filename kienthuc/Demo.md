# Demo Sản Phẩm Phát Hiện và Ngăn Chặn Tấn Công Fuzzing 

## 1. Giới thiệu

Trong dự án này, chúng tôi đã phát triển một ứng dụng web sử dụng **Django** kết hợp với **middleware** để phát hiện và ngăn chặn các hành vi tấn công fuzzing trên các endpoint. Hệ thống sẽ theo dõi các yêu cầu đến từ người dùng, đặc biệt là khi họ cố gắng thay đổi tham số `id` liên tục, nhằm phát hiện tấn công **IDOR (Insecure Direct Object References)**. Nếu phát hiện hành vi đáng ngờ, hệ thống sẽ chặn địa chỉ IP của người dùng trong một khoảng thời gian nhất định.

Ứng dụng sử dụng **Nginx** làm reverse proxy để quản lý lưu lượng truy cập, kết hợp với **Gunicorn** để xử lý các yêu cầu của ứng dụng Django. Điều này đảm bảo hiệu suất và khả năng mở rộng, đồng thời cung cấp khả năng bảo mật cơ bản cho ứng dụng.

![Mô Hình Sản Phẩm](/access_demo/mohinh.jpg)

## 2. Trạng thái khi vào trang web

Khi người dùng truy cập trang web lần đầu tiên, giao diện sẽ hiển thị như sau:

![Trạng thái lúc đầu](/access_demo/trangthailucdau.PNG)

Tại giao diện này, người dùng có thể nhập ID vào ô nhập liệu và gửi yêu cầu để truy cập tài nguyên tương ứng. Hệ thống sẽ xử lý yêu cầu, kiểm tra xem người dùng có quyền truy cập vào tài nguyên đó hay không.

## 3. Trạng thái khi bị chặn

Nếu người dùng liên tục gửi các yêu cầu với ID không hợp lệ hoặc cố gắng thay đổi ID để tấn công, hệ thống sẽ coi đây là hành vi fuzzing. Khi số lượng yêu cầu đáng ngờ vượt quá ngưỡng cho phép, hệ thống sẽ chặn IP của người dùng và hiển thị thông báo lỗi như sau:

![Trạng thái bị chặn](/access_demo/dabichan.PNG)

Trong giao diện này, người dùng sẽ được thông báo rằng IP của họ đã bị chặn do phát hiện hành vi tấn công hoặc truy cập trái phép.

## 4. Phương pháp phát hiện tấn công

Hệ thống sử dụng một middleware tùy chỉnh trong Django để giám sát tất cả các yêu cầu đến endpoint có tham số `id`. Middleware này sẽ:
- Theo dõi tần suất và số lượng thay đổi giá trị của tham số `id`.
- Ghi lại hành vi bất thường nếu phát hiện người dùng cố gắng truy cập liên tục các ID không hợp lệ hoặc không thuộc quyền sở hữu của họ.
- Chặn các yêu cầu tiếp theo từ IP đáng ngờ khi hành vi fuzzing được phát hiện.

## 5. Kết hợp Nginx và Gunicorn

Trong dự án này, chúng tôi sử dụng **Nginx** và **Gunicorn** để đảm bảo tính ổn định và hiệu suất cho ứng dụng:
- **Nginx**: Hoạt động như một reverse proxy, giúp phân phối lưu lượng truy cập và ngăn chặn các cuộc tấn công DDoS cơ bản.
- **Gunicorn**: Được sử dụng để chạy ứng dụng Django, xử lý các yêu cầu từ Nginx và thực hiện các kiểm tra bảo mật để phát hiện tấn công fuzzing.

## 6. Kết luận

Dự án này nhằm nâng cao mức độ bảo mật cho ứng dụng web bằng cách phát hiện và ngăn chặn các cuộc tấn công fuzzing, đặc biệt là tấn công **IDOR**. Hệ thống theo dõi các yêu cầu của người dùng, phát hiện các hành vi tấn công và kịp thời chặn các địa chỉ IP đáng ngờ, giúp bảo vệ dữ liệu người dùng một cách hiệu quả.
