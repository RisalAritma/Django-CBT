from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from exam.models import Question, QuestionAnswer, QuestionTime, QuestionIndicator
from datetime import timedelta
from django.contrib import messages
import random as rnd
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

def results(request):
    indicator = QuestionIndicator.objects.all().order_by('number')
    context = {
        'user': request.user,
        'title': 'Results',
        'heading': 'Results',
        'indicator': indicator,
    }
    return render(request, 'exam/results.html', context)


def save(request):
    if request.method == "POST":
        # Ambil data dari POST
        question_id = request.POST.get("question_id")
        question_next = request.POST.get("question_next")
        answer = request.POST.get("answer")

        # Update atau buat data QuestionAnswer
        obj, created = QuestionAnswer.objects.update_or_create(
            user=request.user,
            question_id=question_id,
            defaults={
                "answer": answer,
            }
        )
        messages.success(request, 'Jawaban Disimpan!')
        if question_next:
            return redirect('exam:run', id=question_next)
        else:
            return redirect('exam:run', id=question_id)
    else:
        messages.error(request, 'Metode tidak diizinkan!')



def start(request):
    try:
        answer_last = QuestionAnswer.objects.filter(user=request.user).order_by('-update_at').first()
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
    
def stop(request):
    ut = QuestionTime.objects.get(user=request.user)
    ut.time_count = timedelta(0)
    ut.save()
    messages.success(request, 'Ujian Berhenti!')
    return redirect('exam:time_out')


def run(request, id):
    soal = Question.objects.all().order_by('number')
    # Buat list baru dengan jawaban user (jika ada)
    soal_with_jawab = []
    for s in soal:
        answer_obj = QuestionAnswer.objects.filter(user=request.user, question=s).order_by('-id').first()
        jawab = answer_obj.answer if answer_obj else ""
        soal_with_jawab.append({
            'soal': s,
            'jawab': jawab,
        })

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

    # Pilihan urutan random
    random_choices = ["ABCD", "BCDA", "CDAB", "DABC"]
    random_order = rnd.choice(random_choices)

    # Update atau buat data QuestionAnswer
    soal_answer = QuestionAnswer.objects.filter(
        user=request.user,
        question_id=soal_select.id
    ).order_by('-id').first()

    if not soal_answer:        
        soal_answer = QuestionAnswer.objects.create(
            user=request.user,
            question_id=soal_select.id,
            random=random_order,
        )


    context = {
        'user': request.user,
        'title': 'Ujian Berjalan',
        'heading': 'Dashboard Ujian',
        'soal': soal_with_jawab,
        'soal_select': soal_select,
        'soal_no_min': Question.objects.order_by('number').first(),
        'soal_no_max': Question.objects.order_by('-number').first(),
        'soal_next': soal_next,
        'soal_back': soal_back,
        'soal_answer': soal_answer,
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
