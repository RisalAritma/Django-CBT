from django.shortcuts import render
from django.http import HttpResponse
from exam.models import Question

# Create your views here.
def index(request):
    soal = Question.objects.all()
    context = {
        'soal': soal
    }
    return render(request, 'exam/index.html', context)
    
def run(request, id):
    soal = Question.objects.all().order_by('number')
    soal_select = Question.objects.get(id=id)
    context = {
        'soal': soal,
        'soal_select': soal_select
    }
    return render(request, 'exam/run.html', context)
    