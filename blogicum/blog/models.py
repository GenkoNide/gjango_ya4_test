from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


from .constants import MAX_LEN_LINE
from .core.models import PublishedModel


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
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               verbose_name='Автор публикации',
                               blank=False,)
    location = models.ForeignKey(Location,
                                 max_length=MAX_LEN_LINE,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Местоположение',
                                 blank=True,)
    category = models.ForeignKey(Category,
                                 max_length=MAX_LEN_LINE,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория',
                                 blank=False,)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
