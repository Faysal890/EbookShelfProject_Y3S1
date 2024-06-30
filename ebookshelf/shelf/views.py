from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Book
from django.http import HttpResponse

import base64
# Create your views here.

def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books':books})


# def pdf_view(request,id):
#     data = Book.objects.get(id=id)
#     book_pdf = data.book_pdf

#     image_data = book_pdf.read()
#     actual_filename = book_pdf.name
#     response = HttpResponse(image_data, content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="{actual_filename}"'
#     return response


def pdf_view(request, id):
    try:
        data = Book.objects.get(id=id)
        pdf_content = data.book_pdf.read()  # Read the binary content
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')  # Convert to Base64
        context = {'pdf_base64': pdf_base64}
        return render(request, 'bookView.html', context)
    except Book.DoesNotExist:
        return HttpResponse("Book not found", status=404)