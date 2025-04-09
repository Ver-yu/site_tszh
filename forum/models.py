from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField(verbose_name='Текст поста')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='forum/images/', blank=True, null=True)

    def __str__(self):
        return f'Пост от {self.author} ({self.created_at.date()})'

class Poll(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='poll')
    question = models.CharField(max_length=200, verbose_name='Вопрос голосования')

    def __str__(self):
        return self.question

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=100, verbose_name='Вариант ответа')

    # Добавьте это свойство для доступа к голосам
    @property
    def votes(self):
        return Vote.objects.filter(option=self)

    def __str__(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
    apartment = models.CharField(max_length=10)

    class Meta:
        unique_together = ('apartment', 'option')

    def __str__(self):
        return f'Голос от {self.apartment} за {self.option}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        banned_words = ['мат1', 'мат2']
        for word in banned_words:
            if re.search(word, self.text, re.IGNORECASE):
                raise ValidationError('Комментарий содержит запрещённые слова!')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Комментарий от {self.author} ({self.created_at.date()})'
