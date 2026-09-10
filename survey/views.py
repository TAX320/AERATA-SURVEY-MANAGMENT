from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import SurveyProject, Client
from .forms import SurveyProjectForm


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


def project_create(request):
    if request.method == 'POST':
        form = SurveyProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save()
            return redirect('project_detail', pk=new_project.pk)
    else:
        form = SurveyProjectForm()
    return render(request, 'survey/project_form_dynamic.html', {'form': form})


@require_POST
def update_project_status(request, pk):
    project = get_object_or_404(SurveyProject, pk=pk)
    new_status = request.POST.get('status')
    valid_statuses = [choice[0] for choice in SurveyProject.STATUS_CHOICES]

    if new_status not in valid_statuses:
        return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)

    project.status = new_status
    project.save()

    return JsonResponse({
        'success': True,
        'status': project.status,
        'status_display': project.get_status_display(),
    })