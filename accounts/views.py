from django.shortcuts import render, redirect

import pyrebase


firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("Key.json")

from firebase_admin import firestore
db = firestore.client()


def choices(request):
    return render(request, 'choices.html')


def login_view(request):
    if(request.method=="GET"):

            return render(request, 'login.html')

    else:

        emailid = request.POST.get('emailid').lower()
        password = request.POST.get('password')



        try:

            user = auth.sign_in_with_email_and_password(emailid, password)

            if(auth.get_account_info(user['idToken'])['users'][0]['emailVerified']==True):

                request.session['emailid'] = emailid
                print("done")

                return render(request, 'login.html',{ "success" : True  })
            else:
                return render(request, 'login.html',{ "exception" : "Please verify your email-id first if you haven't already."  })

        except:
            return render(request, 'login.html',{ "exception" : "Sorry! Make sure you have entered your email id and password correctly. If that's right make sure you have already created an account."  })



def signup_view(request):
    if(request.method=="GET"):
        return render(request, 'signup.html')

    else:

        username = request.POST.get('name')
        emailid = request.POST.get('emailid').lower()
        password = request.POST.get('password')

        user={}

        try:
            user = auth.create_user_with_email_and_password(emailid, password)
            auth.send_email_verification(user['idToken'])
        except:
            return render(request, 'signup.html', {"exception":"This email id has been taken by someone already or does not exist. Also make sure that your password has at least 6 characters."})

        doc_ref = db.collection(u'users').document(user['email'])
        doc_ref.set({
            'Uppermost':[]
        })


        doc_ref2 = db.collection(u'records').document(user['email'])
        doc_ref2.set({
            'userConv':[],
            'botConv':[]
        })

        return render(request, 'signup.html', {"success": "Hey!" + username + "! An email has been sent to your email id. Please verify it's you and then hit sign in on."})
