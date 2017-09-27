# -*- coding: utf-8 -*-

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Başlık')
    slug = models.SlugField(unique=True, editable=False, max_length=130)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:category_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('accounts:category_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('accounts:category_delete', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Etiket')
    slug = models.SlugField(unique=True, editable=False, max_length=130)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:tag_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('accounts:tag_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('accounts:tag_delete', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Tag.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    user = models.ForeignKey('auth.User', verbose_name='Yazar', related_name='posts')
    title = models.CharField(
        max_length=120,
        verbose_name='Başlık')
    content = RichTextField(verbose_name='İçerik')
    publishing_date = models.DateTimeField(verbose_name='Tarih', auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False, max_length=130)    #   editable=False yazarak bu alanı admin panael dahil hiç bir yerde gösterme.
    category = models.ForeignKey(Category, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return "/post/{}".format(self.id)
        return reverse('post:detail', kwargs={'slug': self.slug})

    def get_create_url(self):
        return reverse('post:create')

    def get_update_url(self):
        return reverse('accounts:article_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('accounts:article_delete', kwargs={'slug': self.slug})


    #   Aynı isimle title olusşturduğumuzda slugların karışmaması lazım. Bundan dolayı
    #   aynı isimle oluşturduğumuzda slug oluşurken hata olmaması için slug sonuna sayı gelecek.
    #   Bu fonksiyonu aşağıdaki save() fonksiyonunda çağırırız.
    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Post, self).save(*args, **kwargs)

    # En son oluşturduğumuz postlar en başta yer alıyor. Tarihleri aynı ise
    # id lere bakar. id si büyük olan en başta gösterilir.
    class Meta:
        ordering = ['-publishing_date', 'id']


class CategoryToPost(models.Model):
    post = models.ForeignKey(Post)
    category = models.ForeignKey(Category)


class Comment(models.Model):
    post = models.ForeignKey('post.Post', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name='İsim')
    content = models.TextField(verbose_name='Yorum')
    created_date = models.DateTimeField(auto_now_add=True)