from django.contrib.auth.models import User
from django.db import models
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    asal_paud = models.CharField(max_length=100, blank=True)
    lokasi_paud = models.CharField(max_length=255, blank=True)
    jenis_kelamin = models.CharField(max_length=15, blank=True)
    usia = models.CharField(max_length=30, blank=True)
    pendidikan = models.CharField(max_length=30, blank=True)
    lama_ngajar = models.CharField(max_length=30, blank=True)
    status_pegawai = models.CharField(max_length=30, blank=True)
    apa_pernah_pelatihan = models.CharField(max_length=10, blank=True)
    apa_sudah_ppg = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username
    

class QuestionBank(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class QuestionIndicator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    indicator = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.indicator
    

class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.IntegerField()
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.CASCADE)
    indicator = models.ForeignKey(QuestionIndicator, on_delete=models.CASCADE)
    text = models.TextField()
    bagian = models.TextField(null=True, blank=True)
    kompetensi = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    choice1 = models.TextField()
    choice2 = models.TextField()
    choice3 = models.TextField()
    choice4 = models.TextField()
    choice5 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
    
class QuestionAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    answer = models.CharField(max_length=10)
    update_at = models.DateTimeField(auto_now_add=True)
    time_answer = models.DurationField(null=True, blank=True)
    

class QuestionTime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    time_count = models.DurationField(null=True, blank=True)



