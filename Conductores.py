from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from datetime import datetime
import time

# Iniciar el navegador
driver = webdriver.Chrome()

# Abrir la página de inicio de sesión
driver.get("http://10.80.15.13:17050/#/login")
driver.maximize_window()

# Esperar y encontrar los campos de usuario y contraseña
wait = WebDriverWait(driver, 10)
usuario_input = wait.until(EC.presence_of_element_located((By.ID, "user-id")))
contraseña_input = wait.until(EC.presence_of_element_located((By.ID, "user-pw")))

# Ingresar usuario y contraseña
usuario_input.send_keys("JCASTANO")
contraseña_input.send_keys("PASSWORD")

# Hacer clic en "Ingresar"
boton_ingresar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-login")))
boton_ingresar.click()
time.sleep(2)
# Esperar cambio de ventana y cambiar a la nueva
wait.until(lambda d: len(d.window_handles) > 1)
ventana_original = driver.current_window_handle
for ventana in driver.window_handles:
    if ventana != ventana_original:
        driver.switch_to.window(ventana)
        break


# Esperar y hacer clic en "Recursos"
recursos = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@class='dep-1']/a/span[text()='Recursos']")))
recursos.click()
wait = WebDriverWait(driver, 3)

# Esperar y hacer clic en "Conductor"
conductor = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Conductor')]")))
conductor.click()

# Cargar el archivo Excel
archivo_excel = "tabla.xlsx"  # Ruta del archivo
df = pd.read_excel(archivo_excel, header=None)  # Leer sin encabezados

# Iterar sobre cada fila del archivo Excel
for indice, fila in df.iterrows():
    if len(fila) > 12:
        try:
            # Buscar y llenar "Número de Documento"
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Número de Documento']")))

            input_numero_documento = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Número de Documento']/following::input[1]")
            ))
            input_numero_documento.clear()
            time.sleep(1)
            input_numero_documento.send_keys(str(fila.iloc[1]) + Keys.ENTER)
            time.sleep(1)
            script = '''let element = document.querySelector('[row-index=\"0\"]').click();
if (element) {
    let event = new MouseEvent("click", { bubbles: true, cancelable: true, view: window });
    element.dispatchEvent(event);
} else {
    console.log("Elemento no encontrado");
}'''
            result = driver.execute_script(script)

            
            # **Intentar hacer clic en "Crear Registro"**
            try:
                crear = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='comp-btn-area']//button[@class='btn-create']")))
                crear.click()
            except:
                print(f"⚠️ Fila {indice}: No se encontró el botón 'Crear Registro'. Se omite esta fila.")
                continue  # Salta a la siguiente fila
            time.sleep(1)
            # Llenar "Concesionario de Operación"
            input_element_conce = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@aria-placeholder='Concesionario de Operación']")))
            input_element_conce.clear()
            input_element_conce.send_keys(f"({fila.iloc[5]})" + Keys.ENTER)

            # Llenar "Número de Registro"
            time.sleep(0.1)
            try:
                input_numero_registro = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Número de registro']/following-sibling::div//input")))
                input_numero_registro.clear()
                input_numero_registro.send_keys(f"{fila.iloc[6]}")
            except:
                print(f"⚠️ Fila {indice}: No se encontró el espacio para ingresar el codigo de operador")
                
        
            time.sleep(0.1)
            # Llenar "Tipo de Vehículo"
            div_tipo_vehiculo = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Tipo de Vehículo')]/following-sibling::div//input")))
            div_tipo_vehiculo.clear()
            div_tipo_vehiculo.send_keys(f"({fila.iloc[9]})" + Keys.ENTER)
            time.sleep(0.1)
            # Llenar "Fecha de Registro"
            #fecha_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Fecha de Registro')]/following-sibling::div//input")))
            


            # Convertir fecha de 'YYYYMMDDHHMMSS' a 'DD/MM/YYYY HH:MM:SS'
            fecha_raw = str(fila.iloc[12])
            fecha_obj = datetime.strptime(fecha_raw, "%Y%m%d%H%M%S")
            
            meses_mapeo = {
                "jan": "ene", "feb": "feb", "mar": "mar", "apr": "abr",
                "may": "may", "jun": "jun", "jul": "jul", "aug": "ago",
                "sep": "sept", "oct": "oct", "nov": "nov", "dec": "dic"
            }
            
            mes_en_ing = fecha_obj.strftime("%b").lower()  # Ej: 'mar'
            mes = meses_mapeo[mes_en_ing]  # Traducción


            dia = fecha_obj.day
            año = fecha_obj.year
            hora_completa = fecha_obj.strftime("%H:%M:%S")
                        
                        
                        
            # Hacer clic en el campo de fecha para abrir el calendario
            date_picker = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Fecha de Registro')]/following-sibling::div//input")))
            date_picker.click()
            time.sleep(0.1)
            
            
            # Seleccionar el año
            año_boton =  WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH,  "//div[@role='button' and @aria-label='Open years overlay']"))
            )
            año_boton.click()
            time.sleep(1)
            # Buscar el elemento que contiene el año deseado y hacer clic
            xpath_anio = f"//div[@role='gridcell' and @data-test='{año}']"
            year_button = driver.find_element(By.XPATH, xpath_anio)
            year_button.click()
            time.sleep(1)

    
            # Seleccionar el mes
            mes_boton = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Open months overlay']"))
            )
            mes_boton.click()
            time.sleep(1)


            month_button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[@role='gridcell'][@data-test='{mes}']"))
            )
            month_button.click()
            
            time.sleep(1)
            
            

            # Seleccionar el día
            day_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class, 'dp__cell_inner') and contains(@class, 'dp__pointer') and text()='{dia}']")
            ))
            day_button.click()
            time.sleep(0.1)
            
            
            confirm_button = driver.find_element(By.XPATH, "//button[@class='dp__action_button dp__action_select']")
            confirm_button.click()
            time.sleep(0.1)
            
            for _ in range(8):  # Se ejecuta 8 veces
                date_picker.send_keys(Keys.BACKSPACE)
            time.sleep(0.1)
            
            date_picker.send_keys(hora_completa+Keys.ENTER)
            
            time.sleep(1)

                        
            # Clic en "Guardar"
            guardar = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-save")))
            guardar.click()
            time.sleep(2)

        except Exception as e:
            print(f"⚠️ Error en la fila {indice}: {str(e)}")

    else:
        print(f"⚠️ Fila {indice}: No tiene suficientes columnas")

# Cerrar el navegador
driver.quit()
