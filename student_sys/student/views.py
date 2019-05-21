from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from .forms import StudentForm
from .models import Student

def index(request):
    # words='World!'
    # return render(request,'index.html',context={'words':words})
    students=Student.get_all()
    if request.method=='POST':
        form=StudentForm(request.POST)
        if form.is_valid():

            # cleaned_data=form.cleaned_data
            # student=Student()
            # student.name=cleaned_data['name']
            # student.sex=cleaned_data['sex']
            # student.email=cleaned_data['email']
            # student.profession=cleaned_data['profession']
            # student.qq=cleaned_data['qq']
            # student.phone=cleaned_data['phone']
            # student.save()

            '''
            在ModelForm中，有Model的定义，可以不用手动构建Student
            '''
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            form=StudentForm()
        context={
            'students':students,
            'form':form,
        }
        return render(request,'index.html',context=context)

