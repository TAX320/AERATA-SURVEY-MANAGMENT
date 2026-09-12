import csv
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count, Q
from .models import SurveyProject, Client, Deliverable
from .forms import SurveyProjectForm, DeliverableForm, ClientForm


def dashboard(request):
    projects = SurveyProject.objects.all()
    total_projects = projects.count()
    status_counts = projects.values('status').annotate(count=Count('id'))
    status_map = {item['status']: item['count'] for item in status_counts}
    total_revenue = projects.aggregate(total=Sum('price'))['total'] or 0

    top_clients = list(
        Client.objects
        .annotate(project_count=Count('projects'), total_revenue=Sum('projects__price'))
        .filter(total_revenue__isnull=False)
        .order_by('-total_revenue')[:5]
    )

    max_revenue = top_clients[0].total_revenue if top_clients else 1
    for c in top_clients:
        c.share = int((c.total_revenue / max_revenue) * 100) if max_revenue else 0
        c.formatted_revenue = f"{c.total_revenue:,.2f}"

    formatted_total_revenue = f"{total_revenue:,.2f}"

    total_area_km2 = projects.aggregate(total=Sum('area_km2'))['total'] or 0
    formatted_area_km2 = f"{total_area_km2:,.2f}"

    total_capacity_mw = projects.aggregate(total=Sum('capacity_mw'))['total'] or 0
    formatted_capacity_mw = f"{total_capacity_mw:,.1f}"

    today = date.today()
    todays_events = SurveyProject.objects.select_related('client', 'service_type').filter(
        scheduled_date=today
    )

    return render(request, 'survey/dashboard.html', {
        'total_projects': total_projects,
        'status_map': status_map,
        'total_revenue': formatted_total_revenue,
        'top_clients': top_clients,
        'today': today,
        'todays_events': todays_events,
        'active_missions_count': todays_events.count(),
        'total_area_km2': formatted_area_km2,
        'total_capacity_mw': formatted_capacity_mw,
    })


def global_search(request):
    query = request.GET.get('q', '').strip()
    projects = []
    clients = []
    deliverables = []

    if query:
        projects = SurveyProject.objects.select_related('client').filter(
            title__icontains=query
        )[:5]
        clients = Client.objects.filter(name__icontains=query)[:5]
        deliverables = Deliverable.objects.select_related('project').filter(
            Q(notes__icontains=query) | Q(project__title__icontains=query)
        )[:5]

    return render(request, 'survey/_global_search_results.html', {
        'query': query,
        'projects': projects,
        'clients': clients,
        'deliverables': deliverables,
    })


def project_list(request):
    projects = SurveyProject.objects.select_related('client', 'service_type').all()
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    if query:
        projects = projects.filter(title__icontains=query)
    if status:
        projects = projects.filter(status=status)
    status_display = dict(SurveyProject.STATUS_CHOICES).get(status, '')
    return render(request, 'survey/project_list_dynamic.html', {
        'projects': projects,
        'query': query,
        'status_filter': status,
        'status_filter_display': status_display,
    })


def project_list_partial(request):
    projects = SurveyProject.objects.select_related('client', 'service_type').all()
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    if query:
        projects = projects.filter(title__icontains=query)
    if status:
        projects = projects.filter(status=status)
    return render(request, 'survey/_project_rows.html', {'projects': projects})


def project_detail(request, pk):
    project = get_object_or_404(
        SurveyProject.objects.select_related('client', 'service_type'), pk=pk
    )
    deliverables = project.deliverables.all()
    deliverable_form = DeliverableForm()
    return render(request, 'survey/project_detail_dynamic.html', {
        'project': project,
        'deliverables': deliverables,
        'deliverable_form': deliverable_form,
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


def client_list_partial(request):
    clients = Client.objects.all()
    sector = request.GET.get('sector')
    if sector:
        clients = clients.filter(sector=sector)
    return render(request, 'survey/_client_cards.html', {'clients': clients})


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    projects = client.projects.select_related('service_type').all()
    return render(request, 'survey/client_detail.html', {
        'client': client,
        'projects': projects,
    })


def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            new_client = form.save()
            return redirect('client_detail', pk=new_client.pk)
    else:
        form = ClientForm()
    return render(request, 'survey/client_form.html', {'form': form})


@require_POST
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    client.delete()
    return redirect('client_list')


def project_create(request):
    if request.method == 'POST':
        form = SurveyProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save()
            return redirect('project_detail', pk=new_project.pk)
    else:
        initial = {}
        client_id = request.GET.get('client')
        if client_id:
            initial['client'] = client_id
        form = SurveyProjectForm(initial=initial)
    return render(request, 'survey/project_form_dynamic.html', {'form': form, 'editing': False})


def project_edit(request, pk):
    project = get_object_or_404(SurveyProject, pk=pk)
    if request.method == 'POST':
        form = SurveyProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = SurveyProjectForm(instance=project)
    return render(request, 'survey/project_form_dynamic.html', {'form': form, 'editing': True, 'project': project})


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


@require_POST
def project_delete(request, pk):
    project = get_object_or_404(SurveyProject, pk=pk)
    project.delete()
    return redirect('project_list')


@require_POST
def add_deliverable(request, pk):
    project = get_object_or_404(SurveyProject, pk=pk)
    form = DeliverableForm(request.POST)
    if form.is_valid():
        deliverable = form.save(commit=False)
        deliverable.project = project
        deliverable.save()
    return redirect('project_detail', pk=project.pk)


def export_projects_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="aerata_projects.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Client', 'Service Type', 'Status', 'Area (km2)', 'Capacity (MW)', 'Price (EUR)', 'Requested Date', 'Scheduled Date'])
    projects = SurveyProject.objects.select_related('client', 'service_type').all()
    for p in projects:
        writer.writerow([
            p.title, p.client.name, p.service_type.name, p.get_status_display(),
            p.area_km2, p.capacity_mw, p.price, p.requested_date, p.scheduled_date,
        ])
    return response