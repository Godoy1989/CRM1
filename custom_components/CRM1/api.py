from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class EdistribucionAPI:
    def __init__(self, username, password, gecko_driver_path, firefox_binary_path):
        self.username = username
        self.password = password
        self.gecko_driver_path = gecko_driver_path
        self.firefox_binary_path = firefox_binary_path

    def get_instant_power(self):
        firefox_options = Options()
        firefox_options.headless = True  # Ejecutar en modo headless
        firefox_options.binary_location = self.firefox_binary_path

        service = Service(self.gecko_driver_path)
        driver = webdriver.Firefox(service=service, options=firefox_options)

        try:
            # Iniciar sesión
            driver.get("https://zonaprivada.edistribucion.com/areaprivada/s/login/?language=es")

            # Campos de inicio de sesión
            username_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "input-7"))
            )
            password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "input-8"))
            )
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "slds-button_brand"))
            )

            for char in self.username:
                username_input.send_keys(char)
                time.sleep(0.1)
            for char in self.password:
                password_input.send_keys(char)
                time.sleep(0.1)

            login_button.click()

            # Esperar a que cargue la página principal
            WebDriverWait(driver, 20).until(
                EC.title_is("Home")
            )

            # Navegar a la página de consumo
            driver.get("https://zonaprivada.edistribucion.com/consumption/current")

            # Hacer clic en "Consultar Contador"
            consult_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Consultar Contador']"))
            )
            consult_button.click()

            # Esperar al spinner
            WebDriverWait(driver, 300).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "slds-spinner_container"))
            )

            # Verificar estado del ICP
            tables = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "wp-table"))
            )
            icp_table = None
            for table in tables:
                if "estado del icp" in table.text.lower():
                    icp_table = table
                    break

            if not icp_table:
                raise Exception("No se encontró la tabla con el estado del ICP.")

            rows = icp_table.find_elements(By.TAG_NAME, "tr")
            icp_status = None
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 2 and "estado del icp" in cells[0].text.lower():
                    icp_status = cells[1].text.strip()
                    break

            if not icp_status or "conectado" not in icp_status.lower():
                raise Exception(f"ICP no está conectado. Estado: {icp_status}")

            # Extraer potencia instantánea
            description_elements = WebDriverWait(driver, 60).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "description"))
            )

            power_value = None
            for element in description_elements:
                if "potencia instantánea actual" in element.text.lower():
                    power_span = element.find_element(By.XPATH, ".//span")
                    power_text = power_span.text.strip()
                    power_value = power_text.split(" ")[0]  # Quedarse solo con el número
                    break

            if not power_value:
                raise Exception("No se pudo obtener la potencia instantánea.")

            return float(power_value)  # Devolver el valor como número

        except Exception as e:
            raise Exception(f"Error al obtener la potencia instantánea: {e}")
        finally:
            driver.quit()