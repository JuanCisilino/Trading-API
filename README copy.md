# 🚀 Trading MVP API (Django + IQ Option)

API REST para ejecutar operaciones en IQ Option (modo PRACTICE o REAL), registrar resultados y exponer métricas + balance en tiempo real para un dashboard.

---

## 🎯 Objetivo

Construir un MVP **vendible** que permita:

- Ejecutar trades (manual o desde estrategia)
- Elegir modo `PRACTICE` o `REAL`
- Obtener balance en vivo
- Guardar historial de operaciones
- Exponer métricas para dashboard

---

## 🧱 Stack

- Python 3
- Django
- Django REST Framework
- IQ Option API (`iqoptionapi`)
- SQLite (MVP) / PostgreSQL (futuro)

---

## 📂 Estructura
trading-mvp/
├── config/
│ └── settings.py
├── trading/
│ ├── models.py
│ ├── views.py
│ ├── serializers.py
│ ├── urls.py
│ └── services/
│ ├── init.py
│ └── iq.py
├── manage.py
└── .env


---

## ⚙️ Setup

### 1. Clonar / crear proyecto

```bash
mkdir trading-mvp
cd trading-mvp
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar depencias

```bash
pip install django djangorestframework python-dotenv
pip install git+https://github.com/iqoptionapi/iqoptionapi.git
```

### 4. Crear variable de entorno

```bash
touch .env
```
IQ_EMAIL=tu_email
IQ_PASSWORD=tu_password

### 5. Configurar settings

config/settings.py
```bash
import os
from dotenv import load_dotenv

load_dotenv()

IQ_EMAIL = os.getenv("IQ_EMAIL")
IQ_PASSWORD = os.getenv("IQ_PASSWORD")
```

### 6. Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Ejecutar servidor

```bash
python manage.py runserver
```
