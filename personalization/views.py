from django.shortcuts import render

import firebase_admin
from firebase_admin import credentials
from google.cloud.firestore_v1 import ArrayRemove, ArrayUnion

cred = credentials.Certificate(("Key.json"))


from firebase_admin import firestore
db = firestore.client()
records = db.collection(u'recs')
docs = records.stream()


def personalize(request):
    if(request.method=="POST"):
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        doc=records.document(request.session['emailid'])

        user_conv_old = doc.get().to_dict()['userConv']
        bot_conv_old = doc.get().to_dict()['botConv']



        user_conv_old.append(question)
        bot_conv_old.append(answer)

        print(user_conv_old)
        print(bot_conv_old)

        doc.update({
            u'userConv' : user_conv_old,
            u'botConv' : bot_conv_old
        })

        print(question, answer)
        return render(request, 'personalize.html',{"success":question})
    else:
        return render(request , 'personalize.html')
