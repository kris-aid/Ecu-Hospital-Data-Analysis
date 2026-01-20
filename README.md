# MSP - DATA 
Este repositorio contiene scripts para tratar informacion de  hospitales del ministerio de salud publica del ecuador

# Estructura del repositorio
- `data/`: Carpeta que contiene los datos en bruto y los datos procesados.
- `scripts/`: Carpeta que contiene los scripts de Python para el procesamiento de datos.(vacia)
- `notebooks/`: Carpeta que contiene notebooks de Jupyter para análisis exploratorio y visualización de datos.
- `README.md`: Este archivo de documentación.
- requirements.txt: Archivo que lista las dependencias del proyecto.

# Instrucciones para ejecutar los scripts
1. Clona este repositorio a tu máquina local.
2. Navega a la carpeta del proyecto.
3. Instala las dependencias listadas en `requirements.txt` usando pip:
   ```
   pip install -r requirements.txt
   ```
4. Coloca los archivos de datos que te pasamos en el zip en la carpeta `data/`
5. Ejecuta el notebook `notebooks/msp_geo.ipynb` para realizar visualizaciones
6. Si vas a crear nuevos scripts, colocalos en la carpeta `scripts/` y asegúrate de que funcionen correctamente.
7. Si tienes notebooks adicionales, colocalos en la carpeta `notebooks/`.
8. Asegúrate de documentar cualquier cambio que hagas en este archivo `README.md`.
9. Si están en visual studio code, les recomiendo instalar la extension: "DataWrangler" para poder visualizar los dataframes. Es más util que hacer prints en el propio Jupiter ;)

# Investigacion
##  Base sistema de salud

Base completa (solca,msp, etc) Tiene 6 gb de datos
###  prevalencia

fecha clase, canton, parroquia, # egresos totales,#mortaildad total, antes de las 48 , despues, dias de estancia,# de metabolicos ( que sea la sumatoria de los sindromes metabolicos), diabetes, hipertension, infarto


## Base MSP

Es la que es solo del msp. Tiene 3 gb de datos

### prevalencia

En esta base ya tenie limpio el cau221
Hay que ver el cie100
### eficiencia 
Andres tiene esto para hacer paneles
### combinado
Esta va a relacionar la prevalencia con la eficiencia. 

Juntar fecha clase, canton, parroquia, # egresos totales,#mortaildad total, mortaildad antes de las 48 ,mortaildad despues, dias de estancia, con numero de personal, gastos


