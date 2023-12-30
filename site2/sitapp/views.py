from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from datetime import datetime

# Create your views here.
def home(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        #authenticate
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"successful login")
            return redirect('home')
        else:
            messages.success(request,"failed to login")
            return redirect('home')
    else:
        return render(request,'home.html')

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request,"you were logged out")
    return redirect('home')

def quote_form_v1(request):
    return render(request,'quote_form_v1.html',{})
def bill_v1(request):
    return render(request,'bill_v1.html',{})

def los(request):
    selected_option = request.POST.get('option')
    print(type(selected_option))
    opt_integer = int(selected_option)
    items_to_display = range(opt_integer)
    context={
        'items_to_display':items_to_display,
    }
    return render(request,'quote_form_v1.html',context=context)
def los2(request):
    selected_option = request.POST.get('option')
    print(type(selected_option))
    opt_integer = int(selected_option)
    items_to_display = range(opt_integer)
    context={
        'items_to_display':items_to_display,
    }
    return render(request,'bill_v1.html',context=context)
def quote(request):
    if request.method == 'POST':
        date=request.POST.get('date')
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date = date_obj.strftime("%d/%m/%Y")
        a1=request.POST.get('a1')
        a2=request.POST.get('a2')
        a3=request.POST.get('a3')
        sub=request.POST.get('sub')
        adet=request.POST.get('adet')
        nof=request.POST.get('nof')
        nof_int = int(nof)
        nof_int = range(nof_int)
        desclist=[]
        amountlist=[]
        for i in range(len(nof_int)):
            desclist.append(request.POST.get(f'desc{i}'))
            amountlist.append(request.POST.get(f'amount{i}'))
        combined_data = []
        for a, b in zip(desclist,amountlist):
            combined_data.append({'a': a, 'b': b,})

        context={
            'd':date,'a1':a1,'a2':a2,'a3':a3,'s':sub,'adet':adet,'nof':nof,'combined_data':combined_data,
        }
        return render(request,'preview.html',context=context)

def bill(request):
    if request.method == 'POST':
        date=request.POST.get('date')
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date = date_obj.strftime("%d/%m/%Y")
        a1=request.POST.get('a1')
        a2=request.POST.get('a2')
        a3=request.POST.get('a3')
        bno=request.POST.get('bno')
        sub=request.POST.get('sub')
        nof=request.POST.get('nof')
        tot=request.POST.get('total')
        adv=request.POST.get('advance')
        ba=request.POST.get('balance')
        nof_int = int(nof)
        nof_int = range(nof_int)
        desclist=[]
        amountlist=[]
        
        for i in range(len(nof_int)):
            desclist.append(request.POST.get(f'desc{i}'))
            amountlist.append(request.POST.get(f'amount{i}'))
        # ali=[int(x) for x in amountlist]
        # ali=sum(ali)
        # print(ali)
        combined_data = []
        for a, b in zip(desclist,amountlist):
            combined_data.append({'a': a, 'b': b,})

        context={
            'adv':adv,'ba':ba,'tot':tot,'d':date,'bno':bno,'a1':a1,'a2':a2,'a3':a3,'s':sub,'nof':nof,'combined_data':combined_data,
        }
        return render(request,'preview2.html',context=context)