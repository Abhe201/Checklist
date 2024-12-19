# **Daily Checklist Application**

## **Overview**

The Daily Checklist Application is a web-based tool developed using Django to manage and display services dynamically. It includes the ability to:

- Map services to specific **locations**.
- Filter services based on a user's **default location**.
- Allow users to mark services as **"Yes"**, **"No"**, or **"N/A"** with remarks where required.
- Manage services, users, and locations via the Django Admin Panel.
- Upload service data in bulk using a **CSV file**.
- Provide confirmation before form submission.

---

## **Features**

1. **Dynamic Service Filtering**:
   - Displays services based on the logged-in user’s default location.

2. **Admin Management**:
   - Add, edit, and delete services, locations, and users via the Django Admin Panel.
   - Inline editing of services and filtering options.

3. **Bulk Data Import**:
   - Import services directly from a CSV file.

4. **User-Friendly Interface**:
   - Dropdowns for selecting statuses (`Yes`, `No`, `N/A`).
   - Input fields for remarks (enabled only when status is `No`).
   - Confirmation popup when submitting the checklist.

---

## **Tech Stack**

- **Backend**: Django (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Local LAN or server

---

## **Installation**

Follow these steps to install and run the project locally:

### **1. Prerequisites**

- Python 3.8+
- MySQL
- Django (5.1+)
- Virtual Environment (`venv` or similar)

### **2. Clone the Repository**

```bash
git clone [https://github.com/Abhe201/Checklist.git]
cd daily-checklist
```

### **3. Set Up the Virtual Environment**

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
source venv/bin/activate      # On Linux/Mac
```

### **4. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **5. Configure Database**

- Set up a **MySQL database** and note down the credentials.
- Update the `DATABASES` setting in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

- Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Load Initial Data (Optional)**

If you have a CSV file to bulk upload services:

1. Place the CSV file (`services.csv`) in the project root directory.
2. Run the import script via the Django shell:

```bash
python manage.py shell
>>> from checklist.import_services import run
>>> run()
```

### **7. Create a Superuser**

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the admin credentials.

### **8. Run the Development Server**

```bash
python manage.py runserver 0.0.0.0:8000
```

Access the site from any LAN-connected device using your local IP:

```
http://<your-ip>:8000/
```

---

## **Usage**

### **1. Admin Panel**

Log in as an admin:

- URL: `/admin/`
- Add or edit:
  - **Locations**: Add locations like "Noida", "Delhi", etc.
  - **Services**: Map services to multiple locations.

### **2. Checklist Page**

- **Login**: The user will log in and be redirected to the checklist page.
- **Service Display**: Services are filtered based on the user's default location.
- **Updating Status**:
   - Select `Yes`, `No`, or `N/A` from the dropdown.
   - Add remarks (mandatory if status is `No`).
- **Form Submission**:
   - Confirmation popup ensures user validation before submission.

---

## **Project Structure**

```
checklist_app/
│
├── checklist/                # Main app
│   ├── models.py             # Database models (Service, Location, Profile)
│   ├── views.py              # Business logic for checklist page
│   ├── urls.py               # URL routing
│   ├── templates/            # HTML templates
│   │   └── checklist.html    # Checklist frontend
│   ├── static/               # Static files (CSS, JS)
│   │   └── checklist_style.css
│   ├── import_services.py    # Bulk service import script
│
├── checklist_app/            # Project root
│   ├── settings.py           # Django settings
│   ├── urls.py               # Project-wide URLs
│
├── db.sqlite3                # Default database (if using SQLite)
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```

---

## **Customization**

### **Default Location for Users**

You can assign a default location to a user via the **Profile** model in the admin panel:

1. Go to **Profiles** in the admin interface.
2. Edit the user’s location and save.

### **Adding Services**

1. Use the **Service** model in the admin panel to add or edit services.
2. Map each service to one or more locations.

---

## **Contributing**

If you'd like to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add some feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Open a pull request.

---



## **Contact**

For any issues or suggestions:

- **Email**: Abhe201@gmail.com
- **GitHub**: [Abhe201]([(https://github.com/Abhe201/])

---

