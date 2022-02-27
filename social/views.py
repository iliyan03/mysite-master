from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


from . import models, forms
# Create your views here.

def index(request):
    posts = models.Post.objects.order_by('-created')
    suggested = models.User.objects.order_by('?')[:5]

    if request.method == 'POST':
        data = request.POST
        if 'like_post_id' in data:
            like_objects = models.Like.objects.all()
            post = models.Post.objects.get(id=data.get('like_post_id'))
            if like_objects.filter(post=post, user=request.user).exists():
                like_objects.get(post=post, user=request.user).delete()
            else:
                like_objects.create(user=request.user, post=post)
            return HttpResponse(post.like.count())
        if 'search_for_user' in data:
            return redirect('profile', username=data.get('search_for_user'))
        if 'user_name' in data:
            user_options = list(models.User.objects.filter(username__startswith=data.get('user_name')).values('username'))
            return JsonResponse({'user_options': user_options})

    context = {
        'posts': posts,
        'suggested': suggested,
    }
    return render(request, "social/index.html", context)

@login_required
def profile(request, username):
    user = get_object_or_404(models.User, username=username)
    posts = user.post.order_by('-created')

    if request.method == 'POST':
        data = request.POST
        if 'search_for_user' in data:
            return redirect('profile', username=data.get('search_for_user'))
        if 'user_name' in data:
            user_options = list(models.User.objects.filter(username__startswith=data.get('user_name')).values('username'))
            return JsonResponse({'user_options': user_options})


    context = {
        'user': user,
        'posts': posts,
    }
    return render(request, 'social/profile.html', context)

def register(request):
    User = get_user_model()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print("Invalid Form")
    else:
        form = forms.SignUpForm()

    context = {
        "form": form,
    }
    return render(request, 'register.html', context)

@login_required
def create_post(request):

    if request.method == 'POST':
        form = forms.PostModelForm(request.POST, request.FILES)
        data = request.POST
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            form.save_m2m()
            return redirect('home')
        else: 
            print("Form is NOT valid")
        if 'search_for_user' in data:
            return redirect('profile', username=data.get('search_for_user'))
        if 'user_name' in data:
            user_options = list(models.User.objects.filter(username__startswith=data.get('user_name')).values('username'))
            return JsonResponse({'user_options': user_options})
    else: 
        form = forms.PostModelForm()

    context = {'form': form}
    return render(request, "social/create-post.html", context)


@login_required
def post_detail(request, username, id):
    post = get_object_or_404(models.Post, id=id, user__username=username)
    comments = post.comment.all()

    if request.method == 'POST':
        data = request.POST
        if 'comment' in data:
            models.Comment.objects.create(user=request.user, post=post, content=data.get('comment'))
        if 'like_post_id' in data:
            like_objects = models.Like.objects.all()
            if like_objects.filter(post=post, user=request.user).exists():
                like_objects.get(post=post, user=request.user).delete()
            else:
                like_objects.create(user=request.user, post=post)
            return HttpResponse(post.like.count())
        if 'comment_like_id' in data:
            comment_like_objects = models.Comment_like.objects.all()
            comment = models.Comment.objects.get(id=data.get('comment_like_id'))
            if comment_like_objects.filter(comment=comment, user=request.user).exists():
                comment_like_objects.get(comment=comment, user=request.user).delete()
            else:
                comment_like_objects.create(user=request.user, comment=comment)
            return HttpResponse(comment.comment_like.count())
        if 'search_for_user' in data:
            return redirect('profile', username=data.get('search_for_user'))
        if 'user_name' in data:
            user_options = list(models.User.objects.filter(username__startswith=data.get('user_name')).values('username'))
            return JsonResponse({'user_options': user_options})

    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, "social/post-detail.html", context)

@login_required
def post_delete(request, username, id):
    post = get_object_or_404(models.Post, id=id)

    if post in request.user.post.all():
        post.delete()
    else: 
        messages.error(request, "You can't delete this post!")

    return redirect('profile', username)

@login_required
def edit(request):
    user = request.user
    if request.method == 'POST':
        form = forms.UserModelForm(request.POST, request.FILES, instance=user)
        data = request.POST
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
        if 'search_for_user' in data:
            return redirect('profile', username=data.get('search_for_user'))
        if 'user_name' in data:
            user_options = list(models.User.objects.filter(username__startswith=data.get('user_name')).values('username'))
            return JsonResponse({'user_options': user_options})

    else: 
        form = forms.UserModelForm(initial={'username': user.username, 'bio': user.bio, 'profile_pic': user.profile_pic})
    context = {
        'form': form,
    }
    return render(request, "social/edit.html", context)