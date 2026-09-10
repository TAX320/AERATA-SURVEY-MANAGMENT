from django.shortcuts import render
from .models import SurveyProject


def project_list(request):
    projects = SurveyProject.objects.select_related('client', 'service_type').all()
    return render(request, 'survey/project_list_dynamic.html', {'projects': projects})