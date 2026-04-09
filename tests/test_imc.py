import time #Permite hacer pausas (sleep) para simular escritura humana
from selenium import webdriver #Controla el navegador (abre Chrome, navega, etc.).
from selenium.webdriver.common.by import By #Define cómo buscar elementos:By.ID, By.NAME y By.XPATH
from selenium.webdriver.chrome.service import Service #Configura el servicio del driver de Chrome
from selenium.webdriver.support.ui import WebDriverWait #Permiten esperar elementos dinámicamente (clave en Selenium)
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager #Descarga automáticamente el ChromeDriver

# ================================
# FUNCIONES
# ================================
#Simula que un humano escribe carácter por carácter
def escribir_lento(elemento, texto, delay=0.1):
    for c in texto:
        elemento.send_keys(c)
        time.sleep(delay)

#IMC = peso / estatura² ----- redondea a 2 decimales
def calcular_imc(peso, estatura):
    return round(peso / (estatura ** 2), 2)

def clasificar_imc(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"

# ================================
# CASOS DE PRUEBA
# ================================
casos = [
    {"peso": 45, "estatura": 1.75},
    {"peso": 70, "estatura": 1.75},
    {"peso": 85, "estatura": 1.75},
    {"peso": 110, "estatura": 1.75},
]

# ================================
# DRIVER
# ================================
#Abre Chrome automáticamente
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#Maximiza la ventana
driver.maximize_window()
#Espera hasta 10 segundos por elementos
wait = WebDriverWait(driver, 10)

# ================================
# PRUEBAS
# ================================
#Recorre todos los casos
for i, caso in enumerate(casos, start=1):
    print(f"\n🔹 Ejecutando caso #{i}")

    # Ir directamente a la vista
    driver.get("http://127.0.0.1:5000/calcular")
 
    #Extrae datos del caso
    peso = caso["peso"]
    estatura = caso["estatura"]

    # Calcular esperado
    imc_esperado = calcular_imc(peso, estatura)
    clasificacion_esperada = clasificar_imc(imc_esperado)

    # Inputs
    peso_input = wait.until(EC.presence_of_element_located((By.NAME, "peso")))
    estatura_input = wait.until(EC.presence_of_element_located((By.NAME, "estatura")))

    #Escribe lentamente los valores
    escribir_lento(peso_input, str(peso))
    escribir_lento(estatura_input, str(estatura))

    # Click
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(),'Calcular')]"))
    ).click()

    # Resultado
    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "resultado-imc"))
    ).text

    print("📊 Resultado UI:", resultado)
    print("📐 Esperado IMC:", imc_esperado)
    print("📌 Esperado Clasificación:", clasificacion_esperada)

    # ================================
    # VALIDACIONES (ASSERT)
    # ================================
    #Verifica que el IMC calculado esté en la pantalla
    assert str(imc_esperado) in resultado, f"❌ IMC incorrecto en caso {i}"
    #Verifica que la clasificación sea correcta
    assert clasificacion_esperada in resultado, f"❌ Clasificación incorrecta en caso {i}"

    print("✅ Caso aprobado")

    time.sleep(2)

# ================================
# FINAL
# ================================
print("\n🎉 TODOS LOS CASOS PASARON CORRECTAMENTE")
driver.quit()

"""
Este script hace:

Simula usuario real
Ejecuta múltiples pruebas
Calcula resultados esperados
Compara contra la UI
Detecta errores automáticamente
"""