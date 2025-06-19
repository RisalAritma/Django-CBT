from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from exam.models import Question, QuestionAnswer, QuestionTime, QuestionIndicator, Profile
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from tablib import Dataset
from exam.resources import UserAnswerResource

import random as rnd
import json

# Create your views here.

@login_required
def index(request):
    if request.user.is_staff:
        return redirect('exam:administrator')
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


@login_required
def administrator(request):
    user = Profile.objects.filter(user__is_staff=0).order_by('user')
    data = []

    for u in user:
        time = QuestionTime.objects.filter(user=u.user).first() 
        if not time:
            time_count = "Belum Mulai"
        elif time.time_count == timedelta(0):
            time_count = "Selesai"
        else:
            time_count = "Sisa Waktu "+ str(time.time_count)

        data.append({
            'user': u,
            'time': time_count,
        })

    context = {
        'user': request.user,
        'title': 'Administrator',
        'heading': 'Administrator',
        'data': data,
    }
    return render(request, 'exam/administrator.html', context)

@login_required
def time_out(request):
    context = {
        'user': request.user,
        'title': 'Time Out',
        'heading': 'Time Out',
    }
    return render(request, 'exam/time_out.html', context)

@login_required
def results(request):
    indicator = QuestionIndicator.objects.all().order_by('number')
    indicator_with_answer = []

    for ind in indicator:
        answer_correct = 0
        answer = QuestionAnswer.objects.filter(user=request.user, question__indicator=ind).order_by('-update_at')
        for s in answer:
            if s.random == 'ABCD' and s.answer == 'A':
                answer_correct += 1            
            if s.random == 'BCDA' and s.answer == 'B':
                answer_correct += 1            
            if s.random == 'CDAB' and s.answer == 'C':
                answer_correct += 1            
            if s.random == 'DABC' and s.answer == 'D':
                answer_correct += 1            
        indicator_with_answer.append({
            'indicator': ind,
            'answer_correct': answer_correct,
        })
            

    context = {
        'user': request.user,
        'title': 'Results',
        'heading': 'Results',
        'data': indicator_with_answer,
    }
    return render(request, 'exam/results.html', context)

@login_required
def result(request, id):
    indicator = QuestionIndicator.objects.all().order_by('number')
    indicator_with_answer = []

    for ind in indicator:
        answer_correct = 0
        answer = QuestionAnswer.objects.filter(user=id, question__indicator=ind).order_by('-update_at')
        for s in answer:
            if s.random == 'ABCD' and s.answer == 'A':
                answer_correct += 1            
            if s.random == 'BCDA' and s.answer == 'B':
                answer_correct += 1            
            if s.random == 'CDAB' and s.answer == 'C':
                answer_correct += 1            
            if s.random == 'DABC' and s.answer == 'D':
                answer_correct += 1            
        indicator_with_answer.append({
            'indicator': ind,
            'answer_correct': answer_correct,
        })
            

    context = {
        'user': request.user,
        'user_select': User.objects.get(id=id),
        'user_select_profile': Profile.objects.get(user=id),
        'title': 'Results',
        'heading': 'Results',
        'data': indicator_with_answer,
    }
    return render(request, 'exam/result.html', context)


@login_required
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



@login_required
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
    
@login_required
def stop(request):
    ut = QuestionTime.objects.get(user=request.user)
    ut.time_count = timedelta(0)
    ut.save()
    messages.success(request, 'Ujian Berhenti!')
    return redirect('exam:time_out')


@login_required
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
@login_required
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


@login_required
def export_user_answer(request):
    user_answer = UserAnswerResource()
    dataset = user_answer.export()
    response = HttpResponse(
        dataset.export('csv'),
        content_type='text/csv',
    )
    response['Content-Disposition'] = 'attachment; filename="Rekapan Data.csv"'
    return response
