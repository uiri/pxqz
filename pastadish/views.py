import cgi, hashlib
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from models import *

# Create your views here.

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return render_to_response('index.html')
    else:
        if request.POST['t']:
            newpaste = Paste(text=request.POST['t'])
            needskey = True
            i = 0
            while needskey:
                if i > 40:
                    return render_to_response('400.html')
                elif i > 35:
                    j = 5 - (40 - i)
                else:
                    j = i+5
                sha = hashlib.sha1(request.POST['t']).hexdigest()[i:j]
                try:
                    Paste.objects.get(key=sha)
                    i += 1
                except Paste.DoesNotExist:
                    newpaste.key = sha
                    needskey = False
            newpaste.save()
            return HttpResponseRedirect('/'+sha)

def retrieve(request):
    if request.method == 'GET':
        try:
            data = Paste.objects.get(key=request.path[1:])
        except:
            return render_to_response('404.html')
        return HttpResponse(data, content_type='text/plain')
    else:
        return render_to_response('404.html')
