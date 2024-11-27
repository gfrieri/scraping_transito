from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

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
        
        # Wait for the ticket to be clickable
        ticket_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ticket_html_id)))
        ticket_element.click()

        # Wait for the ticket details modal to load
        ticket_details_modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-dialog-content')))
        print(f"Details for ticket {ticket_row}:", ticket_details_modal.text)

        # Append the modal content to the list
        ticket_info.append(ticket_details_modal.text)

        # Close the modal by clicking the "X" button
        close_button = driver.find_element(By.CLASS_NAME, 'ui-icon ui-icon-closethick')
        close_button.click()

        # Wait briefly before processing the next ticket
        WebDriverWait(driver, 1)
        
        # Increment the row index
        ticket_row += 1
        
    except Exception as e:
        print(e)
        break

driver.quit()

# Convert the list of ticket details to a DataFrame
df = pd.DataFrame(ticket_info, columns=['Ticket Details'])
print(df)
