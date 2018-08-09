from django.db import models


# Create your models here.
# 轮播、导航、必购、商店的数据拥有相同的字段
# 定义共同的父类以节省代码
class Recommend(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=20)

    # 将父类定义为抽象类（不会创建表）
    class Meta:
        abstract = True


# 轮播，继承父类拥有其全部字段
class Wheel(Recommend):
    class Meta:
        db_table = 'axf_wheel'


# 导航
class Nav(Recommend):
    class Meta:
        db_table = 'axf_nav'


# 必购
class Mustbuy(Recommend):
    class Meta:
        db_table = 'axf_mustbuy'


# 商店
class Shop(Recommend):
    class Meta:
        db_table = 'axf_shop'


'''
insert into axf_mainshow(
trackid,name,img,
categoryid,brandname,
img1,childcid1,productid1,longname1,price1,marketprice1,
img2,childcid2,productid2,longname2,price2,marketprice2,
img3,childcid3,productid3,longname3,price3,marketprice3)
values(
"21782","优选水果","http://img01.bqstatic.com//upload/activity/2017031018205492.jpg@90Q.jpg",
"103532","爱鲜蜂",
"http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164159_996462.jpg@200w_200h_90Q","103533","118824","爱鲜蜂·特小凤西瓜1.5-2.5kg/粒","25.80","25.8",
"http://img01.bqstatic.com/upload/goods/201/611/1617/20161116173544_219028.jpg@200w_200h_90Q","103534","116950","蜂觅·越南直采红心火龙果350-450g/盒","15.3","15.8",
"http://img01.bqstatic.com/upload/goods/201/701/1916/20170119164119_550363.jpg@200w_200h_90Q","103533","118826","爱鲜蜂·海南千禧果400-450g/盒","9.9","13.8");
'''


class Mainshow(Recommend):
    categoryid = models.CharField(max_length=20)
    brandname = models.CharField(max_length=20)

    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=20)
    productid1 = models.CharField(max_length=20)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=20)
    productid2 = models.CharField(max_length=20)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=20)
    productid3 = models.CharField(max_length=20)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'


'''
insert into axf_foodtypes
(typeid,typename,childtypenames,typesort)
values
("104749","热销榜","全部分类:0",1),("104747","新品尝鲜","全部分类:0",2),("103532","优选水果","全部分类:0#进口水果:103534#国产水果:103533",3),("103581","卤味熟食","全部分类:0",4),("103536","牛奶面包","全部分类:0#酸奶乳酸菌:103537#牛奶豆浆:103538#面包蛋糕:103540",5),("103549","饮料酒水","全部分类:0#饮用水:103550#茶饮/咖啡:103554#功能饮料:103553#酒类:103555#果汁饮料:103551#碳酸饮料:103552#整箱购:104503#植物蛋白:104489#进口饮料:103556",6),("103541","休闲零食","全部分类:0#进口零食:103547#饼干糕点:103544#膨化食品:103543#坚果炒货:103542#肉干蜜饯:103546#糖果巧克力:103545",7),("103557","方便速食","全部分类:0#方便面:103558#火腿肠卤蛋:103559#速冻面点:103562#下饭小菜:103560#罐头食品:103561#冲调饮品:103563",8),("103569","粮油调味","全部分类:0#杂粮米面油:103570#厨房调味:103571#调味酱:103572",9),("103575","生活用品","全部分类:0#个人护理:103576#纸品:103578#日常用品:103580#家居清洁:103577",10),("104958","冰激凌","全部分类:0",11);
'''


# 食品种类模型
class FoodType(models.Model):
    # 将typeid声明为主键
    typeid = models.CharField(max_length=20, primary_key=True)

    typename = models.CharField(max_length=20)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1024)

    # 输出和打印实例时，显示typename
    def __str__(self):
        return self.typename

    class Meta:
        db_table = 'axf_foodtypes'


'''
insert into axf_goods
(productid,productimg,productname,productlongname,
isxf,pmdesc,specifics,price,marketprice,
categoryid,childcid,childcidname,dealerid,storenums,productnum)
 values
 ("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q","","乐吧薯片鲜虾味50.0g",
 0,0,"50g",2.00,2.500000,
 103541,103543,"膨化食品","4858",200,4);
'''


# 商品模型管理器
class GoodsManager(models.Manager):
    # 覆写了BaseManager,实现查询时默认过滤掉已下架的商品
    def get_queryset(self):
        return super().get_queryset().exclude(onSale=False)


# 商品模型
class Goods(models.Model):
    productid = models.CharField(max_length=20)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=100, verbose_name='商品名称')
    isxf = models.BooleanField(default=False, verbose_name='是否精选')
    pmdesc = models.BooleanField(default=False, verbose_name='店长推荐')
    specifics = models.CharField(max_length=20, verbose_name='规格')
    price = models.FloatField(default=0, verbose_name='价格')
    marketprice = models.FloatField(default=0, verbose_name='市场价')

    # 当前商品的大类id，外键指向FoodType
    categoryid = models.ForeignKey(FoodType, default=None, null=True, blank=True, verbose_name='大类')

    childcid = models.IntegerField(default=None, null=True, blank=True)
    childcidname = models.CharField(max_length=20, verbose_name='小类')
    dealerid = models.CharField(max_length=20, verbose_name='商家id')
    storenums = models.IntegerField(default=0, verbose_name='库存')
    productnum = models.IntegerField(default=0, verbose_name='销量')

    # 是否在架
    # onSale = models.BooleanField(default=1, )
    onSale = models.BooleanField(default=True)

    # 交由管理器进行管理
    gmanager = GoodsManager()

    class Meta:
        db_table = 'axf_goods'
        verbose_name_plural = '商品'


class User(models.Model):
    uname = models.CharField(max_length=20, unique=True)
    upwd = models.CharField(max_length=20)

    # 需要依赖于pillow
    uicon = models.ImageField()
    utoken = models.CharField(max_length=100, default=None, null=True, blank=True)
    ulevel = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_user'


# 订单模型
class Order(models.Model):

    STATUS_UNPAID = 0
    STATUS_PAID = 1
    STATUS_UNFEEDBACK = 2
    STATUS_ALL = 9

    # 哪个用户
    ouser = models.ForeignKey(User)

    # 什么时间下单
    otime = models.DateTimeField(auto_now_add=True)

    # 当前状态：0=未支付，1=已支付，2=已签收（待评价）,9=所有类型
    ostatus = models.IntegerField(default=0)


# 购物车模型，里面的记录代表一个的采购意向
class CartItem(models.Model):
    # 哪个用户
    user = models.ForeignKey(User)

    # 看中了什么商品
    goods = models.ForeignKey(Goods)

    # 想购买多少件
    gnum = models.IntegerField(default=0)

    # 选中了没有
    select = models.BooleanField(default=True)

    # 最终下单在哪一单
    order = models.ForeignKey(Order, default=None, null=True, blank=True)
