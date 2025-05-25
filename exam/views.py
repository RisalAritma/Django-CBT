from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from exam.models import Question, QuestionAnswer, QuestionTime
from datetime import timedelta
import json

# Create your views here.
def index(request):
   
    try:
        getTime = QuestionTime.objects.get(user=request.user)
        time_count = getTime.time_count
    except QuestionTime.DoesNotExist:
        time_count = None
    
    if not time_count :  
        time_count = "00:00:00"
    context = {
        'user': request.user,
        'title': 'Dashboard',
        'heading': 'Dashboard Ujian',
        'time_count' : time_count
    }
    return render(request, 'exam/index.html', context)


def time_out(request):
    context = {
        'user': request.user,
        'title': 'Time Out',
        'heading': 'Time Out',
    }
    return render(request, 'exam/time_out.html', context)


def start(request):
    try:
        answer_last = QuestionAnswer.objects.filter(user=request.user).order_by('-time_answer').first()
    except QuestionAnswer.DoesNotExist:
        answer_last = None

    addTime = QuestionTime.objects.filter(user=request.user)
    if not addTime.filter(user=request.user).exists():
        QuestionTime.objects.create(user=request.user, time_count=timedelta(minutes=90))

    if answer_last:
        return redirect('exam:run', id=answer_last.question.id)
    else:        
        soal = Question.objects.order_by('number').first()
        return redirect('exam:run', id=soal.id)



    
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

    getTime = QuestionTime.objects.get(user=request.user)
    time_count = getTime.time_count

    context = {
        'user': request.user,
        'title': 'Ujian Berjalan',
        'heading': 'Dashboard Ujian',
        'soal': soal,
        'soal_select': soal_select,
        'soal_no_min': Question.objects.order_by('number').first(),
        'soal_no_max': Question.objects.order_by('-number').first(),
        'soal_next': soal_next,
        'soal_back': soal_back,
        'time_count' : time_count
    }
    return render(request, 'exam/run.html', context)

@csrf_exempt
def update_time(request):
    if request.method == "POST":
        data = json.loads(request.body)
        total_seconds = int(data.get("time_count", 0))
        # Ambil QuestionTime user
        try:
            qtime = QuestionTime.objects.get(user=request.user)
            qtime.time_count = timedelta(seconds=total_seconds)
            qtime.save()
            return JsonResponse({"status": "success"})
        except QuestionTime.DoesNotExist:
            return JsonResponse({"status": "not_found"}, status=404)
    return JsonResponse({"status": "invalid"}, status=400)
