#CHEATSHEET КОМАНД

# django-admin startproject NewsPortal
# python3 manage.py startapp news

# python3 manage.py makemigrations
# python3 manage.py migrate

# exec(open('comshell.py').read())

#ГЕНЕРАТЦИЯ ДАННЫХ
from news.models import *

import random

ptype = ['AL', 'NS']
aindex = [1, 2]
usersQTY = 11
authQTY = 3
postQTY = 16
commQTY = 26
catQTY = 5

# Создать двух пользователей (с помощью метода User.objects.create_user)
for n in range(1, usersQTY):
    globals()[f'user{n}'] = User.objects.create_user(username = f"UserName{n}", password = f"UN{n}pass")

# Создать два объекта модели Author, связанные с пользователями.
for n in range(1, authQTY):
    globals()[f'author{n}'] = Author.objects.create(authorUser = globals()[f'user{n}'])

# Добавить 4 категории в модель Category
for n in range(1, catQTY):
    globals()[f'cat{n}'] = Category.objects.create(name = f'Category{n}')

# Добавить 2 статьи и 1 новость
for n in range(1, postQTY):
    globals()[f'post{n}'] = Post.objects.create(postType = f'{random.choice(ptype)}',
                                                postName = f'Post {n} Name',
                                                postBody = f'Very long post Nr.{n} body created for tests just to fill database. '
                                                           f'it will be longer, than 124 characters, to make sure - preview '
                                                           f'method does the job. It does not need to have any meaning. '
                                                           f'Just ID1 to make sure this post belongs to Post {n}',
                                                postAuthor = Author.objects.get(id = random.choice(aindex)),
                                                )
# Присвоить им категории
for n in range(1, postQTY):
    Post.objects.get(id = n).postCategory.add(Category.objects.get(id = random.choice(range(1, catQTY))))

# (как минимум в одной статье/новости должно быть не меньше 2 категорий)
for n in [3, 5, 7]:
    Post.objects.get(id = n).postCategory.add(Category.objects.get(id = random.choice(range(1, catQTY))))

# Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
for n in range(1, commQTY):
    globals()[f'comment{n}'] = Comment.objects.create(post = globals()[f'post{random.choice(range(1, postQTY))}'],
                                                      user = globals()[f'user{random.choice(range(1, usersQTY))}'],
                                                      commentBody = f'Generated comment {n} body.')

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
for n in range(1, 100):
    Comment.like(Comment.objects.get(id = random.choice(range(1, commQTY))))
    Post.like(Post.objects.get(id = random.choice(range(1, postQTY))))


# Обновить рейтинги пользователей.
for n in range(1, 3):
    Author.objects.get(id = n).update_rating()


#ВЫДОД ДАННЫХ

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
Author.objects.order_by('-autorRating')[:1]

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
pid = 0 #сохраним сюда айди поста, чтобы потом использовать для выведения коментов
p = Post.objects.order_by('-postRating')[:1].values()
for i in p:
    print(f"Дата поста: {i['postDate']}")
    print(f"Автор поста: {Author.objects.get(id=i['postAuthor_id']).authorUser.username}")
    print(f"Рейтинг поста: {i['postRating']}")
    print(f"Заголовок поста: {i['postName']}")
    print(f"Предпросмотр поста: {Post.objects.get(id=i['id']).preview()}")
    pid = i['id']

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
c = Comment.objects.filter(post=pid) #используем сохранённый айди поста
for i in c.values():
    print(f"Comment date: {i['commentDate']}")
    usr = i["user_id"]
    print(f"Comment user: {User.objects.get(id=usr).username}")
    print(f"Comment rating: {i['commentRating']}")
    print(f"Comment: {i['commentBody']}")
    print("----------------")
