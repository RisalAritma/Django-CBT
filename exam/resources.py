# resources.py
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Question, QuestionBank, QuestionIndicator, Profile, QuestionAnswer
from django.contrib.auth.models import User

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
            'number', 'question_bank', 'indicator', 'text',
            'choice1', 'choice2', 'choice3', 'choice4', 'choice5',
        )


class UserAnswerResource(resources.ModelResource):
    # Data profil
    email = fields.Field(
        column_name='Email',
        attribute='username'
    )
    nama_lengkap = fields.Field(
        column_name='nama_lengkap',
        attribute='first_name'
    )
    phone = fields.Field(
        column_name='phone',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'phone')
    )
    asal_paud = fields.Field(
        column_name='asal_paud',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'asal_paud')
    )
    lokasi_paud = fields.Field(
        column_name='lokasi_paud',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'lokasi_paud')
    )
    jenis_kelamin = fields.Field(
        column_name='jenis_kelamin',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'jenis_kelamin')
    )
    usia = fields.Field(
        column_name='usia',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'usia')
    )
    pendidikan = fields.Field(
        column_name='pendidikan',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'pendidikan')
    )
    jurusan = fields.Field(
        column_name='jurusan',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'jurusan')
    )
    lama_ngajar = fields.Field(
        column_name='lama_ngajar',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'lama_ngajar')
    )
    status_pegawai = fields.Field(
        column_name='status_pegawai',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'status_pegawai')
    )
    apa_pernah_pelatihan = fields.Field(
        column_name='apa_pernah_pelatihan',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'apa_pernah_pelatihan')
    )
    apa_sudah_ppg = fields.Field(
        column_name='apa_sudah_ppg',
        attribute='profile',
        widget=ForeignKeyWidget(Profile, 'apa_sudah_ppg')
    )

    def dehydrate_usia(self, obj):
        # Ambil nilai asli
        val = obj.profile.usia if hasattr(obj, 'profile') and obj.profile else ''
        # Ganti semua variasi dash/unicode dash dengan '-'
        if val:
            val = val.replace('–', '-').replace('â€“', '-').replace('—', '-')
        return val

    def dehydrate_lama_ngajar(self, obj):
        val = obj.profile.lama_ngajar if hasattr(obj, 'profile') and obj.profile else ''
        if val:
            val = val.replace('–', '-').replace('â€“', '-').replace('—', '-')
        return val
    

    def __init__(self):
        super().__init__()
        # Tambahkan field no1 sampai no60 secara dinamis
        for i in range(1, 61):
            field_name = f'no{i}'
            self.fields[field_name] = fields.Field(column_name=field_name)

    def __getattr__(self, name):
        if name.startswith('dehydrate_no'):
            def dehydrate_dynamic(obj, name=name):
                try:
                    number = int(name.replace('dehydrate_no', ''))
                    question = Question.objects.get(number=number)
                    answer_obj = QuestionAnswer.objects.filter(user=obj, question=question).first()
                    if answer_obj:
                        if answer_obj.random == 'ABCD' and answer_obj.answer == 'A':
                            return 1
                        elif answer_obj.random == 'BCDA' and answer_obj.answer == 'B':
                            return 1
                        elif answer_obj.random == 'CDAB' and answer_obj.answer == 'C':
                            return 1
                        elif answer_obj.random == 'DABC' and answer_obj.answer == 'D':
                            return 1
                        else:   
                            return 0
                    else:
                        return ''   
                except Question.DoesNotExist:
                    return ''
            return dehydrate_dynamic
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {name}")
    
    indikator1 = fields.Field(
        column_name='indikator1'
    )
    indikator2 = fields.Field(
        column_name='indikator2'
    )
    indikator3 = fields.Field(
        column_name='indikator3'
    )
    indikator4 = fields.Field(
        column_name='indikator4'
    )

    def dehydrate_indikator1(self, obj):
        total = 0
        for i in range(1, 26):
            method_name = f'dehydrate_no{i}'
            if hasattr(self, method_name):
                value = getattr(self, method_name)(obj)
            else:
                value = self.__getattr__(method_name)(obj)
            try:
                total += int(value)
            except (TypeError, ValueError):
                pass
        return total

    def dehydrate_indikator2(self, obj):
        total = 0
        for i in range(26, 31):
            method_name = f'dehydrate_no{i}'
            if hasattr(self, method_name):
                value = getattr(self, method_name)(obj)
            else:
                value = self.__getattr__(method_name)(obj)
            try:
                total += int(value)
            except (TypeError, ValueError):
                pass
        return total

    def dehydrate_indikator3(self, obj):
        total = 0
        for i in range(31, 56):
            method_name = f'dehydrate_no{i}'
            if hasattr(self, method_name):
                value = getattr(self, method_name)(obj)
            else:
                value = self.__getattr__(method_name)(obj)
            try:
                total += int(value)
            except (TypeError, ValueError):
                pass
        return total

    def dehydrate_indikator4(self, obj):
        total = 0
        for i in range(56, 61):
            method_name = f'dehydrate_no{i}'
            if hasattr(self, method_name):
                value = getattr(self, method_name)(obj)
            else:
                value = self.__getattr__(method_name)(obj)
            try:
                total += int(value)
            except (TypeError, ValueError):
                pass
        return total
    

    KL_1 = fields.Field(
        column_name='KL_1'
    )
    KL_2 = fields.Field(
        column_name='KL_2'
    )
    KL_3 = fields.Field(
        column_name='KL_3'
    )
    KL_4 = fields.Field(
        column_name='KL_4'
    )

    def dehydrate_KL_1(self, obj):
        indikator = self.dehydrate_indikator1(obj)
        try:
            indikator = int(indikator)
        except (TypeError, ValueError):
            return ''
        if indikator >= 20:
            return "Mahir"
        elif indikator >= 15:
            return "Terampil"
        elif indikator >= 10:
            return "Berkembang"
        else:
            return "Dasar"

    def dehydrate_KL_2(self, obj):
        indikator = self.dehydrate_indikator2(obj)
        try:
            indikator = int(indikator)
        except (TypeError, ValueError):
            return ''
        if indikator >= 4:
            return "Mahir"
        elif indikator == 3:
            return "Terampil"
        elif indikator == 2:
            return "Berkembang"
        else:
            return "Dasar"

    def dehydrate_KL_3(self, obj):
        indikator = self.dehydrate_indikator3(obj)
        try:
            indikator = int(indikator)
        except (TypeError, ValueError):
            return ''
        if indikator >= 20:
            return "Mahir"
        elif indikator >= 15:
            return "Terampil"
        elif indikator >= 10:
            return "Berkembang"
        else:
            return "Dasar"

    def dehydrate_KL_4(self, obj):
        indikator = self.dehydrate_indikator4(obj)
        try:
            indikator = int(indikator)
        except (TypeError, ValueError):
            return ''
        if indikator >= 4:
            return "Mahir"
        elif indikator == 3:
            return "Terampil"
        elif indikator == 2:
            return "Berkembang"
        else:
            return "Dasar"

    def get_queryset(self):
        return User.objects.filter(is_staff=False)

    class Meta:
        model = User
        fields = (
            'email', 'nama_lengkap', 'phone', 'asal_paud', 'lokasi_paud',
            'jenis_kelamin', 'usia', 'pendidikan', 'jurusan', 'lama_ngajar',
            'status_pegawai', 'apa_pernah_pelatihan', 'apa_sudah_ppg', 
            'no1', 'no2', 'no3', 'no4', 'no5','no6', 'no7', 'no8', 'no9', 'no10', 
            'no11', 'no12', 'no13', 'no14', 'no15','no16', 'no17', 'no18', 'no19', 'no20', 
            'no21', 'no22', 'no23', 'no24', 'no25', 'no26', 'no27', 'no28', 'no29', 'no30',
            'no31', 'no32', 'no33', 'no34', 'no35', 'no36', 'no37', 'no38', 'no39', 'no40',
            'no41', 'no42', 'no43', 'no44', 'no45', 'no46', 'no47', 'no48', 'no49', 'no50',
            'no51', 'no52', 'no53', 'no54', 'no55', 'no56', 'no57', 'no58', 'no59', 'no60',
            'indikator1', 'indikator2', 'indikator3', 'indikator4',
            'KL_1','KL_2','KL_3','KL_4',
        )

