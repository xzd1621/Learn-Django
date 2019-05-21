import datetime

from django.core.mail import send_mail
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template

from .forms import ContactForm

'''
视图函数，至少有一个参数，约定为request
第一个参数是HttpRequest对象，返回HttpReponse实例
'''
def hello(request):
    return HttpResponse('Hello,World!')

def current_time(request):
    now=datetime.datetime.now()
    html='It is %s.'%now
    return HttpResponse(html)

def hours_ahead(request,offset):
    try:
        offset=int(offset)
    except ValueError:
        return Http404()
    dt=datetime.datetime.now()+datetime.timedelta(hours=offset)
    return render(request,'hours_ahead.html',{'offset':offset,'dt':dt})

'''
使用模板
'''
def current_datetime(request):
    now=datetime.datetime.now()
    return render(request,'current_datetime.html',{'current_date':now})

'''
获取请求的其它信息
'''
def ua_dispaly(request):
    ua=request.META.get('HTTP_USER_AGENT','unknown')
    return HttpResponse('your browser is %s '% ua)

def display_meta(request):
    values=request.META.items()
    # values.sort()
    html=[]
    for k,v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' %(k,v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def contact(request):
    if request.method=='POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            cd=form.clean_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email','noreply@example.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks')
        else:
            form=ContactForm()
        return render(request,'contact_form.html',{'form':form})
    else:
        return HttpResponse('It is a get filed')