from django.shortcuts import render
from .models import Topic

# The views.py file is the bridge between the database data and the server. Whenever we want to draw data from the database, we need to create a view.

# Create your views here.

# When a URL request matches the pattern we just defined, Django looks for a function called index() in the views.py file

def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    topics = Topic.objects.order_by('date_added')
    # A context is a dictionary in which the keys are names we'll use in the template 
    # to access the data, and the values are the data we need to send to the template. 
    # In this case, there's one key-value pair, which contains 
    # the set of topics we'll display on the page.
    context = {'topics':topics}
    # When building a page that uses data, we pass the contex variable 
    # to render() as well as the request object and the path to the template.
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # foreign key can be accessed using '_set' after lowercase name of the related model, in this case, 'entry'
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries} # <-- dictionary with required data to load page
    return render(request, 'learning_logs/topic.html', context)