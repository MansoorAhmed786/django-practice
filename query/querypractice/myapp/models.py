from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.username.username

class Library(models.Model):
    location = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.location

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    library = models.ManyToManyField(Library)

    def __str__(self):
        return self.name