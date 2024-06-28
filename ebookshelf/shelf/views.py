from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Book
from django.http import HttpResponse
# Create your views here.

def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books':books})


def pdf_view(request,id):
    data = Book.objects.get(id=id)
    book_pdf = data.book_pdf

    image_data = book_pdf.read()
    actual_filename = book_pdf.name
    response = HttpResponse(image_data, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{actual_filename}"'
    return response