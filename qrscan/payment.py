from django.shortcuts import render, redirect
from qrcode import *
import razorpay
from .mail import sendMail
from django.views.decorators.csrf import csrf_exempt
from .models import MonumentTickets, MonumentTickets


@csrf_exempt
def book(request):
    global MonumentTickets
    print(request.POST)
    name=request.POST["name"]
    city=request.POST['city']
    monument=request.POST['monument']
    date=request.POST['date']
    phone = request.POST['phone']
    email=request.POST['emailID']

    count_children=request.POST['count_children']
    count_adult=request.POST['count_adult']
    count_abroad=request.POST['count_abroad']
    total_count = int(count_abroad)+int(count_adult)+int(count_children)

    price_adult=request.POST['price_adult']
    price_children=request.POST['price_children']
    price_abroad=request.POST['price_abroad']

    total_cost=int(float(price_abroad))*int(count_abroad)+int(float(price_adult))*int(count_adult)+int(float(price_children))*int(count_children)

    doc_type=request.POST['doc_type']
    personal_id_no=request.POST['personal_id_no']

    global payment
    client = razorpay.Client(auth=('rzp_test_A0pbku9Y5vKP6Z', 'V70rauYt6WIeDQi7vfMmhQD5')) # create Razorpay client

    response_payment = client.order.create(dict(amount=total_cost*100, currency='INR'))# create order
    order_id = response_payment['id']
    order_status = response_payment['status']
    if order_status == 'created':
        Ticket=MonumentTickets(name=name, city=city, monument =monument, date=date, email=email, phone=phone, count_abroad=count_abroad,
        count_adult=count_adult,
        count_children=count_children,

        price_abroad=price_abroad,
        price_adult=price_adult,
        price_children=price_children,
         
        total_count=total_count,
        total_cost=total_cost,
        order_id=order_id,
        doc_type=doc_type,
        personal_id_no=personal_id_no)
        
        Ticket.save()
        response_payment['name'] = name
        response_payment['number'] = phone
        print(response_payment)
        # return Response(response_payment)
        return render(request,'coffee_payment.html',{ 'payment': response_payment})    

    return redirect("homepage")

def payment_status(request):
    responses = request.POST['razorpay_order_id']
    response=request.POST
    print(responses)
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_A0pbku9Y5vKP6Z', 'V70rauYt6WIeDQi7vfMmhQD5'))
    status = client.utility.verify_payment_signature(params_dict)
    cold_coffee = MonumentTickets.objects.get(order_id=response['razorpay_order_id'])
    cold_coffee.razorpay_payment_id = response['razorpay_payment_id']
    cold_coffee.paid = True
    cold_coffee.save()
    # delete_unpaid()
    img=make(response['razorpay_order_id'])
    img_path = "Frontend/build/static/Generated_QR/test.png"
    img.save(img_path)
    context_dict={
                    'name': cold_coffee.name,
                    'date':cold_coffee.date,
                    'city':cold_coffee.city,
                    'monument': cold_coffee.monument,
                    'count_adult':cold_coffee.count_adult,
                    'count_children':cold_coffee.count_children,
                    'count_abroad':cold_coffee.count_abroad,
                    'total_count':cold_coffee.total_count,
                    'total_cost':cold_coffee.total_cost,
                    'img':img_path,
                    'status': True,
                    'safar_logo_1':"Frontend/build/static/Images/banner.png",
                    'safar_logo_2':"Frontend/build/static/Images/banner1.png",
                    'safar_logo_3':"Frontend/build/static/Images/solid-color-image-2.png",
                    'id':response['razorpay_order_id'],
                    'doc_type':cold_coffee.doc_type,
                    'personal_id_no':cold_coffee.personal_id_no,
                }
    
    filename = "Frontend/build/static/Generated_ticket/"+response['razorpay_order_id']+".pdf"
    write_pdf('monumentTicket.html', context_dict, filename, cold_coffee)
    sendMail(cold_coffee.email, response['razorpay_order_id'],cold_coffee,context_dict)
    
    return render(request, 'payment_status.html', context_dict)
    # except:
    #     return render(request, 'payment_status.html', {'status': False})

from django.template.loader import get_template
from django.template import Context
from xhtml2pdf import pisa
from io import BytesIO

def write_pdf(template_src, context_dict, filename, cold_coffee):
    template = get_template(template_src)
    context = (context_dict)
    html  = template.render(context)
    result = open(filename, 'wb') # Changed from file to filename
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    result.close()