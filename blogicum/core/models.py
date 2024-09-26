from django.db import models


class PublishedModel(models.Model):
    is_published = models.BooleanField('Опубликовано',
                                       default=True,
                                       blank=False,
                                       help_text='Снимите галочку, '
                                                 'чтобы скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено',
                                      auto_now_add=True,
                                      blank=False)

    class Meta:
        abstract = True
        default_related_name = '%(app_label)s_%(model_name)s'
