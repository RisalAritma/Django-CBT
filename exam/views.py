from django.shortcuts import render
from django.http import HttpResponse
from exam.models import Question

# Create your views here.
def index(request):
    soal = Question.objects.all()
    context = {
        'soal': soal,
        'soal_no1' : Question.objects.filter(number=1).first(),
    }
    return render(request, 'exam/index.html', context)
    
def run(request, id):
    soal = Question.objects.all().order_by('number')
    soal_select = Question.objects.get(id=id)
    try:
        soal_next = Question.objects.get(number=soal_select.number + 1)
    except Question.DoesNotExist:
        soal_next = ""

    try:
        soal_back = Question.objects.get(number=soal_select.number-1)
    except Question.DoesNotExist:
        soal_back = ""


    context = {
        'soal': soal,
        'soal_select': soal_select,
        'soal_no_min': Question.objects.order_by('number').first(),
        'soal_no_max': Question.objects.order_by('-number').first(),
        'soal_next': soal_next,
        'soal_back': soal_back,
    }
    return render(request, 'exam/run.html', context)
