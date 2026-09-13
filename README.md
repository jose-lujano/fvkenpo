# FVK - Federación Venezolana de Kenpo

Primera fase del portal institucional y sistema de gestión deportiva con Django 5, MariaDB, Tailwind CDN y Alpine.js.

## Instalación

1. Instala Python 3.12+ y MariaDB 10.5 o superior. Django 5.2.17 no es compatible con MariaDB 10.4.32. En este equipo Python 3.14.7 está instalado en `C:\Program Files\Python314\python.exe`; si `python` apunta a Microsoft Store, usa esa ruta absoluta o desactiva los alias de ejecución de aplicaciones.
2. Crea la base de datos:

```sql
CREATE DATABASE fvk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. Crea un entorno virtual e instala dependencias:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

También puedes crear la base de datos directamente con `database.sql`:

```powershell
mysql -u root -p < database.sql
```

El SQL crea la base, las tablas propias de FVK y las tablas necesarias de Django. Después ejecuta `migrate` para que Django registre migraciones, permisos y tipos de contenido.

## Correo de contacto

El formulario guarda cada mensaje en `ContactMessage` y lo envía al correo configurado en `SiteSetting.email_contacto`. Para SMTP define estas variables antes de iniciar Django:

```powershell
$env:EMAIL_HOST = 'smtp.gmail.com'
$env:EMAIL_PORT = '587'
$env:EMAIL_USE_TLS = '1'
$env:EMAIL_HOST_USER = 'tu-cuenta@gmail.com'
$env:EMAIL_HOST_PASSWORD = 'tu-clave-de-aplicacion'
$env:DEFAULT_FROM_EMAIL = 'tu-cuenta@gmail.com'
```

En Gmail debes usar una contraseña de aplicación, no la contraseña normal de la cuenta. Después de definir estas variables, reinicia `runserver` en la misma terminal para que Django las lea.

El dashboard está disponible en `/admin/dashboard/`. La bandeja de mensajes está en el menú de administración y permite filtrar, buscar y marcar mensajes como leídos o no leídos.

La configuración SMTP se administra desde `/admin/cms/emailsetting/`. Crea un único registro con el servidor, puerto, usuario, contraseña de aplicación, TLS y remitente. El destinatario sigue siendo `email_contacto` dentro de `SiteSetting`.

En Windows, `mysqlclient` puede requerir las herramientas de desarrollo de MariaDB/MySQL. Como alternativa, instala `PyMySQL` y añade en `fvk_project/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

4. Ejecuta migraciones y crea el usuario administrador:

```powershell
python manage.py makemigrations cms deporte competencia
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Si MariaDB ya está instalado en la versión 10.4, actualízalo antes de ejecutar `migrate`. La base `fvk_db` ya puede crearse con `python create_database.py` o con `database.sql`; no es necesario ejecutar ambos métodos.

Abre `http://localhost:8000/` y `http://localhost:8000/admin/`.

## Configuración

Las credenciales solicitadas están en `settings.py` como valores por defecto. En un entorno real usa variables `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DJANGO_SECRET_KEY` y `DJANGO_DEBUG`.

Desde el admin configura un único `SiteSetting`, sube el logo/fondo y personaliza el gradiente. La carpeta `images/` contiene los recursos originales de la marca; súbelos desde el admin como archivos de medios.
