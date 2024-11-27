from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Edge()
driver.get('https://portal.barranquilla.gov.co:8181/ConsultaEstadoCuenta/consultaPlaca')
driver.find_element(By.ID,'form:hora').send_keys('HGP937')
driver.find_element(By.ID,'form:btnIngresar').click()

#physical_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'form:tblfisicos_data'))).text
electronic_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'form:tblelectronicos_data'))).text

ticket_info = []
ticket_row = 0

while True:
    try:
        ticket_html_id = f'form:tblelectronicos:{ticket_row}:j_idt46'
        
        ticket_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ticket_html_id)))
        ticket_element.click()

        ticket_details_modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'form:j_idt89')))
        print(f"Details for ticket {ticket_row}:", ticket_details_modal.text)

        ticket_info.append(ticket_details_modal.text)
        
        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ui-dialog-titlebar-close")))
        driver.execute_script("arguments[0].click();", close_button)
        #close_button = driver.find_element(By.CSS_SELECTOR, "a.ui-dialog-titlebar-close")
        #Wclose_button.click()

        WebDriverWait(driver, 10).until_not(EC.visibility_of_element_located((By.ID, 'form:j_idt89')))

        ticket_row += 1
        
    except Exception as e:
        print(f"Stopping at ticket {ticket_row}: {e}")
        break

driver.quit()

df = pd.DataFrame(ticket_info, columns=['Ticket Details'])
print(df)
