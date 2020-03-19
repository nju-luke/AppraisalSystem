from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login,authenticate,logout
from django.shortcuts import render, redirect


@login_required
def index(request):
    return render(request,'index.html')

def accounts_login(request):
    if request.method=='GET':
        return  render(request,'login.html')
    else:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user= authenticate(username=username,password=password)
        if user:
            login(request,user)
            print("OK................")
            return redirect('/index')
        else:
            err_msg="loging error"
            return render(request, 'login.html',{'err_msg':err_msg})

def accounts_logout(request):
    logout(request)
    return redirect('/accounts/login')