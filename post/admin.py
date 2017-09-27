# -*- coding: utf-8 -*-


from django.contrib import admin
from .models import Post, Category, CategoryToPost, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'publishing_date', 'slug']
    list_display_links = ['publishing_date']
    list_filter = ['title', 'publishing_date']
    search_fields = ['title', 'content']
    list_editable = ['title']

    '''
     Aşağıdaki satırı models.py de slug değişkeninde editable=False yazdığımız için bu satırı sileriz.
     
    prepopulated_fields = {'slug': ('title',)}      # Bu satır ile girdiğimiz title a göre slug oluşuyor.
    
    '''

    class Meta:
        model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_filter = ['title']
    search_fields = ['title']

    class Meta:
        model = Category


@admin.register(CategoryToPost)
class CategoryToPostInline(admin.ModelAdmin):
    list_display = ['category', 'post']
    list_filter = ['category', 'post']

    class Meta:
        model = CategoryToPost


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_filter = ['title']
    search_fields = ['title']

    class Meta:
        model = Tag