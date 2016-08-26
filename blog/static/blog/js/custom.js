function request() {
        $.ajax({
            url: 'http://127.0.0.1:8000/blog/hello/',
            success: function(data) {
                $('#para').html(data)
            }
        }).error(function() {
            alert('Error');
        });
    }

setInterval(request, 5000);