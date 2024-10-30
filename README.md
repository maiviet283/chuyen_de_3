# Chuyên Đề 3: Bảo Mật Endpoint bằng Middleware Chống Fuzzing

## Giới Thiệu Đề Bài
Đề tài của chúng ta nhằm mục đích phát hiện và ngăn chặn các cuộc tấn công fuzzing trên các endpoint của ứng dụng web. Trong trường hợp cụ thể này, chúng ta sẽ bảo vệ ứng dụng khỏi kiểu tấn công IDOR (Insecure Direct Object References), nơi hacker cố gắng thay đổi giá trị `id` trong các yêu cầu để truy cập trái phép vào dữ liệu của người dùng khác.

Giả sử một ứng dụng web cung cấp endpoint `/resource/?id=1`, hacker có thể thay đổi tham số `id` một cách liên tục để truy cập vào các tài nguyên khác như `/resource/?id=2`, `/resource/?id=3`,... Nếu số lần thay đổi giá trị `id` vượt quá một ngưỡng cho phép trong thời gian ngắn, chúng ta sẽ coi đây là hành vi tấn công và chặn yêu cầu.

## 1. Mục tiêu của đề tài

Mục tiêu của đề tài này là xây dựng một hệ thống giúp **phát hiện** và **ngăn chặn** các cuộc tấn công **fuzzing** trên các endpoint của ứng dụng web. Trong trường hợp cụ thể này, chúng ta tập trung bảo vệ ứng dụng khỏi kiểu tấn công **IDOR (Insecure Direct Object References)**. IDOR xảy ra khi hacker cố tình thay đổi giá trị tham số như `id` trong URL để truy cập trái phép vào tài nguyên của người dùng khác. 

Ví dụ:
- Endpoint: `/resource/?id=1`
- Hacker có thể thay đổi giá trị `id` một cách liên tục, chẳng hạn `/resource/?id=2`, `/resource/?id=3`,... để khai thác các tài nguyên không thuộc quyền truy cập của họ.

Đề tài này sẽ đặt mục tiêu:
- Phát hiện hành vi **fuzzing**, khi hacker cố gắng thay đổi tham số `id` quá nhiều lần trong một khoảng thời gian ngắn.
- Ngăn chặn các yêu cầu tiếp theo từ đối tượng tấn công khi phát hiện hành vi đáng ngờ.

## 2. Tổng quan về các khái niệm liên quan

### 2.1. Fuzzing
**Fuzzing** là một kỹ thuật tấn công mà hacker gửi nhiều yêu cầu với dữ liệu thay đổi liên tục nhằm mục đích phát hiện lỗ hổng bảo mật. Trong trường hợp IDOR, hacker có thể gửi hàng loạt yêu cầu với giá trị `id` khác nhau để cố gắng truy cập dữ liệu của người dùng khác.

### 2.2. IDOR (Insecure Direct Object References)
IDOR là một lỗ hổng bảo mật cho phép hacker truy cập trực tiếp vào các đối tượng (dữ liệu, tài nguyên) thông qua việc thay đổi các tham số trong yêu cầu (ví dụ: `id` của đối tượng). Nếu không có cơ chế kiểm tra quyền truy cập chính xác, hacker có thể sử dụng kiểu tấn công này để truy cập thông tin nhạy cảm của người dùng khác.

## 3. Phương pháp phát hiện và ngăn chặn

### 3.1. Phát hiện hành vi tấn công Fuzzing
Để phát hiện hành vi fuzzing, hệ thống sẽ giám sát số lượng yêu cầu với các giá trị `id` khác nhau từ cùng một địa chỉ IP trong một khoảng thời gian ngắn. Nếu số lần thay đổi giá trị `id` vượt quá một ngưỡng nhất định, hệ thống sẽ xác định đây là hành vi tấn công.

### 3.2. Ngăn chặn tấn công
Khi phát hiện hành vi fuzzing:
- Hệ thống sẽ chặn các yêu cầu tiếp theo từ địa chỉ IP nghi ngờ trong một khoảng thời gian.
- Ghi lại log để phục vụ cho việc phân tích sau này.
- Cảnh báo đến quản trị viên về hành vi tấn công.

## 4. Định hướng thực hiện

### 4.1. Sử dụng Django Framework
**Django** là framework chính được sử dụng để xây dựng ứng dụng web và các endpoint. Với hệ thống routing mạnh mẽ và hỗ trợ tốt về bảo mật, Django sẽ cung cấp nền tảng để thực hiện các biện pháp phát hiện và ngăn chặn tấn công IDOR.

### 4.2. Sử dụng Middleware trong Django
**Middleware** sẽ được sử dụng để giám sát tất cả các yêu cầu tới endpoint `/resource/?id=...`. Middleware này sẽ:
- Theo dõi số lượng yêu cầu đến từ cùng một địa chỉ IP.
- Ghi lại giá trị `id` của mỗi yêu cầu và kiểm tra tần suất thay đổi giá trị này.
- Ngăn chặn yêu cầu nếu phát hiện hành vi fuzzing.

