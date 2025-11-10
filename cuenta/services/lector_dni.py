import cv2
import pytesseract
import re
from django.conf import settings
from datetime import datetime
from pathlib import Path
import numpy as np
import os
from django.utils import timezone


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#Definimos la funcion y le pasamos como argumento una imagen que puede ser un str o un Path y le indicamos que devuelve un diccionario.
def lector_mrz(image_path: str | Path) -> dict:

#leemos la imagen con el procesador de imagenes y le decimos que si no existe lance el error FileNotFoundError acompañados de ese mensaje.
    img = cv2.imread(str(image_path.resolve()))
    if img is None:
        print(image_path)
        raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")

#obtenemos el alto y ancho de la imagen.
    h, w = img.shape[:2]

# Recortar MRZ: último 30% de la imagen
    y0 = int(h * 0.70)
    mrz_roi = img[y0:h, 0:w]

    # Hace la escala de grises
    bw = cv2.cvtColor(mrz_roi, cv2.COLOR_BGR2GRAY) #gray

    # Redimensiona (recorta) para mejorar la precision del OCR
    bw = cv2.resize(bw, None, fx=1.3, fy=2, interpolation=cv2.INTER_LINEAR)

    # Configuración Tesseract
    config = "--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"
    
    """
    --oem (0-3): Define el motor OCR que utilizara tesseract.     Usamos el 3 que elige el mejor modelo posible ( generalmente es el 1, que es una red neural LSTM OCR, es moderno y entrenado con deep learning)
    
    --psm (0-13): Indica cómo interpretar la estructura del texto.     Usamos 6 que interpreta como bloque de texto sin uniforme.

    -c: permite setear los parametros y configuraciones generales del tesseract.   ej: caracteres permitidos(whitelist), caracteres prohibidos (blacklist), guardar imagenes intermedias para debug (tessedit_write_image), solo numeros o configurar sensibilidad, DPI, etc.
    """


    # Ejecutamos el OCR (procesador de texto) para que "lea" nuestra imagen
    texto = pytesseract.image_to_string(bw, config=config, lang="eng")
    
    #guardamos las lineas separadas y eliminamos vacios.
    lineas = [l for l in texto.splitlines() if l.strip()]

    # 1️⃣ Número de DNI: línea 1, posición 5-14
    dni_match = re.search(r'ARG(\d{8})', lineas[0]) if len(lineas) > 0 else None  #En la primera linea, Buscamos 8 digitos luego de la palabra ARG. Ademas validamos si existe la primera linea

    dni = dni_match.group(1) if dni_match else None #Si se encuentra algo, devuelve solo los digitos luego del "ARG". si no encuentra nada, devuelvo none.

    # 2️⃣ Fechas: línea 2, nacimiento y vencimiento (YYMMDD)
    fechas = re.search(r'\d{6}', lineas[1]) if len(lineas) > 1 else None #Buscamos los primeros 6 digitos (basandonos en el MRZ es el nacimiento.) Ademas validamos si existe la segunda linea.
    fecha_v = re.search(r'[MF](\d{6})', lineas[1]) if len(lineas) > 1 else None #Buscamos los 6 digitos luego de una letra M o F (Muestra genero en MRZ)

    #Convertimos las fechas a formato humano (DD/MM/YYYYY)
    fecha_nac = datetime.strptime(fechas.group(0), "%y%m%d").strftime("%d/%m/%Y") if fechas else None
    fecha_venc = datetime.strptime(fecha_v.group(1), "%y%m%d").strftime("%d/%m/%Y") if fecha_v else None

    # 3️⃣ Nombre y apellido: línea 3
    nombre_raw = lineas[2].replace("<", " ").strip() if len(lineas) > 2 else None #Reemplazamos los "<" por espacios y posteriormente los eliminamos. Ademas validamos la existencia de la tercera linea

    return {
        "numero_dni": dni,
        "fecha_nacimiento": fecha_nac,
        "fecha_vencimiento": fecha_venc,
        "nombre": nombre_raw,
    } #Devolvemos todo en un diccionario organizado.



def lector_mrz_sombras(image_path: str | Path) -> dict:

