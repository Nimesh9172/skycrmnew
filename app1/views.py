from calendar import c
import json
from operator import methodcaller
from re import A
from urllib import response
from django.http import HttpResponse,JsonResponse
import pandas as pd
from django.shortcuts import render,redirect
from .models import *
from .forms import otsdataForm, personalForm,additionalForm,DataUploadForm,SmsUploadForm

from datetime import datetime
from django.conf import settings
from datetime import datetime,timedelta
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Count,Sum,Case,When
import xlwt
import pymysql
import requests
import random
import ast

apilink = '192.168.1.46:1001'

def dbconnection():
    try:
        db=pymysql.connect(host="192.168.1.46",user="root",password="robust",database="asterisk")
        return db
    except Exception as e:
        print(e)
        return None


def userajax(request):
    db = dbconnection()
    cur = db.cursor()
    query = f"SELECT user,pass,user_level,user_group FROM vicidial_users"
    cur.execute(query)  
    r = cur.fetchall()
    try:
        
        for i in r:
            if User.objects.filter(username= i[0]).exists():
                a = User.objects.get(username= i[0])
                a.username = i[0]
                #a.set_password(i[1])
                a.user_level=i[2]
                a.usergroup=i[3]
                #a.save()
            else:
                obj = User.objects.create_user(username=i[0],password=i[1],user_level=i[2],usergroup=i[3])
                obj.save()
            return JsonResponse({'status':200})

    except Exception as e:
            print(e)

    return JsonResponse({'status':200})

def mobno(request):
    return render(request,"mobilenopopup.html")

def qualityscore(request):
    return render(request,"qualityscore.html")


@login_required(login_url='login')
def base3(request):
    return render(request,"base3.html")


@login_required(login_url='login')
def dialer(request):
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    print(today)
    print(yesterday)
    try:
        db=dbconnection()
        cur=db.cursor()
        link = 'omkara.rmantra.in'
    except Exception as e:
        print(e)
        link = ''
   
    return render(request,"vicidial.html",{'link':''})


def dialstatus(request):
    status = "offline"

    try:
        db=dbconnection()
        cur=db.cursor()
        q=f'select user from vicidial_live_agents'
        # cur.execu
        cur.execute(q)
        b=cur.fetchall()
        user=[]
        for i in b:
            user.append(i[0])
        print(user,request.user.username)
        cur.close()
        db.close()
        if request.user.username in user:
            status = "online"
          
            return JsonResponse({'status':200,'dstatus':status})
    except Exception as e:
        print(e)
   
    return JsonResponse({'status':200,'dstatus':status})
    