### 4.3. Kết hợp Nginx và Gunicorn
**Nginx** sẽ được sử dụng như một **reverse proxy** để quản lý lưu lượng truy cập vào ứng dụng và hỗ trợ bảo mật. Kết hợp với **Gunicorn** để chạy ứng dụng Django, hệ thống sẽ đảm bảo hiệu năng và khả năng mở rộng, đồng thời cho phép xử lý nhiều kết nối cùng lúc.

- **Nginx** sẽ giúp quản lý lưu lượng yêu cầu từ client, bảo vệ khỏi các cuộc tấn công DDoS cơ bản.
- **Gunicorn** sẽ xử lý các yêu cầu từ Nginx và truyền chúng vào Django để xử lý logic phát hiện tấn công IDOR.

### 4.4. Sử dụng WebSocket (nếu cần)
Nếu ứng dụng có yêu cầu thời gian thực, chẳng hạn như cập nhật trạng thái cảnh báo về các cuộc tấn công, **WebSocket** có thể được tích hợp để gửi cảnh báo ngay lập tức cho quản trị viên khi phát hiện tấn công IDOR.

### 4.5. Cơ chế Rate Limiting (Giới hạn tốc độ yêu cầu)
Một phần quan trọng trong việc phát hiện tấn công fuzzing là giới hạn số lượng yêu cầu từ một địa chỉ IP trong một khoảng thời gian ngắn. Sử dụng cơ chế **rate limiting**, hệ thống có thể ngăn chặn kịp thời các cuộc tấn công bằng cách giới hạn số lượng yêu cầu mà một người dùng có thể thực hiện trong một thời gian nhất định.

## 5. Kết luận

Bằng cách kết hợp các công nghệ như **Django**, **Nginx**, **Gunicorn**, và **WebSocket**, hệ thống sẽ có khả năng phát hiện và ngăn chặn các cuộc tấn công fuzzing nhắm vào các endpoint của ứng dụng web. Đặc biệt, hệ thống sẽ bảo vệ ứng dụng khỏi các tấn công **IDOR** bằng cách giám sát và chặn những yêu cầu có dấu hiệu nghi vấn, từ đó tăng cường bảo mật và đảm bảo tính toàn vẹn của dữ liệu người dùng.


## Giới Thiệu Middleware

Middleware chống fuzzing được phát triển để theo dõi các yêu cầu từ phía người dùng dựa trên địa chỉ IP và tham số `id` của họ. Middleware này hoạt động như sau:

- Theo dõi số lượng thay đổi liên tiếp của tham số `id` trong một khoảng thời gian nhất định.
- Nếu số lần thay đổi vượt quá ngưỡng cho phép (ví dụ 10 lần), yêu cầu sẽ bị chặn và trả về mã lỗi HTTP 403.
- Middleware cũng có thể reset lại bộ đếm nếu không có thay đổi nào trong một thời gian nhất định.

## Cách Middleware Được Code và Hoạt Động

### 1. Cấu Trúc Dự Án
- **myapp**: Ứng dụng chính chứa endpoint và logic xử lý.
- **middleware**: Chứa middleware `IDFuzzingMiddleware` để theo dõi và chặn fuzzing.

### 2. Cách Code Middleware

Middleware `IDFuzzingMiddleware` hoạt động như sau:

- Khi có yêu cầu đến, middleware sẽ lấy địa chỉ IP của người dùng và tham số `id` từ query string.
- Lưu lại thông tin người dùng, bao gồm địa chỉ IP, giá trị `id` cuối cùng, số lần thay đổi `id`, và thời gian bắt đầu theo dõi.
- Nếu số lần thay đổi giá trị `id` liên tiếp vượt quá ngưỡng (mặc định là 10 lần trong vòng 30 giây), middleware sẽ trả về phản hồi chặn yêu cầu với mã 403 (Forbidden).

### 3. Cách Cài Đặt

Để tích hợp middleware này vào dự án Django, ta cần thực hiện các bước sau:

1. Thêm middleware vào danh sách `MIDDLEWARE` trong file `settings.py`:
    ```python
    MIDDLEWARE = [
        ...,
        'myapp.middleware.IDFuzzingMiddleware',
    ]
    ```

2. Thêm endpoint vào file `urls.py` để người dùng có thể truy cập tài nguyên:
    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('resource/', views.get_resource),
    ]
    ```

3. Triển khai logic trong file `views.py` để hiển thị dữ liệu theo `id`:
    ```python
    from django.http import JsonResponse

    def get_resource(request):
        id_value = request.GET.get('id')
        return JsonResponse({"message": f"Accessing resource with id={id_value}"})
    ```

### 4. Cách Middleware Hoạt Động
Khi người dùng gửi nhiều yêu cầu đến `/resource/?id=`, middleware sẽ giám sát các giá trị `id` được yêu cầu. Nếu phát hiện số lần thay đổi `id` vượt quá 10 lần trong vòng 30 giây, middleware sẽ chặn yêu cầu và trả về phản hồi:

```json
{
  "message": "Request blocked due to suspicious behavior"
}