from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import unicodedata

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

driver = webdriver.Edge()
driver.get('https://portal.barranquilla.gov.co:8181/ConsultaEstadoCuenta/consultaPlaca')
driver.find_element(By.ID,'form:hora').send_keys('HGP937')
driver.find_element(By.ID,'form:btnIngresar').click()

#physical_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'form:tblfisicos_data'))).text
electronic_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'form:tblelectronicos_data'))).text
print(electronic_results)

ticket_info = []
ticket_row = 0

while True:
    try:
        ticket_html_id = f'form:tblelectronicos:{ticket_row}:j_idt46'
        
        ticket_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ticket_html_id)))
        ticket_element.click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'form:j_idt89')))
        
        ticket_details_panel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'form:paneldetalle2E')))

        ticket_info.append(ticket_details_panel.text)
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="form:j_idt89"]/div[1]/a'))).click()

        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.ID, 'form:j_idt89')))
        driver.switch_to.default_content()

        ticket_row += 1
        
    except Exception as e:
        print(f"Stopping at ticket {ticket_row}: {e}")
        break

driver.quit()

parsed_data = []

for ticket in ticket_info:
    ticket_data = {}
    lines = ticket.split("\n")
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1) 
            ticket_data[normalize_text(key).strip()] = normalize_text(value).strip()
    parsed_data.append(ticket_data)

json_file = "HGP937_tickets.json"
with open(json_file, "w") as f:
    json.dump(parsed_data, f, indent=4, ensure_ascii=False)
print(f"JSON file saved as {json_file}")
