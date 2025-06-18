from django.shortcuts import render, redirect


def home(request):
    
    return render(request, 'index_new2.html', {})
