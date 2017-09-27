# -*- coding: utf-8 -*-


from django import template

from post.models import Category, Post, Tag
register = template.Library()

@register.assignment_tag
def get_categories():
    # kategorileri burada çağırıyoruz.

    category_list = Category.objects.all()
    return category_list


@register.assignment_tag
def get_posts():
    # post title larını burada çağırıyoruz.

    post_list = Post.objects.all()
    return post_list


@register.assignment_tag
def get_tags():
    # post title larını burada çağırıyoruz.

    tag_list = Tag.objects.all()
    return tag_list