def notificationCount(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    if request.user.user_level == 9:
        d=personaldetails.objects.all().filter(callbacktime__contains=d4).aggregate(total=Sum(Case(When( (Q(sub_dispossitions='Call Back')|Q(sub_dispossitions="Schedule Call")|Q(sub_dispossitions="Promise To Pay")),then=1),default=0
          )))
    else:
       
        d=personaldetails.objects.filter(callbacktime__contains=d4).filter(callername=request.user.username).aggregate(total=Sum(Case(When( (Q(sub_dispossitions='Call Back')|Q(sub_dispossitions="Schedule Call")|Q(sub_dispossitions="Promise To Pay")),then=1),default=0
        )))
        
    value=d["total"]
  
    return JsonResponse({'value':value})


def misscallednotiCount(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    # d4="2022-09-22"
    if request.user.user_level == 9:
        d=MissedCall.objects.filter(missdt__contains=d4).exclude(contacted="Yes").count()
        print("missssssssssssssssssssssssssssssssssssssssssssssss",d)
    else:
       
        d=MissedCall.objects.filter(missdt__contains=d4).filter(username=request.user.username).exclude(contacted="Yes").count()
        print(d)
        
 
  
    return JsonResponse({'d':d})

@login_required(login_url="login")
def incomingcms(request):
    info=personaldetails.objects.all()
    id=0
    db=dbconnection()
    cur=db.cursor()
    q= f"select distinct category,status_name from vicidial_campaign_statuses"
    # q= f"select * from vicidial_campaign_statuses"
    cur.execute(q)
    sub =  cur.fetchall()
    contacted = []
    noncontacted = []
    for i in sub:
        if i[0] == 'contacted':
            contacted.append(i[1])
        else:
            noncontacted.append(i[1])
    print(sub)
    # print(noncontacted)
    
    try:
        p=request.GET["phone_number"]
        print(type(p),p)
       
        
        if len(p) > 10:
            p=p[2:]
        a=0
        try :
            a = Additional.objects.values_list('debtor_id',flat=True).get(contactnum=p)
            
        except Exception as e:
            print(e)

        info=personaldetails.objects.filter(Q(mobile_number=p)| Q(alt_mno_1=p) | Q(alt_mno_2=p)  | Q(alt_mno_3=p) | Q(id=a))
        
        for i in info:
            id=i.id
        o=f'select status from vicidial_live_agents'
        for i in b:
           agentstatus=i
           if agentstatus==('PAUSED',):
                personaldetails.objects.filter(id=id).update(what="oncall")
           else:
                personaldetails.objects.filter(id=id).update(what="")
    
    except Exception as e:
        print(e)
    cur.close()
    db.close()
    if len(info)!=0:
       
        personaldetails.objects.filter(id=id).update(what="oncall")
        if request.method=="POST":
            disval=request.POST.get("dispositionvalue")
            subval=request.POST.get("subdispositionvalue")
            dail=request.POST.get("dialnum3")
            print('dail',dail)
        
            mode=request.POST.get("radio-group")
            cash=request.POST.get('cashtype')
            trans_cheq1=request.POST.get("trans1")
            trans_cheq2=request.POST.get("trans2")
            field=request.POST.get("field_branch")
            ptpamt=request.POST.get("ptpamt")
            ptpdate=request.POST.get("ptpdate")
            paidamt=request.POST.get("paidamt")
            callscheduletime=request.POST.get("checks[]")
            schedule=request.POST.get("scheduledate")
            remarkall=request.POST.get("remark")
            emino=request.POST.get("settle")
            emiamt1=request.POST.get("emiamt1")
            emiamt2=request.POST.get("emiamt2")
            emiamt3=request.POST.get("emiamt3")
            emiamt4=request.POST.get("emiamt4")
            emidate1=request.POST.get("emidate1")
            emidate2=request.POST.get("emidate2")
            emidate3=request.POST.get("emidate3")
            emidate4=request.POST.get("emidate4")
            # eremark=request.POST.get("eremark")
            #emi info ends
            otsamt=request.POST.get("otsamt")
            otspercent=request.POST.get("tospercent")
            # otsremark=request.POST.get("otsremark")
            #send fe to collect start
            area=request.POST.get("sarea")
            address=request.POST.get("saddress")
            land=request.POST.get("slandmark")
            pin=request.POST.get("spincode")
            modeofpay=request.POST.get("femode")
            time=request.POST.get("stime")
            sendate=request.POST.get("sdate")
            amt=request.POST.get("amt")
            dt=datetime.now()
            nowdate=dt.now().date() 
            try:
                cash = int(cash)
            except:
                cash = None
            
            try:
                ptpamt = int(ptpamt)
            except:
                ptpamt = None

            bn=personaldetails.objects.filter(id=id).values('borrowor_name') 
            loanid=personaldetails.objects.filter(id=id).values('bank_loan_accountno')
            TOS=personaldetails.objects.filter(id=id).values('TOS') 

    
            trans_cheq = ""
            if trans_cheq1 != "":
                trans_cheq = trans_cheq1
            elif trans_cheq2 != "":
                trans_cheq = trans_cheq2
            
            date = ''
            if ptpdate != "":
                date = ptpdate
            elif schedule!= "":
                date= schedule

        
            dt = datetime.now()
            am = dt + timedelta(minutes=0)

            # print(type(am))
            if callscheduletime == "15min":
                am = dt + timedelta(minutes=15)
            elif callscheduletime == "30min":
                am = dt + timedelta(minutes=30)
            elif callscheduletime == "45min":
                am = dt + timedelta(minutes=45)
            elif callscheduletime == "1hr":
                am = dt + timedelta(minutes=60)

            ft= am.strftime("%Y-%m-%d %H:%M:%S")
            if paidamt == "":
               paidamt = None
            if disval != "" or subval != "" or mode != " " or trans_cheq != "" or cash != "" or ptpamt !="" or date==''   or schedule != "" or remarkall !="" :
            
                add=personaldetails.objects.filter(id=id).update(disposition=disval,sub_dispossitions=subval,mode=mode,transactionid_chequeno=trans_cheq,cash=paidamt,lastdial=dail,amount=ptpamt,remark=remarkall,user_id=request.user.id,callername=request.user.username,contacted_DateTime=dt,attempted=F("attempted") + 1)

                if date!="":
                    add=personaldetails.objects.filter(id=id).update(disposition=disval,sub_dispossitions=subval,callbacktime=date,user_id=request.user.id,callername=request.user.username,attempted=F("attempted") + 1)
        
            if callscheduletime != None:
                up=personaldetails.objects.filter(id=id).update(callbacktime=ft,user_id=request.user.id,callername=request.user.username,attempted=F("attempted") + 1)

            if otsamt!= "":
                otsexists = otsdata.objects.filter(info_id=id)
                print(otsexists)
                if otsexists:
                    otsinfo=otsdata.objects.update(ots_amt=otsamt,remark=remarkall,borrower_name=bn,loan_id=loanid,otspercentage=otspercent,tos=TOS,info_id=id,callername=request.user.username)
                else:
                    otsinfo=otsdata.objects.create(ots_amt=otsamt,remark=remarkall,otspercentage=otspercent,borrower_name=bn,loan_id=loanid,tos=TOS,info_id=id,callername=request.user.username)
                    otsinfo.save()


            if schedule !=None and schedule!="":
                up=personaldetails.objects.filter(id=id).update(callbacktime=schedule,user_id=request.user.id,callername=request.user.username,attempted=F("attempted") + 1)
            try:
                if  emidate1=="" or emiamt1 == '':
                    emiamt1 = 0
                    emidate1 = None
                if  emidate2=="" or emiamt2 == '':
                    emiamt2 = 0
                    emidate2 = None
                if  emidate3=="" or emiamt3 == '':
                    emiamt3 = 0
                    emidate3 = None
                if  emidate4=="" or emiamt4 == '':
                    emiamt4 = 0
                    emidate4 = None
                if  emidate1!=None or emidate2!=None or emidate3!=None or emidate4!=None:
                    e=emi.objects.create(emidate1=emidate1,emidate2=emidate2,emidate3=emidate3,emidate4=emidate4,amount1=emiamt1,amount2=emiamt2,amount3=emiamt3,amount4=emiamt4,refrence_id=id,emi=emino)
            
            except Exception as e:
                print(e)
                
            #  main code running for sendfe
            if address != "" or area != "" or land!= '' or pin != '' or modeofpay != "" or time !=None or sendate != '' or  amt !=None  :
                print(1,address,2,area,3,land,4,pin,5,modeofpay,6,time,7,sendate,8,amt)
                fedata=sendfeto.objects.create(address=address,area=area,pincode=pin,landmark=land,fe_datetime=sendate,amount=amt,modeofpay=modeofpay,client_id=id,user_id=request.user.username,contacted_datetime=dt)
                fedata.save()
           
            try:
                camp=""
                a=personaldetails.objects.filter(id=id)
                u=User.objects.filter(username=request.user.username)

                for i in u:
                    camp=i.campaign
                    

                for i in a :
                    # if i.bank_loan_accountno == 'nan':
                    #     i.bank_loan_accountno = None
                    
                 
                    b = LogData.objects.create(borrowor_name=i.borrowor_name,mobile_number=i.mobile_number,address=i.address,state=i.state,pincode=i.pincode,dateofbirth=i.dateofbirth,email_id=i.email_id,phone_number=i.phone_number,bankname=i.bankname,trustname=i.trustname,systemlan=i.systemlan,bank_loan_accountno=i.bank_loan_accountno,branchname=i.branchname,bankstate=i.bankstate,nature_of_facility=i.nature_of_facility,sanctionamount=i.sanctionamount,loan_sanction_date=i.loan_sanction_date,NPA_Date=i.NPA_Date,interest_rate=i.interest_rate,account_status=i.account_status,security_value=i.security_value,document_custody=i.document_custody,security_flag=i.security_flag,current_allocation=i.current_allocation,current_allocation_date=i.current_allocation_date,team_leader=i.team_leader,zone_name=i.zone_name,branch_mail_id=i.branch_mail_id,branch_contact_details=i.branch_contact_details,total_collected_amount=i.total_collected_amount,balance_POS_amount=i.balance_POS_amount,TOS=i.TOS,TOS_as_on_Date=i.TOS_as_on_Date,next_action_date=i.next_action_date,current_principal_outstanding=i.current_principal_outstanding,payment_date=i.payment_date,agent_username=i.agent_username,city=i.city,disposition=i.disposition,sub_dispossitions=i.sub_dispossitions,mode=i.mode,transactionid_chequeno=i.transactionid_chequeno,cash=i.cash,schedule=i.schedule,field_branch=i.field_branch,datetime=i.datetime,callbacktime=i.callbacktime,amount=i.amount,remark=i.remark,contacted_DateTime=i.contacted_DateTime,created_by=i.created_by,caller_name=i.callername,loanamt=i.loanamt,lastdial=i.lastdial,personalForkey_id=id,list_id=i.list_id_id,campaign=camp)
                    print("after")
                    if  emidate1!=None or emidate2!=None or emidate3!=None or emidate4!=None:
                        b = LogData.objects.create(borrowor_name=i.borrowor_name,mobile_number=i.mobile_number,address=i.address,state=i.state,pincode=i.pincode,dateofbirth=i.dateofbirth,email_id=i.email_id,phone_number=i.phone_number,bankname=i.bankname,trustname=i.trustname,systemlan=i.systemlan,bank_loan_accountno=i.bank_loan_accountno,branchname=i.branchname,bankstate=i.bankstate,nature_of_facility=i.nature_of_facility,sanctionamount=i.sanctionamount,loan_sanction_date=i.loan_sanction_date,NPA_Date=i.NPA_Date,interest_rate=i.interest_rate,account_status=i.account_status,security_value=i.security_value,document_custody=i.document_custody,security_flag=i.security_flag,current_allocation=i.current_allocation,current_allocation_date=i.current_allocation_date,team_leader=i.team_leader,zone_name=i.zone_name,branch_mail_id=i.branch_mail_id,branch_contact_details=i.branch_contact_details,total_collected_amount=i.total_collected_amount,balance_POS_amount=i.balance_POS_amount,TOS=i.TOS,TOS_as_on_Date=i.TOS_as_on_Date,next_action_date=i.next_action_date,current_principal_outstanding=i.current_principal_outstanding,payment_date=i.payment_date,agent_username=i.agent_username,city=i.city,disposition=i.disposition,sub_dispossitions=i.sub_dispossitions,mode=i.mode,transactionid_chequeno=i.transactionid_chequeno,cash=i.cash,schedule=i.schedule,field_branch=i.field_branch,datetime=i.datetime,callbacktime=i.callbacktime,amount=i.amount,remark=i.remark,contacted_DateTime=i.contacted_DateTime,created_by=i.created_by,caller_name=i.callername,loanamt=i.loanamt,lastdial=i.lastdial,emidate1=emidate1,emidate2=emidate2,emidate3=emidate3,emidate4=emidate4,amount1=emiamt1,amount2=emiamt2,amount3=emiamt3,amount4=emiamt4,emi=emino,personalForkey_id=id,list_id=i.list_id_id,campaign=camp)
                
            except Exception as e:
                print(e)

            pers = LogData.objects.filter(personalForkey_id=id)
            personaldetails.objects.update(what="")
        return render(request,"incomingcms.html",{"info":info,"contacted":contacted,"noncontacted":noncontacted,"p":p})

    else:
         personaldetails.objects.update(what="oncall")
         if request.method=="POST":
            name=request.POST.get("name")
            lan=request.POST.get("lan")
            disval=request.POST.get("dispositionvalue")
            subval=request.POST.get("subdispositionvalue")
            remark=request.POST.get("remark")
            p=request.GET["phone_number"]
            add=IncomingDetails.objects.create(name=name,mobile=p,accountno=lan,disposition=disval,sub_disposition=subval,remark=remark)
            add.save()
            personaldetails.objects.update(what="")
         return render(request,"unknown.html",{"info":info,"p":p})
    



@login_required(login_url='login')
def test(request):
    db=dbconnection()
    cur=db.cursor()
    p=f'select * from recording_log'
    cur.execute(p)
    b=cur.fetchall()
    stat=[]
    for i in b:
        agentstatus=i
        if agentstatus==('PAUSED',):
            personaldetails.objects.update(what="oncall")
        else:
            personaldetails.objects.update(what="")
    if request.method=="POST":
        print("hello")
        username=request.POST.get("user")
        password=request.POST.get("pass")
        print(username,password)
        cur.execute("select *  from  vicidial_users where user='{username}' and pass='{password}'")
        r=cur.fetchall()
        
    return render(request,'test.html',{"api":"api"}) 


def dialcal(request):
    if request.method == 'POST':
        number = request.POST.get("dialnum3")
        print("numberrrrrrrrrrrrrrrrr",number)
        name = request.user.username
        print(name)
        url = f'http://{apilink}/agc/api.php?source=test&user=6666&pass=robust&agent_user={name}&function=external_dial&value={number}&phone_code=1&search=YES&preview=NO&focus=YES'
        g_url = requests.get(url)
        print(g_url)
        r=g_url.text
        print(g_url.text)
        if 'ERROR' in r:
            return JsonResponse({'status':300,"msg":r})
        elif 'SUCCESS' in r:
            return JsonResponse({'status':200})

        return JsonResponse({'status':202})

    return JsonResponse({'r': 'r'})

def  disconnectcall(request):
    if request.method == 'POST':
        number = request.POST.get("dialnum3")
        print(number)
        name = request.user.username
        print('Name',name)
        url = f'http://{apilink}/agc/api.php?source=test&user=6666&pass=robust&agent_user={name}&function=external_hangup&value=1'
        g_url = requests.get(url)
        print(g_url)
        return JsonResponse({'status':400})


def testworking(request):
    if request.method =="POST":
            grp=''
            username=request.POST.get('name')
       
            o=User.objects.filter(username=username)
        
            for i in o:
                grp=i.usergroup

            u=user_group.objects.filter(usergroup=grp)
          
            for i in u:
                ac=i.allowed_campaigns
                grp=ac.rstrip(ac[-1])
        
            grp=grp.strip()

            a = grp.split(" ")

            if "-ALL-CAMPAIGNS-" in a :
                c=campaign.objects.all()
            else:
                c=campaign.objects.filter(campaign_id__in=a)
       
            campname=''
            for i in c:
                campname=i.campaign_name

    return JsonResponse({'campaigns':list(c.values())})


def  dispose(request):
    print("dispose")
    if request.method == 'POST':
        name = request.user.username
        dispos = request.POST.get('dispos')
        callscheduletime=request.POST.get("checks")
        schedule=request.POST.get("schedule")
        dt = datetime.now()
        am = dt + timedelta(minutes=0)
        if callscheduletime == "15min":
            am = dt + timedelta(minutes=15)
        elif callscheduletime == "30min":
            am = dt + timedelta(minutes=30)
        elif callscheduletime == "45min":
            am = dt + timedelta(minutes=45)
        elif callscheduletime == "1hr":
            am = dt + timedelta(minutes=60)

        ft= am.strftime("%Y-%m-%d %H:%M:%S")
       
        if dispos == 'Paid':
            dispos = 'paid'
        elif dispos == 'Promise to Pay':
            dispos = 'PTP'
        elif dispos == 'Call Back':
            dispos = 'CBK'
      
            print("call back time")
            url=f"http://{apilink}/agc/api.php?source=test&user=6666&pass=robust&agent_user={name}&function=external_status&value=CBK&callback_datetime={ft}&callback_type=USERONLY&callback_comments=callback+comments+go+here&qm_dispo_code={dispos}"
            g_url = requests.get(url)
            return JsonResponse({'status':200})

        elif dispos == 'Schedule Call':
            dispos = 'SCBK'
            print("scheduleeeeeeeeeeeeeeeeeeeeee",schedule)
            #url=f"http://{apilink}/agc/api.php?source=test&user=6666&pass=robust&agent_user={name}&function=external_status&value=SCBK&callback_datetime={schedule}&callback_type=USERONLY&callback_comments=callback+comments+go+here&qm_dispo_code=SCBK"
            url=f"http://{apilink}/agc/api.php?source=test&user=6666&pass=robust&agent_user={name}&function=external_status&value=SCBK&callback_datetime={schedule}&callback_type=USERONLY&callback_comments=callback+comments+go+here&qm_dispo_code={dispos}"
            g_url = requests.get(url)
            return JsonResponse({'status':200})


        elif dispos == 'OTS Request':
            dispos = 'OTS'
        elif dispos == 'Settlement':
            dispos = 'SETTEL'
        elif dispos == 'Send FE To Collect':
            dispos = 'SFTCOL'
        elif dispos == 'Broken Promise ':
            dispos = 'BPTP'
        elif dispos == 'Refuesd To Pay':
            dispos = 'RTP'

        elif dispos == 'No-recall':
            dispos = 'nocall'
        elif dispos == 'Ringing No Response':
            dispos = 'RNR'
        
        elif dispos == 'Switch OFF':
            dispos = 'SOFF'
        elif dispos == 'Wrong Contact':
            dispos = 'WCN'
        elif dispos == 'Not Available':
            dispos = 'NOTAVL'
        elif dispos == 'Language Not Communicale':
            dispos = 'LNC'
        elif dispos == 'Fake Number':
            dispos = 'FN'
        elif dispos == 'Exsisting Customer':
            dispos = 'EXC'
        url = f'http://{apilink}/agc/api.php?source=test&user=6666&pass=robust&agent_user={name}&function=external_status&value={dispos}'
        g_url = requests.get(url)
        # print(g_url)
        return JsonResponse({'status':800})



@login_required(login_url='login')
def home(request):
    return redirect('dashboard')


def qsdash(request):
    return render(request,"qsdash.html")

@login_required(login_url='login')
def teamoverall(request):
    value = notificationCount(request)
    return render(request,"teamoverall.html",{"value":value})


@login_required(login_url='login')
def display(request):
    if request.method=="POST":
        rval=request.POST.get("custom-radio-btn")
    return render(request,"display.html")

@login_required(login_url='login')
def dashtl(request):
    if request.user.user_level== 9:
        return render(request,'dashtl.html')
    elif request.user.user_level== 1:
        return redirect('dashboard')


@login_required(login_url='login')
def dashtlots(request):
    data=otsdata.objects.all().order_by("tlstat")
    if request.user.user_level== 9:
        return render(request,'dashtlots.html',{"data":data})
    elif request.user_level== 1:
        return redirect('dashboard')

@login_required(login_url='login')
def logoutuser(request):
    dt = datetime.now()
    LoginHistory.objects.create(username=request.user.username,logdt=dt,event="LOGOUT")   
    logout(request)
    return redirect('login')

def userajax(request):
    db = dbconnection()
    cur=db.cursor()
    query = f"SELECT user,pass,user_level,user_group FROM vicidial_users"
    cur.execute(query)  
    r = cur.fetchall()
    
    try:
    	for i in r:

            if User.objects.filter(username= i[0]).exists():
                    a = User.objects.get(username= i[0])
                    a.username = i[0]
                    a.set_password(i[1])
                    a.user_level=i[2]
                    a.usergroup=i[3]
                    #a.save()
            else:
                    obj = User.objects.create_user(username=i[0],password=i[1],user_level=i[2],usergroup=i[3])
                    obj.save()
           
       
    except Exception as e:
            print(e)

    return JsonResponse({'status':200})


def loginuser(request):
    db = dbconnection()
    cur=db.cursor()
    us=User.objects.all()
    print("total",us)
    query2 = f"SELECT campaign_id,campaign_name FROM vicidial_campaigns"
    cur.execute(query2)
    camp =  cur.fetchall()

    campn=[]
    campid = []
    campname = []
    for i in camp:
        campid.append(i[0])
        campname.append(i[1])
        if campaign.objects.filter(campaign_id=i[0]).exists():
            pass
        else:
            campaign.objects.create(campaign_id=i[0],campaign_name=i[1])

        
          
    p=f'select user_group,allowed_campaigns from vicidial_user_groups'
    cur.execute(p)
    b = cur.fetchall()
   
   
    for i in b:
        
        if user_group.objects.filter(usergroup=i[0]).exists():
            user_group.objects.filter(usergroup=i[0]).update(allowed_campaigns=i[1])
            
        else:
            usergroup=user_group.objects.create(usergroup=i[0],allowed_campaigns=i[1])
            usergroup.save()
    
    ug = user_group.objects.filter(usergroup=i[1])

    
  
    cur.close()
    db.close()
	
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            campaigns = request.POST.get('campaign_sel')
            entry=datetime.now()
            print(1,username,2,password,3,campaigns)
            request.session['userid'] = request.user.id
        
            try:
                user = authenticate(request,username=username,password=password,campaign=campaigns)
                u=User.objects.filter(username=username).update(campaign=campaigns)
                
                if user is not None and user.user_level== 1:
                    login(request,user)
                    print('login')
                    LoginHistory.objects.create(username=username,logdt=entry,event="LOGIN")
                    return redirect('dashboard')

                elif user is not None and user.user_level== 9:
            
                    login(request,user)
                    LoginHistory.objects.create(username=username,logdt=entry,event="LOGIN")
                    return redirect('dashboard')
                
                elif user is not None and user.user_level == 5:
                    login(request,user)
                    return redirect("qsdash")
                else:
                    messages.error(request,"Incorrect username or password")
            except Exception as e:
                messages.warning(request,"Something went wrong")
                print('error',e)

    return render(request,'login.html',{'campname':campname})



@login_required(login_url="login")
def dashboard(request):
    value = notificationCount(request)
    data=otsdata.objects.all()
    
    return render(request,"dashboard.html",{"data":data})
  
@login_required(login_url="login")
def tlcms(request,id):
    pers=LogData.objects.filter(personalForkey=id)	
    info=personaldetails.objects.filter(id=id)
    otsd = otsdata.objects.filter(info_id=id)
    otsamt = 0
    try:
        for i in otsd:
            otsamt = i.ots_amt
    except:
        otsamt = 0


    if request.method=="POST":
        otsamt=request.POST.get("otsamt")
        per = request.POST.get('percentage')
        status=request.POST.get("status")
        remark=request.POST.get("remark")
        dt=datetime.now()
        print(otsamt,per,status)
        if status=="Accepted":
            otsdata.objects.filter(info_id=id).update(suggest=otsamt,tlstat=status,tlstatdate=dt,remark=remark)
        else:
            otsdata.objects.filter(info_id=id).update(suggest=otsamt,otspercentage=per,tlstat=status,tlstatdate=dt,remark=remark)
        return redirect("dashtlots")


    return render(request,"tlcms.html",{"info":info,'otsamt':otsamt,"pers":pers})

@login_required(login_url="login")
def cms(request,id):
    db=dbconnection()
    cur=db.cursor()
    q= f"select distinct category,status_name from vicidial_campaign_statuses where status_name!='Exsisting Customer' and status_name != 'Fake Number'"

    
    
    cur.execute(q)
    sub =  cur.fetchall()
    
    contacted = []
    noncontacted = []

    for i in sub:
        if i[0] == 'contacted':
            contacted.append(i[1])
        else:
            noncontacted.append(i[1])

    

    print(contacted)
    print(noncontacted)
    pers = LogData.objects.filter(personalForkey_id=id)
    print(len(pers))
    if len(pers) == 0:
        print("inside if")
        show=False
    else:
        print("else")
        show=True
    
    print(show,"status")
    
    try:
        #url = requests.get('http://10.65.94.241/agc/api.php?source=test&user=6666&pass=robust&agent_user=IIT&function=external_dial&value=7972861253&phone_code=1&search=YES&preview=NO&focus=YES')
        url=""
    except Exception as e:
        print(e)
    mode=''
    field=''
    disval=''
    info=personaldetails.objects.filter(id=id)
    for i in info:
        what=i.what
    a=Additional.objects.filter(debtor_id_id=id)
    obj = Additional.objects.filter(debtor_id_id=id)
    flag=False
    em = False
    con = False
    add = False
    altno= False
    for i in obj:
        flag= True
        print(i)
        if i.contactnum != "":
            con = True
        if i.email != "":
            em = True
        if i.address != "":
            add = True
    for i in info:
        if i.alt_mno_1 != "None":
            altno = True
    cur.close()
    db.close()
    if request.method=="POST":
        disval=request.POST.get("dispositionvalue")
        subval=request.POST.get("subdispositionvalue")
        dail=request.POST.get("dialnum3")
       
        mode=request.POST.get("radio-group")
        cash=request.POST.get('cashtype')
        trans_cheq1=request.POST.get("trans1")
        trans_cheq2=request.POST.get("trans2")
        field=request.POST.get("field_branch")
        ptpamt=request.POST.get("ptpamt")
        ptpdate=request.POST.get("ptpdate")
        paidamt=request.POST.get("paidamt")
        callscheduletime=request.POST.get("checks[]")
        schedule=request.POST.get("scheduledate")
        remarkall=request.POST.get("remark")
        emino=request.POST.get("settle")
        emiamt1=request.POST.get("emiamt1")
        emiamt2=request.POST.get("emiamt2")
        emiamt3=request.POST.get("emiamt3")
        emiamt4=request.POST.get("emiamt4")
        emidate1=request.POST.get("emidate1")
        emidate2=request.POST.get("emidate2")
        emidate3=request.POST.get("emidate3")
        emidate4=request.POST.get("emidate4")
        otsamt=request.POST.get("otsamt")
        otspercent=request.POST.get("tospercent")
        area=request.POST.get("sarea")
        address=request.POST.get("saddress")
        land=request.POST.get("slandmark")
        pin=request.POST.get("spincode")
        modeofpay=request.POST.get("femode")
        time=request.POST.get("stime")
        sendate=request.POST.get("sdate")
        amt=request.POST.get("amt")
        dt=datetime.now()
        nowdate=dt.now().date() 
 
        
        try:
            cash = int(cash)
        except:
            cash = None
        
        try:
            ptpamt = int(ptpamt)
        except:
            ptpamt = None

        bn=personaldetails.objects.filter(id=id).values('borrowor_name') 
        loanid=personaldetails.objects.filter(id=id).values('bank_loan_accountno')
        TOS=personaldetails.objects.filter(id=id).values('TOS') 

        
        trans_cheq = ""
        if trans_cheq1 != "":
            trans_cheq = trans_cheq1
        elif trans_cheq2 != "":
            trans_cheq = trans_cheq2
        
        date = ''
        if ptpdate != "":
             date = ptpdate
        elif schedule!= "":
            date= schedule

      

        dt = datetime.now()
        am = dt + timedelta(minutes=0)

        # print(type(am))
        if callscheduletime == "15min":
            am = dt + timedelta(minutes=15)
        elif callscheduletime == "30min":
            am = dt + timedelta(minutes=30)
        elif callscheduletime == "45min":
            am = dt + timedelta(minutes=45)
        elif callscheduletime == "1hr":
            am = dt + timedelta(minutes=60)

        ft= am.strftime("%Y-%m-%d %H:%M:%S")
        if paidamt == "":
            paidamt = None
        if disval != "" or subval != "" or mode != " " or trans_cheq != "" or cash != "" or ptpamt !="" or date==''   or schedule != "" or remarkall !="" :
           
            add=personaldetails.objects.filter(id=id).update(disposition=disval,sub_dispossitions=subval,mode=mode,transactionid_chequeno=trans_cheq,cash=paidamt,lastdial=dail,amount=ptpamt,remark=remarkall,user_id=request.user.id,callername=request.user.username,contacted_DateTime=dt,attempted=F("attempted") + 1)

            if date!="":
                add=personaldetails.objects.filter(id=id).update(disposition=disval,sub_dispossitions=subval,callbacktime=date,user_id=request.user.id,contacted_DateTime=dt,callername=request.user.username,attempted=F("attempted") + 1)
       
        if callscheduletime != None:
            up=personaldetails.objects.filter(id=id).update(callbacktime=ft,user_id=request.user.id,callername=request.user.username,contacted_DateTime=dt,attempted=F("attempted") + 1)

        if otsamt!= "":
            otsexists = otsdata.objects.filter(info_id=id)
            if otsexists:
                otsinfo=otsdata.objects.update(ots_amt=otsamt,remark=remarkall,borrower_name=bn,loan_id=loanid,otspercentage=otspercent,tos=TOS,info_id=id,callername=request.user.username)
            else:
                otsinfo=otsdata.objects.create(ots_amt=otsamt,remark=remarkall,otspercentage=otspercent,borrower_name=bn,loan_id=loanid,tos=TOS,info_id=id,callername=request.user.username)
                otsinfo.save()


        if schedule !=None and schedule!="":
            up=personaldetails.objects.filter(id=id).update(callbacktime=schedule,user_id=request.user.id,callername=request.user.username,contacted_DateTime=dt,attempted=F("attempted") + 1)
        try:
            if  emidate1=="" or emiamt1 == '':
                emiamt1 = 0
                emidate1 = None
            if  emidate2=="" or emiamt2 == '':
                emiamt2 = 0
                emidate2 = None
            if  emidate3=="" or emiamt3 == '':
                emiamt3 = 0
                emidate3 = None
            if  emidate4=="" or emiamt4 == '':
                emiamt4 = 0
                emidate4 = None

            print(emiamt1,emiamt2,emiamt3,emiamt4)
            print(emidate1,emidate2,emidate3,emidate4)
            if  emidate1!=None or emidate2!=None or emidate3!=None or emidate4!=None:
                e=emi.objects.create(emidate1=emidate1,emidate2=emidate2,emidate3=emidate3,emidate4=emidate4,amount1=emiamt1,amount2=emiamt2,amount3=emiamt3,amount4=emiamt4,refrence_id=id,emi=emino)
        
        except Exception as e:
             print(e)
            
        #  main code running for sendfe
        if address != "" or area != "" or land!= '' or pin != '' or modeofpay != "" or time !=None or sendate != '' or  amt !=None  :
            print(1,address,2,area,3,land,4,pin,5,modeofpay,6,time,7,sendate,8,amt)
            print(sendate)
            fedata=sendfeto.objects.create(address=address,area=area,pincode=pin,landmark=land,fe_datetime=sendate,amount=amt,modeofpay=modeofpay,client_id=id,user_id=request.user.username,contacted_datetime=dt)
            fedata.save()
        
        try:
            camp=""
            a=personaldetails.objects.filter(id=id)
            u=User.objects.filter(username=request.user.username)

            for i in u:
                camp=i.campaign
                print(camp)
            for i in a :
                # if i.bank_loan_accountno == 'nan':
                #     i.bank_loan_accountno = None
                
                b = LogData.objects.create(borrowor_name=i.borrowor_name,mobile_number=i.mobile_number,address=i.address,state=i.state,pincode=i.pincode,dateofbirth=i.dateofbirth,email_id=i.email_id,phone_number=i.phone_number,bankname=i.bankname,trustname=i.trustname,systemlan=i.systemlan,bank_loan_accountno=i.bank_loan_accountno,branchname=i.branchname,bankstate=i.bankstate,nature_of_facility=i.nature_of_facility,sanctionamount=i.sanctionamount,loan_sanction_date=i.loan_sanction_date,NPA_Date=i.NPA_Date,interest_rate=i.interest_rate,account_status=i.account_status,security_value=i.security_value,document_custody=i.document_custody,security_flag=i.security_flag,current_allocation=i.current_allocation,current_allocation_date=i.current_allocation_date,team_leader=i.team_leader,zone_name=i.zone_name,branch_mail_id=i.branch_mail_id,branch_contact_details=i.branch_contact_details,total_collected_amount=i.total_collected_amount,balance_POS_amount=i.balance_POS_amount,TOS=i.TOS,TOS_as_on_Date=i.TOS_as_on_Date,next_action_date=i.next_action_date,current_principal_outstanding=i.current_principal_outstanding,payment_date=i.payment_date,agent_username=i.agent_username,city=i.city,disposition=i.disposition,sub_dispossitions=i.sub_dispossitions,mode=i.mode,transactionid_chequeno=i.transactionid_chequeno,cash=i.cash,schedule=i.schedule,field_branch=i.field_branch,datetime=i.datetime,callbacktime=i.callbacktime,amount=i.amount,remark=i.remark,contacted_DateTime=i.contacted_DateTime,created_by=i.created_by,caller_name=i.callername,loanamt=i.loanamt,lastdial=i.lastdial,personalForkey_id=id,list_id=i.list_id_id,campaign=camp,additional_number=i.additional_number,additional_address=i.additional_address,additional_emailid=i.additional_emailid)
                if  emidate1!=None or emidate2!=None or emidate3!=None or emidate4!=None:
                    b = LogData.objects.create(borrowor_name=i.borrowor_name,mobile_number=i.mobile_number,address=i.address,state=i.state,pincode=i.pincode,dateofbirth=i.dateofbirth,email_id=i.email_id,phone_number=i.phone_number,bankname=i.bankname,trustname=i.trustname,systemlan=i.systemlan,bank_loan_accountno=i.bank_loan_accountno,branchname=i.branchname,bankstate=i.bankstate,nature_of_facility=i.nature_of_facility,sanctionamount=i.sanctionamount,loan_sanction_date=i.loan_sanction_date,NPA_Date=i.NPA_Date,interest_rate=i.interest_rate,account_status=i.account_status,security_value=i.security_value,document_custody=i.document_custody,security_flag=i.security_flag,current_allocation=i.current_allocation,current_allocation_date=i.current_allocation_date,team_leader=i.team_leader,zone_name=i.zone_name,branch_mail_id=i.branch_mail_id,branch_contact_details=i.branch_contact_details,total_collected_amount=i.total_collected_amount,balance_POS_amount=i.balance_POS_amount,TOS=i.TOS,TOS_as_on_Date=i.TOS_as_on_Date,next_action_date=i.next_action_date,current_principal_outstanding=i.current_principal_outstanding,payment_date=i.payment_date,agent_username=i.agent_username,city=i.city,disposition=i.disposition,sub_dispossitions=i.sub_dispossitions,mode=i.mode,transactionid_chequeno=i.transactionid_chequeno,cash=i.cash,schedule=i.schedule,field_branch=i.field_branch,datetime=i.datetime,callbacktime=i.callbacktime,amount=i.amount,remark=i.remark,contacted_DateTime=i.contacted_DateTime,created_by=i.created_by,caller_name=i.callername,loanamt=i.loanamt,lastdial=i.lastdial,emidate1=emidate1,emidate2=emidate2,emidate3=emidate3,emidate4=emidate4,amount1=emiamt1,amount2=emiamt2,amount3=emiamt3,amount4=emiamt4,emi=emino,personalForkey_id=id,list_id=i.list_id_id,campaign=camp,additional_number=i.additional_number,additional_address=i.additional_address,additional_emailid=i.additional_emailid)
              
        except Exception as e:
            print(e)

    
    personaldetails.objects.update(what="")

    return render(request,"cms.html",{"info":info,"a":a,"show":show,"flag":flag,"em":em,"con":con,"altno":altno,"add":add,"mode":mode,"field":field,'pers':pers,"contacted":contacted,"noncontacted":noncontacted,"what":what})


@login_required(login_url="login")
def tlcmsresponse(request):
     all_data =personaldetails.objects.all()
     return JsonResponse({'all_data':list(all_data.values())})

@login_required(login_url="login")
def noncontacted(request):
    value = notificationCount(request)
    data=personaldetails.objects.filter(callername=request.user.username).filter(attempted=0)
    return render(request,"noncontacted.html",{"data":data,"value":value})

@login_required(login_url="login")
def search(request):
    return render(request,"search.html")

def searchajax(request):
    if request.method == 'POST':
        given_name=request.POST.get('borrowor_name')
        given_phone=request.POST.get("mobile_number")
        given_loan=request.POST.get("loan_id")
        print(given_name)
        print(given_phone)
        print(given_loan)
        if given_name == None or given_phone == None or given_loan == None:
            given_name = ""
            given_loan = ""
            given_phone = ""
        
        try:
            add = Additional.objects.values_list('debtor_id',flat=True).get(contactnum=given_phone)
        except:
            add = None
            if add == 0:
                add = None
        try:
            if request.user.user_level == 9:
                per=personaldetails.objects
            else:
                per=personaldetails.objects.filter(callername=request.user.username)[:100]
            
            if given_name != "":
                per=per.filter(borrowor_name__icontains=given_name)[:100]
            elif given_phone != "":
                per=per.filter(Q(mobile_number__icontains=given_phone) | Q(id = add) | Q(alt_mno_1__icontains=given_phone) | Q(alt_mno_2__icontains=given_phone)  | Q(alt_mno_3__icontains=given_phone))[:100]
            elif given_loan != "":
                per=per.filter(bank_loan_accountno__icontains=given_loan)[:100]

            if given_name  == "" and given_phone == "" and given_loan == "":
                per=personaldetails.objects.filter(id__isnull=True)[:100]
     
            return JsonResponse({"status":200,'all_data':list(per.values())})
        except Exception as e:
            print(e)
            return JsonResponse({'status':300})

    
    return JsonResponse({'status':400})



@login_required(login_url="login")
def Reminder(request):
    value = notificationCount(request)
    data=personaldetails.objects.filter(Q(sub_dispossitions='Promise To Pay') | Q(sub_dispossitions='Call Back')| Q(sub_dispossitions='Schedule Call'))
   
    if request.method=="POST":
        boxval=request.POST.get("checks[]")
       
    return render(request,"Remainder.html",{"data":data,"value":value})

@login_required(login_url="login")
def ots(request):
    value = notificationCount(request)
    selectots=request.POST.get("selectval")
    o=otsdata.objects.all().order_by("-tlstatdate")
   
    return render(request,"ots.html",{"o":o,"value":value})

@login_required(login_url="login")
def recovery(request):
    value = notificationCount(request)
    return render(request,"Recoverystatus.html",{"value":value})

@login_required(login_url="login")
def SendtoFE(request):
    value = notificationCount(request)
    data=sendfeto.objects.all()
    return render(request,'sendToFe.html',{'data':data,"value":value})

@login_required(login_url="login")
def add(request):
    form=additionalForm(request.POST)
    if request.method=="POST":
            print(request.POST)
            if form.is_valid(): 
                form=additionalForm(request.POST)
                form.save()
                return redirect('/c')
    return render(request,"cms.html")


def additional(request):
    if request.method=="POST":
        email=request.POST.get('email')
        contactnum=request.POST.get('contactnum')
        relation=request.POST.get('relation')
        address=request.POST.get('address')
        state=request.POST.get('state')
        city=request.POST.get('city')
        forid=request.POST.get("additional")
        landmark=request.POST.get('landmark')
        pincode=request.POST.get('pincode')
        print(email,contactnum,"Relation",relation,address,state,city)
        if address == None:
            address = ""

        addr = address + " " + state + " " + city + " " + landmark + " " + pincode
        pdid = personaldetails.objects.get(id=forid)
        try:
            if contactnum != "":
                personaldetails.objects.filter(id=forid).update(additional_number=contactnum)
        
            if len(address) != 0:
                personaldetails.objects.filter(id=forid).update(additional_address=addr)
            
            if len(email) != 0:
                personaldetails.objects.filter(id=forid).update(additional_emailid=email)


        except Exception as e:
            print(e)
        d=Additional.objects.create(debtor_id=pdid,email=email,contactnum=contactnum,relation=relation,address=address,state=state,city=city,landmark=landmark,pincode=pincode)
        d.save()
        return HttpResponse()

def connect(request):
    value = notificationCount(request)
    return render(request,"connectto.html",{"value":value})

@login_required(login_url="login")
def sendfetagging(request,id):
    info=personaldetails.objects.filter(id=id)
    if request.method=='POST':
        otsselect=request.post.get('selectval')
        otsdate=request.post.get('otsdate')
        otsamt=request.post.get('otsamt')

    return render(request,"fetagging.html",{"info":info})

# @login_required(login_url="login")
def upload(request):
    db=dbconnection()
    cur=db.cursor()


    if request.method == 'POST':
        campion=request.POST.get('campion')
        listname = request.POST.get('listname')
        listid = request.POST.get('listid')
        file = request.FILES.get('listfile')
        entry=datetime.now()
        user = request.user.username
       
   
        # url=f"http://{apilink}/vicidial/non_agent_api.php?source=test&function=add_list&user={user}&pass=robust&list_id={listid}&list_name={listname}&active=Y&campaign_id={campion}"
        # g_url = requests.get(url)
        # a=f"{listid},{listname}"
        # print(a)
        # p=f"INSERT INTO asterisk.vicidial_lists(list_id,list_name,campaign_id,active,list_description,list_changedate) VALUES('{listid}','{listname}','{campion}','Y','{campion}','{entry}')"
        # cur.execute(p)
      
        try:
            form = Dataupload(listid=listid,listname=listname,file=file,campion=campion,entry=entry)
            form.save()
            csv_file_path = Dataupload.objects.filter(listid=listid)
            for i in csv_file_path:   
                csv_file = i.file.url
                id=i.id
                print("iddddddddddddddddddddddd",id)
            path = f'{settings.BASE_DIR}{csv_file}'
            df = pd.read_csv(path, dtype={"Bank Loan Account No.":"string","SystemLan":"string"},encoding='cp1252')
            count = len(df.values)
            print(count)
            Dataupload.objects.filter(listid=listid).update(count=count)
            for i in  (df.values.tolist()):
                # print("before conversion",i[1])
                print(i[5],i[16],i[17],i[24],i[32])
                dbd = str(i[5])
                print(type(i[1]))
                mbno=str(i[1])
                mbno=mbno.replace(".0","")
                print("finallllllly",mbno)
                phno=str(i[7])
                phno=phno.replace(".0","")
                pin=str(i[4])
                pin=pin.replace(".0","")
                print("after conversion",mbno,len(mbno))
                try:
                    dbd = datetime.strptime(dbd,'%Y-%m-%d')
                    dbd = dbd.strftime("%Y-%m-%d")
                except Exception as e:
                    print(e)
                    dbd = None
                lpd = str(i[16])
                try:
                    lpd = datetime.strptime(lpd,'%Y-%m-%d')
                    lpd = lpd.strftime("%Y-%m-%d")
                except Exception as e:
                    print(e)
                    lpd = None

                pdd = str(i[17])
                try:
                    pdd = datetime.strptime(pdd,'%Y-%m-%d')
                    pdd = pdd.strftime("%Y-%m-%d")
         
                except Exception as e:
                    print(e)
                    pdd = None

                dt = str(i[24])
                try:
                    dt = datetime.strptime(dt,'%Y-%m-%d')
                    dt = dt.strftime("%Y-%m-%d")

                except Exception as e:
                    print(e)
                    dt = None

                ddt = str(i[32])
                try:
                    ddt = datetime.strptime(dt,'%Y-%m-%d')
                    ddt = ddt.strftime("%Y-%m-%d")
         
                except Exception as e:
                    print(e)
                    ddt = None
                if str(i[15]) == 'nan'  or str(i[15]) =='' or ' ' in str(i[15]):
                    i[15] = 0

                if str(i[29]) == 'nan'  or str(i[29]) =='' or ' ' in str(i[29]):
                    i[29] = 0

                if str(i[30]) == 'nan'  or str(i[30]) =='' or ' ' in str(i[30]) :
                    i[30] = 0

                if str(i[31]) == 'nan'  or str(i[31]) =='' or ' ' in str(i[31]) :
                    i[31] = 0
                 
                if str(i[33]) == 'nan' or str(i[33])=='' or ' ' in str(i[33]) :
                    i[33] = 0
                
                
                
                
                
                obj=personaldetails.objects.create(borrowor_name=i[0],mobile_number=mbno,address=i[2],state=i[3],pincode=pin,dateofbirth=dbd,email_id=i[6],phone_number=phno,bankname=i[8],trustname=i[9],systemlan=i[10],bank_loan_accountno=i[11],branchname=i[12],bankstate=i[13],nature_of_facility=i[14],sanctionamount=i[15],loan_sanction_date=lpd,NPA_Date=pdd,interest_rate=i[18],account_status=i[19],security_value=i[20],document_custody=i[21],security_flag=i[22],current_allocation=i[23],current_allocation_date=dt,team_leader=i[25],zone_name=i[26],branch_mail_id=i[27],branch_contact_details=i[28],total_collected_amount=i[29],balance_POS_amount=i[30],TOS=i[31],TOS_as_on_Date=ddt,current_principal_outstanding=i[33],callername=i[34],alt_mno_1=i[35],alt_mno_2=i[36],alt_mno_3=i[37],list_id_id=id)
                obj.save() 
                # print("after saving",lpd,dbd,ddt,pdd,dt)
                # query2 = f"INSERT INTO vicidial_list(first_name,status,list_id,gmt_offset_now,called_since_last_reset,phone_code,phone_number,called_count,rank,entry_list_id, address1, address2) VALUES({i[0]},'NEW',{listid},'-4.00','N','1',{i[1]},'0','0','0',{i[11]}, {i[2]});"

                # url=f"http://{apilink}/vicidial/non_agent_api.php?source=test&user={user}&pass=robust&function=add_lead&phone_number={i[7]}&phone_code=1&list_id={listid}&dnc_check=N&first_name={i[0]}"
                # g_url = requests.get(url)
                # q=f"INSERT INTO vicidial_list(entry_date,status,list_id,gmt_offset_now,called_since_last_reset,phone_code,phone_number,called_count,rank,entry_list_id) VALUES('{entry}','NEW','{listid}','-4.00','N','1','{mbno}','0','0','0')"
                # cur.execute(q)
               

            db.close()
            return JsonResponse({'status':200})
        except Exception as e:
            print("error msg",e)
            return JsonResponse({'status':400})
    form = DataUploadForm
    read = Dataupload.objects.all()

    return JsonResponse({"status":300})


@login_required(login_url="login")
def dataupload(request):
    # db=dbconnection()
    # cur=db.cursor()
    # query2 = f"SELECT campaign_id,campaign_name FROM vicidial_campaigns"
    # cur.execute(query2)
    # camp =  cur.fetchall()
    # campn=[]
    # campid = []
    # campname = []
    # for i in camp:
    #     campid.append(i[0])
    #     campname.append(i[1])
    # db.close()    
    camp=campaign.objects.all()
    read = Dataupload.objects.all()
    form = DataUploadForm
    context = {'form':form,'read':read,'campname':"campname","camp":camp}
    return render(request,'upload.html',context)


    
@login_required(login_url="login")
def filterrm(request):
    value = notificationCount(request)
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    all_data=personaldetails.objects.filter(callername=request.user.username).filter(callbacktime__contains=d4).filter(Q(sub_dispossitions='Promise To Pay') | Q(sub_dispossitions='Call Back')| Q(sub_dispossitions='Schedule Call'))
    if request.user.user_level == 9:
        all_data=personaldetails.objects.filter(callbacktime__contains=d4).filter(Q(sub_dispossitions='Promise To Pay') | Q(sub_dispossitions='Call Back')| Q(sub_dispossitions='Schedule Call'))
        print("99999999999999",all_data)
    if request.method == "POST":
        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('tdate').rstrip()
        fil = request.POST.get('remfilter')
        fil = fil.split(",")
        sortval = request.POST.get('sortby') 
        try:

            if fd != "" and td != "":
                fd = datetime.strptime(fd,'%d-%m-%Y')
                td = datetime.strptime(td,'%d-%m-%Y')
                td = td + timedelta(days=1)
                fd = fd.strftime("%Y-%m-%d")
                td = td.strftime("%Y-%m-%d")
                if request.user.user_level == 9:
                    all_data=personaldetails.objects.filter(Q(sub_dispossitions='Promise To Pay') | Q(sub_dispossitions='Call Back')| Q(sub_dispossitions='Schedule Call'))			
                else:
                    all_data = personaldetails.objects.filter(callername=request.user.username).filter(Q(sub_dispossitions='Promise To Pay') | Q(sub_dispossitions='Call Back')| Q(sub_dispossitions='Schedule Call'))
                all_data = all_data.filter(callbacktime__range=[fd,td])
                print("now",all_data)
            else:
                if request.user.user_level == 9:
                    all_data=personaldetails.objects.filter(callbacktime__contains=d4).filter(Q(sub_dispossitions='Promise To Pay') | Q(sub_dispossitions='Call Back')| Q(sub_dispossitions='Schedule Call'))			
                else:
                    all_data = personaldetails.objects.filter(callbacktime__contains=d4).filter(callername=request.user.username).filter(Q(sub_dispossitions='Promise To Pay') | Q(sub_dispossitions='Call Back')| Q(sub_dispossitions='Schedule Call'))

            if sortval != '':
                if sortval == "ascending":
                    all_data = all_data.order_by('TOS')
                elif sortval == "descending":
                    all_data = all_data.order_by('-TOS')    
            if fil != ['']:
                all_data = all_data.filter(Q(sub_dispossitions__in=fil))
        
        except  Exception as e:
            print(e)
            all_data = personaldetails.objects.all()
    print("all_data",all_data)
    return JsonResponse({'all_data':list(all_data.values())})

def filterrs(request):
    today = datetime.today()
    d4 = today.strftime("%Y-%m-%d")
    all_data=personaldetails.objects.filter(contacted_DateTime__contains=d4).filter(callername=request.user.username).exclude(Q(sub_dispossitions='Schedule Call')|Q(sub_dispossitions='Promise To Pay')|Q(sub_dispossitions='Call Back')|Q(sub_dispossitions='Paid')).exclude(attempted=0)
    if request.user.user_level == 9:
        all_data=personaldetails.objects.filter(contacted_DateTime__contains=d4).exclude(Q(sub_dispossitions='Schedule Call')|Q(sub_dispossitions='Promise To Pay')|Q(sub_dispossitions='Call Back')|Q(sub_dispossitions='Paid')).exclude(attempted=0)

    if request.method == "POST":
        
        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('tdate').rstrip()
        sel = request.POST.get('sortval')
        sel = sel.split(",")
        try:
            if fd != "" and td != "":
                fd = datetime.strptime(fd,'%d-%m-%Y')
                td = datetime.strptime(td,'%d-%m-%Y')
                td = td + timedelta(days=1)
                fd = fd.strftime("%Y-%m-%d")
                td = td.strftime("%Y-%m-%d")
                all_data=personaldetails.objects.filter(callername=request.user.username).exclude(Q(sub_dispossitions='Schedule Call')|Q(sub_dispossitions='Promise To Pay')|Q(sub_dispossitions='Call Back')|Q(sub_dispossitions='Paid')).exclude(attempted=0)
                if request.user.user_level == 9:
                    all_data=personaldetails.objects.exclude(Q(sub_dispossitions='Schedule Call')|Q(sub_dispossitions='Promise To Pay')|Q(sub_dispossitions='Call Back')|Q(sub_dispossitions='Paid')).exclude(attempted=0)

                all_data = all_data.filter(contacted_DateTime__range=[fd,td])
            else:
                all_data=personaldetails.objects.filter(contacted_DateTime__contains=d4).filter(callername=request.user.username).exclude(Q(sub_dispossitions='Schedule Call')|Q(sub_dispossitions='Promise To Pay')|Q(sub_dispossitions='Call Back')|Q(sub_dispossitions='Paid')).exclude(attempted=0)
                if request.user.user_level == 9:
                    all_data=personaldetails.objects.filter(contacted_DateTime__contains=d4).filter(callername=request.user.username).exclude(Q(sub_dispossitions='Schedule Call')|Q(sub_dispossitions='Promise To Pay')|Q(sub_dispossitions='Call Back')|Q(sub_dispossitions='Paid')).exclude(attempted=0)


            if sel != ['']:
                all_data = all_data.filter(Q(sub_dispossitions__in=sel))

        except Exception as e:
            print(e)
    return JsonResponse({'all_data':list(all_data.values())})


@login_required(login_url="login")
def filterots(request):

    all_data =otsdata.objects.filter(callername=request.user.username).order_by("tlstat")
    if request.user.user_level == 9:
        all_data =otsdata.objects.all().order_by("-tlstatdate")

    if request.method == "POST":
        fd = request.POST.get('fdate').rstrip()
        td = request.POST.get('tdate').rstrip()
        sel = request.POST.get('selval')
        sortval = request.POST.get('sortval')
        try:
            all_data =otsdata.objects.filter(callername=request.user.username)
            if request.user.user_level == 9:
                all_data =otsdata.objects.all()	

            if sel != "all" and sel!="":
                all_data=all_data.filter(tlstat=sel)
            elif sel == "all":
                all_data=all_data.all()
            
            if fd != "" and td != "":
                fd = datetime.strptime(fd,'%d-%m-%Y')
                td = datetime.strptime(td,'%d-%m-%Y')
                fd = fd.strftime("%Y-%m-%d")
                td = td.strftime("%Y-%m-%d")
                all_data = all_data.filter(tlstatdate__range=[fd,td])
            if sortval != 'undefined':
                if sortval == "Largest to Smallest":
                    all_data = all_data.order_by('-ots_amt')
                elif sortval == "Oldest to Newest":
                    all_data = all_data.order_by('tlstatdate')
           
        except Exception as e:
            print(e)
            all_data = otsdata.objects.all()
    return JsonResponse({'all_data':list(all_data.values())})
	      
@login_required(login_url="login")
def dataexport(request):
    db=dbconnection()
    cur=db.cursor()
    query2 = f"SELECT campaign_id,campaign_name FROM vicidial_campaigns"
    cur.execute(query2)
    camp =  cur.fetchall()
    campn=[]
    campid = []
    campname = []
    for i in camp:
        campid.append(i[0])
        campname.append(i[1])
    

    print("ID",campid,"Name",campname)
    value = notificationCount(request)
    if request.method == "POST":
        sd = request.POST.get('sdate').rstrip()
        ed = request.POST.get('edate').rstrip()
        sel = request.POST.getlist('remcb')

        read=LogData.objects
        print(sel)
        if sel!="":
            print(sel,"inside if")
            read=read.filter(sub_dispossitions__in=sel)
            print(read)
    

        if sd != "" and ed != "":
            sd = datetime.strptime(sd,'%d-%m-%Y')
            ed= datetime.strptime(ed,'%d-%m-%Y')
            ed = ed + timedelta(days=1)
            sd= sd.strftime("%Y-%m-%d")
            ed= ed.strftime("%Y-%m-%d")
            read=read.filter(contacted_DateTime__range=[sd,ed])

        # for i in read:

            print(i.contacted_DateTime)
        print("YOUR FINAL REPORT",read)
        
        db.close()
        try:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data') 

            row_num = 0

            columns = ["borrowor_name","mobile_number","address","state","pincode","dateofbirth","email_id","phone_number","bankname","trustname","systemlan","bank_loan_accountno","branchname","bankstate","nature_of_facility","sanctionamount","loan_sanction_date","NPA_Date","interest_rate","account_status","security_value","document_custody","security_flag","current_allocation","current_allocation_date","team_leader","zone_name","branch_mail_id","branch_contact_details","total_collected_amount","balance_POS_amount","TOS","TOS_as_on_Date","next_action_date","current_principal_outstanding","payment_date","agent_username","city","disposition","sub_dispossitions","mode","transactionid_chequeno","cash","schedule","field_branch","datetime","callbacktime","remark","contacted_DateTime","created_by","caller_name","Campaign","loanamt","lastdial","ots_amt","ots_tos","otspercentage","tlstat","tlstatdate","suggest","otsremark","emi","emidate1","amount1","emidate2","amount2","emidate3","amount3","emidate4","amount4","emiremark","fe_address","fe_area","fe_landmark","fe_pincode","fe_date","time","amount","modeofpay","Additional Number","Aditional Email","Additional Address"]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num]) # at 0 row 0 column 

            # Sheet body, remaining rows
            
            rows = read.values_list("borrowor_name","mobile_number","address","state","pincode","dateofbirth","email_id","phone_number","bankname","trustname","systemlan","bank_loan_accountno","branchname","bankstate","nature_of_facility","sanctionamount","loan_sanction_date","NPA_Date","interest_rate","account_status","security_value","document_custody","security_flag","current_allocation","current_allocation_date","team_leader","zone_name","branch_mail_id","branch_contact_details","total_collected_amount","balance_POS_amount","TOS","TOS_as_on_Date","next_action_date","current_principal_outstanding","payment_date","agent_username","city","disposition","sub_dispossitions","mode","transactionid_chequeno","cash","schedule","field_branch","datetime","callbacktime","remark","contacted_DateTime","created_by","caller_name","campaign","loanamt","lastdial","ots_amt","ots_tos","otspercentage","tlstat","tlstatdate","suggest","otsremark","emi","emidate1","amount1","emidate2","amount2","emidate3","amount3","emidate4","amount4","emiremark","fe_address","fe_area","fe_landmark","fe_pincode","fe_datetime","amount","modeofpay","additional_number","additional_emailid","additional_address")
            
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]))

            wb.save(response)

            return response

        except Exception as e:
            print(e)

    
    return render(request,"dataexport.html",{"campname":campname})

