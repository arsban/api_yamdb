from django.contrib import admin

from .models import Review, Comment

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author','text','pub_date',)
    search_fields = ('id','title','author',)
    list_filter = ('pub_date','author')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date','text',)
    search_fields = ('author',)
    list_filter = ('author',)
