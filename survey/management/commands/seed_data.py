import random
from datetime import timedelta, date
from django.core.management.base import BaseCommand
from survey.models import Client, ServiceType, SurveyProject


CLIENTS = [
    {"name": "RWE Renewables Greece", "sector": "energy", "contact_person": "Charilaos Mitrelias", "email": "", "phone": ""},
    {"name": "iSOLAR S.A.", "sector": "energy", "contact_person": "Argyris Iliadis", "email": "", "phone": ""},
    {"name": "PPC Renewables", "sector": "energy", "contact_person": "Konstantinos Mavros", "email": "", "phone": ""},
    {"name": "EDF Energy", "sector": "energy", "contact_person": "Business Development", "email": "", "phone": ""},
    {"name": "ΔΕΔΔΗΕ", "sector": "infrastructure", "contact_person": "Network Operations", "email": "", "phone": ""},
    {"name": "Gastrade", "sector": "oil_gas", "contact_person": "Business Development", "email": "", "phone": ""},
    {"name": "ΕΥΔΑΠ", "sector": "infrastructure", "contact_person": "Network Operations", "email": "", "phone": ""},
    {"name": "iXion Energy", "sector": "energy", "contact_person": "Ioannis Papadopoulos", "email": "", "phone": ""},
]

SERVICE_TYPES = {
    "Solar Panel Inspection": "Thermal & visual inspection of PV installations",
    "Wind Turbine Inspection": "Blade and structural inspection via drone",
    "Power Lines Inspection": "Aerial inspection of MV/HV power line corridors",
    "Pipeline Inspection": "Oil & gas / water network inspection",
    "Telecom Tower Inspection": "Structural inspection of telecom towers",
    "Topographic & LiDAR Survey": "Corridor mapping and topographic surveying",
    "Agricultural Monitoring": "Crop health and environmental monitoring via drone",
}

# Which service types make sense for each client, with
# (service_name, area_min, area_max, price_min, price_max, capacity_min, capacity_max)
# capacity_min/max is None for services with no MW capacity (e.g. pipelines, telecom, surveying)
CLIENT_SERVICES = {
    "RWE Renewables Greece": [
        ("Wind Turbine Inspection", 0.3, 1.5, 3500, 9000, 18, 65),
        ("Power Lines Inspection", 5, 25, 5000, 14000, None, None),
    ],
    "iSOLAR S.A.": [
        ("Solar Panel Inspection", 0.5, 3.5, 2800, 7500, 5, 35),
        ("Topographic & LiDAR Survey", 1, 8, 3200, 9000, None, None),
    ],
    "PPC Renewables": [
        ("Wind Turbine Inspection", 0.3, 1.2, 3800, 8500, 20, 80),
        ("Solar Panel Inspection", 0.4, 2.8, 2500, 6800, 8, 40),
    ],
    "EDF Energy": [
        ("Wind Turbine Inspection", 0.3, 1.0, 3600, 8000, 15, 50),
        ("Solar Panel Inspection", 0.5, 2.0, 2600, 6000, 6, 25),
    ],
    "ΔΕΔΔΗΕ": [
        ("Power Lines Inspection", 8, 40, 6000, 18000, None, None),
        ("Telecom Tower Inspection", 0.01, 0.05, 700, 2200, None, None),
    ],
    "Gastrade": [
        ("Pipeline Inspection", 10, 55, 7000, 22000, None, None),
    ],
    "ΕΥΔΑΠ": [
        ("Topographic & LiDAR Survey", 2, 12, 4000, 11000, None, None),
        ("Pipeline Inspection", 5, 30, 6000, 17000, None, None),
    ],
    "iXion Energy": [
        ("Wind Turbine Inspection", 0.3, 1.3, 3700, 8800, 22, 90),
    ],
}

PROJECT_NAME_TEMPLATES = [
    "{client} — {service} Q{q}",
    "{client} {service} — Site {n}",
    "{client} Annual {service}",
    "{client} {service} — Phase {n}",
]

STATUS_WEIGHTS = [
    ("requested", 25),
    ("scheduled", 25),
    ("flown", 25),
    ("delivered", 25),
]


def weighted_status():
    statuses, weights = zip(*STATUS_WEIGHTS)
    return random.choices(statuses, weights=weights, k=1)[0]


class Command(BaseCommand):
    help = "Seed the database with realistic Aerata clients and survey projects."

    def handle(self, *args, **options):
        random.seed(42)
        today = date.today()

        # 1. Create/get service types
        service_type_objs = {}
        for name, description in SERVICE_TYPES.items():
            obj, created = ServiceType.objects.get_or_create(
                name=name, defaults={"description": description}
            )
            service_type_objs[name] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created service type: {name}"))

        # 2. Create/get clients
        client_objs = {}
        for c in CLIENTS:
            obj, created = Client.objects.get_or_create(
                name=c["name"],
                defaults={
                    "sector": c["sector"],
                    "contact_person": c["contact_person"],
                    "email": c["email"],
                    "phone": c["phone"],
                },
            )
            client_objs[c["name"]] = obj
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created client: {c['name']}"))
            else:
                self.stdout.write(f"Client already exists, skipping creation: {c['name']}")

        # 3. Create realistic projects per client
        total_created = 0
        for client_name, services in CLIENT_SERVICES.items():
            client = client_objs[client_name]
            num_projects = random.randint(4, 7)

            for i in range(num_projects):
                service_name, area_min, area_max, price_min, price_max, cap_min, cap_max = random.choice(services)
                service_type = service_type_objs[service_name]

                area = round(random.uniform(area_min, area_max), 2)
                price = round(random.uniform(price_min, price_max), 2)

                capacity_mw = None
                if cap_min is not None and cap_max is not None:
                    capacity_mw = round(random.uniform(cap_min, cap_max), 2)

                days_ago = random.randint(10, 270)
                requested_date = today - timedelta(days=days_ago)

                status = weighted_status()
                scheduled_date = None
                if status in ("scheduled", "flown", "delivered"):
                    scheduled_date = requested_date + timedelta(days=random.randint(5, 30))

                template = random.choice(PROJECT_NAME_TEMPLATES)
                title = template.format(
                    client=client_name,
                    service=service_name,
                    q=random.randint(1, 4),
                    n=random.randint(1, 5),
                )

                description = f"{service_name} engagement for {client_name}, covering approximately {area} km²."
                if capacity_mw:
                    description += f" Installed capacity: {capacity_mw} MW."

                SurveyProject.objects.create(
                    title=title,
                    description=description,
                    client=client,
                    service_type=service_type,
                    status=status,
                    area_km2=area,
                    capacity_mw=capacity_mw,
                    requested_date=requested_date,
                    scheduled_date=scheduled_date,
                    price=price,
                )
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f"Done. Created {total_created} new survey projects."))