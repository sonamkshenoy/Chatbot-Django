from django.shortcuts import render
import os
import datetime
from dotenv import load_dotenv
from django.http import HttpResponse


import firebase_admin
from firebase_admin import credentials
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion

import conversation.python_files.modelwork as modelwork
#Ending loading of model


cred = credentials.Certificate(("Key.json"))
firebase_admin.initialize_app(cred)



from firebase_admin import firestore
db = firestore.client()
conversations = db.collection(u'users')
docs = conversations.stream()

records = db.collection(u'records')
docs2 = records.stream()


def interaction(request):

    if(request.method=="POST"):

        user_text = request.POST['user_text']
        print(user_text)

        list_of_emo_conv=[]


        doc=conversations.document(request.session['emailid'])


        doc2=records.document(request.session['emailid'])

        custom_user_conv = doc2.get().to_dict()['userConv']
        custom_bot_conv = doc2.get().to_dict()['botConv']

        if(user_text in custom_user_conv):
            index = custom_user_conv.index(user_text)
            return HttpResponse(custom_bot_conv[index])


        if(user_text!="Bye" and user_text!="bye"):
            reply, list_of_emo_conv = modelwork.callme(user_text)
        else:
            import time
            time.sleep(10)
            reply = modelwork.task3(list_of_emo_conv)


        print(reply)

        user_conv_old = doc.get().to_dict()['Uppermost'][-1]['UserConv']
        bot_conv_old = doc.get().to_dict()['Uppermost'][-1]['BotConv']
        time = doc.get().to_dict()['Uppermost'][-1]['time']

        doc.update({
            u'Uppermost':ArrayRemove([
            {
                u'time' : time,
                u'BotConv': bot_conv_old,
                u'UserConv': user_conv_old,
                #u'Uppermost.Time': firestore.SERVER_TIMESTAMP
            }
         ])
        })

        user_conv_old.append(user_text)
        bot_conv_old.append(reply)

        print(user_conv_old)

        doc.update({
            u'Uppermost':ArrayUnion([
                {
                u'time' : time,
                u'BotConv': bot_conv_old,
                u'UserConv': user_conv_old,
                }

            ])
        })

        return HttpResponse(reply)

    else:
        doc=conversations.document(request.session['emailid'])

        doc.update({
            u'Uppermost':ArrayUnion([
                {
                u'time' : datetime.datetime.now(),
                u'BotConv': [],
                u'UserConv': []
                }

            ])
        })
        return render(request, 'chatbot.html', {"trial":"Added"})

def handler500(request):
    return render(request, '500.html', status=500)

def handler404(request):
    return render(request, '404.html', status=404)