def listid(request):
    data = Dataupload.objects.all().values('listid')
    return JsonResponse({'status':200,'listid':list(data.values())})



def nonattempted(request):
    value = notificationCount(request)
    data=personaldetails.objects.filter(user_id=request.user.id).filter(attempted=0).exclude(list_id__status__contains="0")[:100]
    u=User.objects.all()
    if request.user.user_level == 9:
        data=personaldetails.objects.filter(attempted=0).exclude(list_id__status__contains="0")[:100]
        if request.method=="POST":
            agent=request.POST.get("agent")
            print("itssssss",agent)
            if agent == "all" and agent !="":
                data=personaldetails.objects.filter(attempted=0)[:100]
            else:
                data=personaldetails.objects.filter(attempted=0).filter(callername=agent)
            return JsonResponse({"data":list(data.values())})


    return render(request,'nonattempted.html',{'data':data,"value":value,"u":u})




def sms(request):
    id=0
    smsid = random.randint(1000,9999)
    s=SMSUpload.objects.all()
    dsb = "none"
    if request.method == 'POST':
        smsty=request.POST.get('smstype')
        file = request.FILES.get('smsfile')

        entry=datetime.now()
        try:
          
            form = SMSUpload(smstype=smsty,file=file,entry=entry,smsid=smsid)
            form.save()
            

            csv_file_path = SMSUpload.objects.filter(smsid=smsid)
            print("smsuploadddddd",csv_file_path)
            for i in csv_file_path:   
                csv_file = i.file.url
                id=i.id
          
            path = f'{settings.BASE_DIR}{csv_file}'
            df = pd.read_csv(path)
        
            count = len(df.values)
            # print('asd',df.values)
            SMSUpload.objects.filter(id=id).update(count=count)

            msgs = ""
            cl = ''
        

            for i in df.values:
                
                if smsty == "Payment Acceptance":
                    
                    try:
                        lpd = str(i[3])
                        lpd = datetime.strptime(lpd,'%Y-%m-%d')
                        lpd = lpd.strftime("%Y-%m-%d")
                       
                    except Exception as e:
                        print(e)
                        lpd = None
                    url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=n7OtTfzmtE6uXFjgMNmQ5g&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={i[0]}&text=We%20are%20in%20receipt%20of%20your%20payment%20amounting%20to%20Rs.%20{i[2]}%20dated%20{lpd}%20in%20your%20loan%20account%20no.%20{i[1]}.%20In%20case%20of%20any%20dispute%20with%20respect%20to%20your%20payment%20please%20contact%20toll-free%20number%201800120757575%20or%20email%20us%20at%20customercare@omkaraarc.com%20with%20your%20loan%20account%20%26%20contact%20details.&route=1&DLTtemplateid=1207165778573635216"
                    g_url = requests.get(url)
                    r=g_url.text
                   
                    a=ast.literal_eval(r.replace("null",'None'))
                    res=a["ErrorMessage"]
                    print("error",a["ErrorMessage"])
                    
                    s=SMSDetails.objects.create(phone_no=i[0],Date=lpd,loan_account_no=i[1],amount=i[2],response=res,smsty=smsty,created_by_id=id,entry=entry)
                    s.save()
                    s=SMSUpload.objects.all()
                    msgs = 'SMS Uploaded Successfully'
                    cl = 'info'
                    dsb = "block"
                elif smsty=="Awareness":
                     print(i)
                     print(i[0])
                     print(i[1])
                     print("aware")
                     url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=n7OtTfzmtE6uXFjgMNmQ5g&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={i[0]}&text=Your%20loan%20account%20number%20{i[1]}%20with%20Fullerton%20{i[1]}%20has%20been%20transferred%20to%20Omkara%20Assets%20Reconstruction%20Private%20Limited%20as%20of%2001.01.21.%20To%20have%20more%20clarity%20contact%20Omkara%20ARC%20on%201800120757575%20or%20email%20us%20at%20customercare@omkaraarc.com%20with%20your%20loan%20account%20%26%20contact%20details&route=1&DLTtemplateid=1207165778558300648"
                     g_url = requests.get(url)
                     r=g_url.text
                     print("its",type(r))
                     a=ast.literal_eval(r.replace("null",'None'))
                     res=a["ErrorMessage"]
                     print("error",a["ErrorMessage"])
                    
                     s=SMSDetails.objects.create(phone_no=i[0],loan_account_no=i[1],response=res,smsty=smsty,created_by_id=id,entry=entry)
                     s.save()
                     print("done phon",i[0])
                     s=SMSUpload.objects.all()
                     msgs = 'SMS Uploaded Successfully'
                     cl = 'info'
                     dsb = "block"
                    
                elif smsty=="Payment Confirmation Agency":
                      print(i[0])
                      print(i[1])
                      print(i[2],i[3],i[4])

                      try:
                        lpd = str(i[3])
                        lpd = datetime.strptime(lpd,'%Y-%m-%d')
                        lpd = lpd.strftime("%Y-%m-%d")
                        print(lpd)
                      except Exception as e:
                        print(e)
                        lpd = None
                      print("pay")
                      url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=n7OtTfzmtE6uXFjgMNmQ5g&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={i[0]}&text=We are in receipt of your payment amounting to Rs. {i[2]} dated {lpd} in your loan account no {i[1]} by our authorised representative from {i[4]}. In case of any dispute with respect to your payment please contact toll-free number 1800120757575 or email us at customercare@omkaraarc.com with your loan account %26 contact details.&route=1&DLTtemplateid=1207165778580107494"
                      g_url = requests.get(url)
                      r=g_url.text
                      print("its",type(r))
                      a=ast.literal_eval(r.replace("null",'None'))
                      res=a["ErrorMessage"]
                      print("error",a["ErrorMessage"])
                      
                      s=SMSDetails.objects.create(phone_no=i[0],Date=lpd,loan_account_no=i[1],amount=i[2],agency_name=i[4],response=res,smsty=smsty,created_by_id=id,entry=entry)
                      s.save()
                     
                      msgs = 'SMS Uploaded Successfully'
                      cl = 'info'
                      dsb = "block"
                      
                    
                elif smsty == "CIBIL":
                      print("cibil")
                      url=f"https://www.smsgatewayhub.com/api/mt/SendSMS?APIKey=n7OtTfzmtE6uXFjgMNmQ5g&senderid=OMARPL&channel=2&DCS=0&flashsms=0&number={i[0]}&text=Your CIBIL will get impacted because of the non-payment of RS. {i[2]} in your loan account no.{i[1]}. You are requested to make the payment to OMKARA ARC against your respective{i[1]}. In case of any query please call our toll-free number 1800120757575 or email us at customercare@omkaraarc.com with your loan account %26 contact details.&route=1&DLTtemplateid=1207165778565465130"
                      g_url = requests.get(url)
                      r=g_url.text
                      print("its",type(r))
                      a=ast.literal_eval(r.replace("null",'None'))
                      res=a["ErrorMessage"]
                      print("error",a["ErrorMessage"])
                      
                      s=SMSDetails.objects.create(phone_no=i[0],loan_account_no=i[1],amount=i[2],response=res,smsty=smsty,created_by_id=id,entry=entry)
                      s.save()
                      s=SMSUpload.objects.all()
                      msgs = 'SMS Uploaded Successfully'
                      cl = 'info'
                      dsb = "block"

           
            
            st=SMSDetails.objects.filter(created_by_id=id).filter(response="Success").count()
            SMSUpload.objects.filter(id=id).update(sent=st)
            s=SMSUpload.objects.all()
            return render(request,"sms.html",{"s":s,'cl':cl,'msg':msgs,'dsb':dsb,"st":st})
        except Exception as e:
            print("error msg",e)
            messages.warning(request,"Something Went Wrong")
    return render(request,"sms.html",{"s":s,"dsb":dsb})


