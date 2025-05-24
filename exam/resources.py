# resources.py
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Question, QuestionBank, QuestionIndicator

class QuestionResource(resources.ModelResource):
    question_bank = fields.Field(
        column_name='question_bank',
        attribute='question_bank',
        widget=ForeignKeyWidget(QuestionBank, 'title')
    )

    indicator = fields.Field(
        column_name='indicator',
        attribute='indicator',
        widget=ForeignKeyWidget(QuestionIndicator, 'indicator')
    )

    class Meta:
        model = Question
        # Hapus id dari import_id_fields agar tidak wajib ada
        import_id_fields = []  # <- baris penting
        fields = (
            'number', 'question_bank', 'indicator', 'bagian', 'kompetensi', 'text',
            'choice1', 'choice2', 'choice3', 'choice4', 'choice5',
        )