#leemos la imagen con el procesador de imagenes y le decimos que si no existe lance el error FileNotFoundError acompañados de ese mensaje.
    img = cv2.imread(str(image_path.resolve()))
    if img is None:
        raise FileNotFoundError(f"No se pudo encontrar la imagen en {image_path}")

#obtenemos el alto y ancho de la imagen.
    h, w = img.shape[:2]

# Recortar MRZ: último 30% de la imagen
    y0 = int(h * 0.70)
    mrz_roi = img[y0:h, 0:w]

    # Escalado de grises
    gray = cv2.cvtColor(mrz_roi, cv2.COLOR_BGR2GRAY)

    #Funcion con cadenas de mejoras especificas para el MRZ
    def preprocess_mrz(image):
        # 1. Reducción de ruido, mantiene bordes y controla la intensidad.
        denoised = cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
        
        # 2. clahe que mejora el constraste.
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(4,4))
        enhanced = clahe.apply(denoised)
        
        # 3. Eliminación de sombras con manipulacion de sombras.    Este punto puede pasarse de iluminacion cuando la imagen esta bien iluminada.
        background = cv2.medianBlur(enhanced, 15)
        shadow_free = cv2.addWeighted(enhanced, 1.5, background, -0.5, 0)
        
        # 4. Binarización especializada para texto de máquina
        def mrz_binarization(img):
            # Suavizado muy ligero
            smoothed = cv2.GaussianBlur(img, (1, 1), 0)
            
            # Convierte a blanco y negro localmente (pensado para iluminacion no uniforme)
            binary = cv2.adaptiveThreshold(
                smoothed, 
                255, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 
                11,    # Valores pensados para texto pequeño.
                3      
            )
            
            return binary
        binary = mrz_binarization(shadow_free)
        
        # 5. Limpieza MORFOLÓGICA E
        # Kernel horizontal (el texto MRZ es horizontal)
        kernel_horizontal = np.ones((1, 3), np.uint8)
        kernel_vertical = np.ones((2, 1), np.uint8)
        
        # Operaciones para conectar caracteres rotos
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_horizontal) #Conecta caracteres rotos en una linea
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_vertical) #Elimina carcteres de ruido.
        
        # 6. Borra elementos muy pequeños (manchas,ruido), rellenando con negro.
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 5:  # Eliminar elementos muy pequeños
                cv2.drawContours(binary, [cnt], 0, 0, -1)
        
        return binary
    
    #Aplica todo el preprocesamiento para sombras.
    bw = preprocess_mrz(gray)

    #Re-escala la imagen para agrandar los caracteres.
    bw_scaled = cv2.resize(bw, None, fx=1.3, fy=2, interpolation=cv2.INTER_CUBIC)

    # Configuración Tesseract.
    config = ("--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<"
    " -c tessedit_do_invert=0"  # No invertir el fondo de imagen
    "-c load_system_dawg=0 -c load_freq_dawg=0" ) #Desactiva diccionarios, evita que intente adivinar palabras.  

    # Ejecutamos el OCR (procesador de texto) para que "lea" nuestra imagen
    texto = pytesseract.image_to_string(bw_scaled, config=config, lang="eng")
    
    #guardamos las lineas separadas y eliminamos vacios.
    lineas = [l for l in texto.splitlines() if l.strip()]


    # 1️⃣ Número de DNI: línea 1, posición 5-14
    dni_match = re.search(r'ARG(\d{8})', lineas[0]) if len(lineas) > 0 else None  #En la primera linea, Buscamos 8 digitos luego de la palabra ARG. Ademas validamos si existe la primera linea

    dni = dni_match.group(1) if dni_match else None #Si se encuentra algo, devuelve solo los digitos luego del "ARG". si no encuentra nada, devuelvo none.

    # 2️⃣ Fechas: línea 2, nacimiento y vencimiento (YYMMDD)
    fechas = re.search(r'\d{6}', lineas[1]) if len(lineas) > 1 else None #Buscamos los primeros 6 digitos (basandonos en el MRZ es el nacimiento.) Ademas validamos si existe la segunda linea.
    fecha_v = re.search(r'[MF](\d{6})', lineas[1]) if len(lineas) > 1 else None #Buscamos los 6 digitos luego de una letra M o F (Muestra genero en MRZ)

    #Convertimos las fechas a formato humano (DD/MM/YYYYY)
    fecha_nac = datetime.strptime(fechas.group(0), "%y%m%d").strftime("%d/%m/%Y") if fechas else None
    fecha_venc = datetime.strptime(fecha_v.group(1), "%y%m%d").strftime("%d/%m/%Y") if fecha_v else None

    # 3️⃣ Nombre y apellido: línea 3
    nombre_raw = lineas[2].replace("<", " ").strip() if len(lineas) > 2 else None #Reemplazamos los "<" por espacios y posteriormente los eliminamos. Ademas validamos la existencia de la tercera linea

    return {
        "numero_dni": dni,
        "fecha_nacimiento": fecha_nac,
        "fecha_vencimiento": fecha_venc,
        "nombre": nombre_raw,
    } #Devolvemos todo en un diccionario organizado.