def exportsms(request):
    s=SMSDetails.objects
    if request.method == 'POST':
        seltype=request.POST.get("seltype")
        sd=request.POST.get("sdate").rstrip()
        ed=request.POST.get("edate").rstrip()
        sd = datetime.strptime(sd,'%d-%m-%Y')
        ed= datetime.strptime(ed,'%d-%m-%Y')
        ed = ed + timedelta(days=1)
        sd= sd.strftime("%Y-%m-%d")
        ed= ed.strftime("%Y-%m-%d")
        s=SMSDetails.objects.filter(smsty=seltype).filter(entry__range=[sd,ed])
        print(s)
        try:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data') 

            row_num = 0
            if seltype =="Payment Acceptance":
                columns=["SMS Type","Phone Number","Account No","Date","Response","Entry Date"]
                rows = s.values_list("smsty","phone_no","loan_account_no","Date","response","entry")
            elif seltype =="Awareness":
                columns=["SMS Type","Phone Number","Account No","Response","Entry Date"]
                rows = s.values_list("smsty","phone_no","loan_account_no","response","entry")
            elif seltype =="Payment Confirmation  Agency":
                columns=["SMS Type","Phone Number","Account No","Entry Date","Response"," Date","Amount","Agency Name"]
                rows = s.values_list("smsty","phone_no","loan_account_no","entry","response","Date","amount","agency_name")
            elif seltype =="CIBIL":
                columns=["SMS Type","Phone Number","Account No","Entry Date","Response","Amount"]
                rows = s.values_list("smsty","phone_no","loan_account_no","entry","response","amount")
            else:
                return render(request,"sms.html")
            
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num]) # at 0 row 0 column 
           
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]))

            wb.save(response)
         
            form = SmsUploadForm()
            read = SMSDetails.objects.all()



            return response

        except Exception as e:
            print(e)

    
    return render(request,"sms.html",{"s":s})


