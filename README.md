[README.md](https://github.com/user-attachments/files/32144703/README.md)

[README (1).md](https://github.com/user-attachments/files/32144698/README.1.md)
# Aerata Survey & Client Management System

## Περιγραφή# Aerata Survey & Client Management System

## 1. Σύντομη περιγραφή της εφαρμογής

Η **Aerata** είναι εταιρεία που παρέχει υπηρεσίες αεροφωτογράφησης και επιθεώρησης υποδομών με χρήση drones (power lines, φωτοβολταϊκά πάρκα, ανεμογεννήτριες, γραμμικές χαρτογραφήσεις) σε πελάτες του ενεργειακού και υποδομικού τομέα στην Ελλάδα. Καθώς ο αριθμός των πελατών και των έργων αυξάνεται, η παρακολούθηση του ποιος πελάτης έχει ζητήσει τι είδους survey, σε ποιο στάδιο βρίσκεται κάθε έργο, και ποια παραδοτέα έχουν ήδη σταλεί γίνεται δύσκολη χωρίς ένα κεντρικό εργαλείο.

Η εφαρμογή **Aerata Survey & Client Management System** καλύπτει ακριβώς αυτή την ανάγκη: πρόκειται για ένα εσωτερικό εργαλείο (mini-CRM) που επιτρέπει στην ομάδα πωλήσεων/λειτουργιών της Aerata να καταχωρεί πελάτες, να δημιουργεί και να παρακολουθεί survey projects ανά τύπο υπηρεσίας (Power Lines Inspection, Solar Audit, Wind Turbine Inspection, Corridor Mapping), να ενημερώνει την κατάσταση κάθε έργου (Requested → Scheduled → Flown → Delivered), και να καταγράφει τα παραδοτέα που στέλνονται σε κάθε πελάτη.

Κύριοι χρήστες είναι τα μέλη της ομάδας της Aerata (sales/ops), τα οποία μέσω της εφαρμογής μπορούν να έχουν άμεση εικόνα του pipeline εργασιών χωρίς να χρειάζεται να ανατρέχουν σε spreadsheets ή emails.

---

## 2. Περιγραφή και τεκμηρίωση λειτουργιών

### Λειτουργία 1: Προβολή Survey Projects

- **Περιγραφή:** Η εφαρμογή εμφανίζει στον χρήστη μια λίστα με όλα τα survey projects της Aerata, μαζί με τον πελάτη, τον τύπο υπηρεσίας, την κατάσταση και βασικά στοιχεία κάθε έργου.
- **Είσοδος χρήστη:** Δεν απαιτείται κάποια είσοδος.
- **Έξοδος:** Ένας πίνακας με τη λίστα των projects. Κάθε εγγραφή περιλαμβάνει:
  - Τίτλο έργου
  - Πελάτη
  - Τύπο υπηρεσίας
  - Κατάσταση (badge χρωματισμένο ανάλογα με το status)
  - Εμβαδόν (km²)
  - Ημερομηνία αιτήματος
- **HTTP Method/URL:** `GET /projects/`
- **Mock-up / Υλοποιημένη οθόνη:** `project_list.html` (mock-up) / `project_list_dynamic.html` (πλήρως λειτουργική — αντλεί δεδομένα από τη βάση μέσω Django ORM)

---

### Λειτουργία 2: Προβολή λεπτομερειών ενός Survey Project

- **Περιγραφή:** Η εφαρμογή εμφανίζει αναλυτικά στοιχεία για ένα συγκεκριμένο project: περιγραφή, στοιχεία πελάτη, τιμή, ημερομηνίες, και τα παραδοτέα που έχουν σταλεί ή εκκρεμούν.
- **Είσοδος χρήστη:** Ο χρήστης επιλέγει ένα project από τη λίστα (π.χ. κάνοντας κλικ στο κουμπί "View").
- **Έξοδος:** Καρτέλα με:
  - Τίτλο, περιγραφή, κατάσταση (status badge)
  - Πελάτης, τύπος υπηρεσίας, εμβαδόν, τιμή, ημερομηνίες
  - Στοιχεία επικοινωνίας πελάτη
  - Λίστα παραδοτέων με κατάσταση παράδοσης
- **HTTP Method/URL:** `GET /projects/<id>/`
- **Mock-up οθόνη:** `project_detail.html`

---

### Λειτουργία 3: Προβολή Clients

- **Περιγραφή:** Η εφαρμογή εμφανίζει όλους τους πελάτες της Aerata, φιλτραρισμένους προαιρετικά ανά τομέα (Energy, Infrastructure, Agriculture), μαζί με τον αριθμό ενεργών projects που έχει ο καθένας.
- **Είσοδος χρήστη:** Προαιρετική επιλογή τομέα από dropdown φίλτρο.
- **Έξοδος:** Λίστα καρτών πελατών, κάθε μία με:
  - Όνομα εταιρείας
  - Υπεύθυνο επικοινωνίας
  - Τομέα δραστηριότητας (badge)
  - Αριθμό ενεργών projects
- **HTTP Method/URL:** `GET /clients/`
- **Mock-up οθόνη:** `client_list.html`

---

### Λειτουργία 4: Δημιουργία νέου Survey Project

- **Περιγραφή:** Η εφαρμογή παρέχει φόρμα μέσω της οποίας ο χρήστης μπορεί να καταχωρήσει ένα νέο survey project, επιλέγοντας πελάτη και τύπο υπηρεσίας από λίστες, και συμπληρώνοντας στοιχεία όπως εμβαδόν, τιμή και ημερομηνίες.
- **Είσοδος χρήστη:** Τίτλος, περιγραφή, πελάτης (dropdown), τύπος υπηρεσίας (dropdown), εμβαδόν, τιμή, ημερομηνία αιτήματος, ημερομηνία προγραμματισμού.
- **Έξοδος:** Δημιουργία νέας εγγραφής SurveyProject στη βάση δεδομένων και ανακατεύθυνση στη λίστα projects.
- **HTTP Method/URL:** `GET /projects/new/` (εμφάνιση φόρμας) — `POST /projects/new/` (υποβολή δεδομένων)
- **Mock-up οθόνη:** `project_form.html`

---

## 3. Mock-up οθόνες

Όλες οι mock-up οθόνες (HTML/CSS με Bootstrap 5) βρίσκονται στον φάκελο `survey/templates/survey/`:

| Αρχείο | Λειτουργία |
|---|---|
| `project_list.html` | Λειτουργία 1 — mock-up |
| `project_detail.html` | Λειτουργία 2 — mock-up |
| `client_list.html` | Λειτουργία 3 — mock-up |
| `project_form.html` | Λειτουργία 4 — mock-up |
| `project_list_dynamic.html` | Λειτουργία 1 — **πλήρως λειτουργική υλοποίηση** |

Το σχέδιο ακολουθεί το brand system της Aerata: σκούρο φόντο (`#1B2025`), πράσινο accent (`#8BB25C`), με status badges σε μπλε/πορτοκαλί/πράσινο ανάλογα με την κατάσταση κάθε project.

---

## 4. Σχήμα βάσης δεδομένων

```
┌─────────────────┐         ┌──────────────────┐
│  ServiceType     │         │     Client        │
├─────────────────┤         ├──────────────────┤
│ id (PK)          │         │ id (PK)           │
│ name             │         │ name              │
│ description      │         │ sector            │
└─────────────────┘         │ contact_person    │
        │ 1                  │ email             │
        │                    │ phone             │
        │ *                  └──────────────────┘
┌─────────────────────┐              │ 1
│   SurveyProject       │              │
├─────────────────────┤              │ *
│ id (PK)               │◄─────────────┘
│ title                 │
│ description           │
│ client (FK)           │
│ service_type (FK)     │
│ status                │
│ area_km2              │
│ requested_date        │
│ scheduled_date        │
│ price                 │
└─────────────────────┘
        │ 1
        │
        │ *
┌─────────────────────┐
│    Deliverable        │
├─────────────────────┤
│ id (PK)               │
│ project (FK)           │
│ file_type              │
│ delivered_date          │
│ notes                   │
└─────────────────────┘
```

**Σχέσεις:**
- Ένας **Client** μπορεί να έχει πολλά **SurveyProject** (one-to-many)
- Ένα **ServiceType** μπορεί να εφαρμόζεται σε πολλά **SurveyProject** (one-to-many)
- Ένα **SurveyProject** μπορεί να έχει πολλά **Deliverable** (one-to-many)

**Django models:** το πλήρες σχήμα έχει μεταφραστεί σε Django models στο αρχείο `survey/models.py`.

---

## 5. Πλήρως λειτουργική οθόνη

Η λειτουργία **"Προβολή Survey Projects"** (Λειτουργία 1) έχει υλοποιηθεί πλήρως:

- **View:** `survey/views.py` → `project_list(request)`
- **URL:** `survey/urls.py` → `GET /projects/`
- **Template:** `survey/templates/survey/project_list_dynamic.html`

Η υλοποίηση αντλεί τα δεδομένα απευθείας από τη βάση SQLite μέσω του Django ORM (`SurveyProject.objects.select_related('client', 'service_type').all()`) και τα εμφανίζει δυναμικά στο HTML χρησιμοποιώντας το Django template engine (`{% for %}`), χωρίς hardcoded δεδομένα.

---

## Πώς εκτελείται η εφαρμογή

```bash
# 1. Δημιουργία και ενεργοποίηση virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 2. Εγκατάσταση εξαρτήσεων
pip install -r requirements.txt

# 3. Εφαρμογή migrations
python manage.py migrate

# 4. (Προαιρετικό) Δημιουργία superuser για πρόσβαση στο admin panel
python manage.py createsuperuser

# 5. Εκκίνηση development server
python manage.py runserver
```

Μετά, άνοιξε στον browser:
- `(http://127.0.0.1:8000/)` — Dashboard - κεντρική σελίδα εφαρμογής (πλήρως λειτουργικo)
- `http://127.0.0.1:8000/admin/` — Django admin panel


Web εφαρμογή διαχείρισης πελατών και survey projects για την Aerata (drone inspection εταιρεία). Επιτρέπει καταχώρηση πελατών, δημιουργία/επεξεργασία/διαγραφή projects, παρακολούθηση status, deliverables, και προβολή στατιστικών σε dashboard.

**Αλλαγές σε σχέση με το πρώτο παραδοτέο:**
- Πλήρης υλοποίηση όλων των λειτουργιών (όχι μόνο μία)
- Νέες λειτουργίες: Edit project, Delete project/client, Add deliverable, Create client
- Dashboard με KPIs, revenue, top clients, calendar, live wind map, area/capacity coverage
- Global search (Ctrl/Cmd+K) σε projects/clients/deliverables
- AJAX: live search, live filtering, status update χωρίς reload
- Django Forms με custom validation
- CSS/JS οργανωμένα σε static/ φάκελο
- Πραγματικό logo και custom design system

## Πώς εκτελείται

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_data     # δημιουργεί demo δεδομένα
python manage.py runserver
```

Άνοιξε: `http://127.0.0.1:8000/`

## Λειτουργίες

| Λειτουργία | URL |
|---|---|
| Dashboard | `/` |
| Λίστα projects (+ search, φίλτρο status) | `/projects/` |
| Λεπτομέρειες project (status update, deliverables) | `/projects/<id>/` |
| Νέο / Επεξεργασία project | `/projects/new/`, `/projects/<id>/edit/` |
| Export CSV | `/projects/export/` |
| Λίστα clients (+ φίλτρο sector) | `/clients/` |
| Λεπτομέρειες / Νέος client | `/clients/<id>/`, `/clients/new/` |
| Admin panel | `/admin/` |

## Τεχνολογίες

Django 6.1, SQLite, Bootstrap 5, vanilla JavaScript (AJAX/fetch), Windy.com embed (δωρεάν, χωρίς API key).

## Περιορισμοί

- Τα δεδομένα (πελάτες, projects) είναι demo/πλασματικά, παραγόμενα από το `seed_data` management command
- Το πεδίο "MW Inspected" στο dashboard αθροίζει το πεδίο `capacity_mw`, το οποίο συμπληρώνεται προαιρετικά μόνο σε energy projects (solar/wind)
- Το Windy widget δείχνει live χάρτη ανέμου αλλά όχι αριθμητικά δεδομένα (wind speed) — αυτό απαιτεί δωρεάν API key από windy.com που δεν έχει ενσωματωθεί
- Δεν υπάρχει authentication/permissions πέρα από το Django admin — η εφαρμογή θεωρείται εσωτερικό εργαλείο μίας ομάδας
