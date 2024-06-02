from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db import connection
from datetime import datetime
import mysql.connector as mc

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
    # print(type(selected_option))
    opt_integer = int(selected_option)
    items_to_display = range(opt_integer)
    context={
        'items_to_display':items_to_display,
    }
    return render(request,'quote_form_v1.html',context=context)
def los2(request):
    selected_option = request.POST.get('option')
    # print(type(selected_option))
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
        totalamount=request.POST.get('totalamount')
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
            'd':date,'a1':a1,'a2':a2,'a3':a3,'s':sub,'adet':adet,'nof':nof,'total':totalamount,'combined_data':combined_data,
        }
        with connection.cursor() as cursor:
            query = "INSERT INTO QUOTEGEN (DATE, SUBJECT, TO1, TO2, TO3, ADDITIONAL_DETAILS,TOTALAMOUNT) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (date_obj, sub, a1, a2, a3, adet,totalamount)
            cursor.execute(query, values)
            qid=cursor.lastrowid
            for i in range(len(nof_int)):
                query_quotelist = "INSERT INTO QUOTELIST (QID, DESCRIPTIONS, AMOUNT) VALUES (%s, %s, %s)"
                values_quotelist = (qid,desclist[i], amountlist[i])
                cursor.execute(query_quotelist, values_quotelist)
            connection.commit()
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
        with connection.cursor() as cursor:
            query = "INSERT INTO BILLGEN(DATE,SUBJECT,TO1,TO2,TO3,TOTALAMOUNT,ADVANCEPAID,BALANCEAMOUNT,BILLNO) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s)"
            values = (date_obj, sub, a1, a2, a3, tot,adv,ba,bno)
            cursor.execute(query, values)
            qid=cursor.lastrowid
            for i in range(len(nof_int)):
                query_quotelist = "INSERT INTO BILLIST (ID, DESCRIPTIONS, AMOUNT) VALUES (%s, %s, %s)"
                values_quotelist = (qid,desclist[i], amountlist[i])
                cursor.execute(query_quotelist, values_quotelist)
            connection.commit()
        return render(request,'preview2.html',context=context)
