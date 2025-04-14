from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)  # Правильное имя поля
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='forum_images/', blank=True, null=True)
    has_poll = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Poll(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='poll')
    question = models.CharField(max_length=200)
    options = models.JSONField(default=dict)
    voted_apartments = models.JSONField(default=list)

    def add_vote(self, apartment, option):
        if apartment not in self.voted_apartments:
            self.options[option] = self.options.get(option, 0) + 1
            self.voted_apartments.append(apartment)
            self.save()
            return True
        return False

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.author.apartment} on {self.post.title}"