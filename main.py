import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import time


def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    return df


def print_and_view_data(df):
    data = {}
    for column in df.columns:
        data[column] = df[column].tolist()

    for key, value in data.items():
        print(f"{key}: {value}")


def setup_chrome_options():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(r'--no-sandbox')
    return chrome_options


def init_chrome_driver(chrome_options):
    driver = uc.Chrome(options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    return driver, wait


def init_action_chains(driver):
    actions = ActionChains(driver)
    return actions


def open_address_validation_webpage(driver, url='https://www.smarty.com/products/single-address?street'):
    driver.get(url)
    driver.implicitly_wait(10)
    driver.execute_script("window.scrollBy(0, 1000);")


def switch_to_international_address_validation_tab(driver):
    international_tab_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'International')]")
    international_tab_btn.click()


def switch_to_US_address_validation_tab(driver):
    us_tab_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'US')]")
    us_tab_btn.click()


def interact_with_lookup_type_dropdown(driver, actions, down_arrow_presses):
    dropdown = driver.find_element(By.XPATH, "//div[@role='combobox' and contains(text(), 'Address Components')]")
    actions.move_to_element(dropdown).click().perform()
    # Press the down arrow key to navigate to the desired option
    for _ in range(down_arrow_presses):
        actions.send_keys(Keys.ARROW_DOWN).perform()
    # Press Enter to select the option
    actions.send_keys(Keys.ENTER).perform()


def find_US_input_elements__address_components(driver):
    us_address_line_1_input_field = driver.find_element(By.XPATH, "//input[@id='us-street-address-entry']")
    us_address_line_2_input_field = driver.find_element(By.XPATH, "//label[contains(text(), 'Address line 2')]/following-sibling::div//input")
    us_city_input_field = driver.find_element(By.XPATH, "//label[contains(text(), 'City')]/following-sibling::div//input")
    us_state_input_field = driver.find_element(By.XPATH, "//label[contains(text(), 'State')]/following-sibling::div//input")
    us_zip_code_input_field = driver.find_element(By.XPATH, "//label[contains(text(), 'ZIP Code')]/following-sibling::div//input")
    return us_address_line_1_input_field, us_address_line_2_input_field, us_city_input_field, us_state_input_field, us_zip_code_input_field


def find_US_input_elements__freeform_address(driver):
    return driver.find_element(By.XPATH, "//input[@id='us-street-address-entry']")


def find_US_input_elements__city_state_zip(driver):
    us_city_input_field = driver.find_element(By.XPATH, "//label[contains(text(), 'City')]/following-sibling::div//input")
    us_state_input_field = driver.find_element(By.XPATH, "//label[contains(text(), 'State')]/following-sibling::div//input")
    us_zip_code_input_field = driver.find_element(By.XPATH, "//label[contains(text(), 'ZIP Code')]/following-sibling::div//input")
    return us_city_input_field, us_state_input_field, us_zip_code_input_field


def find_international_input_elements__address_components(driver):
    international_country_input = driver.find_element(By.XPATH, "//input[@id='country-input']")
    international_street_address_input = driver.find_element(By.XPATH, "//input[@id='international-street-address-entry']")
    international_locality_input = driver.find_element((By.XPATH, "//input[@id=':r64:']"))
    international_administrative_area_input = driver.find_element((By.XPATH, "//input[@id=':r65:']"))
    international_postal_code_input = driver.find_element((By.XPATH, "//input[@id=':r66:']"))
    return international_country_input, international_street_address_input, international_locality_input, international_administrative_area_input, international_postal_code_input


def find_international_input_elements__freeform_address(driver):
    international_country_input = driver.find_element(By.XPATH, "//input[@id='country-input']")
    international_address_input = driver.find_element(By.XPATH, "//input[@id='international-street-address-entry']")
    return international_country_input, international_address_input


def interact_with_country_dropdown(driver, actions, country_name):
    int_country_input, _ = find_international_input_elements__freeform_address(driver)
    int_country_input.send_keys(country_name)
    actions.move_to_element(int_country_input).click().send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()


def find_Results_btn(driver):
    return driver.find_element(By.XPATH, "//button[contains(text(), 'View results')]")


def get_validation_status(driver):
    output_status_text = driver.find_element(By.XPATH,"//div[@class='outputHeading_outputStatusWrapper__xkOwj']/div[@class='outputHeading_outputStatus__s4qHh']").text
    return output_status_text


def set_input_value(driver, element, value):
    driver.execute_script("arguments[0].value = arguments[1];", element, value)


def main():
    file_path = 'Sample Adress.xlsx'
    print("Reading Excel File")
    df = read_excel_file(file_path)

    print("Setting up Chrome Options and intializing Chrome Driver, Wait and Action Chains")
    chrome_options = setup_chrome_options()
    driver, wait = init_chrome_driver(chrome_options)
    actions = init_action_chains(driver)

    print("Opening Address Validation Webpage")
    open_address_validation_webpage(driver)

    # Separate US and International addresses
    print("Separating US and International Addresses")
    us_addresses = df[df['Country'] == 'United States']
    international_addresses = df[df['Country'] != 'United States']

    # Switch to US freeform address validation lookup type
    interact_with_lookup_type_dropdown(driver, actions, 1)

    print("Finding View Results Button")
    view_results_btn = find_Results_btn(driver)
    
    # Process US addresses
    for index, row in us_addresses.iterrows():
        print(f"\nProcessing US Address: {row['Address1']}, {row['Address2']}, {row['City']}, {row['Province/State']}, {row['Zip Code']}")
        us_addresses_input = find_US_input_elements__freeform_address(driver)
        address_components = [row['Address1'], row['Address2'], row['City'], row['Province/State'], row['Zip Code']]
        filtered_address_components = [component for component in address_components if pd.notna(component)]
        combined_address = " ".join(filtered_address_components)
        print(f"Combined Address: {combined_address}")

        us_addresses_input.send_keys(combined_address)
        actions.move_to_element(us_addresses_input).click().send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()

        view_results_btn.click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='outputHeading_outputStatusWrapper__xkOwj']/div[@class='outputHeading_outputStatus__s4qHh']")))

        validation_status = get_validation_status(driver)
        print(f"Validation Status: {validation_status}")

        us_addresses_input.clear()

        time.sleep(1)



    # # Process International addresses
    # switch_to_international_address_validation_tab(driver)
    # for index, row in international_addresses.iterrows():
    #     interact_with_country_dropdown(driver, actions, row['Country'])
    #     interact_with_lookup_type_dropdown(driver, actions, 0)  # Assuming '0' selects 'Freeform Address'
    #     _, international_address_input = find_international_input_elements__freeform_address(driver)
    #     international_address_input.send_keys(row['Address'])
    #     actions.send_keys(Keys.ENTER).perform()
    #     time.sleep(2)  # Wait for the validation to complete
    #     # Assuming there's a way to fetch the validation status
    #     validation_status = driver.find_element(By.ID, 'validation-status').text
    #     df.at[index, 'Status'] = validation_status
    #
    # # Save the updated DataFrame
    # df.to_excel('Updated Sample Address.xlsx', index=False)
    #
    # driver.quit()


if __name__ == '__main__':
    main()