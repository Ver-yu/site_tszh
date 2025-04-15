from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from users.mixins import TSZHMemberRequiredMixin
from .models import Post, Poll, Comment
from .forms import PostForm, PollForm, CommentForm
from .utils import check_profanity  # Самописный фильтр матов


class ForumView(ListView):
    model = Post
    template_name = 'forum.html'  # Изменен путь к шаблону
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']


@login_required
def create_post(request):
    if not request.user.is_tszh_member:
        raise PermissionDenied("Только члены ТСЖ могут создавать посты")

    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        poll_form = PollForm(request.POST) if 'add_poll' in request.POST else None

        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()

            if poll_form and poll_form.is_valid():
                poll = poll_form.save(commit=False)
                poll.post = post
                poll.save()
                post.has_poll = True
                post.save()

            return redirect('forum')
    else:
        post_form = PostForm()
        poll_form = PollForm()

    return render(request, 'forum/create_post.html', {
        'post_form': post_form,
        'poll_form': poll_form,
    })


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    apartment = request.user.apartment

    if request.method == 'POST' and 'option' in request.POST:
        option = request.POST['option']
        if poll.add_vote(apartment, option):
            return redirect('forum')
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
            comment.is_approved = not check_profanity(comment.content)  # Используем самописный фильтр
            comment.save()
    return redirect('forum')


@method_decorator(login_required, name='dispatch')
class DeletePostView(TSZHMemberRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('forum')

    def get_queryset(self):
        if self.request.user.role == 1:  # Глава ТСЖ может удалять любые посты
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)  # Остальные - только свои