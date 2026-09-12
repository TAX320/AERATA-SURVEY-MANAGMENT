from django.db import models


class ServiceType(models.Model):
    """Τύπος υπηρεσίας drone survey (π.χ. Power Lines, Solar, Wind)."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    """Πελάτης (εταιρεία) της Aerata."""

    SECTOR_CHOICES = [
        ('energy', 'Energy'),
        ('infrastructure', 'Infrastructure'),
        ('oil_gas', 'Oil & Gas'),
        ('surveying', 'Surveying & Mapping'),
        ('agriculture', 'Agriculture'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default='energy')
    contact_person = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name


class SurveyProject(models.Model):
    """Ένα project/αίτημα drone survey για συγκεκριμένο πελάτη."""

    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('scheduled', 'Scheduled'),
        ('flown', 'Flown'),
        ('delivered', 'Delivered'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    area_km2 = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    capacity_mw = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Installed capacity in MW, for solar/wind inspection projects only."
    )
    requested_date = models.DateField()
    scheduled_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.title} — {self.client.name}"


class Deliverable(models.Model):
    """Παραδοτέο ενός project (αρχείο/report που παραδόθηκε στον πελάτη)."""

    FILE_TYPE_CHOICES = [
        ('report', 'Report'),
        ('orthomosaic', 'Orthomosaic'),
        ('thermal', 'Thermal Imagery'),
        ('3d_model', '3D Model'),
        ('raw_footage', 'Raw Footage'),
    ]

    project = models.ForeignKey(SurveyProject, on_delete=models.CASCADE, related_name='deliverables')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='report')
    delivered_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_file_type_display()} — {self.project.title}"