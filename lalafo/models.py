from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name


class Lalafo(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='pubs',
                             verbose_name='Пользователь')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='cat',
                                 verbose_name='Категория')
    image = models.ImageField('Выберите изображение', upload_to='image', blank=True)
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    price = models.IntegerField('Цена')
    created_at = models.DateField("Дата создания", auto_now_add=True)
    updated_at = models.DateField("Дата редактирования", auto_now=True)

    def __str__(self):
        return self.title

    def avr_rating(self):
        summ = 0
        ratings = Rating.objects.filter(post=self)
        for rating in ratings:
            summ += rating.rate
        if len(ratings) > 0:
            return summ / len(ratings)
        else:
            return 'Нет рейтинга'


class Rating(models.Model):
    post = models.ForeignKey(Lalafo, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                            verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = (('user', 'post'),)
        index_together = (('user', 'post'),)


class Like(models.Model):
    post = models.ForeignKey(Lalafo,
                             on_delete=models.CASCADE,
                             related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    is_liked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Favourite(models.Model):
    post = models.ForeignKey(Lalafo,
                               on_delete=models.CASCADE,
                               related_name='favourites')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favourites')
    is_favourite = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'


class Comment(models.Model):
    post = models.ForeignKey(Lalafo, on_delete=models.CASCADE, related_name='comments',
                               verbose_name='Продукт')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    text = models.TextField('Текст')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.post} --> {self.user}'

