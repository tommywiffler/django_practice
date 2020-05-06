from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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

def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No Data subimtted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id = topic_id)

    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Initial request: pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)