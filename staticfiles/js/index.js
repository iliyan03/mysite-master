/* Load posts on scroll */

$(function(){
    $('div.post').slice(0, 2).show();
})

function getDocHeight() {
    var D = document;
    let docHeight = Math.max(
        D.body.scrollHeight, D.documentElement.scrollHeight,
        D.body.offsetHeight, D.documentElement.offsetHeight,
        D.body.clientHeight, D.documentElement.clientHeight
    );
    let closest = [];
    for(let i = 0; i < 5; i++){
        let num = docHeight - i;
        closest.push(num);
    }
    return docHeight
}

$(window).scroll(function() {
    let height = Math.floor($(window).scrollTop() + $(window).height());
    if(height == getDocHeight()) {
        $('div.post:hidden').slice(0, 2).slideDown();
    }
});

