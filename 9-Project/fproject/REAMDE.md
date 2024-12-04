# Student Resource Manager

## Descripción

Student Resource Manager es una plataforma web diseñada para ayudar a los estudiantes a organizar, gestionar y acceder a sus recursos académicos de manera eficiente. Los usuarios pueden subir archivos, categorizarlos, buscar contenido específico, gestionar tareas mediante un calendario interactivo y obtener resúmenes automáticos y tests de repaso basados en sus archivos.

## Características Principales

- **Autenticación de Usuarios**: Registro y inicio de sesión seguro.
- **Carga y Gestión de Archivos**: Soporte para múltiples tipos de archivos con organización por etiquetas.
- **Motor de Búsqueda Avanzado**: Búsqueda por nombre, etiquetas y contenido.
- **Calendario Interactivo**: Gestión de tareas y eventos académicos.
- **Resumenes Automáticos**: Generación de resúmenes de documentos.
- **Tests de Repaso**: Cuestionarios automáticos basados en el contenido de los archivos.
- **Previsualización de Archivos**: Visualización directa en el navegador.

## Distinción y Complejidad

Este proyecto se distingue de los demás proyectos del curso por su enfoque integral en la organización académica, combinando múltiples funcionalidades avanzadas como búsqueda por contenido, generación de resúmenes automáticos y tests de repaso. La integración de tecnologías como FullCalendar.js para la gestión de eventos y librerías de procesamiento de lenguaje natural para los resúmenes y tests agrega una capa de complejidad significativa, asegurando que el proyecto sea más robusto y útil que los ejemplos proporcionados en el curso.

## Estructura del Proyecto

- **student_resource_manager/**: Directorio principal del proyecto Django.
  - **settings.py**: Configuraciones del proyecto.
  - **urls.py**: Rutas principales del proyecto.
- **resources/**: Aplicación principal para la gestión de recursos.
  - **models.py**: Definición de los modelos `File` y `Event`.
  - **views.py**: Vistas para manejar la lógica de carga, búsqueda y gestión de archivos.
  - **templates/**: Plantillas HTML para las diferentes páginas.
  - **static/**: Archivos estáticos como CSS y JavaScript.
- **templates/**: Plantillas globales del proyecto.
- **requirements.txt**: Lista de dependencias de Python.

## Instalación y Uso

### Prerrequisitos

- Python 3.8+
- pip
- PostgreSQL (opcional, SQLite por defecto)

### Pasos de Instalación

1. **Clonar el Repositorio**:

    ```bash
    git clone https://github.com/tu_usuario/student_resource_manager.git
    cd student_resource_manager
    ```

2. **Crear un Entorno Virtual**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. **Instalar Dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configurar la Base de Datos**:

    - Edita `settings.py` para configurar PostgreSQL si lo prefieres.
    - Ejecuta migraciones:

      ```bash
      python manage.py makemigrations
      python manage.py migrate
      ```

5. **Crear un Superusuario**:

    ```bash
    python manage.py createsuperuser
    ```

6. **Iniciar el Servidor de Desarrollo**:

    ```bash
    python manage.py runserver
    ```

7. **Acceder a la Aplicación**:

    - Ve a `http://localhost:8000/` en tu navegador.

## Tecnologías Utilizadas

- **Backend**: Django, Django ORM.
- **Frontend**: HTML, CSS (Bootstrap), JavaScript.
- **Librerías y APIs**:
  - FullCalendar.js para el calendario.
  - PDF.js para la previsualización de PDFs.
  - NLTK/spaCy para procesamiento de lenguaje natural.
  - Prism.js para resaltar sintaxis en archivos de programación.

## Consideraciones Adicionales

- **Seguridad**: Implementación de validaciones para la carga de archivos y protección de rutas.
- **Escalabilidad**: Diseño modular que facilita la adición de nuevas funcionalidades.
- **Despliegue**: Instrucciones para desplegar en plataformas como Heroku o AWS.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
