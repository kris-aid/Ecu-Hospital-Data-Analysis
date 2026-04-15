# Documentación de Transformación y Enriquecimiento de Datos

Este documento detalla el pipeline de procesamiento aplicado a la base de egresos hospitalarios. El objetivo es la estandarización de variables clínicas y la georreferenciación de registros a nivel parroquial.

## 🛠️ Tecnologías Utilizadas
- **Procesamiento de Datos:** `Polars` (Core) y `Pandas`.
- **Análisis Geoespacial:** `GeoPandas` y `Shapely`.
- **Similitud de Texto:** `RapidFuzz` (algoritmos `token_set_ratio` y `token_sort_ratio`).
- **Coordenadas:** Proyección WGS84 (EPSG:4326).

---

## 📊 Diccionario de Columnas Generadas

### 1. Variables Clínicas y Demográficas

#### `edad_std` (Float64)
* **Descripción:** Edad del paciente estandarizada en años decimales.
* **Lógica:** Convierte unidades mixtas basándose en la columna `cod_edad`:
    * **Horas:** $Edad / 24 / 365.25$
    * **Días:** $Edad / 365.25$
    * **Meses:** $Edad / 12$
    * **Años:** Valor original.
* **Propósito:** Habilitar análisis estadísticos continuos sobre la edad.

#### `cau221rx_std` (String)
* **Descripción:** Descripción normalizada de la causa de muerte (Lista 221).
* **Lógica:** Reemplazo mediante diccionario manual para corregir inconsistencias de formato y errores tipográficos.
* **Propósito:** Unificar categorías para agrupaciones precisas.

#### `cau_cie10_std` (String)
* **Descripción:** Diagnóstico estandarizado que incluye Nombre + Código CIE-10.
* **Lógica:** 1.  **Limpieza de Encoding:** Corrección de caracteres corruptos (mojibakes) como `A" -> O` o `"` -> `O` en nombres clínicos.
    2.  **Extracción de Código:** Regex para identificar códigos alfanuméricos (ej: `E11`, `I10`).
    3.  **Fuzzy Matching:** Para descripciones sin código, se comparó contra un catálogo canónico (umbral $\ge 90\%$).
* **Propósito:** Asegurar la integridad de la clasificación internacional de enfermedades.

#### `sindrome_metabolico` (Int8)
* **Descripción:** Flag binario (1: Sí, 0: No) para pacientes con sospecha de síndrome metabólico.
* **Lógica:** Búsqueda concurrente de patrones en texto y códigos:
    * **Diabetes:** `E1[0-4]|O24`
    * **Hipertensión:** `I1[0-5]`
    * **Obesidad:** `E66` o texto "OBES".
* **Propósito:** Segmentación epidemiológica rápida.

---

### 2. Localización y Georreferenciación

#### `code_parroquia_ubi` / `code_parroquia_res` (String)
* **Descripción:** Código oficial DPA (INEC) de la parroquia de ocurrencia y residencia.
* **Lógica de Match:**
    1.  **Limpieza:** Remoción de *Stop Words* geográficas (ej: "CANTON", "PARROQUIA", "D.M.").
    2.  **Deduplicación:** Priorización de registros con código SRI sobre nulos en el catálogo de referencia.
    3.  **Cascada:** Cruce exacto $\rightarrow$ Fallback a Fuzzy Match ($\ge 80\%$).
* **Propósito:** Llave primaria para cruce con bases de datos administrativas.

#### `lat_ubi`, `lon_ubi` / `lat_res`, `lon_res` (Float64)
* **Descripción:** Coordenadas decimales del centroide de la parroquia.
* **Lógica:** 1.  **Mapeo Electoral-Administrativo:** Vinculación de códigos CONALI/CNE (antiguos) a Códigos INEC (actuales) mediante la tabla de equivalencias del proyecto "Así votamos los ecuatorianos 2023".
    2.  **Cálculo Espacial:** Extracción de centroides de polígonos del shapefile CONALI 2024.
* **Propósito:** Habilitar mapas de calor y análisis de distancias residencia-hospital.

---

## 📂 Archivos de Referencia Necesarios
- `mapping_cie10.txt`: Diccionario para la estandarización de diagnósticos.
- `std_parroquias.csv`: Tabla de cruce de códigos CNE a códigos INEC.
- `inec_parroquias`: Catálogo DPA oficial del Ecuador. Es la correspondencia entre SRI e INEC
- `conali_parroquias_shape`: Cartografía oficial de límites internos. (Solicitar a la interna del datahub)

## ⚙️ Notas de Mantenimiento
Para evitar la duplicación de registros (explosión de filas) en los procesos de `merge`, siempre se debe limpiar el catálogo de referencia utilizando `.drop_duplicates(subset=["code_parroquia"])` antes de la unión con la base principal.