import os
from django.conf import settings


# myapp/context_processors.py
def web_name(request):
    return {
        'baseurl': 'http://127.0.0.1:8000/',
        'web_name': 'Self Assessment Kompetensi Guru PAUD',
        'webname': 'SelfAssessment',
        'address': 'Jl.....',
        'address_ttd': 'Makassar',
        'telp': '(0422) 22559',
        'fax': '(0422) 22559',
        'email': '............',
        'api_qrcode' : 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=',
    }

# Izin adding versi static kak, (proble browsing chace css)
def versioned_static(request):
    version = 'v1.0.3'  # You can update this version number when needed
    return {
        'STATIC_VERSION': version,
    }

