from dataclasses import fields
import django_filters

from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model=MonumentTickets
        fields=['city', 'verified', ]
        

class DetailFilter(django_filters.FilterSet):
    class Meta:
        model=MonumentTickets
        fields=['date']
        