def ptp(request):
    u=User.objects.all()
    bnk=[]
    bank=personaldetails.objects.all()
    for i in bank:
        print(i.bankname)
        if i.bankname not in bnk:
            bnk.append(i.bankname)
           
    rem=[]
    log=LogData.objects.filter(sub_dispossitions="Promise To Pay").order_by("personalForkey_id")

    return render(request,"ptp.html",{"log":log,"l":"l","u":u,"rem":rem,"bnk":bnk})

def ptpajax(request):
     
    data=[]
   
    if request.method=="POST":
        agent=request.POST.get("ptpagent")
        bk=request.POST.get('bankname')
        st=request.POST.get("statusn")
        print(agent,bk,st)
        # print("just",log_data)
        log_data=LogData.objects.filter(Q(sub_dispossitions="Promise To Pay")).order_by("personalForkey_id")
        print('asd',agent)
        # if st !="" :
        #     log_data=LogData.objects.filter(sub_dispossitions=st)
        # log_data=LogData.objects.all().order_by("personalForkey_id")
        ls = []
        for i in log_data:
            if i.personalForkey_id not in ls:
                ls.append(i.personalForkey_id)

        b = [] 
        for  i in ls:
            a=LogData.objects.filter(Q(sub_dispossitions="Paid")|Q(sub_dispossitions="Promise To Pay")).filter(personalForkey_id=i)
            a=LogData.objects.filter(personalForkey_id=i).exclude(sub_dispossitions="Paid")

            if agent == "all":
                a=LogData.objects.filter(personalForkey_id=i).exclude(sub_dispossitions="Paid")

            if agent != "" and agent != "all" :
                a=a.filter(caller_name=agent)
            
            if bk =="all":
                a=LogData.objects.filter(personalForkey_id=i).exclude(sub_dispossitions="Paid")

            if bk != "" and bk !="all":
                a=a.filter(bankname=bk)
                
            a = a[:5]
            b.append(list(a.values()))
   
        return JsonResponse({"b":b})
    return JsonResponse({'log_data':200,"b":list(b)})

    

