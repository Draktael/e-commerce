# E-commerce — Backend (Django + DRF + SimpleJWT)

Backend del proyecto de **E-commerce** construido con **Django** y **Django REST Framework**.  
Expone endpoints para **productos**, **carrito** (anónimo y autenticado), **órdenes**, **checkout** y **autenticación JWT**.

---

## 🚀 Características

- API REST con **Django REST Framework**.
- **JWT (SimpleJWT)** para autenticación.
- Carrito para usuario anónimo y autenticado.
- Checkout (p. ej., para integrarse con Stripe).
- Base de datos local **SQLite** (fácil de iniciar); preparada para Postgres u otro en producción.

---

## 📦 Requisitos

- Python 3.10+
- pip
- (Opcional) `virtualenv`

---

## 📂 Estructura principal
.
├── db.sqlite3
├── ecommerce/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── products/               # (imágenes)
│   └── 27229620.jpg
└── store/
├── admin.py
├── migrations/
├── models.py
├── serializers.py
├── urls.py
└── views.py

> **Tip:** No subas `db.sqlite3` al repositorio; usa `.gitignore`.

---

## ⚙️ Instalación y uso (local)

```bash
# 1) Crear y activar un entorno virtual (recomendado)
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.\.venv\Scripts\activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Migraciones
python manage.py makemigrations
python manage.py migrate

# 4) Crear superusuario (opcional)
python manage.py createsuperuser

# 5) Ejecutar servidor
python manage.py runserver
```
La API quedará disponible en: http://127.0.0.1:8000/
🌱 Variables de entorno (.env.example)

Crea un archivo .env en la raíz (y cárgalo con django-environ o python-dotenv):
# Django
DEBUG=True
SECRET_KEY=pon_aqui_una_secret_key_segura
ALLOWED_HOSTS=localhost,127.0.0.1

# DB (por defecto SQLite; para Postgres usa DATABASE_URL)
# DATABASE_URL=postgres://USER:PASS@HOST:5432/DBNAME

# CORS/CSRF (ajusta dominios del frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000

# Archivos media
MEDIA_URL=/media/
Ajustes recomendados en settings.py:
	•	Leer .env y configurar DEBUG, SECRET_KEY, ALLOWED_HOSTS.
	•	Habilitar CORS/CSRF según tu frontend.
	•	Configurar MEDIA_URL/MEDIA_ROOT para imágenes de productos.
	•	En producción: DEBUG=False, ALLOWED_HOSTS reales, DATABASE_URL a Postgres y storage de media (S3 o similar).

 🔗 Enrutado

En ecommerce/urls.py monta las rutas del app store (ajusta el prefijo a tu preferencia, aquí usamos /api/):
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),  # <- prefijo de la API
]

🗃️ Base de datos y media
	•	SQLite local: db.sqlite3 (no subir al repo).
	•	Carpeta products/ con imágenes de producto (define MEDIA_ROOT y sirve MEDIA_URL en desarrollo).
	•	Producción: PostgreSQL + storage de objetos (S3, etc.).
 
# Python / Django
__pycache__/
*.py[cod]
*.sqlite3
db.sqlite3
.env
.venv/
venv/

# Media local
/products/
media/

# IDE
.vscode/
.idea/

🤝 Integración con el frontend

Si tu cliente React usa Axios, define la base URL en el frontend:
	•	CRA: REACT_APP_API_URL=http://localhost:8000/api
	•	Vite: VITE_API_URL=http://localhost:8000/api

Asegúrate de permitir ese origen en CORS/CSRF (ver variables de entorno).
# E-commerce — Frontend (React + CRA + Tailwind)

Frontend de una tienda en línea: permite **ver productos**, **agregarlos al carrito**, **modificar cantidades**, **eliminar ítems** y **proceder al pago con Stripe**. Soporta **usuario registrado** o **compra anónima**.

## ✨ Características
- Catálogo de productos con detalles.
- Carrito: agregar, aumentar/disminuir cantidad y eliminar.
- Checkout con **Stripe**.
- Autenticación opcional (login/registro) o **modo anónimo**.
- Notificaciones con **React Toastify**.
- Navegación con **React Router**.
- Iconografía con **react-icons**.
- Estilos con **Tailwind CSS** (configurado con `tailwind.config.js` y `postcss.config.js`).

## 🛠️ Stack
- **React (Create React App)** + **react-scripts**
- **React Router DOM 7**
- **React Toastify**
- **react-icons**
- **Tailwind CSS / PostCSS**
- Testing: **@testing-library/**, **jest-dom**, **user-event**
- Métricas: **web-vitals**
 [oai_citation:0‡package.json](file-service://file-FKz3mVeRHdUthjNEwD9ifN)

## 📂 Estructura
.
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── App.js
│   ├── components/
│   ├── index.css
│   ├── index.js
│   ├── output.css
│   ├── reportWebVitals.js
│   └── setupTests.js
├── postcss.config.js
├── tailwind.config.js
└── package.json

## ⚙️ Instalación y uso
```bash
# 1) Clonar
git clone https://github.com/tu-usuario/ecommerce-frontend.git
cd ecommerce-frontend

# 2) Instalar deps
npm install

# 3) Variables de entorno
cp .env.example .env

# 4) Desarrollo
npm start

# 5) Build producción
npm run build

# 6) Tests
npm test
```
Scripts soportados: start, build, test, eject.  ￼

🌱 Variables de entorno (.env.example)
# URL base de la API (backend Django)
REACT_APP_API_URL=http://localhost:8000/api

# Stripe (clave pública)
REACT_APP_STRIPE_PK=pk_test_XXXXXXXXXXXXXXXXXXXXXXXX
🔗 Integración con el backend

La app consume el backend Django en los endpoints bajo /api/:
	•	Productos: /api/products/, /api/products/:id/
	•	Carrito (anónimo/autenticado): /api/cart/anonymous/, /api/cart/authenticated/, /api/cart/:id/…
	•	Órdenes: /api/orders/, /api/orders/:id/
	•	Checkout: /api/checkout/:cart_id/
	•	Auth JWT: /api/token/, /api/token/refresh/, /api/register/, /api/me/, /api/history-orders/

Configura REACT_APP_API_URL con la URL del backend (local o deploy).

🎨 Tailwind CSS (CRA)
	•	Tailwind ya está configurado con tailwind.config.js y postcss.config.js.
	•	Asegúrate de importar las directivas en index.css:
 
 @tailwind base;
@tailwind components;
@tailwind utilities;

🔔 Notificaciones
Usa react-toastify para feedback de acciones (añadir al carrito, errores de checkout, etc.). Recuerda envolver la app con <ToastContainer />.

🚀 Despliegue
	•	Vercel / Netlify: compila con npm run build y sirve la carpeta build/.
	•	Define variables en el panel (por ejemplo REACT_APP_API_URL, REACT_APP_STRIPE_PK).
	•	Si usas rutas de React Router, habilita “SPA fallback” (rewrites a index.html).

 🧪 Testing

Incluye React Testing Library y jest-dom para pruebas de componentes:
npm test

✅ Checklist rápido
	•	.env creado con REACT_APP_API_URL (y REACT_APP_STRIPE_PK si aplica).
	•	CORS/CSRF del backend configurado para el origen del frontend.
	•	Claves de Stripe públicas/privadas ubicadas donde corresponde (solo la pública en el frontend).
