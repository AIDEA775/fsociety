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

        var li_class;

        if (data[i].user_id === user_id)
            li_class = "self";
        else
            li_class = "other";

        $("#messages-content").append(
            "<li class='"+ li_class +"'>"
                +"<div class='bubble'>"
                    + "<div class='user'><a href=''>" + data[i].user + "</a></div>"
                    + "<hr/>"
                    + "<div class='message-text'>" + data[i].msg + "</div>"
                    + "<div class='message-date'>" + date.toLocaleTimeString() + "</div>"
                + "</div>"
            + "</li>");

        last_seen_id = data[i].id;
    }
}

$(function() {
    $('#msg_submit').attr('disabled', 'disabled');
    $('#chat-input').keyup(function() {
        $('#chat-input').each(function() {
            if ($(this).val().replace(/\s/g, "") .length == 0) {
                $('#msg_submit').attr('disabled', 'disabled');
            } else {
                $('#msg_submit').removeAttr('disabled');
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
    var msg = $("#chat-input").val();

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