def history(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM QUOTEGEN")
        quote_list_data = cursor.fetchall()
        cursor.execute("SELECT * FROM BILLGEN")
        bill_list_data = cursor.fetchall()
        connection.commit()
    context = {
    'quote_list_data': quote_list_data,
    'bill_list_data':bill_list_data,
    }
    return render(request,'history.html',context=context)
def updatequote(request,id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM QUOTEGEN WHERE QID={id}")
        gendata=cursor.fetchall()
        cursor.execute(f"SELECT * FROM QUOTELIST WHERE QID={id}")
        genlistdata=cursor.fetchall()
        items=len(genlistdata)
        connection.commit()
    context = {
    'gendata': gendata,
    'genlistdata':genlistdata,
    'id':id,
    'items':items,
    }
    # print(genlistdata)
    return render(request,'updatequote.html',context=context)

def updatequotedata(request):
    if request.method == 'POST':
        date=request.POST.get('date')
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date = date_obj.strftime("%d/%m/%Y")
        qid=request.POST.get('qid')
        qlid=request.POST.getlist('qlid[]')
        qlid = [int(x) for x in qlid]
        dlist=request.POST.getlist('desc[]')
        alist=request.POST.getlist('amount[]')
        a1=request.POST.get('a1')
        a2=request.POST.get('a2')
        a3=request.POST.get('a3')
        sub=request.POST.get('sub')
        adet=request.POST.get('adet')
        nof=request.POST.get('nof')
        totalamount=request.POST.get('totalamount')
        nof_int = int(nof)
        nof_int = range(nof_int)
        # desclist=[]
        # amountlist=[]
        # for i in range(len(nof_int)):
        #     desclist.append(request.POST.get(f'desc{i}'))
        #     amountlist.append(request.POST.get(f'amount{i}'))
        combined_data = []
        for a, b in zip(dlist,alist):
            combined_data.append({'a': a, 'b': b,})
        # print(desclist)
        # print(amountlist) 

        with connection.cursor() as cursor:
            query = """
                UPDATE QUOTEGEN 
                SET DATE = %s, SUBJECT = %s, TO1 = %s, TO2 = %s, TO3 = %s, ADDITIONAL_DETAILS = %s, TOTALAMOUNT = %s
                WHERE QID=%s
            """
            values = (date_obj, sub, a1, a2, a3, adet, totalamount,qid)
            cursor.execute(query,values)
            for i in range(len(qlid)):
                query_quotelist = """
                UPDATE QUOTELIST 
                SET DESCRIPTIONS = %s, AMOUNT = %s
                WHERE QLID=%s
                """
                values_quotelist = (dlist[i], alist[i],qlid[i])
                cursor.execute(query_quotelist, values_quotelist)
            connection.commit()
        context={
            'd':date,'a1':a1,'a2':a2,'a3':a3,'s':sub,'adet':adet,'nof':nof,'total':totalamount,'combined_data':combined_data,
        }
        return render(request,'preview.html',context=context)
    
def updatebill(request,id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM BILLGEN WHERE ID={id}")
        gendata=cursor.fetchall()
        cursor.execute(f"SELECT * FROM BILLIST WHERE ID={id}")
        genlistdata=cursor.fetchall()
        # print(genlistdata)
        items=len(genlistdata)
        connection.commit()
    context = {
    'gendata': gendata,
    'genlistdata':genlistdata,
    'id':id,
    'items':items,
    }
    return render(request,'updatebill.html',context=context)

def updatebilldata(request):
    if request.method == 'POST':
        date=request.POST.get('date')
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date = date_obj.strftime("%d/%m/%Y")
        a1=request.POST.get('a1')
        a2=request.POST.get('a2')
        a3=request.POST.get('a3')
        bid=request.POST.get('bid')
        blid=request.POST.getlist('blid[]')
        blid = [int(x) for x in blid]
        dlist=request.POST.getlist('desc[]')
        alist=request.POST.getlist('amount[]')
        bno=request.POST.get('bno')
        sub=request.POST.get('sub')
        nof=request.POST.get('nof')
        tot=request.POST.get('totalamount')
        adv=request.POST.get('advance')
        ba=request.POST.get('balance')
        nof_int = int(nof)
        nof_int = range(nof_int)
        # desclist=[]
        # amountlist=[]
        # for i in range(len(nof_int)):
        #     desclist.append(request.POST.get(f'desc{i}'))
        #     amountlist.append(request.POST.get(f'amount{i}'))
        combined_data = []
        for a, b in zip(dlist,alist):
            combined_data.append({'a': a, 'b': b,})

        context={
            'adv':adv,'ba':ba,'tot':tot,'d':date,'bno':bno,'a1':a1,'a2':a2,'a3':a3,'s':sub,'nof':nof,'combined_data':combined_data,
        }
        with connection.cursor() as cursor:
            query = """
                UPDATE BILLGEN 
                SET DATE = %s, SUBJECT = %s, TO1 = %s, TO2 = %s, TO3 = %s,TOTALAMOUNT = %s,ADVANCEPAID= %s,BALANCEAMOUNT= %s,BILLNO= %s
                WHERE ID=%s
            """
            values = (date_obj, sub, a1, a2, a3,tot,adv,ba,bno,bid)
            cursor.execute(query,values)
            for i in range(len(blid)):
                query_quotelist = """
                UPDATE BILLIST 
                SET DESCRIPTIONS = %s, AMOUNT = %s
                WHERE BLID=%s
                """
                values_quotelist = (dlist[i], alist[i],blid[i])
                cursor.execute(query_quotelist, values_quotelist)
                connection.commit()
        return render(request,'preview2.html',context=context)
    
def deletebill(request,id):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM BILLIST WHERE ID={id}")
        # gendata=cursor.fetchall()
        cursor.execute(f"DELETE FROM BILLGEN WHERE ID={id}")
        # genlistdata=cursor.fetchall()
        # items=len(genlistdata)
        connection.commit()
    return redirect("history")

def deletequote(request,id):
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM QUOTELIST WHERE QID={id}")
        # gendata=cursor.fetchall()
        cursor.execute(f"DELETE FROM QUOTEGEN WHERE QID={id}")
        # genlistdata=cursor.fetchall()
        # items=len(genlistdata)
        connection.commit()
    return redirect("history")
    
