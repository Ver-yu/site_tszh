from django.contrib import admin
from .models import Post, Poll, PollOption, Vote, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'text_short')
    def text_short(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_short', 'text_short')
    def post_short(self, obj):
        return obj.post.text[:30] + '...'
    def text_short(self, obj):
        return obj.text[:30] + '...'

admin.site.register([Poll, PollOption, Vote])
