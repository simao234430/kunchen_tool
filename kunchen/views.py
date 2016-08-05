from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import os
from django import forms
from django.http import HttpResponse, StreamingHttpResponse
from tool import * 
from wsgiref.util import FileWrapper
from django.conf import settings
from datetime import datetime
from time_tool import * 
import uuid


#class UploadFileForm(forms.Form):
#    title = forms.CharField(max_length=50)
#    file = forms.FileField()ko
def handle_uploaded_file(temp_dir,f):
    os.makedirs(settings.SETTINGS_PATH + "/static/" + temp_dir)
    destination = open( settings.SETTINGS_PATH + "/static/" + temp_dir + '/' + 'aa.csv', 'wb')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def test(request):
    #return HttpResponse('dd')
    return render(request, 'test.html')

def generate_temp_dir():
    return str(uuid.uuid1()) + '/'


def postion(request):
    try:
        if request.method == 'POST':
            temp_dir = generate_temp_dir()
            min_precision = request.POST['inputmin']
            max_precision = request.POST['inputmax']
            f =  request.FILES['inputfile']
            handle_uploaded_file(temp_dir,f)
            analysis_postion_data(settings.SETTINGS_PATH + '/aa.csv',settings.SETTINGS_PATH + "/static/" + temp_dir,\
                    min_precision,max_precision)
            return render(request, 'position_result.html',{'dir':temp_dir})

            file_path = settings.SETTINGS_PATH + '/analysis_positon_result.xls'

            response = StreamingHttpResponse(FileWrapper(open(file_path), 8192), content_type='application/vnd.ms-excel')
            response['Content-Length'] = os.path.getsize(file_path)
            response['Content-Disposition'] = 'attachment; filename=analysis_positon_result-%s.xls' % datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            return response
            #return HttpResponse('success handler')
        else:
            return render_to_response('position.html')
    except Exception, e:
        print "excp", e
        traceback.print_exc()
        response(str(e))


def timestamp(request):
    try:
        if request.method == 'POST':
            temp_dir = generate_temp_dir()
            print temp_dir
            min_precision = request.POST['inputmin']
            max_precision = request.POST['inputmax']
            f = request.FILES['inputfile']
            handle_uploaded_file(temp_dir,f)

            write_data_to_excel(settings.SETTINGS_PATH + '/Record.csv',settings.SETTINGS_PATH + "/static/" + temp_dir,min_precision,max_precision)
            return render(request, 'timestamp_result.html',{'dir':temp_dir})

            file_path = settings.SETTINGS_PATH + '/time_diff_result.xls'
            response = StreamingHttpResponse(FileWrapper(open(file_path), 8192), content_type='application/vnd.ms-excel')
            response['Content-Length'] = os.path.getsize(file_path)
            response['Content-Disposition'] = 'attachment; filename=time_diff_result-%s.xls' % datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            return response
            #return HttpResponse('success handler')
        else:
            return render_to_response('timestamp.html')
    except Exception, e:
        print "excp", e
        traceback.print_exc()
        response(str(e))
