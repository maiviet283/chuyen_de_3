from django.shortcuts import render,HttpResponse

# Create your views here.

def get_resource(request):
    # Lấy địa chỉ IP từ request
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]  # Lấy IP đầu tiên
    else:
        user_ip = request.META.get('REMOTE_ADDR')  # Nếu không có, lấy REMOTE_ADDR

    id_value = request.GET.get('id')  # Lấy giá trị ID từ query string

    # Truyền cả IP và ID vào context để hiển thị trên trang
    return render(request, 'myapp/index.html', {
        'message': f"Đang truy cập tài nguyên có ID = {id_value}",
        'user_ip': user_ip
    })



def index(request):
    return HttpResponse("<h1>Xin Chào</h1>")