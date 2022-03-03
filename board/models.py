from django.db import models
from django.urls import reverse

# Create your models here.

from account.models import User
from django.utils.text import slugify

from mysite import settings


class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=50)
    slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='one word for title alias')
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'board_posts'
        ordering = ('-modify_dt',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board:post_detail', args=(self.slug,))

    def get_previous(self):
        return self.get_previous_by_modify_dt()

    def get_next(self):
        return self.get_next_by_modify_dt()

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        try:
            points = settings.POINTS_SETTINGS['CREATE_ARTICLE']
        except KeyError:
            points = 0
        User.objects.get(username=self.owner.username).modify_points(points)
        super(Post, self).save(*arg, **kwargs)


class Comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=False)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name.username)
