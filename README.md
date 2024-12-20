# Chuyên Đề 3: Bảo Mật Endpoint bằng Middleware Chống Fuzzing

## Giới Thiệu Đề Bài
Đề tài của chúng ta nhằm mục đích phát hiện và ngăn chặn các cuộc tấn công fuzzing trên các endpoint của ứng dụng web. Trong trường hợp cụ thể này, chúng ta sẽ bảo vệ ứng dụng khỏi kiểu tấn công IDOR (Insecure Direct Object References), nơi hacker cố gắng thay đổi giá trị `id` trong các yêu cầu để truy cập trái phép vào dữ liệu của người dùng khác.

Giả sử một ứng dụng web cung cấp endpoint `/resource/?id=1`, hacker có thể thay đổi tham số `id` một cách liên tục để truy cập vào các tài nguyên khác như `/resource/?id=2`, `/resource/?id=3`,... Nếu số lần thay đổi giá trị `id` vượt quá một ngưỡng cho phép trong thời gian ngắn, chúng ta sẽ coi đây là hành vi tấn công và chặn yêu cầu.

![Mô Hình Sản Phẩm](access_demo/mohinh.jpg)

Đề tài này hướng tới xây dựng một hệ thống bảo vệ ứng dụng web khỏi các cuộc tấn công **fuzzing** và đặc biệt là **tấn công IDOR (Insecure Direct Object References)**, nơi hacker cố gắng khai thác việc kiểm soát trực tiếp tham chiếu đối tượng (như `id`) để truy cập dữ liệu không được phép. Để đạt được mục tiêu này, chúng ta thiết lập một mô hình gồm nhiều lớp bảo vệ nhằm phát hiện và ngăn chặn các hành vi tấn công ngay từ giai đoạn ban đầu.

### 1. **Tổng Quan về Mô Hình Kiến Trúc**
Mô hình triển khai hệ thống bảo vệ ứng dụng của chúng ta sẽ bao gồm các thành phần sau:

   - **Web Application Firewall (WAF)**: Là lớp bảo vệ đầu tiên, giúp lọc và giám sát lưu lượng truy cập, phát hiện các dấu hiệu tấn công, bao gồm cả **fuzzing** và **IDOR**. WAF áp dụng các quy tắc bảo mật (Core Set Rules) để chặn yêu cầu không hợp lệ.
   - **Nginx**: Đóng vai trò proxy ngược (reverse proxy) để nhận yêu cầu từ người dùng, chuyển đến Gunicorn. Nginx cũng có thể cache các nội dung tĩnh để giảm tải cho ứng dụng.
   - **Gunicorn**: Ứng dụng Web Server Gateway Interface (WSGI) để triển khai Django, đảm bảo việc xử lý các request từ Nginx đến Django một cách hiệu quả.
   - **Django với Middleware**: Django xử lý logic ứng dụng và có middleware tùy chỉnh để chặn yêu cầu từ các IP có dấu hiệu truy cập quá nhiều, giảm thiểu rủi ro từ các cuộc tấn công lặp đi lặp lại.
   - **Redis Cache**: Được sử dụng như một cache trung gian để lưu trữ tạm thời các dữ liệu truy xuất nhiều lần, giảm thiểu tần suất truy cập trực tiếp vào cơ sở dữ liệu, giúp tăng tốc độ truy xuất và giảm tải cho database.
   - **Cơ sở dữ liệu (Database)**: Lưu trữ toàn bộ dữ liệu của ứng dụng.

### 2. **Vai Trò của Các Thành Phần**
   - **WAF (kèm Core Set Rule)**: 
      - WAF là thành phần bảo vệ nằm giữa **người dùng** và **Nginx**. 
      - Sử dụng Core Set Rules từ OWASP, WAF phát hiện và ngăn chặn các cuộc tấn công bằng cách kiểm tra mọi request từ người dùng. Core Set Rules bao gồm các quy tắc để phát hiện tấn công SQL injection, Cross-Site Scripting (XSS), và các dấu hiệu của fuzzing như gửi nhiều yêu cầu không hợp lệ liên tiếp.
      - Với tấn công IDOR, Core Set Rules có thể được cấu hình để nhận diện các mẫu yêu cầu bất thường khi hacker cố gắng thay đổi giá trị `id` trong các endpoint.

   - **Nginx**:
      - Sau khi WAF cho phép request đi qua, Nginx nhận và chuyển tiếp request đến Gunicorn. 
      - Ngoài ra, Nginx có thể lưu các nội dung tĩnh (static) để giảm tải cho Django, như các file hình ảnh, CSS, JavaScript.

   - **Gunicorn**:
      - Gunicorn là server WSGI, kết nối giữa Nginx và Django, đảm bảo rằng Django có thể xử lý song song nhiều yêu cầu từ người dùng một cách hiệu quả.
      
   - **Django Middleware**:
      - Middleware chặn và quản lý các IP có dấu hiệu bất thường (thực hiện quá nhiều yêu cầu trong thời gian ngắn) bằng cách lưu lại các IP vào Redis Cache. Điều này giúp phát hiện và ngăn chặn các IP đang cố gắng thực hiện các cuộc tấn công fuzzing bằng cách gửi nhiều request liên tiếp.
      - Middleware kiểm tra quyền truy cập vào các tài nguyên dựa trên `id` và người dùng, nhằm bảo vệ khỏi các cuộc tấn công IDOR. Khi nhận thấy hành vi bất thường (như thay đổi `id` không hợp lệ), middleware sẽ từ chối yêu cầu và gửi cảnh báo.

   - **Redis Cache**:
      - Redis Cache hoạt động như bộ nhớ tạm để lưu các kết quả truy vấn từ Django. Khi một dữ liệu đã có trong Redis, Django sẽ lấy dữ liệu từ Redis trước, thay vì truy vấn lại cơ sở dữ liệu, giúp giảm tải và tăng tốc độ xử lý.
      - Redis Cache cũng lưu trạng thái của các IP bị chặn, giúp middleware nhanh chóng tra cứu và xác định các IP có dấu hiệu bất thường.

