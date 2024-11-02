### Kiến thức về Redis Cache và Tác động của nó trong Dự Án

**Redis** là một công cụ lưu trữ dữ liệu **cache** trong bộ nhớ, nhanh và hiệu quả, được sử dụng rộng rãi để tối ưu hóa hiệu suất của các ứng dụng web. Khi ứng dụng có những thao tác cần truy xuất dữ liệu thường xuyên, như lấy danh sách sản phẩm, thông tin người dùng, Redis giúp giảm tải cho **database chính** bằng cách lưu trữ tạm thời những dữ liệu này.

#### Redis Cache là gì?

- **Redis** là một hệ quản trị cơ sở dữ liệu kiểu **NoSQL** dạng key-value, chạy trên bộ nhớ RAM, có khả năng truy xuất dữ liệu rất nhanh.
- **Cache** là bộ nhớ tạm thời lưu trữ các bản sao dữ liệu từ database, giúp ứng dụng truy xuất dữ liệu này nhanh hơn mà không cần kết nối trực tiếp với database mỗi lần.

#### Cách Redis Cache hoạt động trong Dự Án

1. **Lưu trữ dữ liệu tạm thời**:
   - Khi một endpoint của Django cần dữ liệu từ database, hệ thống sẽ kiểm tra Redis trước. Nếu dữ liệu đã có trong Redis (**cache hit**), ứng dụng sẽ lấy dữ liệu từ Redis mà không phải truy cập database.
   - Nếu dữ liệu chưa có trong Redis (**cache miss**), ứng dụng sẽ truy vấn từ database, sau đó lưu dữ liệu đó vào Redis để phục vụ cho các lần truy cập sau.

2. **Thiết lập thời gian sống cho dữ liệu (TTL)**:
   - Redis cho phép thiết lập **TTL (Time To Live)** cho từng dữ liệu cache, nghĩa là dữ liệu này sẽ tự động bị xóa sau một khoảng thời gian nhất định. Điều này giúp đảm bảo rằng cache không lưu trữ dữ liệu quá cũ, tránh việc người dùng nhận được thông tin lỗi thời.

3. **Cải thiện tốc độ phản hồi**:
   - Redis giúp giảm tải database, vì các truy vấn lặp lại không cần gửi đến database mà lấy trực tiếp từ cache.
   - Điều này làm tăng tốc độ phản hồi của ứng dụng Django, giúp người dùng trải nghiệm mượt mà hơn.

4. **Tối ưu hóa tải cho database**:
   - Đối với các ứng dụng có lượng người dùng lớn và truy cập thường xuyên, việc truy vấn nhiều vào database sẽ làm hệ thống bị quá tải. Redis giảm thiểu áp lực này, cho phép database chỉ xử lý những truy vấn phức tạp hoặc chưa có trong cache.

#### Tác động của Redis Cache trong Dự Án

1. **Giảm độ trễ**:
   - Redis là một trong những công cụ cache nhanh nhất, với thời gian truy cập dữ liệu chỉ trong vài micro giây. Điều này đặc biệt hữu ích khi ứng dụng có các trang hoặc endpoint yêu cầu tải dữ liệu lớn và thường xuyên.

2. **Tiết kiệm tài nguyên và chi phí**:
   - Bằng cách giảm số lượng truy vấn đến database, Redis giúp tiết kiệm tài nguyên CPU và I/O của hệ thống database, giảm chi phí vận hành và bảo trì hệ thống.

3. **Hỗ trợ khả năng mở rộng**:
   - Redis hoạt động rất tốt khi mở rộng hệ thống. Trong trường hợp cần thêm máy chủ để đáp ứng lượng truy cập lớn, Redis có thể dễ dàng mở rộng quy mô theo chiều ngang (thêm nhiều Redis instance) mà không ảnh hưởng đến hiệu suất.

4. **Cải thiện trải nghiệm người dùng**:
   - Người dùng sẽ thấy tốc độ tải trang nhanh hơn, đặc biệt là đối với các dữ liệu tĩnh hoặc ít thay đổi, ví dụ: bảng xếp hạng, danh sách sản phẩm phổ biến, v.v.

#### Redis Cache trong Mô Hình Dự Án

- **Redis Cache** nằm giữa **Django** và **database chính**. Khi Django cần lấy dữ liệu, nó sẽ ưu tiên truy vấn Redis trước. Nếu dữ liệu có trong Redis, hệ thống sẽ trả về kết quả ngay lập tức từ cache; nếu không có, hệ thống truy vấn từ database và sau đó lưu dữ liệu này vào Redis cho các lần truy cập sau.
  
- **WAF** không can thiệp trực tiếp vào Redis Cache, mà Redis sẽ hoạt động với các lớp bên trong, như middleware và Django.

### Tóm lại

Redis Cache đóng vai trò quan trọng trong việc tăng hiệu suất và tối ưu hóa khả năng phản hồi của hệ thống. Nó giảm tải cho database, giúp ứng dụng phản hồi nhanh hơn, tiết kiệm tài nguyên và đảm bảo rằng người dùng có trải nghiệm tốt nhất khi sử dụng ứng dụng.