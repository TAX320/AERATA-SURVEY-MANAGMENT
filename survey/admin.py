from django.contrib import admin
from .models import Client, ServiceType, SurveyProject, Deliverable

admin.site.register(Client)
admin.site.register(ServiceType)
admin.site.register(SurveyProject)
admin.site.register(Deliverable)