def ptpcount(request):
    agent=User.objects.all()
    ls=[]
    usl=[]
    twl=[]
    tml=[]
    tosl=[]
    ptpl=[]
    ptpper=[]
    # d={}
    today=datetime.now().date()
    this_week = today + timedelta(days=7)
    this_month=  today + timedelta(days=30)
    print(this_week,"next",this_month)
    for i in agent:
        us=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Promise To Pay").filter(callbacktime=today).count()
        tw=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Promise To Pay").filter(callbacktime__range=[today,this_week]).count()
        tm=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Promise To Pay").filter(callbacktime__range=[today,this_month]).count()
        tos=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Promise To Pay").filter(callbacktime__range=[today,this_month]).aggregate(Sum('TOS'))
        t=tos['TOS__sum']
        ptp=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Promise To Pay").filter(callbacktime__range=[today,this_month]).aggregate(Sum('amount'))
        a=ptp['amount__sum']
        print("asls",tos['TOS__sum'])
        if a != None:
            per=round((a/t)*100,2)
            ptpper.append(per)
        else:
            per=0
            
            ptpper.append(per)
        

        usl.append(us)
        twl.append(tw)
        tml.append(tm)
        tosl.append(t)
        ptpl.append(a)
        # print(i.username,us,tw,tm)
        ls.append(i.username)
        # d[ls[i.username]]=values[us]
   
    d={i:{} for i in ls}
    count=0
    for i in d:
    
        d[i] = {'td':usl[count],"tw":twl[count],"tm":tml[count],"tos":tosl[count],"ptp":ptpl[count],"per":ptpper[count]}
        count+=1
    ptp=personaldetails.objects.filter(callername__in=ls).filter(sub_dispossitions="Promise To Pay")
    print(d)
    print("this",ptpper)
    for i in ptp:
        pass
    #     print(i.callername)
    # print(ptp)
    
    print(today)
    return render(request,"ptpcount.html",{"d":d})

