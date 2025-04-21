from django.db import models
from users.models import CustomUser

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'В обработке'),
        ('accepted', 'Принято'),
        ('closed', 'Завершено'),
    ]

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_tickets')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_tickets')
    description = models.TextField()
    photo = models.ImageField(upload_to='tickets/photos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заявка #{self.id} от {self.author.username}"
