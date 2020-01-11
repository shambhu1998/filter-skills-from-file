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

        return render(request, 'file/index.html', {
            'upload_file_path': upload_file_path,
            'Name': data['name'],
            'Email': data['email'],
            'Skills': data['skills']

        })


    else:
        return render(request, 'file/index.html')


# output = open('output.txt', 'w')
# subprocess.call(['pdf2txt.py', upload_file_path], stdout=output)
# output.close()
# os.remove(upload_file_path)

# tables = camelot.read_pdf(upload_file_path, flavor='stream', table_areas=['0,800,800,0'])
# tables.export('foo.csv', f='csv', compress=True)
# tables[0].to_csv('foo.csv')
# os.remove(upload_file_path)
