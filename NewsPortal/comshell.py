#django-admin startproject NewsPortal
#python3 manage.py startapp news


#exec(open('shell_commands.py').read())

from news.models import *

import random

ptype = ['AL','NS']
aindex = [1,2]
usersQTY = 11
authQTY = 3
postQTY = 16
commQTY = 26
catQTY = 5

for n in range(1, catQTY):
    globals()[f'cat{n}'] = Category.objects.create(name=f'Category{n}')

for n in range(1, usersQTY):
    globals()[f'user{n}'] = User.objects.create_user(username=f"UserName{n}", password=f"UN{n}pass")

for n in range(1, authQTY):
    globals()[f'author{n}'] = Author.objects.create(authorUser=globals()[f'user{n}'])

for n in range(1, postQTY):
    globals()[f'post{n}'] = Post.objects.create(postType=f'{random.choice(ptype)}',
                                postName=f'Post {n} Name',
                                postBody=f'Very long post Nr.{n} body created for tests just to fill database. '
                                         f'it will be longer, than 124 characters, to make sure - preview '
                                         f'method does the job. It does not need to have any meaning. '
                                         f'Just ID1 to make sure this post belongs to Post {n}',
                                postAuthor=Author.objects.get(id=random.choice(aindex)),
                                )
for n in range(1, commQTY):
    globals()[f'comment{n}'] = Comment.objects.create(post=globals()[f'post{random.choice(range(1,postQTY))}'],
                                                      user=globals()[f'user{random.choice(range(1,usersQTY))}'],
                                                      commentBody=f'Generated comment {n} body.')

for n in range(1, postQTY):
    Post.objects.get(id=n).postCategory.add(Category.objects.get(id=random.choice(range(1,catQTY))))

for n in range(1,100):
    Comment.like(Comment.objects.get(id=random.choice(range(1,commQTY))))
    Post.like(Post.objects.get(id=random.choice(range(1,postQTY))))

# Author.objects.get(id=1)