from App.models import CartItem, Order


# 获得用户的购物车商品列表
def getUserCartItems(request):
    userid = request.session.get('userid', None)
    if userid:
        cartItems = CartItem.objects.filter(user_id=userid).filter(order_id=None)
        return cartItems
    return None


def getCartItems(request, ordered=None, unordered=None, select=None, unselected=None, goodsid=None):
    items = getUserCartItems(request)
    if ordered:
        items = items.exclude(order_id=None)
    if unordered:
        items = items.filter(order_id=None)
    if select:
        items = items.filter(select=1)
    if unselected:
        items = items.filter(select=0)
    if goodsid:
        items = items.filter(goods_id=goodsid)
    return items


def getTotalPrice(request):
    totalPrice = 0
    items = getCartItems(request, unordered=True, select=True)
    for item in items:
        totalPrice += item.gnum * item.goods.price
    return '%.2f' % (totalPrice)


def getUserOrders(request):
    userid = request.session.get('userid', None)
    if userid:
        orders = Order.objects.filter(ouser_id=userid)
        if orders:
            unpaidOrders = orders.filter(ostatus=0)
            paidOrders = orders.filter(ostatus=1)
            unfeedbackOrders = orders.filter(ostatus=2)

            data = {
                'orders': orders,
                'unpaidOrders': unpaidOrders,
                'paidOrders': paidOrders,
                'unfeedbackOrders': unfeedbackOrders,
            }
            return data

    return None
