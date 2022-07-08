from django.shortcuts import render, redirect
from .models import *
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index (request):
    return render (request, 'learning_logs/index.html')

@login_required
def topics (request):
    topics = Topic.objects.order_by('date_added')
    return render (request, 'learning_logs/topics.html', {'topics' : topics})

def topic (request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic. entry_set.order_by('-date_added')
    return render (request, 'learning_logs/topic.html', {'topic' : topic, 'entries' : entries})

def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect ('learning_logs:topics')
    
    return render (request, 'learning_logs/new_topic.html', {'form' : form})


def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:

        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    return render(request, 'learning_logs/new_entry.html',  {'topic': topic, 'form': form})

def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    return render(request, 'learning_logs/edit_entry.html', {'entry': entry, 'topic': topic, 'form': form})