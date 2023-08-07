import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


endpoint = "https://www.instagram.com/graphql/query/?query_hash=be13233562af2d229b008d2976b998b5&"


def instagram_id_user(driver: webdriver.Chrome, wait: WebDriverWait, username: str):
    sleep(1)
    driver.get(f"https://www.instagram.com/web/search/topsearch/?query={username}")
    pre_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//pre")))
    return int(json.loads(pre_element.get_attribute("textContent"))["users"][0]["user"]["pk"])


def tagged_post(driver: webdriver.Chrome, wait: WebDriverWait, ig_id: int):
    first_request = True
    tagged = 0
    end_cursor = ""

    while True:
        if first_request:
            init_variables = f'variables={{"id":"{ig_id}","first":50}}'
        else:
            init_variables = f'variables={{"id":"{ig_id}","after":"{end_cursor}","first":50}}'
            
        url = endpoint + init_variables
        driver.get(url)
        
        # Chrome
        pre_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//pre")))
        
        # Firefox
        # wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Raw Data")))
        # driver.find_element_by_link_text("Raw Data").click()
        # pre_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//pre[@class='data']")))

        data = json.loads(pre_element.get_attribute("textContent"))

        sleep(1)
        # Check if the 'data' dictionary has the required keys
        if ("data" in data and "user" in data["data"] and "edge_user_to_photos_of_you" in data["data"]["user"]):
            tagged += data["data"]["user"]["edge_user_to_photos_of_you"]["count"]  # int
            end_cursor = data["data"]["user"]["edge_user_to_photos_of_you"]["page_info"]["end_cursor"]  # str

            # Break the loop if end_cursor is empty
            if not end_cursor:
                break

            first_request = False
        else:
            print("Error: Invalid response format")
            break

    # print("Total tagged count:", tagged)
    return tagged