#Convierte los datos leidos del ocr a los tipos de datos que trae Django.
def normalizar_datos(datos_leidos: dict ) -> dict:

    fecha_nac = datos_leidos.get("fecha_nacimiento")
    
    if fecha_nac:
        datos_leidos["fecha_nacimiento"] = datetime.strptime(fecha_nac, "%d/%m/%Y").date()
    else:
        datos_leidos["fecha_nacimiento"] = None

    fecha_venc = datos_leidos.get("fecha_vencimiento")
    if fecha_nac:
        datos_leidos["fecha_vencimiento"] = datetime.strptime(fecha_venc, "%d/%m/%Y").date()
    else:
        datos_leidos["fecha_vencimiento"] = None
    
    return datos_leidos

def crear_ruta(imagen, usuario):
    if hasattr(imagen, "temporary_file_path"):
        ruta = Path(imagen.temporary_file_path())
        
    else:
        os.makedirs(f"{settings.MEDIA_ROOT}/tmp/{usuario}", exist_ok=True)
        ruta = f"{settings.MEDIA_ROOT}/tmp/{usuario}/{imagen.name}"
        with open(ruta , "wb") as f:
            for chunk in imagen.chunks():
                f.write(chunk)
    return Path(ruta)

def validador(datos_form, datos_leidos):
    nombre_leido = (datos_leidos.get("nombre") or "").upper()
    nombre_leido = " ".join(nombre_leido.split())  # quita espacios múltiples

    apellido = (datos_form.get("last_name") or "").strip().upper()
    nombre = (datos_form.get("first_name") or "").strip().upper()

    # Condición flexible: ambos deben estar presentes en el texto leído
    coincide_nombre = apellido in nombre_leido and nombre in nombre_leido

    if (
        coincide_nombre  and
        (datos_leidos.get("numero_dni") or "") == (datos_form.get("numero_dni") or "") and
        datos_leidos.get("fecha_nacimiento") == datos_form.get("fecha_nacimiento") and
        datos_leidos.get("fecha_vencimiento") > timezone.localdate()
        ):

        print("✅ Éxito: Todos los datos son correctos")
        return True
    else:
        print("❌ Error: Los datos ingresados no coinciden con lo leido. Vuelva a intentarlo.")
        return False


def lector_total(request, form):
    usuario = request.POST.get("username")
    imagen = request.FILES["foto_dni"]
    datos_form = form.cleaned_data
    image_path = crear_ruta(imagen, usuario)
    resultado = lector_mrz(image_path)
    # Validar datos
    """
    resultado.values()  Devuelve los valores por separa de resultado.
    for j in resultado.values()     Recorre los valores de resultado y los guarda en j.
    j i None.   Devuelve True si j es None. y al contrario. Esto devulve una lista con todos los elementos en su sinonimo Booleano.
    any().  Devuelve True si uno de los elementos de esa lista es True. si no, devulve False y nunca entrara en el if.
    """
    if any(j is None for j in resultado.values()):
        print("!!!OCR incompleto, usando lector de sombras...")
        resultado = lector_mrz_sombras(image_path)
        if any(j is None for j in resultado.values()):
            return None
    datos_normalizados = normalizar_datos(resultado)
    # print(f"datos NORMALIZADOS: {datos_normalizados}")
    # print(f"datos INGRESADOS: {datos_form}")
    datos_validados = validador(datos_form, datos_normalizados)
    print(f"DATOS COINCIDEN: {datos_validados} ")
    if datos_validados:
        return datos_validados
    else:
        return datos_validados