from django.db import models

# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length = 200)
    book_writer = models.CharField(max_length = 100)
    book_desc = models.TextField()
    book_image = models.ImageField(upload_to='book_images/')
    book_catagory = models.CharField(max_length=50)
    book_pdf = models.FileField(upload_to='pdfs', default='default.pdf')