

$(document).ready(function(){

    $('#success_tic').on('hidden.bs.modal', function(){
        $('.cart .label').prop('disabled', false)
    })
    $('#success_tic').on('shown.bs.modal', function(){
        $('.cart .label').prop('disabled', true)
    })

    $('.newsletter-box').submit(function(event){
        event.preventDefault();
        $('#success_tic h1').removeClass('d-none');
        $('#success_tic').removeClass('reload_page');
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

    $('#success_tic').on('hidden.bs.modal', function () {
        if ($('#success_tic').hasClass('reload_page')) {
            location.reload();
        }
    })

    $(document).on('click', '.trash_btn', function(){
        var _course_id = $(this).attr('data-id');
        $('#success_tic').removeClass('reload_page');
        $('#success_tic').addClass('reload_page');
        $.ajax({
            url: '/delete-bookmark-item/',
            data: {
                '_course_id': _course_id,
            },
            success: function(response){
                $('.modal-content h2').text('Deleted from bookmarks');
                $('.modal-content p').text('This course has been successfully deleted from your wishlist');
                $('#success_tic').modal('show');
            }
        })
    })

    $(document).on('click', '.bookmark_btn', function() {
        var _btn = $(this);
        var course_id = $(this).attr("data-id")
        $('#success_tic h1').removeClass('d-none');
        $('#success_tic').removeClass('reload_page');
        $.ajax({
            url: '/bookmark-it/',
            method: 'GET',
            data: {
                course_id: course_id,
            },
            success: function(response){
                if (response.status == 'success') {
                    _btn.attr('disabled', true);
                    _btn.addClass('active')
                    $('.modal-content h2').text('Added to Bookmarks')
                    $('.modal-content p').text('This course has been successfully added to your bookmarks')
                    $('#success_tic').modal('show');
                } else {
                    $('.modal-content h2').text('Failed to add to Bookmarks')
                    $('.modal-content p').text("Please login before you add course to your bookmarks's list")
                    $('#success_tic h1').addClass('d-none');
                    $('#success_tic').modal('show');
                }
            }
        });
    })

})