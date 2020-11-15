from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Choice, Question, Idea, PollUser

import datetime
import sqlite3
from django.db import connection

def index(request):
    
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def search(request):
    #if request.method=='POST':
    searchWord=request.POST.get('search')
    print(searchWord)
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    filtered_question_list=cursor.execute("SELECT * FROM polls_question WHERE question_text LIKE '%%%s%%'" %(searchWord)).fetchall()
    print(filtered_question_list)
    context = {'filtered_question_list': filtered_question_list}
    return render(request, 'polls/search.html', context)

def register(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user = PollUser.objects.create(username=username, password=password)
    return redirect("/polls/loginView/")

def login(request):
    username=request.POST.get('username')
    passwordPut=request.POST.get('password')
    print('Hihhei perillä')
    user = PollUser.objects.get(username=username)
    if getattr(user, 'password')==passwordPut:
        return redirect("/polls/search/")
    return render(request, 'polls/index.html')

def loginView(request):
    return render(request, 'polls/login.html')