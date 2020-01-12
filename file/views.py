import time

from django.shortcuts import redirect

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


import nltk
from pyresparser import ResumeParser

# import camelot

# import subprocess

import os, datetime


def index_redirect(request):
    return redirect('/file/')

# Create your views here.

def index(request):
    if request.method == 'POST' and request.FILES['file']:
        start_time = time.time()

        upload_file = request.FILES['file']
        extension = os.path.splitext(upload_file.name)[1]
        if extension=='.pdf' or '.doc':

            rename = datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S") + extension
            fss = FileSystemStorage()
            filename = fss.save(rename, upload_file)
            upload_file_path = fss.path(filename)
            data = ResumeParser(upload_file_path).get_extracted_data()
            print(data)

            os.remove(upload_file_path)
        stop_time = time.time()
        response = {
            'upload_file_path': upload_file_path,
            'Name': data['name'],
            'Email': data['email'],
            'Skills': data['skills'],
            'time': format(stop_time - start_time, '.2f'),
        }

        return render(request, 'file/index.html', context=response )


    else:
        return render(request, 'file/index.html')
