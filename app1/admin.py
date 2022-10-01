from django.contrib import admin
from .models import Additional, emi, personaldetails,otsdata, sendfeto,Dataupload,Excelformat


# Register your models here.

admin.site.register(personaldetails)
admin.site.register(Additional)
admin.site.register(otsdata)
admin.site.register(emi)
admin.site.register(sendfeto)
admin.site.register(Dataupload)
admin.site.register(Excelformat)

