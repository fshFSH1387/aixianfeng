# 继承框架中间件
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from aixianfeng.settings import LOGIN_REQUIRED_PATHS, BLACK_LIST


class MyappMiddleware(MiddlewareMixin):

    # 下钩子于所有路由被交给路由表之前
    def process_request(self, request):
        print('process_request>>>>>',request)
        path = request.path
        utoken = request.COOKIES.get('utoken',None)

        #拦截黑名单IP
        # for k,v in request.META.items():
        #     print(k,":",v)
        clientIP = request.META.get('REMOTE_ADDR',None)
        if clientIP in BLACK_LIST and path!='/app/fuckoff/':
            return redirect(reverse('app:fuckoff'))

        if path in LOGIN_REQUIRED_PATHS and not utoken:
            return redirect(reverse('app:login'))



