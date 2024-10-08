from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_LEN_LINE
from core.models import PublishedModel

User = get_user_model()


class Location(PublishedModel):
    name = models.CharField(verbose_name='Название места',
                            max_length=MAX_LEN_LINE,
                            blank=True)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(PublishedModel):
    title = models.CharField(verbose_name='Заголовок',
                             max_length=MAX_LEN_LINE,
                             blank=False)
    description = models.TextField(verbose_name='Описание',
                                   blank=False)
    slug = models.SlugField(verbose_name='Идентификатор',
                            max_length=MAX_LEN_LINE,
                            unique=True,
                            blank=False,
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, '
                                      'цифры, дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Post(PublishedModel):
    title = models.CharField(verbose_name='Заголовок',
                             max_length=MAX_LEN_LINE,
                             blank=False)
    text = models.TextField(verbose_name='Текст',
                            blank=False)
    pub_date = models.DateTimeField(verbose_name='Дата и время публикации',
                                    blank=False,
                                    help_text='Если установить '
                                              'дату и время в будущем — '
                                              'можно делать '
                                              'отложенные публикации.')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации',
                               blank=False,
                               related_name='posts',
                               related_query_name='posts')
    location = models.ForeignKey(Location,
                                 max_length=MAX_LEN_LINE,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Местоположение',
                                 blank=True,
                                 related_name='posts',
                                 related_query_name='posts')
    category = models.ForeignKey(Category,
                                 max_length=MAX_LEN_LINE,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория',
                                 blank=False,
                                 related_name='posts',
                                 related_query_name='posts')

    image = models.ImageField('Фото',
                              upload_to='post',
                              blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Comment(PublishedModel):
    text = models.TextField(verbose_name='Текст',
                            blank=False)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments', )
    created_at = models.DateTimeField(auto_now_add=True, )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE, )

    class Meta:
        ordering = ['created_at']
