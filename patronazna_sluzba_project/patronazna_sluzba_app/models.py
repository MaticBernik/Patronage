from django.db import models
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import Group


class Author(models.Model):
    # author_id --> ze po defaultu
    firstName=models.CharField(max_length=100, null=False)
    lastName=models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.firstName+' '+self.lastName


class Book(models.Model):
    # book_id --> ze po defaultu
    title = models.CharField(max_length=100, null=False)
    added_date = models.DateTimeField(default=datetime.now())
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    genre = models.CharField(max_length=10,null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.author.firstName+' '+self.author.lastName+': '+self.title


class Lease(models.Model):
    # lease_id  --> ze po defaultu
    user_id= models.ForeignKey(User,on_delete=models.CASCADE)
    book_id= models.ForeignKey(Book,on_delete=models.CASCADE)
    start_date= models.DateTimeField(default=datetime.now())
    expiration_date = models.DateTimeField(default=datetime.now() + timedelta(days=14))

    def is_expired(self):
        if self.expiration_date < timezone.now():
            return True
        else:
            return False

    def __str__(self):
        return str(self.start_date)+': '+self.user_id.first_name+' '+self.user_id.last_name+' - '+self.book_id.title


class Reservation(models.Model):
    # reservation_id  --> ze po defaultu
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=datetime.now())
    expiration_date = models.DateTimeField(default=datetime.now() + timedelta(days=14))

    def is_expired(self):
        if self.expiration_date < timezone.now():
            return True
        else:
            return False

    def __str__(self):
        return 'EXP:'+str(self.expiration_date) + ': ' + self.user_id.first_name + ' ' + self.user_id.last_name + ' - ' + self.book_id.title


class Message(models.Model):
    text = models.CharField(max_length=200, null=False)

    def __str__(self):
        if len(self.text) > 10:
            return self.text[:10]
        else:
            return self.text


class Users_Messages(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        s=self.user_id.username+": '"
        if len(self.message_id.text) >10:
            return s+self.message_id.text[:10]+"'"
        else:
            return s+self.message_id.text+"'"
