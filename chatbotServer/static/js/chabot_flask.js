$(document).ready(function() {
    $('#chatbot-form-btn').click(function(e) {
        e.preventDefault();
        $('#chatbot-form').submit();
    });

    $('#chatbot-form').submit(function(e) {
        e.preventDefault();

        var message = $('#messageText').val();
        $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body"><strong>User:    </strong>' + message + '<hr/></div></div></div></li>');
        $.ajax({
            type: "POST",
            url: "/ask",
            data: $(this).serialize(),
            success: function(response) {
                $('#messageText').val('');

                var answer = response.answer;
                const chatPanel = document.getElementById("chatPanel");
                $(".media-list").append('<li class="media"><div class="media-body"><div class="media"><div class="media-body"><strong>Bot:    </strong>' + answer + '<hr/></div></div></div></li>');
    $(".fixed-panel").stop().animate({ scrollTop: $(".fixed-panel")[0].scrollHeight}, 1000);
            
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
