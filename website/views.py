from django.shortcuts import render, redirect


def home(request):
    
    return render(request, 'index_new2.html', {})


def  privacy_policy(request):
    
    return render(request, 'privacy_policy.html', {})

def  about(request):
    
    return render(request, 'about.html', {})

