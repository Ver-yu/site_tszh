from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from users.mixins import TSZHMemberRequiredMixin
from .models import Post, Poll, Comment
from .forms import PostForm, PollForm, CommentForm
from better_profanity import profanity

profanity.load_censor_words(['мат', 'оскорбление'])  # Ваш список запрещенных слов


class ForumView(ListView):
    model = Post
    template_name = 'forum/forum.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()
        return context


@login_required
def create_post(request):
    """Функция для создания поста"""
    if not request.user.is_tszh_member:
        raise PermissionDenied("Только члены ТСЖ могут создавать посты")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('forum')
    else:
        form = PostForm()

    return render(request, 'forum/create_post.html', {'form': form})


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

            if profanity.contains_profanity(comment.content):
                comment.is_approved = False
                messages.warning(request, 'Комментарий отправлен на модерацию')

            comment.save()
    return redirect('forum')


@method_decorator(login_required, name='dispatch')
class DeletePostView(TSZHMemberRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('forum')

    def get_queryset(self):
        if self.request.user.role == 1:  # Глава ТСЖ
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)  # Свои посты