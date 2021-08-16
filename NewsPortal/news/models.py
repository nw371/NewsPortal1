from django.contrib.auth.models import User
from django.db import models
#from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    autorsRating = models.SmallIntegerField(default=0)

    def update_rating(self):
        # pr = self.post_set.aggregate(SumPostRating=Sum('postRating'))
        # prt = 0
        # prt += pr.get('SumPostRating')

        postsRating = Post.objects.filter(postAuthor=self.authorUser).values('postRating')
        postsRating = sum(postsRating)*3
        self.rating=postsRating
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

class Post(models.Model):
    news = 'NS'
    article = 'AL'
    TYPES = [
        (news,'Новость'),
        (article,'Статья')
    ]

    postType = models.CharField(max_length=2, choices=TYPES, default='NS')
    postDate = models.DateField(auto_now_add=True)
    postName = models.CharField(max_length=255)
    postBody = models.TextField()
    postRating = models.SmallIntegerField(default=0)

    postAuthor = models.ForeignKey(Author, on_delete=models.CASCADE)
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
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentBody = models.TextField()
    commentDate = models.DateField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()