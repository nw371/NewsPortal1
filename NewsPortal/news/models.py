from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    #cвязь «один к одному» с встроенной моделью пользователей User;
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    #рейтинг пользователя
    autorRating = models.SmallIntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора
        poRe = self.post_set.aggregate(SumPostRating=Sum('postRating'))
        pstrtng = 0
        pstrtng += poRe.get('SumPostRating')

        # суммарный рейтинг всех комментариев автора
        coRe = self.authorUser.comment_set.aggregate(SumComsRating=Sum('commentRating'))
        cmmrtng = 0
        cmmrtng += coRe.get('SumComsRating')

        # суммарный рейтинг всех комментариев к статьям автора
        auPoRe = self.authorUser.post_set.aggregate(SumAurPstsRating=Sum('commentRating'))
        athrpstrthg = 0
        athrpstrthg += auPoRe.get('SumAurPstsRating')

        self.autorRating = pstrtng * 3 + cmmrtng + athrpstrthg
        self.save()


class Category(models.Model):
    #единственное поле: название категории. Поле должно быть уникальным
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    news = 'NS'
    article = 'AL'
    TYPES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    #поле с выбором — «статья» или «новость»
    postType = models.CharField(max_length=2, choices=TYPES, default='NS')
    #автоматически добавляемая дата и время создания
    postDate = models.DateField(auto_now_add=True)
    #заголовок статьи/новости
    postName = models.CharField(max_length=255)
    #текст статьи/новости
    postBody = models.TextField()
    #рейтинг статьи/новости
    postRating = models.SmallIntegerField(default=0)

    #связь «один ко многим» с моделью Author
    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
    #связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        postPreview = self.postBody[0:123]
        return f"{postPreview}..."

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()


class PostCategory(models.Model):
    #связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #связь «один ко многим» с моделью Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    #связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #связь «один ко многим» с встроенной моделью User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #текст комментария
    commentBody = models.TextField()
    #дата и время создания комментария
    commentDate = models.DateField(auto_now_add=True)
    #рейтинг комментария
    commentRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
