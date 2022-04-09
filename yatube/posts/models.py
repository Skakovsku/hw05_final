from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField('text')
    pub_date = models.DateTimeField(
        'date',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='connection'
    )
    group = models.ForeignKey(
        'Group',
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='group_name',
    )
    image = models.ImageField(
        'image',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.text[:15]


class Group(models.Model):
    title = models.CharField('title', max_length=200)
    slug = models.SlugField('adress', unique=True)
    description = models.TextField('description')

    class Meta:
        verbose_name = 'Group'

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
    )
    text = models.TextField('text_comment')
    created = models.DateTimeField(
        'date_comment',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Comment'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Follow'

    def create_follow(self):
        follow_obj = Follow.objects.filter(user=self.user, author=self.author)
        if self.user == self.author:
            raise ValueError('Нельзя подписаться на самого себя')
        elif follow_obj is True:
            raise ValueError('Вы уже подписаны на этого автора')

    def __str__(self):
        return f'Подписка {self.user} на {self.author}'
