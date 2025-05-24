from django.contrib import admin
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Profile, Question, QuestionBank, QuestionIndicator
from .resources import QuestionResource


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'asal_paud', 'lokasi_paud', 'jenis_kelamin', 'usia', 'pendidikan', 'lama_ngajar', 'status_pegawai', 'apa_pernah_pelatihan', 'apa_sudah_ppg')
    search_fields = ('user__username', 'phone')
    list_filter = ('user__is_staff',)
    ordering = ('user',)
    fieldsets = (
        (None, {
            'fields': ('user', 'phone', 'asal_paud', 'lokasi_paud', 'jenis_kelamin', 'usia', 'pendidikan', 'lama_ngajar', 'status_pegawai', 'apa_pernah_pelatihan', 'apa_sudah_ppg')
        }),
    )

@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_by')
    search_fields = ('title', 'subject', 'created_by__username')
    list_filter = ('created_by__is_staff',)
    ordering = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title', 'subject', 'created_by')
        }),
    )

@admin.register(QuestionIndicator)
class QuestionIndicatorAdmin(admin.ModelAdmin):
    list_display = ('indicator', 'created_by')
    search_fields = ('indicator', 'created_by__username')
    list_filter = ('created_by__is_staff',)
    ordering = ('indicator',)
    fieldsets = (
        (None, {
            'fields': ('indicator', 'created_by')
        }),
    )

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ('number', 'question_bank', 'indicator', 'text', 'created_at')
    search_fields = ('question_bank__title', 'indicator__indicator', 'text')
    list_filter = ('question_bank__created_by__is_staff',)
    ordering = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('number','question_bank', 'indicator', 'text', 'image', 'choice1', 'choice2', 'choice3', 'choice4', 'choice5')
        }),
    )