### 3. **Luồng Xử Lý Request và Response**
   1. **Request từ người dùng đến ứng dụng**:
      - **Bước 1**: Request từ người dùng đầu tiên đi qua WAF, WAF kiểm tra theo **Core Set Rules**. Nếu WAF phát hiện yêu cầu bất thường hoặc vi phạm quy tắc, nó sẽ chặn yêu cầu.
      - **Bước 2**: Nếu request hợp lệ, WAF chuyển request đến Nginx.
      - **Bước 3**: Nginx chuyển request tới Gunicorn, từ đó đến Django để xử lý logic ứng dụng.

   2. **Middleware kiểm tra IDOR và hành vi bất thường**:
      - **Bước 4**: Middleware sẽ xác minh các yêu cầu về dữ liệu `id`, kiểm tra xem người dùng có quyền truy cập vào tài nguyên được yêu cầu hay không. Nếu không hợp lệ, request sẽ bị từ chối.
      - **Bước 5**: Middleware kiểm tra IP của người dùng xem có nằm trong danh sách bị chặn (Redis Cache) hay không.

   3. **Truy xuất dữ liệu từ Redis Cache và Database**:
      - **Bước 6**: Khi yêu cầu hợp lệ, Django kiểm tra Redis Cache xem dữ liệu đã được cache hay chưa. Nếu có, dữ liệu sẽ được trả về từ Redis. Nếu không, Django truy xuất dữ liệu từ cơ sở dữ liệu và lưu vào Redis để tái sử dụng trong lần tiếp theo.

   4. **Trả lại response cho người dùng**:
      - **Bước 7**: Sau khi Django xử lý xong, response được gửi ngược trở lại qua các tầng middleware, Gunicorn, và Nginx để đến tay người dùng mà không cần duyệt lại qua WAF.

### 4. **Kết Luận**
Mô hình này giúp đảm bảo an toàn cho ứng dụng web khỏi các cuộc tấn công fuzzing và IDOR. Các tầng bảo vệ (WAF với Core Set Rules, middleware chặn IP bất thường, và Redis Cache) phối hợp chặt chẽ để ngăn chặn các cuộc tấn công từ bên ngoài, bảo vệ dữ liệu và tài nguyên ứng dụng khỏi bị truy cập trái phép.


# Tài Liệu Dự Án
## 1. [Cấu Trúc Dự Án](/kienthuc/directory_configuration.md)
   -  Giải thích chi tiết về cấu trúc dự án được đưa lên GitHub.

## 2. [Demo Sản Phẩm](/kienthuc/Demo.md)
   - Giới thiệu sản phẩm và tính năng nổi bật.

## 3. [Kiến Thức về Nginx - WAF - Core Rule Set (CRS)](/kienthuc/nginx_waf_rule.md)
   - Tổng quan về Nginx và WAF.
   - Tầm quan trọng của Core Rule Set (CRS) trong việc bảo vệ ứng dụng.

## 4. [Kiến Thức về Gunicorn](/kienthuc/gunicorn.md)
   - Cấu trúc và cách hoạt động của Gunicorn.
   - Vai trò của Gunicorn trong việc làm cầu nối giữa Django và Nginx.

## 5. [Kiến Thức về Django và Middleware](/kienthuc/django_middleware.md)
   - Giới thiệu về Django và các Middleware phổ biến.
   - Tác dụng của Middleware trong việc xử lý các yêu cầu và bảo vệ ứng dụng.

## 6. [Kiến Thức về Cache - Redis](/kienthuc/cache_redis.md)
   - Redis là gì và cách hoạt động của Cache.
   - Ứng dụng của Redis trong việc tối ưu hóa hiệu năng của ứng dụng.

## 7. [Video Youtube Hướng Dẫn Deploy Django lên Nginx](https://youtu.be/NSHshIEVL-M?si=4vJCZxAdR4DgiuM7)
   - Video Youtube hướng dẫn chi tiết các bước triển khai Django lên Nginx.

## 8. [Tài Liệu Hướng Dẫn Deploy Django lên Nginx](/kienthuc/tutorial_deploy.txt)
   - Tài liệu những đoạn code trong video ở mục 6 và giải thích hơn 1 tý.
