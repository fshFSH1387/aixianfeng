from django.conf.urls import url

from App import views

urlpatterns = [

    # 访问主页
    url(r'^home/', views.home, name='home'),

    # 访问商品信息，路由参数：大类id，小类id(0=全部小类)，排序id（0=默认排序）
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.market, name='market'),

    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),

    # 注册、登录、登出
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),

    url(r'^fuckoff/', views.fuckoff, name='fuckoff'),

    url(r'^addcart/', views.addCart, name='addcart'),
    url(r'^subcart/', views.subCart, name='subcart'),
    url(r'^swapselect/', views.swapSelect, name='swapselect'),
    url(r'^genorder/', views.genOrder, name='genorder'),
    url(r'^payorder/(\d+)/', views.payOrder, name='payorder'),
    url(r'^myorders/(\d+)/', views.myOrders, name='myorders'),
]
