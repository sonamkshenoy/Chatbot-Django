from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import pyrebase

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()


def upload(request):
    return render(request, 'upload.html')

def upload_save(request):
    if(request.method == 'POST' and request.FILES['myfile']):
        myfile = request.FILES['myfile']
            storage.child("files/"+myfile.name).put(myfile)
        print(myfile)
        print("nice")
    return render(request, 'upload_save.html')
