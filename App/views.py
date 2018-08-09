import uuid

import time
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.cache import cache_page

from App.DBUtill import *
from App.PayUtil import pay
from App.models import *


# 访问主页的响应函数
def index(request):
    # 重定向到/app/home
    return redirect(reverse('app:home'))

@cache_page(60*60,cache='default')
def home(request):

    time.sleep(5)

    # 查询轮播、导航、必购、商店数据
    wheels = Wheel.objects.all()
    navs = Nav.objects.all()
    mustbuys = Mustbuy.objects.all()

    shops = Shop.objects.all()

    # 对查询到的数据容器进行切片分类
    shop0 = shops[0]
    shops2 = shops[1:3]
    shops4 = shops[3:7]
    shopsx = shops[7:]

    mainshows = Mainshow.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop0': shop0,
        'shops2': shops2,
        'shops4': shops4,
        'shopsx': shopsx,
        'mainshows': mainshows,
    }

    # 将数据丢给页面进行渲染
    return render(request, 'home.html', context=data)


'''
foodtypes
goodss
childdict（cid:cname）
categoryid childid sortid
'''
sortRules = (
    ('0', 'id', '默认排序'),
    ('1', '-productnum', '销量排序'),
    ('2', '-price', '价格降序'),
    ('3', 'price', '价格升序'),
)

@cache_page(60*60,cache='redis')
def market(request, categoryid, childid, sortid):

    time.sleep(5)

    # 查询数据
    foodtypes = FoodType.objects.all().order_by('typesort')

    # 查出大类下的所有商品
    goodss = Goods.gmanager.filter(categoryid=categoryid)

    # childid=0代表所有的小类，所以无需筛选
    if int(childid) > 0:
        goodss = goodss.filter(childcid=childid)

    # sortid=0代表默认排序，所以无需排序
    if int(sortid) > 0:
        goodss = goodss.order_by(sortRules[int(sortid)][1])

    # 找出当前大类：eg牛奶面包
    ftype = foodtypes.filter(typeid=categoryid).first()

    # childtypenames形如：全部分类:0#酸奶乳酸菌:103537#牛奶豆浆:103538#面包蛋糕:103540
    # 炸开为小类信息列表
    items = ftype.childtypenames.split("#")

    # 将[全部分类:0,酸奶乳酸菌:103537,牛奶豆浆:103538,面包蛋糕:103540]中的每一项使用【冒号:】炸开
    # 炸开后使用103537为key，使用‘酸奶乳酸菌’为value，形成小类字典
    childdict = {s.split(':')[1]: s.split(':')[0] for s in items}

    data = {
        'foodtypes': foodtypes,
        'goodss': goodss,
        'childdict': childdict,
        'categoryid': categoryid,
        'childid': childid,
        'sortid': sortid,
        'childname': childdict[childid],
        'sortname': sortRules[int(sortid)][2],
    }
    return render(request, 'market.html', context=data)


def cart(request):
    # 查询当前登录用户的所有购物车数据
    cartItems = getCartItems(request, unordered=True)
    print('cartItems=', cartItems)

    if cartItems:
        data = {
            'cartItems': cartItems,
            'total': getTotalPrice(request),
        }
        return render(request, 'cart2.html', context=data)

    else:
        return render(request, 'cart-empty.html')


def mine(request):
    utoken = request.COOKIES.get('utoken', None)
    user = User.objects.filter(utoken=utoken).first()
    uicon = '/static/uploads/' + str(user.uicon)

    orders = Order.objects.filter(ouser=user)
    unpaidOrders = orders.filter(ostatus=0)
    paidOrders = orders.filter(ostatus=1)

    data = {
        'user': user,
        'uicon': uicon,
        'unpaid': len(unpaidOrders),
        'paid': len(paidOrders),
    }
    return render(request, 'mine.html', context=data)


'''
用户注册：
从表单的POST数据和FILES数据中获取用户属性，并插入相应的记录
'''


def register(request):
    if request.method == 'GET':
        data = {
            'title': '注册'
        }
        return render(request, 'register.html', context=data)

    else:
        uname = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)
        upwd2 = request.POST.get('upwd2', None)

        # 从表单中获取文件数据直接赋值为ImageField字段uicon,框架会自动将文件中的图片存储到MEDIA_ROOT所对应的文件夹
        uicon = request.FILES.get('uicon', None)

        if uname and upwd and upwd2 and uicon and upwd2 == upwd:
            user = User()
            user.uname = uname
            user.upwd = upwd
            user.uicon = uicon

            # 插入数据记录+将uicon对应的文件下载到MEDIA_ROOT对应的文件夹
            user.save()

            # 注册成功后静默登录
            return login(request)

        return HttpResponse('注册失败')


'''
从表单中获取用户数据，与数据库进行比对，判断登录是否成功
会话选型用seesion:将要使用的用户信息一一存储在session的具体key-value中
会话选型用token:后端直接将token植入在user表里，找到token即等于找到所有用户信息
'''


def login(request):
    if request.method == 'GET':
        data = {
            'title': '登录'
        }
        return render(request, 'login.html', context=data)

    else:
        uname = request.POST.get('uname', None)
        upwd = request.POST.get('upwd', None)

        if uname and upwd:
            user = User.objects.filter(uname=uname).first()
            if user and user.upwd == upwd:
                # 生成宇宙唯一的token
                utoken = uuid.uuid4()

                # 登录成功后跳转个人中心页
                resp = HttpResponseRedirect(reverse('app:mine'))

                # 后端将token植入user表
                user.utoken = utoken
                user.save()

                # 前端也持有相同的token
                resp.set_cookie('utoken', utoken)
                request.session['userid'] = user.id

                return resp

    return HttpResponse('登录失败')


