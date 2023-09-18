from django.contrib import admin
from .models import Book, Author, Library

# Register your models here.
admin.site.register(Author)
admin.site.register(Library)
admin.site.register(Book)