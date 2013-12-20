import cgi, hashlib, time, datetime
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, Http404
from models import *

# Create your views here.

@csrf_exempt
def index(request):
    request.encoding = 'utf-8'
    if request.method == 'GET':
        return render_to_response('index.html', {'data': ''})
    else:
        if request.POST['t'] != "":
            try:
                oldpaste = Paste.objects.get(text=request.POST['t'])
                return HttpResponseRedirect('/'+oldpaste.key)
            except Paste.DoesNotExist:
                newpaste = Paste(text=request.POST['t'])
                needskey = True
                i = 0
                while needskey:
                    if i > 40:
                        return HttpResponseBadRequest('<h1>400 Bad Request</h1><p>Mad SHA1 conflicts :/</p>')
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
        else:
            return HttpResponseRedirect('/')

def retrieve(request, returntype="plain"):
    pastename = request.path[1:]
    if "/" in pastename:
        if request.path[1:].split('/')[1] == "html":
            returntype = "html"
            pastename = request.path[1:].split('/')[0]
    if request.method == 'GET':
        try:
            data = Paste.objects.get(key=pastename)
        except:
            raise Http404
        response = HttpResponse()
        response['content-type'] = 'text/'+returntype
        response['title'] = 'Plain Text Paste'
        if request.path[1:] == 'script':
            response['title'] = "PXQZ Command line script"
        if request.path[1:] == 'emacs':
            response['title'] = "PXQZ Emacs Minor Mode"
        response.write(data)
        return response
    else:
        raise Http404

def edit(request):
    if request.method == 'GET':
        try:
            data = Paste.objects.get(key=request.path[1:].split('/')[0])
        except:
            raise Http404
        return render_to_response('index.html', {'data': data})
    else:
        raise Http404

def clean(request):
    Paste.objects.filter(date__lte = datetime.datetime.fromtimestamp(time.time()-86400)).delete()
    Paste.objects.filter(key = "script").delete()
    Paste.objects.filter(key = "emacs").delete()
    newpaste = Paste(text="""#!/usr/bin/env perl

my $input = 't=';
while (<STDIN>) {
      $input .= qq($_);
}
$input =~ s/\+/%2B/g;
$input =~ s/\\\\/%5C/g;
$input =~ s/"/%22/g;
$input =~ s/`/%60/g;
$input =~ s/;/%3B/g;
$input =~ s/&/%26/g;
$input .= '"';
$data = 'curl -id "' . $input . " http://p.xqz.ca/ 2>/dev/null | grep ^Location | sed 's/Location: //'";
exec($data);
""")
    newpaste.key = "script"
    newpaste.save()
    newpaste = Paste(text="""(defun pxqz-post ()
  (interactive)
  (let ((url-request-method "POST")
        (url-request-extra-headers
         '(("Content-Type" . "application/x-www-form-urlencoded")))
        (url-request-data
         (concat "t="
                 (buffer-string))))
    (url-retrieve "http://p.xqz.ca/" 'pxqz-handle-url)))

(defun pxqz-handle-url (status)
  (message "%s" (nth 1 status))
  (kill-new (current-message)))

(define-minor-mode pxqz-mode
  "Minor mode for easy pasting of buffers to p.xqz.ca"
  :lighter pxqz
  :keymap (let ((map (make-sparse-keymap)))
            (define-key map (kbd "C-x p") 'pxqz-post)
            map))

(provide 'pxqz)
""")
    newpaste.key = "emacs"
    newpaste.save()
    return HttpResponse('All clear', content_type='text/plain')