def logout(request):
    resp = HttpResponseRedirect(reverse('app:home'))

    # 将token从前端拿走
    resp.delete_cookie('utoken')
    request.session.flush()

    return resp

@cache_page(60*60*24*30,cache='redis')
def fuckoff(request):
    return render(request, 'fuckoff.html')


def addCart(request):
    data = {
        'status': 900,
        'msg': 'add failed!'
    }

    # 哪个用户，对哪个商品，增加1个购买意向
    userid = request.session.get('userid', None)
    if userid:
        goodsid = request.GET.get('goodsid', None)
        itemid = request.GET.get('itemid', None)

        if not itemid:
            # 新增或修改购物车记录
            cartItem = getCartItems(request, unordered=True, goodsid=goodsid).first()
            print('addCart cartItem=', cartItem)
            if not cartItem:
                cartItem = CartItem()
                cartItem.user_id = userid
                cartItem.goods_id = goodsid
                cartItem.gnum = 0

        else:
            cartItem = CartItem.objects.get(pk=itemid)

        cartItem.gnum = cartItem.gnum + 1
        cartItem.save()

        data['status'] = 200
        data['msg'] = 'add ok!'
        data['gnum'] = cartItem.gnum
        data['total'] = getTotalPrice(request)

    else:
        data['status'] = 901
        data['msg'] = 'not login'

    return JsonResponse(data)


def subCart(request):
    data = {
        'status': 900,
        'msg': 'add failed!'
    }

    # 哪个用户，对哪个商品，增加1个购买意向
    userid = request.session.get('userid', None)
    if userid:
        goodsid = request.GET.get('goodsid', None)
        itemid = request.GET.get('itemid', None)

        if not itemid:
            # 查询对应的购物车商品记录
            cartItem = getCartItems(request, unordered=True, goodsid=goodsid).first()
        else:
            cartItem = CartItem.objects.get(pk=itemid)

        if cartItem:
            cartItem.gnum = cartItem.gnum - 1
            if cartItem.gnum < 1:
                cartItem.gnum = 0
            cartItem.save()

            data['status'] = 200
            data['msg'] = 'sub ok!'
            data['gnum'] = cartItem.gnum
            data['total'] = getTotalPrice(request)

    else:
        data['status'] = 901
        data['msg'] = 'not login'

    return JsonResponse(data)


def swapSelect(request):
    data = {}
    cartid = request.GET.get('cartid', None)

    if not cartid:
        # 没有传递cartid
        pass

    elif cartid == 'all':
        # 全选或全不选
        cartItems = getUserCartItems(request)
        if cartItems:
            select = not cartItems.first().select
            for cartItem in cartItems:
                if cartItem.select != select:
                    cartItem.select = select
                    cartItem.save()

            data['status'] = 200
            data['select'] = cartItems.first().select
            data['total'] = getTotalPrice(request)

            return JsonResponse(data)

    else:
        # 改变一个CartItem的选中状态
        cartItem = CartItem.objects.filter(pk=cartid).first()
        if cartItem:
            cartItem.select = not cartItem.select
            cartItem.save()
            data['status'] = 200
            data['select'] = cartItem.select
            data['total'] = getTotalPrice(request)

            '''
            # 在服务端查询该用户的购物车是否全选，大大增加服务端压力，不可取
            data['all'] = 1
            items = getCartItems(request,unordered=True)
            for item in items:
                if item.select == 0:
                    data['all'] = 0
                    break
            '''

            return JsonResponse(data)

    data['status'] = 902
    data['msg'] = '请传递合法的cartid'
    return JsonResponse(data)


# 生成订单：查询当前用户的所有【选中而未下单的购物车商品】，将其order_id变为新建的订单id
def genOrder(request):
    cartItems = getUserCartItems(request)
    print('getUserCartItems=', cartItems)
    if cartItems:
        cartItems = cartItems.filter(select=1).filter(order_id=None)
        print('选中而未下单的购物车商品=', cartItems)
        if cartItems:
            order = Order()
            order.ouser_id = request.session['userid']
            order.save()

            for item in cartItems:
                item.order_id = order.id
                item.save()

            data = {
                'cartItems': cartItems,
                'orderid': order.id,
            }
            return render(request, 'genorder.html', context=data)

    return redirect(reverse('app:cart'))


def payOrder(request, orderid):
    # 此处调用支付宝的接口，并取得支付结果
    result = pay('王思聪', '本大人', '123456', '987654321.00', '我很崇拜你呀')
    if result:
        order = Order.objects.filter(pk=orderid).first()
        if order:
            order.ostatus = 1
            order.save()
            return redirect(reverse('app:mine'))

    return HttpResponse('支付失败！')


def myOrders(request, orderStatus):
    data = getUserOrders(request)
    print('myOrders data=', data)
    if data:
        orderStatus = int(orderStatus)
        if orderStatus == Order.STATUS_ALL:
            data = {
                'orders': data['orders'],
            }
            return render(request, 'allorders.html', context=data)

        elif orderStatus == Order.STATUS_UNPAID:
            # 自行返回相关页面
            return render(request, 'fuckoff.html')

        elif orderStatus == Order.STATUS_PAID:
            # 自行返回相关页面
            return render(request, 'fuckoff.html')

        else:
            print('fuck=', orderStatus)
            # 自行返回相关页面
            return render(request, 'fuckoff.html')

    return HttpResponse('没有订单')
