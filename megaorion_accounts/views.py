from django.http import FileResponse
from django.conf import settings
import os


def index(request):
    base = str(settings.BASE_DIR)
    html = open(base + '/account/templates/account/index.html', 'rb')
    response = FileResponse(html)
    return response
