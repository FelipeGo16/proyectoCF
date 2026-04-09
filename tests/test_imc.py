import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def escribir_lento(elemento, texto, delay=0.15):
    for c in texto:
        elemento.send_keys(c)
        time.sleep(delay)

casos = [
    {"nombre": "Bajo peso", "peso": "45", "estatura": "1.75"},
    {"nombre": "Peso normal", "peso": "70", "estatura": "1.75"},
    {"nombre": "Sobrepeso", "peso": "85", "estatura": "1.75"},
    {"nombre": "Obesidad", "peso": "110", "estatura": "1.75"},
]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

for caso in casos:
    print(f"\n🔹 Caso: {caso['nombre']}")

    # 🔥 ENTRAR DIRECTO A LA VISTA (EVITA NAVBAR Y ERRORES)
    driver.get("http://127.0.0.1:5000/calcular")

    # Esperar inputs
    peso_input = wait.until(EC.presence_of_element_located((By.NAME, "peso")))
    estatura_input = wait.until(EC.presence_of_element_located((By.NAME, "estatura")))

    # Escribir lento
    escribir_lento(peso_input, caso["peso"])
    escribir_lento(estatura_input, caso["estatura"])

    # Click
    boton = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Calcular')]"))
    )
    boton.click()

    # 🔥 ESPERAR QUE CAMBIE EL RESULTADO
    resultado = wait.until(
        EC.visibility_of_element_located((By.ID, "resultado-imc"))
    )

    print("Resultado mostrado:", resultado.text)

    time.sleep(2)

driver.quit()