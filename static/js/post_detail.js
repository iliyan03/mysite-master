function likeComment(id, url){
    const form = document.getElementById('comment_like_form');
    const input = document.getElementById('comment_id');

    input.setAttribute('value', id);
    form.setAttribute('action', url);

    $("#comment_like_form_submit_btn").click()
}

$(function() {
    $("#comment_like_form").submit(function(event) {
        let comment_id = document.getElementById('comment_id').getAttribute('value');
        let icon_id = 'comment_like_icon_' + comment_id;
        // Stop form from submitting normally
        event.preventDefault();
        var like_form = $(this);
        // Send the data using post
        var posting = $.post( like_form.attr('action'), like_form.serialize() );
        // if success:
        posting.done(function(data) {
            const like_icon = document.getElementById(icon_id);
            if (like_icon.getAttribute('src') == "/static/images/like.png"){
                like_icon.setAttribute('src', "/static/images/liked.png")
            } else{
                like_icon.setAttribute('src', "/static/images/like.png")
            }
            
            let likes_count = document.getElementById('comment_' + comment_id + "_likes");
            likes_count.innerHTML = data;
        });
        // if failure:
        posting.fail(function(data) {
            
        });
    });
});
