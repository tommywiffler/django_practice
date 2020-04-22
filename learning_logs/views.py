from django.shortcuts import render

# Create your views here.

# When a URL request matches the pattern we just defined, Django looks for a function called index() in the views.py file

def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Page for topics in learning logs"""
    return render(request, 'learning_logs/topics.html')