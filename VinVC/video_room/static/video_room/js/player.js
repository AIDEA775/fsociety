var aspect_ratio;

function resizePlayer() {
    var new_height = aspect_ratio * $("#player").width();
    if (new_height < $("#chat-room-container").height()) {
        $("#player").height(new_height);
    }
}

videojs("player").ready(function(){
    var vid = document.getElementById("player_html5_api");
    vid.addEventListener( "loadedmetadata", function (e) {
        var width = this.videoWidth,
            height = this.videoHeight;
        aspect_ratio = height / width;

        resizePlayer();
    }, false );
});

$(window).resize(function() {
    if (aspect_ratio)
      resizePlayer();
});