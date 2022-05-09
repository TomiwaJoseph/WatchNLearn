from django.shortcuts import render, redirect
from .models import Newsletter, LandingPagePictures
from django.http import HttpResponse
from random import randint
from courses.models import Course
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# Ajax Requests Start

def newsletter(request):
    get_email = request.POST.get('email')
    email_in_newsletter = Newsletter.objects.filter(email=get_email)
    if not email_in_newsletter:
        new_email = Newsletter.objects.create(email=get_email)
        new_email.save()

    return HttpResponse('Success')

# Ajax Requests Ends

def index(request):
    random_pick = randint(0, LandingPagePictures.objects.count() -1)
    random_picture = LandingPagePictures.objects.all()[random_pick]
    context = {
        'random_picture': random_picture,
    }
    return render(request, 'main/index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        intro_and_message = f"Hi, {name} here.\n" + message
            
        send_mail(subject, intro_and_message, email,
            [settings.EMAIL_HOST_USER], fail_silently=False)

        messages.success(request, 'Message sent successfully')
        return redirect('contact')
    return render(request, 'main/contact.html')

def search_course(request):
    output = []
    search_input = request.POST.get('search')
    all_words_in_search_input = search_input.split()
    search_results = []
    
    def removeNestings(array):
        for item in array:
            if type(item) == list:
                removeNestings(item)
            else: output.append(item)
    
    for word in all_words_in_search_input:
        query = list(Course.objects.filter(
            Q(title__contains=word) |
            Q(keywords__name__icontains=word)
        ).distinct())
        search_results.append(query)
        
    removeNestings(search_results)
    
    context = {
        'search_input': search_input,
        'search_results': output,
    }
    return render(request, 'main/search.html', context)

def tag_search(request, tag):
    output = []
    all_words_in_search_input = tag.split("-")
    search_results = []
    
    def removeNestings(array):
        for item in array:
            if type(item) == list:
                removeNestings(item)
            else: output.append(item)
    
    for word in all_words_in_search_input:
        query = list(Course.objects.filter(
            Q(title__contains=word) |
            Q(keywords__name__icontains=word)
        ).distinct())
        search_results.append(query)
        
    removeNestings(search_results)
    
    context = {
        'search_input': all_words_in_search_input,
        'search_results': list(set(output)),
    }
    return render(request, 'main/tag_search.html', context)

