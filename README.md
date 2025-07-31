# sUP - Sistema Unificado de Producción

![Logo sUP](static/images/sUP.png)

**sUP** es una aplicación web integral desarrollada con Django, diseñada para centralizar y optimizar la gestión de un negocio. Desde el manejo de inventario y ventas hasta la programación de agenda y reportes inteligentes, sUP provee una solución robusta y escalable.

## 🎥 Video Demostración

Haz clic en la siguiente imagen para ver una demostración completa de la aplicación en YouTube.

<a href="https://youtu.be/j_9BkCQYhQA" target="_blank" title="Haz clic para ver el video en YouTube">
  <img src="https://img.youtube.com/vi/j_9BkCQYhQA/hqdefault.jpg" alt="Demostración de la Agenda de Citas en YouTube" style="max-width: 600px; border: 1px solid #ddd; border-radius: 4px; padding: 5px;">
</a>

<p align="center">
  <strong>O visita el enlace directo:</strong> <a href="https://youtu.be/j_9BkCQYhQA">https://youtu.be/j_9BkCQYhQA</a>
</p>

---

## ✨ Características Principales

El proyecto está organizado en las siguientes aplicaciones, cada una enfocada en un área funcional clave:

*   **Usuarios:** Gestión completa de autenticación, perfiles y suscripciones de usuarios.
*   **Agenda:** Permite agendar y gestionar clientes y proveedores, optimizando el contacto y seguimiento.
*   **Stock:** Control detallado de inventario, incluyendo productos, categorías, proveedores y precios.
*   **Venta:** Módulo para registrar y administrar todas las transacciones de venta.
*   **Reporte:** Generación de reportes y análisis de datos para la toma de decisiones.
*   **IA:** Integra funcionalidades de inteligencia artificial para ofrecer insights y automatizar tareas.
*   **Core:** Contiene la lógica de negocio principal y funcionalidades compartidas a través de la aplicación.

---

## 🚀 Tech Stack

Este proyecto utiliza un conjunto de tecnologías modernas y eficientes para asegurar un rendimiento y escalabilidad óptimos.

*   **Backend:**
    *   ![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
    *   ![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)
    *   ![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
    *   ![WhiteNoise](https://img.shields.io/badge/WhiteNoise-FFFFFF?style=for-the-badge)

*   **Frontend:**
    *   ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
    *   ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
    *   ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
    *   ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
    *   ![jQuery](https://img.shields.io/badge/jQuery-3.7.1-0769AD?style=for-the-badge&logo=jquery&logoColor=white)
    *   ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

*   **Base de Datos:**
    *   ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) (Producción)
    *   ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white) (Caché)
    *   ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) (Desarrollo)

*   **Despliegue y DevOps:**
    *   ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

*   **Notificaciones:**
    *   ![Telegram](https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)

---

## 📦 Instalación y Puesta en Marcha

Puedes ejecutar este proyecto fácilmente utilizando Docker y Docker Compose.

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd sUP
    ```

2.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto basándote en el archivo `.env.example` (si existe) y añade las configuraciones necesarias, como las credenciales de la base de datos y las claves de API.

3.  **Construir y ejecutar con Docker Compose:**
    Este comando construirá las imágenes de los contenedores y los iniciará en segundo plano.
    ```bash
    docker-compose up --build -d
    ```

4.  **Aplicar migraciones de la base de datos:**
    Una vez que los contenedores estén en ejecución, aplica las migraciones de Django.
    ```bash
    docker-compose exec django python manage.py migrate
    ```

5.  **Crear un superusuario (opcional):**
    ```bash
    docker-compose exec django python manage.py createsuperuser
    ```

---

## ▶️ Uso

Una vez completada la instalación, la aplicación estará disponible en:

*   **URL:** `http://localhost:8000`
*   **Admin:** `http://localhost:8000/admin`

Puedes acceder con las credenciales del superusuario que creaste.

---
Powered by sUP