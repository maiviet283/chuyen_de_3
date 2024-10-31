import time
from django.core.cache import cache
from django.shortcuts import render

# Thiết lập thời gian và số lần chặn
BLOCK_THRESHOLD = 5  # Số lần chấp nhận thay đổi id
TIME_FRAME = 30  # Thời gian tối đa cho các lần thay đổi liên tiếp (tính bằng giây)
BLOCK_TIME = 45  # Thời gian chặn (45 giây cho dễ test)

class IDFuzzingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0]
        current_id = request.GET.get('id')
        current_time = time.time()

        # Kiểm tra xem IP có đang bị chặn không
        block_start_time = cache.get(f'blocked_{user_ip}')
        if block_start_time and current_time - block_start_time < BLOCK_TIME:
            return render(request, 'myapp/blocked.html', {'message': 'IP của bạn đã bị chặn do hành vi đáng ngờ'}, status=403)
        elif block_start_time:
            cache.delete(f'blocked_{user_ip}')

        user_data = cache.get(user_ip, {'last_id': None, 'count': 0, 'start_time': current_time})
        if current_time - user_data['start_time'] > TIME_FRAME:
            user_data = {'last_id': current_id, 'count': 1, 'start_time': current_time}
        else:
            if current_id != user_data['last_id']:
                user_data['count'] += 1
                user_data['last_id'] = current_id
            else:
                user_data['count'] = 1

            if user_data['count'] > BLOCK_THRESHOLD:
                cache.set(f'blocked_{user_ip}', current_time, BLOCK_TIME)
                return render(request, 'myapp/blocked.html', {'message': 'IP của bạn đã bị chặn do hành vi đáng ngờ'}, status=403)

        cache.set(user_ip, user_data, TIME_FRAME)
        return self.get_response(request)