def paidcount(request):
    agent=User.objects.all()
    ls=[]
    usl=[]
    twl=[]
    tml=[]
    tosl=[]
    paidl=[]
    paidontos=[]
    # d={}
    today=datetime.now().date()
    this_week = today + timedelta(days=7)
    this_month=  today + timedelta(days=30)
    print(this_week,"next",this_month)
    for i in agent:
        us=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Paid").filter(callbacktime=today).count()
        tw=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Paid").filter(callbacktime__range=[today,this_week]).count()
        tm=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Paid").filter(callbacktime__range=[today,this_month]).count()
        tos=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Paid").filter(callbacktime__range=[today,this_month]).aggregate(Sum('TOS'))
        t=tos['TOS__sum']
        paid=LogData.objects.filter(caller_name=i.username).filter(sub_dispossitions="Paid").filter(callbacktime__range=[today,this_month]).aggregate(Sum('cash'))
        p=paid['cash__sum']
        print("asls",p,type(p))
        if p != None:
            percent=round((p/t)*100,2)
            paidontos.append(percent)
            
        else:
            percent="0"
            paidontos.append(percent)


        usl.append(us)
        twl.append(tw)
        tml.append(tm)
        tosl.append(t)
        paidl.append(p)
        # print(i.username,us,tw,tm)
        ls.append(i.username)
        # d[ls[i.username]]=values[us]
   
    d={i:{} for i in ls}
    count=0
    for i in d:
    
        d[i] = {'td':usl[count],"tw":twl[count],"tm":tml[count],"tos":tosl[count],"ptp":paidl[count],"paidontos":paidontos[count]}
        count+=1
    ptp=personaldetails.objects.filter(callername__in=ls).filter(sub_dispossitions="Promise To Pay")
    print(d)

    print(today)
    return render(request,"paid.html",{"d":d})

def missedcall(request):
    return render(request,"missedcall.html")



def missedcallajax(request):
    db = dbconnection()
    cur=db.cursor()
    query2=f"SELECT user,phone_number,call_date,count(phone_number) as total FROM asterisk.vicidial_closer_log where campaign_id='CAPL_INB4' AND status='DROP' AND date(call_date)= '2022-09-22' group by phone_number "
    cur.execute(query2)
    missinfo =cur.fetchall()
    print(missinfo)
    # print("its",type(missinfo),len(missinfo))
    today=datetime.now().date()
    # today="2022-09-22"
    print(today)
    for i in missinfo:
        if MissedCall.objects.filter(callnum=i[1]).filter(missdt=i[2]).exists() == False:
            m=MissedCall.objects.create(username=i[0],callnum=i[1],missdt=i[2],callcount=i[3],contacted="No")
            m.save()
        elif MissedCall.objects.filter(callnum=i[1]).filter(missdt=i[2]).exists():
             m=MissedCall.objects.filter(callnum=i[1]).update(callcount=i[3])
    
    if request.user.user_level == 9:
        miss=MissedCall.objects.filter(missdt__contains=today)
    else:
        print("else",request.user.username)
        miss=MissedCall.objects.filter(missdt__contains=today).filter(username=request.user.username)
    if request.method=="POST":
        sd=request.POST.get("sd").rstrip()
        ed=request.POST.get("ed").rstrip()
        print("before",sd,ed)
        sd=datetime.strptime(sd,'%d-%m-%Y')
        ed=datetime.strptime(ed,'%d-%m-%Y')
        sd=sd.strftime("%Y-%m-%d")
        ed=ed.strftime("%Y-%m-%d")
        print("after",sd,ed)
        # query2=f"SELECT user,phone_number,call_date,count(phone_number) as total FROM asterisk.vicidial_closer_log where campaign_id='CAPL_INB4' AND status='DROP' AND date(call_date) between '{sd}' and '{ed}' group by phone_number"
        # cur.execute(query2)
        # miss=cur.fetchall()
        # for i in miss:
        #      m=MissedCall.objects.create(username=i[0],callnum=i[1],missdt=i[2],callcount=i[3],contacted="No")
        #      m.save()
        if request.user.user_level == 9: 
            print(miss,sd,ed)
            miss=MissedCall.objects.filter(missdt__range=[sd,ed])
            print("aftre filter",miss)
        else:
            miss=MissedCall.objects.filter(missdt__range=[sd,ed]).filter(username=request.user.username)
            print(miss,type(miss))
    
        return JsonResponse({"miss":list(miss.values())})

    return JsonResponse({"miss":list(miss.values())})

def misscmsajax(request):
    if request.method == "POST":
        user=request.POST.get("user")
        ph=request.POST.get("ph")
        mdt=request.POST.get("misscalldt").rstrip()
        count=request.POST.get("misscallc")
        dt=datetime.now()
        try:
            mdt=datetime.strptime(mdt,'%b %d, %Y, %H:%M:%S')
            mdt=mdt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(e)
        print("ooooooooooooooooooooo",ph,mdt,count)
        if MissedCall.objects.filter(callnum=ph).exists() == False:
            print("done")
            mcreate=MissedCall.objects.create(username=user,callnum=ph,missdt=mdt,callcount=count)
            mcreate.save()
        
        # print(ph)
        phnum=ph[2:]
        print("after",ph)
        try :
            a = Additional.objects.values_list('debtor_id',flat=True).get(contactnum=phnum).first()
            print('a',a)
        except Exception as e:
            a=None
            print(e)
        try:
            inf =personaldetails.objects.filter(Q(mobile_number=phnum)| Q(alt_mno_1=phnum) | Q(alt_mno_2=phnum)  | Q(alt_mno_3=phnum) | Q(id=a))
            print('asd',inf[0].id)
            for i in inf:
             misscall=MissedCall.objects.filter(callnum=ph).update(dispo="Contacted",sub_dispo="Exsisting Customer",lan=i.bank_loan_accountno,name=i.borrowor_name,remark="Exsisting Customer",contacted="Yes",
             cont_dt=dt)
            return JsonResponse({"status":inf[0].id})
        except Exception as e:
            print(e)
        
    
    return JsonResponse({'status':"none"})

