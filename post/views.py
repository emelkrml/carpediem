# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post, Category, Tag
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def post_index(request):
    post_list = Post.objects.all()

    #   Search
    query = request.GET.get('q')    #   'q' değerini header.html form da bulunan input name=q değerini çektik.
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
        ).distinct()                                #   distinct() sayesinde aynı kayıtlar birden fazla gözükmeyecek.

    #   Pagination
    paginator = Paginator(post_list, 4)  # Show 4 contacts per page

    page = request.GET.get('sayfa')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, 'bootstrap/post/index.html', {'posts': posts})


def post_detail(request, slug):

    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'bootstrap/post/detail.html', context)


def post_create(request):

    #   admin olmayan kullanıcıların create, delete ve pdate işlemlerinde yetkili olmalarını
    #   engellemek için bu iki kod satırını yazarız. Bu işlemlerde sadece admin etkili olabilir.
    if not request.user.is_authenticated():
        return Http404()

    # if request.method == "POST":
    #     print(request.POST)

    ''' Aşağıdaki yöntem çok iyi bir yöntem değil. Bunun yerine PostForm u kullanalım.   '''
    # title = request.POST.get('title')
    # content = request.POST.get('content')
    # Post.objects.create(title=title, content=content)

    ''' 46 - 48 satırlarındaki kodlar ile aynı anlama geliyor
    
    if request.method == "POST":
    # Formdan gelen bilgileri kaydet
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
    # Formu kullanıcıya göster
        form = PostForm
        
     '''

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Başarılı bir şekilde Post oluştu', extra_tags='mesaj-basarili')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'bootstrap/post/../templates/bootstrap/accounts/article_form.html', context)


def post_update(request, slug):

    #   admin olmayan kullanıcıların create, delete ve pdate işlemlerinde yetkili olmalarını
    #   engellemek için bu iki kod satırını yazarız. Bu işlemlerde sadece admin etkili olabilir.
    if not request.user.is_authenticated():
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Başarılı bir şekilde güncellendi')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form': form,
    }

    return render(request, 'post/form.html', context)


def post_delete(request, slug):

    #   admin olmayan kullanıcıların create, delete ve pdate işlemlerinde yetkili olmalarını
    #   engellemek için bu iki kod satırını yazarız. Bu işlemlerde sadece admin etkili olabilir.
    if not request.user.is_authenticated():
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post:index')


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'bootstrap/post/category_list.html', context)


def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tag=tag)
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'bootstrap/post/tag_list.html', context)
