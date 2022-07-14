from ast import Try
# from asyncio.windows_events import NULL
from pyexpat import version_info
import cv2
from pyzbar.pyzbar import decode
from sqlalchemy import null
from .models import *
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
import numpy as np
from datetime import date, datetime, timedelta
from django.http import response

object=null
a=False
verified=""
displaytext=""
count=""
def change_param(verified):
    print ("hii")
    global object
    global a
    object=verified
    a=True
def change_param_1():
    global displaytext
    displaytext="Access Denied"

def lcd_display(request):
    global object
    print("ard")
    try:
        if datetime.now()<object.timevalid.replace(tzinfo=None):
            d={
                "message":"Access Granted",
                "count":object.total_count,

            }
            return response.JsonResponse(d)
        else:
            d={
                "message":"Access Denied",
                "count":object.total_count,
            }
            return response.JsonResponse(d)

    except:
        d={
            "message":displaytext,
            "count":count
        }
        return response.JsonResponse(d)

        


def gen_frames(request,monuments):  
    global verified
    camera = cv2.VideoCapture(0)
    global verified
    while True:
        success, frame = camera.read()  
        try:
            if not success:
                break
            else:
                for barcode in decode(frame):
                    text = barcode.data.decode('utf-8')
                    text=str(text) # Order ID String

                    today=date.today()
                    d3 = today.strftime("%Y-%m-%d")
                    
                    verified=MonumentTickets.objects.get(order_id=text,monument=monuments, date=d3) #Object Returned
                    if MonumentTickets.objects.filter(order_id=text,monument=monuments, date=d3).exists(): 
                        if verified.verified==False:
                            color=(0,255,0)
                            displaytext = "Access Granted"
                            verified.verified=True
                            change_param(verified)
                            now = datetime.now()
                            print("NOW: ",now)
                            expire = now + timedelta(minutes=0.5)
                            print("l")
                            verified.timevalid = expire
                            verified.save()
                            print("VALID TILL: ",verified.timevalid)

                        else:
                            if datetime.now()<verified.timevalid.replace(tzinfo=None):
                                color=(0,255,0)
                                displaytext = "Access Granted"
                                print("k")
                                change_param(verified)
                            else:
                                color=(0,0,255)
                                displaytext =  "Unauthorised Access"
                                print("kk")
                                change_param(verified)
                        
                    else:
                        color=(0,0,255)
                        displaytext =  "Unauthorised Access"
                        print("kkk")
                        change_param(verified)
                    
                    polygon_Points = np.array([barcode.polygon], np.int32)
                    polygon_Points=polygon_Points.reshape(-1,1,2)
                    rect_Points= barcode.rect
                    cv2.polylines(frame,[polygon_Points],True,color, 3)
                    frame=cv2.putText(frame, displaytext, (rect_Points[0],rect_Points[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, color, 2)
                    
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') # concat frame one by one and show result
        except:
            color=(0,0,255)
            displaytext =  "Unauthorised Access"
            change_param_1()
            polygon_Points = np.array([barcode.polygon], np.int32)
            polygon_Points=polygon_Points.reshape(-1,1,2)
            rect_Points= barcode.rect
            cv2.polylines(frame,[polygon_Points],True,color, 3)
            frame=cv2.putText(frame, displaytext, (rect_Points[0],rect_Points[1]), cv2.FONT_HERSHEY_PLAIN, 0.9, color, 2)
                    
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') # concat frame one by one and show result



def ScanQR(self,monuments):
    #Video streaming route. Put this in the src attribute of an img ta
    return StreamingHttpResponse(gen_frames(self,monuments), content_type="multipart/x-mixed-replace;boundary=frame")    

def Call_Scan(request,monuments):
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
    displaytext=""
    vid = cv2.VideoCapture(0)
    vid.set(3,640)
    vid.set(4,740)
    counter=0
    global status
    while True:
        success, img = vid.read()
        for barcode in decode(img):
            displaytext=""
            text = barcode.data.decode('utf-8')
            text=str(text)
            print(text)
            
            today=date.today()
            d3 = today.strftime("%Y-%m-%d")
            
            verified=MonumentTickets.objects.get(order_id=text,date=d3)
            if MonumentTickets.objects.filter(order_id=text,monument=monuments, date=d3).exists(): 
                if verified.verified==False:
                    color=(0,255,0)
                    displaytext = "Access Granted"
                    verified.verified=True
                    change_param(verified)
                    now = datetime.now()
                    print("NOW: ",now)
                    expire = now + timedelta(minutes=0.5)

                    verified.timevalid = expire
                    verified.save()
                    print("VALID TILL: ",verified.timevalid)

                else:
                    if datetime.now()<verified.timevalid.replace(tzinfo=None):
                        color=(0,255,0)
                        displaytext = "Access Granted"
                        status=True
                        
                        return render(request,"SCANNER.html",{"displaytext":displaytext,"status":status,"monuments":monuments,"select":select}) 

                    else:
                        color=(0,0,255)
                        displaytext =  "Unauthorised Access"
                        status=False
                        
                        return render(request,"SCANNER.html",{"displaytext":displaytext,"status":status,"select":select})
                
            else:
                color=(0,0,255)
                displaytext =  "Unauthorised Access"
                status=False
                
                return render(request,"SCANNER.html",{"displaytext":displaytext,"status":status,"select":select})

def selectMonument(request):
    monument=request.POST["monuments"]
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
    print(monument)
    return render(request,"SCANNER.html",{"monuments":monument,"select":select})