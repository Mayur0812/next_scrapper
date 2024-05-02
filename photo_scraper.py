from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.request
import json
import time

chrome_options = Options()
chrome_options.add_argument("--headless")

with open('config.json') as config:
    config_ = config.read()

config_file = json.loads(config_)
base_website = config_file.get('web_url')
image_folder = config_file.get('image_folder')

driver = webdriver.Chrome()
driver.get(base_website)


def get_image(object_id):
    """
    This function will get the image downloaded in specified folder
    """
    try:
        search_bar = driver.find_element(By.NAME,"header-big-screen-search-box")
    except Exception as e:
        print(f"Error in serach bar is: {e}")
    search_bar.send_keys(object_id)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(0.5)
    try:
        find_image = driver.find_element(By.CLASS_NAME,"shotWrapper").find_element(By.TAG_NAME,"img")
        #find_image = driver.find_element(By.TAG_NAME, "shotWrapper>shotView")
    except Exception as e:
        print(f"Error in image downloading: {e}")
    img_src = find_image.get_attribute('src')
    img_src = img_src.split("?")[0]
    print(f"Object Id: {object_id}\nImage source: {img_src}")
    print("\n","*"*60,)
    urllib.request.urlretrieve(img_src, image_folder+str(object_id)+".jpg")
    return None

object_ids = ['M96765','530205']
_ = list(map(get_image,object_ids))