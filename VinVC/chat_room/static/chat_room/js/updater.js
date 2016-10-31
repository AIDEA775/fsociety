var last_seen_id = null;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

if (typeof csrftoken  === 'undefined' || csrftoken  === null) {
    var csrftoken = getCookie('csrftoken');
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (settings.type === "POST" && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function updateChat( data ) {
    for (var i in data) {
        date = new Date(data[i].date);
        $("#comments").append("<li>USER = " + data[i].user +
                              " COMMENT = " + data[i].msg +
                              " TIME = " + date.toLocaleTimeString() + "</li>");
        last_seen_id = data[i].id;
    }
}

$(function() {
    $('#btn').attr('disabled', 'disabled');
    $('#ms').keyup(function() {
        $('#ms').each(function() {
            if ($(this).val().replace(/\s/g, "") .length == 0) {
                $('#btn').attr('disabled', 'disabled');
            } else {
                $('#btn').removeAttr('disabled');
            }
        });
    });

    function getNewComments() {
        $.ajax({
            type: "POST",
            url: "/chat_room/" + chat_room_id + "/api/",
            data: {
                last_seen_id: last_seen_id
            },
            success: function( data ) {
                updateChat( data );
            }
        });

        setTimeout( getNewComments, 3000 );
    }

    getNewComments();

});

function sendMessage() {
    var msg = $("#ms").val();

    $.ajax({
        type: "POST",
        url: "/chat_room/" + chat_room_id + "/api/",
        data: {
            msg: msg,
            last_seen_id: last_seen_id
        },
        success: function( data ) {
            updateChat(data);
        }
    });
}
