from django.db import models

from .validators import validate_year
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=256)
    slug = models.SlugField(verbose_name="Идентификатор", max_length=50,
                            unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
        
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name="Название", max_length=256)
    slug = models.SlugField(verbose_name="Идентификатор", max_length=50,
                            unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]
        
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name="Название", max_length=200)
    year = models.IntegerField(verbose_name="Дата выхода",
                               validators=[validate_year])
    description = models.TextField(verbose_name="Описание", null=True,
                                   blank=True)
    genre = models.ManyToManyField(Genre, verbose_name="Жанр")
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
    )
    # rating = models.FloatField(
    #    verbose_name='Рейтинг',
    #    null=True,
    #    default=None
    # )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ["name"]
        
    def __str__(self):
        return self.name


class WholeModel(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        "Дата публикации",
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
        ordering = ("pub_date",)


class Review(WholeModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка",
    )
    to_str = "{text}; {pub_date}; {author}; {title}; {score}"

    class Meta(WholeModel.Meta):
        default_related_name = "reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="author_title_connection"
            )
        ]
        verbose_name = "Обзор"
            
        def __str__(self):
            return self.to_str.format(
            text=self.text,
            pub_date=self.pub_date,
            author=self.author.username,
            title=self.title,
            score=self.score,
        )


class Comment(WholeModel):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, verbose_name="Обзор")

    to_str = "{text}; {pub_date}; {author}; {review};"

    class Meta(WholeModel.Meta):
        default_related_name = "comments"
        verbose_name = "Комментарий"
        
    def __str__(self):
        return self.FIELDS_INFO.format(
            text=self.text,
            pub_date=self.pub_date,
            author=self.author.username,
            review=self.review,
        )
