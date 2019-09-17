from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def download(req, path):
    if path:
        root_path = os.path.join(settings.BASE_DIR, 'library', req.user.username, path)
        file_name = path.strip().split('/')[-1]
        if os.path.isfile(root_path):
            file = open(root_path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
            return response
    return redirect('/showfile/')


@login_required
def show_file(req):
    file_list = os.listdir(os.path.join(settings.BASE_DIR, 'library', req.user.username))
    return render(req, 'showfile.html', locals())


@login_required
def del_file(req, path):
    if path:
        root_path = os.path.join(settings.BASE_DIR, 'library', req.user.username, path)
        if os.path.isfile(root_path):
            os.remove(root_path)
    return redirect('/showfile/')


@login_required
def up_file(req):
    if req.method == "POST":
        ret = req.FILES.get('file')
        with open(os.path.join(settings.BASE_DIR, 'library', req.user.username, ret.name), 'wb')as f:
            for chunk in ret.chunks():
                f.write(chunk)
            return JsonResponse({'code': 0})
    return render(req, 'showfile.html')
