from django.shortcuts import render, redirect
from qrcode import *
from .models import MonumentTickets
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from .filters import OrderFilter,DetailFilter
from .graphs import get_chart
import pandas as pd

def homepage(request):
    return redirect("react_app")


class MyReactView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {'context_variable': 'value'}

@csrf_exempt
def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        seo_specialist = authenticate(username=username, password=password)
        if seo_specialist is not None:
            login(request,seo_specialist)
            return redirect("AdminPage")
        else:
            return redirect("/react/") 


def Ticket_display(request):
    today=date.today()
    d3 = today.strftime("%Y-%m-%d")
    customers = MonumentTickets.objects.filter(date=d3,paid=True)
    myfilter=OrderFilter(request.GET,queryset=customers)
    customers=myfilter.qs
    return render(request,'ticket.html',{"object_list":customers,"filter":myfilter,"date":today})

def display(request,monuments):
    
    customers = MonumentTickets.objects.filter(monument=monuments)
    myfilter=DetailFilter(request.GET,queryset=customers)
    customers=myfilter.qs
    customer = MonumentTickets.objects.filter(monument=monuments)
    if customer.count()!=0:
        df=customer.values()
        df=pd.DataFrame(df)
        a=df['verified'].value_counts()
        b=a.index.tolist()
        print(b)
        if True not in b:
            a=a.append(pd.Series({True:0},index=[1]))
        if False not in b:
            a=a.append(pd.Series({False:0},index=[0]))
        print (a)

        l=[a[True],a[False]]
        chart=get_chart(l)
        return render(request,'detail.html',{"object_list":customers,"filter":myfilter,"chart":chart,"Monument":monuments})
       

    else :
        return render(request,'detail.html',{"object_list":customers,"filter":myfilter})
        
    



@login_required(login_url='/react/admin')
def Admin(request):
    
    select={
        "Taj Mahal":0,
        "Fathepur Sikri":0,
        "Agra Fort":0,
        "Chowmahalla Palace":0,
        "Falaknuma Palace":0,
        "Golconda Fort":0,
        "Amber Fort":0,
        "Hawa Mahal":0,
        "Jantar Mantar":0,
        "Indian Museum":0,
        "Jorasanko Thakur Bari":0,
        "Victoria Museum":0,
        "Humayuns Tomb":0,
        "Qutub Minar":0,
        "Red Fort":0,
        "Aga Khan Palace":0,
        "Kelkar Museum":0,
        "Shanaiwar Wada":0,
    }
    return render(request,"SCANNER.html",{"select":select})


@login_required(login_url='/react/admin')
def Counter(request):
    count=0
    counter={
        "Taj Mahal":0,
        "Fathepur Sikri":0,
        "Agra Fort":0,
        "Chowmahalla Palace":0,
        "Falaknuma Palace":0,
        "Golconda Fort":0,
        "Amber Palace":0,
        "Hawa Mahal":0,
        "Jantar Mantar":0,
        "Indian Museum":0,
        "Jorasanko Thakur Bari":0,
        "Victoria Memorial":0,
        "Humayuns Tomb":0,
        "Qutub Minar":0,
        "Red Fort":0,
        "Aga Khan Palace":0,
        "Raja Dinkar Kelkar Museum":0,
        "Shaniwar Wada":0
    }
    today=date.today()
    d3 = today.strftime("%Y-%m-%d")

    customers = MonumentTickets.objects.filter(date=d3,verified=True)
    monuments   = customers.values_list("monument", flat=True)
    monuments=set(monuments)
    for m in monuments:
        count=0
        mo= MonumentTickets.objects.filter(monument=m,date=d3,verified=True)
        for id in mo:
            count=count+id.total_count
        counter[m]=count
    print(counter)

       
    return render(request,"counter.html",{"counter":counter})
