const navbar = document.querySelector('nav')
const formContainer = document.getElementById('formContainer') 

function changeContainerHeight() {
    let bodyHeight = window.innerHeight;
    let wantedHeight = bodyHeight - navbar.offsetHeight;
    formContainer.style.height = wantedHeight + "px";
}

if (formContainer){
    window.onload = function(){
        changeContainerHeight();
    }
    window.addEventListener('resize', changeContainerHeight);
}

function likePost(id, url){
    const form = document.getElementById('like_form');
    const input = document.getElementById('input_id');

    input.setAttribute('value', id);
    form.setAttribute('action', url);

    $("#like_form_submit_btn").click()
}

/* Like a post */

$(function() {
    $("#like_form").submit(function(event) {
        let icon_id = 'like_icon_' + document.getElementById('input_id').getAttribute('value');
        console.log(icon_id)
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
        });
        // if failure:
        posting.fail(function(data) {
            
        });
    });
});

/* Search input */

const datalist = document.getElementById('users');
const searchFormValue = document.getElementById('searchFormValue'); 

$("#searchFormValue").on("input", function() {
    $("#searchFormSubmitBtn").click()
    let flag = false;
    for(let i = 0; i < datalist.children.length; i++){
        flag = datalist.children[i].value === searchFormValue.value || flag
    }
    if(flag === true){
        $('#search_for_user').attr('name', 'search_for_user');
        $('#search_for_user').attr('value', searchFormValue.value);
        $("#searchFormSubmitBtn").click()
    }
});


$(function() {
    $("#searchForm").submit(function(event) {
        if (document.getElementById('search_for_user').value == ''){
            event.preventDefault();
        }
        // Stop form from submitting normally
        var search_form = $(this);
        // Send the data using post
        var posting = $.post( search_form.attr('action'), search_form.serialize() );
        // if success:
        posting.done(function(data) {
            let user_options = data.user_options;
            datalist.innerHTML = "";
            for (let i=0; i < user_options.length; i++){
                let value = user_options[i].username;
                const option = document.createElement("option");
                option.setAttribute('value', value);
                datalist.appendChild(option); 
            }
        });
        // if failure:
        posting.fail(function(data) {
        });
    });
});
