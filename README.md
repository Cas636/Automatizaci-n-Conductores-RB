# Automatización de Vinculación de Conductores con Selenium

Este script automatiza el proceso de registro de conductores en un sistema web utilizando Selenium y datos de un archivo Excel.

## Requisitos Previos

### Instalación de Dependencias

1. Asegúrate de tener **Python** instalado en tu sistema.
2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate     # En Windows
   ```
3. Instala las dependencias requeridas:
   ```bash
   pip install selenium pandas openpyxl
   ```
4. Descarga e instala el [WebDriver de Chrome](https://sites.google.com/chromium.org/driver/).

### Archivo Excel con Datos

El script requiere un archivo Excel llamado **`tabla.xlsx`** en la misma carpeta que el script. Este archivo debe contener los datos de los conductores a vincular, sin encabezados.

## Uso

Ejecuta el script con el siguiente comando:

```bash
python Conductores.py
```

El script:

- Abre el navegador y accede al sistema.
- Inicia sesión con usuario y contraseña.
- Navega a la sección de registro de conductores.
- Lee los datos del archivo Excel y completa los formularios.
- Guarda la información y repite el proceso para cada conductor.
- Cierra el navegador al finalizar.

## Notas

- **Credenciales**: Modifica el usuario y la contraseña en el script antes de ejecutarlo.
- **Velocidad de ejecución**: Se incluyen `time.sleep()` para evitar errores por carga de la página, pero pueden ajustarse según sea necesario.
- **Manejo de errores**: Se capturan excepciones para continuar con la ejecución si hay errores en algunas filas del Excel.



## Licencia

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license.

You are free to:

Share — copy and redistribute the material in any medium or format.

Adapt — remix, transform, and build upon the material.

Under the following terms:

Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

NonCommercial — You may not use the material for commercial purposes.

ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

Read more about this license at CC BY-NC-SA 4.0.
