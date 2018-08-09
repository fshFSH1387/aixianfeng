/**
 * Created by sirouyang on 2018/6/7.
 */
$(function () {
    $('.is_choose').click(function () {
        console.log('is_choose')
        //获得goodsid
        var cartid = $(this).attr('cartid')
        var spanSelect = $(this)

        $.getJSON(
            '/app/swapselect/',
            {'cartid': cartid},
            function (data) {
                console.log(data);
                if (data['status'] == 200) {
                    var select = data['select']
                    if (select) {
                        spanSelect.find('span').html('√');
                    } else {
                        spanSelect.find('span').html('');
                        $('#all_select>span>span').html('')
                    }

                    //显示总价
                    $('#total-price').html(data['total']);

                    /*if(data['all']==1){
                     $('#all_select>span>span').html('√')
                     }*/

                    //遍历所有条目中的“√”，如果全部已经勾选，则“全选”也被勾选
                    var all = true;
                    var elements = $('.is_choose');
                    for (var i = 0; i < elements.length; i++) {
                        var e = elements[i];
                        if (e.getElementsByTagName('span')[0].innerHTML == '') {
                            all = false;
                            break;
                        }
                    }
                    if (all == true) {
                        $('#all_select>span>span').html('√');
                    } else {
                        $('#all_select>span>span').html('');
                    }

                }
            }
        )
    })

    $('#all_select').click(function () {
        $.getJSON(
            '/app/swapselect/',
            {'cartid': 'all'},
            function (data) {
                if (data['status'] == 200) {
                    var select = data['select']
                    if (select) {
                        $('.is_choose span,#all_select>span>span').html('√');
                    } else {
                        $('.is_choose span,#all_select>span>span').html('');
                    }

                    //显示总价
                    $('#total-price').html(data['total']);
                }
            }
        )
    })

    // find prev next parent fuck attr html
    $('.addShopping').click(function () {
        console.log('addShopping' + $(this).parents('.menuList').attr('cartid'));
        var btnAdd = $(this);
        var cartid = $(this).parents('.menuList').attr('cartid');

        $.getJSON(
            '/app/addcart/',
            {'itemid': cartid},
            function (data) {
                console.log(data);
                if (data['status'] == 200) {
                    var gnum = data['gnum'];
                    var spanGnum = btnAdd.prev()
                    btnAdd.prev().html(gnum)
                    if (gnum < 1) {
                        spanGnum.css('display', 'none');
                        spanGnum.prev().css('display', 'none');
                    } else {
                        spanGnum.css('display', 'inline-block');
                        spanGnum.prev().css('display', 'inline-block');
                    }

                    //显示总价
                    $('#total-price').html(data['total']);
                }
            }
        )
    });

    $('.subShopping').click(function () {
        console.log('subShopping' + $(this).parents('.menuList').attr('cartid'));
        var btnSub = $(this);
        var cartid = $(this).parents('.menuList').attr('cartid');

        $.getJSON(
            '/app/subcart/',
            {'itemid': cartid},
            function (data) {
                console.log(data);
                if (data['status'] == 200) {
                    var gnum = data['gnum'];
                    var spanGnum = btnSub.next();
                    spanGnum.html(gnum)
                    if (gnum < 1) {
                        spanGnum.css('display', 'none');
                        btnSub.css('display', 'none');
                    } else {
                        spanGnum.css('display', 'inline-block');
                        btnSub.css('display', 'inline-block');
                    }

                    //显示总价
                    $('#total-price').html(data['total']);
                }
            }
        )
    })
})