from django.contrib import admin
from .models import Vendor, Purchase_Order, HistoricalPerfomance

admin.site.register(Vendor)
admin.site.register(Purchase_Order)
admin.site.register(HistoricalPerfomance)