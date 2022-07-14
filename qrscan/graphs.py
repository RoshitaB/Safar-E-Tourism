from .models import Tickett
from datetime import date
from django.shortcuts import render, redirect
import uuid, base64
from .models import *
from io import BytesIO
from matplotlib import pyplot
import pandas as pd
def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_chart(data):
    pyplot.switch_backend('AGG')
    pyplot.pie(data,labels=["verified","unverified"])
    chart = get_graph()
    return chart
