# -*- coding: utf-8 -*-


from django import template
from django.db.models import Q

from post.models import Category, Post, Tag
register = template.Library()

@register.assignment_tag
def get_categories():
    category_list = Category.objects.all()
    return category_list


@register.assignment_tag
def get_posts():
    post_list = Post.objects.all()
    return post_list


@register.assignment_tag
def get_tags():
    tag_list = Tag.objects.all()
    return tag_list