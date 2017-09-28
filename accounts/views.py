# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.template import loader
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, RegisterForm, PostForm, CategoryForm, TagForm, ContactForm
from post.models import Post, Category, Tag


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')

    return render(request, 'bootstrap/accounts/user_form.html', {'form': form, 'title': 'Giriş Yap'})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        # user.is_staff = user.is_superuser = True
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('index')

    return render(request, "bootstrap/accounts/user_form.html", {"form": form, 'title': 'Üye Ol'})


def logout_view(request):
    logout(request)
    return redirect('index')


def about_us(request):
    template = loader.get_template("bootstrap/about_us.html")
    return HttpResponse(template.render())

def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['krmlemel@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Mailiniz iletilmiştir.', extra_tags='mesaj-basarili')
            url = reverse('accounts:email')
            return HttpResponseRedirect(url)
    return render(request, "bootstrap/contact.html", {'form': form})


def article(request):
    if not request.user.is_authenticated():
        return Http404()

    post_list = Post.objects.all()

    # # # Post Ekleme Formu # # #
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Başarılı bir şekilde Makale oluştu', extra_tags='mesaj-basarili')
        url = reverse('accounts:article')
        return HttpResponseRedirect(url)
    # # #       # # #       # # #       # # #

    paginator = Paginator(post_list, 7)  # Show 7 contacts per page

    page = request.GET.get('sayfa')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "bootstrap/accounts/articles.html", {'posts': posts, 'form': form})


def article_update(request, slug):
    if not request.user.is_authenticated():
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, 'Başarılı bir şekilde güncellendi')
        url = reverse('accounts:article')
        return HttpResponseRedirect(url)

    context = {
        'form': form,
    }

    return render(request, 'bootstrap/accounts/article_form.html', context)


def article_delete(request, slug):

    if not request.user.is_authenticated():
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Makale başarılı bir şekilde silindi', extra_tags='mesaj-basarili')
    url = reverse('accounts:article')
    return HttpResponseRedirect(url)


def category(request):
    if not request.user.is_authenticated():
        return Http404()

    category_list = Category.objects.all()

    # # # Kategori Ekleme Formu # # #
    form = CategoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category.save()
        messages.success(request, 'Başarılı bir şekilde Kategori oluştu', extra_tags='mesaj-basarili')

        url = reverse('accounts:category')
        return HttpResponseRedirect(url)
    # # #       # # #       # # #       # # #

    paginator = Paginator(category_list, 7)  # Show 7 contacts per page

    page = request.GET.get('sayfa')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "bootstrap/accounts/categories.html", {'categories': categories, 'form': form})


def category_update(request, slug):
    if not request.user.is_authenticated():
        return Http404()

    category = get_object_or_404(Category, slug=slug)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Kategori başarılı bir şekilde güncellendi')
        url = reverse('accounts:category')
        return HttpResponseRedirect(url)

    context = {
        'form': form,
    }

    return render(request, 'bootstrap/accounts/category_form.html', context)


def category_delete(request, slug):

    if not request.user.is_authenticated():
        return Http404()

    category = get_object_or_404(Category, slug=slug)
    category.delete()
    messages.success(request, 'Kategori başarılı bir şekilde silindi', extra_tags='mesaj-basarili')
    url = reverse('accounts:category')
    return HttpResponseRedirect(url)


def tag(request):

    if not request.user.is_authenticated():
        return Http404()

    form = TagForm(request.POST or None)
    if form.is_valid():
        tag = form.save(commit=False)
        tag.user = request.user
        tag.save()
        messages.success(request, 'Başarılı bir şekilde Etiket oluştu', extra_tags='mesaj-basarili')

        url = reverse('accounts:tag')
        return HttpResponseRedirect(url)

    tag_list = Tag.objects.all()

    paginator = Paginator(tag_list, 7)  # Show 7 contacts per page

    page = request.GET.get('sayfa')
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        tags = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "bootstrap/accounts/tags.html", {'tags': tags, 'form': form})


def tag_update(request, slug):
    if not request.user.is_authenticated():
        return Http404()

    tag = get_object_or_404(Tag, slug=slug)
    form = TagForm(request.POST or None, instance=tag)
    if form.is_valid():
        form.save()
        messages.success(request, 'Etiket başarılı bir şekilde güncellendi')
        url = reverse('accounts:tag')
        return HttpResponseRedirect(url)

    context = {
        'form': form,
    }

    return render(request, 'bootstrap/accounts/tag_form.html', context)


def tag_delete(request, slug):

    if not request.user.is_authenticated():
        return Http404()

    tag = get_object_or_404(Tag, slug=slug)
    tag.delete()
    messages.success(request, 'Etiket başarılı bir şekilde silindi', extra_tags='mesaj-basarili')
    url = reverse('accounts:tag')
    return HttpResponseRedirect(url)