from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from .models import Post, Poll, PollOption, Comment, Vote
from .forms import PostForm, CommentForm

User = get_user_model()


@login_required
def forum(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'forum/forum.html', context)


@login_required
def create_post(request):
    if request.user.status not in [1, 2]:  # Только для ТСЖ
        messages.error(request, 'Только члены ТСЖ могут создавать посты')
        return redirect('forum')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Пост успешно создан')
            return redirect('forum')
    else:
        form = PostForm()

    return render(request, 'forum/create_post.html', {'form': form})


@login_required
def vote(request, option_id):
    option = get_object_or_404(PollOption, id=option_id)

    if not hasattr(request.user, 'apartment') or not request.user.apartment:
        messages.error(request, 'Ваш профиль не привязан к квартире!')
        return redirect('forum')

    if Vote.objects.filter(option__poll=option.poll, apartment=request.user.apartment).exists():
        messages.warning(request, 'Ваша квартира уже голосовала!')
    else:
        Vote.objects.create(
            option=option,
            user=request.user,
            apartment=request.user.apartment
        )
        messages.success(request, 'Голос учтён!')

    return redirect('forum')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен')

    return redirect('forum')