def missunknown(request,ph):
    print(ph)
    if request.method == "POST":
        print("came")
        name=request.POST.get("name")
        lan=request.POST.get("lan")
        dispo=request.POST.get("dispo")
        sub=request.POST.get("sub_dispo")
        rem=request.POST.get("rem")
        dt=datetime.now()
        ms=MissedCall.objects.filter(callnum=ph).update(name=name,lan=lan,dispo=dispo,sub_dispo=sub,remark=rem,contacted="Yes",cont_dt=dt)
        return JsonResponse({"status":200})
        
    return render(request,"missunknown.html",{"ph":ph})


def qualityscore(request):
    # print("hi")
    db=dbconnection()
    cur=db.cursor()
    q= f"select distinct category,status_name from vicidial_campaign_statuses where status_name!='Exsisting Customer' and status_name != 'Fake Number'"

    cur.execute(q)
    sub =  cur.fetchall()
    
    contacted = []
    noncontacted = []

    for i in sub:
        if i[0] == 'contacted':
            contacted.append(i[1])
        else:
            noncontacted.append(i[1])
    # p=f"SELECT call_date,status,campaign_id,recording_log.user,location FROM asterisk.recording_log,asterisk.vicidial_log where  vicidial_log.lead_id = recording_log.lead_id and  date(call_date) >= '2022-08-01' AND date(call_date) <= '2022-08-31' and campaign_id = 'IIT' and status='INCALL' and recording_log.user='Nimesh' limit 10"
    # p=f"SELECT call_date,status,campaign_id,recording_log.user,location FROM asterisk.recording_log,asterisk.vicidial_log where vicidial_log.status='B' limit 10" 
    # p=f"SELECT call_date,status,campaign_id,recording_log.user,location FROM asterisk.recording_log,asterisk.vicidial_log where  vicidial_log.lead_id = recording_log.lead_id and  date(call_date) >= '2022-08-01' AND date(call_date) <= '2022-08-31' and campaign_id = 'IIT' and status='B' and recording_log.user='Nimesh' limit 10"
    # p=f'show tables'
    # cur.execute('show columns from vicidial_statuses')
    # query2=f"show columns from vicidial_list"
    # cur.execute(p)
    # b=cur.fetchall()
    # # cmp=""
    
    # info=list(b)
    # print(info)

        # print("********",i[0],type(i[1]),i[1],i[2],i[3],i[4])
        # c=campaign.objects.filter(campaign_id=i[2])
        
        # qs=QualityScore.objects.create(agent=i[3],sub_dispo=i[1],date=i[0],campn="Asd",location=i[4])
            # qs.save()
    
    camp=campaign.objects.all()
    u=User.objects.all()

    return render(request,"qualityscore.html",{"camp":camp,"contacted":contacted,"u":u,"info":"info"})

def qsajax(request):
    db=dbconnection()
    cur=db.cursor()

    q= f"select distinct category,status_name from vicidial_campaign_statuses where status_name!='Exsisting Customer' and status_name != 'Fake Number'"

    cur.execute(q)
    sub =  cur.fetchall()
    
    contacted = []
    noncontacted = []

    for i in sub:
        if i[0] == 'contacted':
            contacted.append(i[1])
        else:
            noncontacted.append(i[1])

    camp=campaign.objects.all()
    u=User.objects.all()
    
    # print("before if")
    rid = []
    try:
        scr = Score.objects.all()
        for i in scr:
            if i.recordingid != None:
                rid.append(i.recordingid)
    except Exception as e:
        print(e)
    if len(rid) < 2:
        print(rid)
        rid.append(1)
        rid.append(2)
    # fd=request.POST.get("fdate")
    # td=request.POST.get("tdate")
    if request.method == "POST":
        # print("inside if")
        campn=request.POST.get("campn")
        agn=request.POST.get("agn")
        dispo=request.POST.get("dispo")
        fd=request.POST.get("fdate").rstrip()
        td=request.POST.get("tdate").rstrip()
        # print('1',campn,'2',agn,'3',dispo,'4',fd,'5',td)
        p=""

        if  campn !="" :
            # print("camp is not empty")
            # print(campn)
            p=f"SELECT vicidial_log.phone_number,call_date,status,campaign_id,recording_log.user,location, recording_log.recording_id, FROM asterisk.recording_log,asterisk.vicidial_log where  vicidial_log.lead_id = recording_log.lead_id and vicidial_log.uniqueid = recording_log.vicidial_id and  recording_log.recording_id not in {tuple(rid)} and campaign_id = '{campn}' limit 60" 
            
    
        if agn !="":
            # print("agn not empty") 
            # print(agn) 
            p=f"SELECT vicidial_log.phone_number,call_date,status,campaign_id,recording_log.user,location, recording_log.recording_id FROM asterisk.recording_log,asterisk.vicidial_log where  vicidial_log.lead_id = recording_log.lead_id and vicidial_log.uniqueid = recording_log.vicidial_id  and  recording_log.recording_id not in {tuple(rid)}  and recording_log.user='{agn}' limit 60" 
            

        if dispo != "":
            # print(dispo,"dispo not empty")
            p=f"SELECT vicidial_log.phone_number,call_date,status,campaign_id,recording_log.user,location, recording_log.recording_id FROM asterisk.recording_log,asterisk.vicidial_log where  vicidial_log.lead_id = recording_log.lead_id and vicidial_log.uniqueid = recording_log.vicidial_id and  recording_log.recording_id not in {tuple(rid)} and status='{dispo}' limit 10" 
        if fd != '' and td != '':
            # print("inside",fd,td)
            try:
                fd = datetime.strptime(fd,'%d-%m-%Y')
                td = datetime.strptime(td,'%d-%m-%Y')
                fd = fd.strftime("%Y-%m-%d")
                td = td.strftime("%Y-%m-%d")
            except Exception as e:
                print(e)
            # print(fd,td,"dates not an empty")
            p=f"SELECT vicidial_log.phone_number,call_date,status,campaign_id,recording_log.user,location, recording_log.recording_id FROM asterisk.recording_log,asterisk.vicidial_log where  vicidial_log.lead_id = recording_log.lead_id and vicidial_log.uniqueid = recording_log.vicidial_id and  recording_log.recording_id not in {tuple(rid)}  and  date(call_date) >= '{fd}' AND date(call_date) <= '{td}'  limit 100" 
        cur.execute(p)
        b=cur.fetchall()
    
        info=list(b)
        print(info)
        
    return JsonResponse({'info':info})

def scoredata(request):
    if request.method=="POST":
        id=0
        pno = request.POST.get("pno")
        agn=request.POST.get("agn")
        camp=request.POST.get("camp")
        dispo=request.POST.get("dispo")
        aud=request.POST.get("aud")
        con=request.POST.get("con")
        rec=request.POST.get("rec")
        up=datetime.now().date()
        print(aud)
        # print(5,pno)
        # print(rec)
        # print(type(rec))
        # print(agn,camp,dispo,aud,con)
        if Score.objects.filter(recordingid=rec).exists():
            u=User.objects.filter(username=agn)
            print(u)
            for i in u:
                id=i.id
            print(id)
            qs=Score.objects.filter(recordingid=rec).update(agent=agn,camp=camp,dispo=dispo,aud=aud,contactdate=con,userForKey_id=id,lastupdate=up,phone=pno)
        else:
            u=User.objects.filter(username=agn)
            print(u)
            for i in u:
                id=i.id
            print("else meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            print(id)
            qs=Score.objects.create(agent=agn,camp=camp,dispo=dispo,aud=aud,contactdate=con,recordingid=rec,userForKey_id=id,lastupdate=up,phone=pno)
            qs.save()
        print(agn,camp,dispo,aud,con)
    return JsonResponse({"status":200})

def score(request,rec):
    print("rec",rec)
    q=Score.objects.filter(recordingid=rec)
    print(q)
    if request.method == "POST":
        m1=request.POST.get("1st")
        m2=request.POST.get("2nd")
        m3=request.POST.get("3rd")
        m4=request.POST.get("4th")
        m5=request.POST.get("5th")
        m6=request.POST.get("6th")
        m7=request.POST.get("7th")
        m8=request.POST.get("8th")
        m9=request.POST.get("9th")
        total=request.POST.get("tot")
        got=request.POST.get("got")
        per=request.POST.get("per")
        ls=request.POST.get("ls")
        ls = ls.split(',')
        s=Score.objects.filter(recordingid=rec).update(getmark1=m1,getmark2=m2,getmark3=m3,getmark4=m4,getmark5=m5,getmark6=m6,getmark7=m7,getmark8=m8,getmark9=m9,total=total,got=got,performance=per,marks1=ls[0],marks2=ls[1],marks3=ls[2],marks4=ls[3],marks5=ls[4],marks6=ls[5],marks7=ls[6],marks8=ls[7],marks9=ls[8])
        
        print(ls)
        print(type(ls))
        
        print(m1,m2,m3,m4,m5,m6,m7,m8,m9,total,got,per,ls)
    return render(request,"score.html",{"q":q})

def qualityexport(request):
    cmp=campaign.objects.all()
    s=Score.objects.values("agent").distinct()
    if request.method == "POST":
        c=request.POST.get("sel1")
        a=request.POST.get("sel2")
        sd = request.POST.get('sdate').rstrip()
        ed = request.POST.get('edate').rstrip()
        print("export details",c,a,sd,ed)
        sc=Score.objects
        if a !="all" and a !="":
            sc=Score.objects.filter(agent=a)
            print("agent if",sc)
        elif a =="all":
            sc=Score.objects.all()
            print("agent elif",sc)
        if c !="":
            sc=sc.filter(camp=c)
            print("camp if",sc)
        if sd != "" and ed != "":
            sd = datetime.strptime(sd,'%d-%m-%Y')
            ed= datetime.strptime(ed,'%d-%m-%Y')
            ed = ed + timedelta(days=1)
            sd= sd.strftime("%Y-%m-%d")
            ed= ed.strftime("%Y-%m-%d")
            sc=sc.filter(lastupdate__range=[sd,ed])
            print("date",sc)
        
        print("its",sc)

        try:
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="report.csv"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Users Data') 

            row_num = 0

            columns = ["Recording ID","Campaign","Disposition","Agent Name","Contacted DateTime","Audio","mark1","getmark1","mark2","getmark2","mark3","getmark3","mark4","getmark4","mark5","getmark5","mark6","getmark6","mark7","getmark7","mark8","getmark8","mark9","getmark9","Total","Score","Performance"]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num]) # at 0 row 0 column 

            # Sheet body, remaining rows
            
            rows = sc.values_list("recordingid","camp","dispo","agent","contactdate","aud","marks1","getmark1","marks2","getmark2","marks3","getmark3","marks4","getmark4","marks5","getmark5","marks6","getmark6","marks7","getmark7","marks8","getmark8","marks9","getmark9","total","got","performance")
            
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, str(row[col_num]))

            wb.save(response)

            return response

        except Exception as e:
            print(e)

        print("cmp",c,"agn",a,"strat",sd,ed)

    return render(request,"qualityexreport.html",{"cmp":cmp,"s":s})







