from django.contrib import admin

from .models import User, Category, Genre, Title


#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'rating', 'description', 'get_genres',
                    'category')
    search_fields = ('name', 'description')
    list_filter = ('year', 'rating', 'genre', 'category')
