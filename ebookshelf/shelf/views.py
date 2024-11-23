from datetime import datetime
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Book
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from subscriptions.models import Subscription
from django.utils import timezone

User = get_user_model()

import base64
# Create your views here.

# def home(request):
#     if request.method == 'POST' and request.POST.get('search')!=None:
#         data = request.POST
#         search = data.get('search')
#         books = Book.objects.filter(book_name__icontains=search)
#         return render(request, 'home.html', {'books':books})
#     books = Book.objects.all()
#     return render(request, 'home.html', {'books':books})

def home(request):
    if request.method == 'POST' and request.POST.get('search')!=None:
        data = request.POST
        search = data.get('search')
        books = Book.objects.filter(book_name__icontains=search)
        if request.user.is_authenticated:
            subscriptions = Subscription.objects.filter(user=request.user)
            status = False
            current_time = timezone.now()
    
            for sub in subscriptions:
                if sub.expires_at and sub.expires_at > current_time:
                    status = True
                    break

        return render(request, 'home.html', {'books': books, 'subscription_status': status})
    books = Book.objects.all()
    if request.user.is_authenticated:
        subscriptions = Subscription.objects.filter(user=request.user)
        status = False
        current_time = timezone.now()

        for sub in subscriptions:
            if sub.expires_at and sub.expires_at > current_time:
                status = True
                break

        return render(request, 'home.html', {'books': books, 'subscription_status': status})
    return render(request, 'home.html', {'books':books})




def pdf_view(request, id):
    try:
        data = Book.objects.get(id=id)
        pdf_content = data.book_pdf.read()  # Read the binary content
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')  # Convert to Base64
        context = {'pdf_base64': pdf_base64}
        return render(request, 'bookView.html', context)
    except Book.DoesNotExist:
        return HttpResponse("Book not found", status=404)