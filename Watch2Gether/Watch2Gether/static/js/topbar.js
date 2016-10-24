var previousScroll = 0,
    headerOrgOffset = $('#header').height();

$('#header-wrap').height($('#header').height());

$(window).scroll(function () {
    var currentScroll = $(this).scrollTop();
    if (currentScroll > headerOrgOffset) {
        if (currentScroll > previousScroll) {
            $('#header-wrap').slideUp(300);
        } else {
            $('#header-wrap').slideDown(300);
        }
    }
    previousScroll = currentScroll;
});
