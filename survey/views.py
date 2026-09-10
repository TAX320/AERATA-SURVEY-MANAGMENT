from django.shortcuts import render, get_object_or_404
from .models import SurveyProject


def project_list(request):
    projects = SurveyProject.objects.select_related('client', 'service_type').all()
    return render(request, 'survey/project_list_dynamic.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(
        SurveyProject.objects.select_related('client', 'service_type'), pk=pk
    )
    deliverables = project.deliverables.all()
    return render(request, 'survey/project_detail_dynamic.html', {
        'project': project,
        'deliverables': deliverables,
    })
    from django.shortcuts import render, get_object_or_404
from .models import SurveyProject, Client


def project_list(request):
    projects = SurveyProject.objects.select_related('client', 'service_type').all()
    return render(request, 'survey/project_list_dynamic.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(
        SurveyProject.objects.select_related('client', 'service_type'), pk=pk
    )
    deliverables = project.deliverables.all()
    return render(request, 'survey/project_detail_dynamic.html', {
        'project': project,
        'deliverables': deliverables,
    })


def client_list(request):
    clients = Client.objects.all()
    sector = request.GET.get('sector')
    if sector:
        clients = clients.filter(sector=sector)
    return render(request, 'survey/client_list_dynamic.html', {
        'clients': clients,
        'selected_sector': sector,
    })