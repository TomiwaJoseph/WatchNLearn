

$(document).ready(function(){

    $('#success_tic').on('hidden.bs.modal', function(){
        $('.cart .label').prop('disabled', false)
    })
    $('#success_tic').on('shown.bs.modal', function(){
        $('.cart .label').prop('disabled', true)
    })

    $('.newsletter-box').submit(function(event){
        event.preventDefault();
        $.ajax({
            url: '/newsletter/',
            type: 'POST',
            data: $('.newsletter-box').serialize(),
            success: function(response){
                $('.modal-content h2').text('Successful subscription');
                $('.modal-content p').text('You will receive email alerts anytime a new product is added to shop')
                $('#success_tic').modal('show');
            }
        });
    });

    $(document).on('click', '.wishlist_btn', function(){
        var _btn = $(this);
        var prod_id = $(this).attr("data-id")
        $.ajax({
            url: '/add-to-wishlist/',
            method: 'GET',
            data: {
                product_id: prod_id,
            },
            success: function(response){
                _btn.attr('disabled', true);
                _btn.addClass('active')
                $('.modal-content h2').text('Added to Wishlist')
                $('.modal-content p').text('This product has been successfully added to your wishlist')
                $('#success_tic').modal('show');
            }
        });
    });

    $(document).on('click', '.add_to_cart_btn', function(){
        var _btn = $(this);
        var _product_id = $(this).attr('data-id');
        var _product_title = $(this).attr('data-title');
        var _product_price = $(this).attr('data-price');
        var _product_image = $(this).attr('data-image');
        $.ajax({
            url: '/add-to-cart/',
            data: {
                'product_id': _product_id,
                'product_title': _product_title,
                'product_price': _product_price,
                'product_image': _product_image,
            },
            dataType: 'json',
            beforeSend:function(){
                _btn.attr('disabled', true);
            },
            success: function(res){
                $('.badge-danger').text(res.total_items);
                _btn.attr('disabled', true);
                _btn.addClass('active');
                $('#cart_update').html(res.total_items);
                $('.modal-content h2').text('Added to Cart');
                $('.modal-content p').text('This product has been successfully added to your cart');
                $('#success_tic').modal('show');
            },
        })
    });

    $(document).on('click', '.delete-product', function(){
        var _product_id = $(this).attr('data-item');
        $.ajax({
            url: '/delete-from-cart/',
            data: {
                'id': _product_id,
            },
            success: function(res){
                $('.badge-danger').text(res.totalItems);
                $("#cartList").html(res.data)
                // $('.gr-total .h5').text(' $ ' + res.total_amount)
            }
        })
    })

    $(document).on('click', '.update-product', function(){
        var _product_id = $(this).attr('data-item');
        var _quantity = $(".qty-" + _product_id).val();
        $.ajax({
            url: '/update-cart/',
            data: {
                'id': _product_id,
                'qty': _quantity,
            },
            success: function(res){
                $("#cartList").html(res.data)
                // $('.gr-total .h5').text(' $ ' + res.total_amount)
            }
        })
    })

    $(document).on('click', '.del_wish_item', function(){
        var _product_id = $(this).attr('data-id');
        $.ajax({
            url: '/delete-wishlist-item/',
            data: {
                'id': _product_id,
            },
            success: function(res){
                $('#wishlist_section').html(res.wishlist_products);
                $('.modal-content h2').text('Deleted from wishlist');
                $('.modal-content p').text('This product has been successfully deleted from your wishlist');
                $('#success_tic').modal('show');
            }
        })
    })

})