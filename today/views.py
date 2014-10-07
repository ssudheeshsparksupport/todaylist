from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from today.models import Project, Task
from django.utils import timezone
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']# 'username' is the name of the textbox
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username,email=email,password=password)
        print '>>>>>>>>>>>>>',user
        return redirect('/today/signin/')
            
    else:
        return render(request,'today/signup.html')
@csrf_exempt
def signin(request):
    print request.POST.get('data')
    if request.method == 'POST':
        a=json.loads(request.POST.get('data'))#using jquery to load the data
        username = a['title']
        password = a['title1']
        #username = request.POST['username']
        #password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("success")
                #return redirect('/today/projectadd/')#html page using redirecting
            else:
                return render(request,'today/signin.html',{'message':'Sorry,your account is disabled'})
        else:
            return render(request,'today/signin.html',{'message':'Failed to authenticate User'})
    else:
        return render(request,'today/signin.html')


@csrf_exempt
@login_required(login_url='/today/signin')#user login only this view occur otherwise not
def projectadd(request):
    if request.method == 'POST':
        print request.POST.get('data')
        a=json.loads(request.POST.get('data'))
        print a
        #print type(a)
        #print request.POST.get('data')
        user=request.user
        #detailsone=Project.objects.filter(user=user)
        details=Project()#model name
        #details.project_name=request.POST['title']
        details.project_name=a['title']
        details.user=request.user
        details.save()
            #return HttpResponseRedirect('/today/projectlist/')
        return HttpResponse("success")
    return render(request, 'today/projectadd.html', {
        #'detailsone': detailsone,

        })
@csrf_exempt
def taskadd(request):
    
    project_list = Project.objects.filter(user=request.user)
    #context = {'project_list': project_list}
    #user=request.user
    task_list=Task.objects.filter(project=project_list)
    paginator = Paginator(task_list, 3)
    #page1 = paginator.page(1)
    #p=page1.object_list
    #print '<<<<<', p

    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasks = paginator.page(1)
        
    except EmptyPage:
        #return HttpResponse("error,page no is not valid")
        # If page is out of range (e.g. 9999), deliver last page of results.
        #tasks = paginator.page(1)
        tasks = paginator.page(paginator.num_pages) 
    #print '>>>>>', task_list
    #user=request.user
    #detailstwo=Task.objects.filter(project=user)
    if request.method == 'POST':
        details=Task()
        #print request.POST.get('projectid')
        #
        details.project=Project.objects.get(id=request.POST.get('projectid'))#getting values to the combobox #projectid is the select class name
        details.title=request.POST['title']#here title is the html textfield name
        #details.project=request.
        details.save()

        #return HttpResponseRedirect('/today/projectlist/')

    return render(request, 'today/taskadd.html', { 
        'project_list':project_list,'tasks':tasks,
    })
    

@login_required(login_url='/today/signin')
def taskediting(request, id):
    print id
    one=Task.objects.get(id=id)
    if request.method == 'POST':
        one.title=request.POST['title']
        one.save()
        return redirect(('/today/taskadd/'))

    return render(request, 'today/taskediting.html', { 'one': one })

@login_required(login_url='/today/signin')
def taskdeleting(request, id):
   #
    one=Task.objects.get(id=id).delete()
    return redirect(('/today/taskadd/'))

@login_required(login_url='/today/signin')
def projectdeleting(request, id):
    one=Project.objects.get(id=id).delete()
    return redirect(('/today/projectlist/'))


@login_required(login_url='/today/signin')
def checkboxdeleting(request):
    todel = request.POST.getlist('checkboxdel')#checkboxdel is the checkbox name in html
    #print '>>>>>>>', todel
    #print 'sdadaasssssssssssssssssss', request.POST.getlist('checkboxdel')
    checkboxselect=Task.objects.filter(id__in=todel)
    #print dd
    for select in checkboxselect:
        select.delete()
    return redirect(('/today/taskadd/'))

def projectlist(request):
    #user=request.user
    #detailsone=Project.objects.filter(user=user)
    detailsone=Project.objects.filter(user=request.user)
    for detail in detailsone:
        detail.Task=Task.objects.filter(project=detail).count()#assigning values to the variable detail.Task
        #print Task.objects.filter(project=detail).count()
        #detail.Taskone=Task.objects.filter(project=detail)
        #print detail.task
    #tasks=Task.objects.filter(project=detailsone)
    

    return render(request, 'today/projectlist.html', {
        'detailsone': detailsone, 
    })
    #return HttpResponse("haaaaaaaaaiiiiiiii")

    
def logout_view(request):
    logout(request)
    return redirect('/today/signin/')

@csrf_exempt
def projectlistone(request):
    projects=Project.objects.all()
    #projectlis=[]
    ##for project in projects:
       #projectlis.append(project.project_name)

    #print projectlis
    #return HttpResponse(json.dumps({'data':projectlis}), content_type="application/json")
    

    #return HttpResponse("success")

    return render(request, 'today/projectlistone.html', {
        'projects': projects, 
    })

@csrf_exempt    
def getconsole(request):

    project=Project.objects.all()
    print '>>>>', project
    projectlis=[]
    for prjct in project:
       projectlis.append(prjct.project_name)

    print '<<<<<<<<<<<<<', projectlis
    return HttpResponse(json.dumps({'data':projectlis}), content_type="application/json")


@csrf_exempt    
def getconsoletasks(request):

    tasks=Task.objects.all()
    #print '>>>>', tasks
    tasklist=[]
    for task in tasks:
       tasklist.append(task.title)

    print '<<<<<<<<<<<<<', tasklist
    return HttpResponse(json.dumps({'data':tasklist}), content_type="application/json")





