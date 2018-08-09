/**
 * Created by sirouyang on 2018/6/5.
 */
$(function () {

    //jq：页面加载完成后执行以下代码
    $('.subShopping').css('display', 'none');
    $('.subShopping').next().css('display', 'none');

    //点击小类名称
    $('#all_types').click(function () {

        //根据盒子的状态，立即改变小箭头的样式（bootstrap样式）
        if ($('#all_types_container').css('display') == 'none') {
            $('#all_type_logo').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        } else {
            $('#all_type_logo').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        }
        //展开小类div
        $('#all_types_container').slideToggle()
    })

    $('#sort_rule').click(function () {
        if ($('#sort_container').css('display') == 'none') {
            $('#sort_rule_logo').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        } else {
            $('#sort_rule_logo').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        }
        //展开排序div
        $('#sort_container').slideToggle()
    });

    //点击展开的盒子，收起自身
    $('#all_types_container').click(function () {
        //立刻改变小箭头的状态为↓
        $('#all_type_logo').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        $(this).slideUp();
    });

    $('#sort_container').click(function () {
        //立刻改变小箭头的状态为↓
        $('#sort_rule_logo').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        $(this).slideUp();
    });


    /*

     $(this)当前被点击的元素

     <a style='color:black;'>你妹</a>
     element.css('color','red')设置元素的CSS样式
     element.css('color')获取元素的CSS样式

     <a href='xxx'>你妹</a>
     element.attr('href','http://www.baidu.com')设置元素的html属性
     element.attr('href')获取元素的html

     <a href='xxx'>你妹</a>
     element.html('我妹')设置元素的html节点内容
     element.html()获取元素的html节点内容

     */

    //点击所有类名为addShopping的元素的监听
    //点击加选商品的业务监听
    $('.addShopping').click(function () {
        console.log('addShopping' + $(this).attr('goodsid'));

        var btnAdd = $(this);
        var goodsid = btnAdd.attr('goodsid');



        //发起ajax请求，get=方法为GET，JSON=返回值类型为JSON

        $.getJSON(
            //请求路由
            '/app/addcart/',

            //GET请求携带的参数
            {'goodsid': goodsid},

            //后端返回时的回调,data=后端返回的数据，格式为JSON
            function (data) {
                console.log(data);

                //前后端【自行约定】的状态码,901=未登录,200=请求成功

                //用户未登录
                if (data['status'] == 901) {
                    //window=浏览器对象
                    //使用浏览器对象在当前窗口打开登录页
                    window.open('/app/login/', target = '_self');
                }

                //请求成功
                else if (data['status'] == 200) {

                    //拿到返回JSON数据中的商品数量
                    var gnum = data['gnum'];

                    //获取btnAdd的上一个元素（其实就是用于显示商品数量的那个span）
                    var spanGnum = btnAdd.prev();

                    //将显示数目的span的文本节点内容设置为后台返回的商品数量
                    spanGnum.html(gnum);

                    //如果购物车中的商品数为0，则隐藏减号和数字
                    if (gnum < 1) {
                        spanGnum.css('display', 'none');
                        spanGnum.prev().css('display', 'none');
                    } else {
                        spanGnum.css('display', 'inline-block');
                        spanGnum.prev().css('display', 'inline-block');
                    }
                }
            }
        )
    });

    $('.subShopping').click(function () {
        console.log('subShopping' + $(this).attr('goodsid'));

        var btnSub = $(this);
        var goodsid = btnSub.attr('goodsid');

        //发起ajax请求，get=方法为GET，JSON=返回值类型为JSON
        $.getJSON(
            //请求路由
            '/app/subcart/',

            //GET请求携带的参数
            {'goodsid': goodsid},

            //后端返回时的回调,data=后端返回的数据，格式为JSON
            function (data) {
                console.log(data);

                //前后端【自行约定】的状态码,901=未登录,200=请求成功

                //用户未登录
                if (data['status'] == 901) {
                    //window=浏览器对象
                    //使用浏览器对象在当前窗口打开登录页
                    window.open('/app/login/', target = '_self');
                }

                //请求成功
                else if (data['status'] == 200) {

                    //拿到返回JSON数据中的商品数量
                    var gnum = data['gnum'];

                    //获取btnAdd的上一个元素（其实就是用于显示商品数量的那个span）
                    var spanGnum = btnSub.next()

                    //将显示数目的span的文本节点内容设置为后台返回的商品数量
                    spanGnum.html(gnum);

                    //如果购物车中的商品数为0，则隐藏减号和数字
                    if (gnum < 1) {
                        btnSub.css('display', 'none');
                        spanGnum.css('display', 'none');
                    } else {
                        btnSub.css('display', 'inline-block');
                        spanGnum.css('display', 'inline-block');
                    }

                }
            }
        )
    })

})
