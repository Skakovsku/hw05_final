from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User


@cache_page(20)
def index(request):
    template = 'posts/index.html'
    text = 'Последние обновления на сайте'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.COUNT_POSTS_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'text_index': text,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    text = 'Записи сообщества '
    post_list = group.group_name.all()
    paginator = Paginator(post_list, settings.COUNT_POSTS_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'text_group_posts': text,
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    profile_context = User.objects.get(username=username)
    user_id = User.objects.get(username=username).id
    post_list = Post.objects.filter(author=user_id)
    following = False
    if Follow.objects.filter(author=profile_context):
        following = True
    paginator = Paginator(post_list, settings.COUNT_POSTS_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'following': following,
        'user_id': user_id,
        'profile_context': profile_context,
        'post_list': post_list,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post_object = Post.objects.get(pk=post_id)
    author_name = post_object.author
    post_count_auth = Post.objects.filter(author=author_name).count()
    comments_post = Comment.objects.filter(post=post_object)
    form = CommentForm(request.POST or None)
    context = {
        'form': form,
        'comments': comments_post,
        'post_object': post_object,
        'author_name': author_name,
        'post_count_auth': post_count_auth,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect('posts:profile', post.author)
    template = 'posts/create_post.html'
    text_heading = 'Новый пост'
    listing = Group.objects.all()
    form = PostForm()
    context = {
        'form': form,
        'listing': listing,
        'text_heading': text_heading,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            files=request.FILES,
            instance=post,
        )
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('posts:post_detail', post_id)
    post_object = Post.objects.get(pk=post_id)
    author_id = post_object.author
    if author_id != request.user:
        raise UserWarning('Права на редактирование поста у автора')
    template = 'posts/create_post.html'
    text_heading = 'Редактировать пост'
    form = PostForm(instance=post_object)
    context = {
        'form': form,
        'text_heading': text_heading,
        'is_edit': True,
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = Post.objects.get(pk=post_id)
        comment.author = request.user
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    text = 'Ваши подписки'
    post_list = []
    follow = Follow.objects.filter(user=request.user)
    for post_authors in follow:
        post_author = Post.objects.filter(author=post_authors.author)
        for post in post_author:
            post_list.append(post)
    paginator = Paginator(post_list, settings.COUNT_POSTS_PAGES)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'text_index': text,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    fol_list = Follow.objects.filter(user=request.user)
    for i in fol_list:
        if i.author == author:
            return redirect('posts:profile', username=username)
    if request.user == author:
        return redirect('posts:profile', username=username)
    Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('posts:profile', username=username)
