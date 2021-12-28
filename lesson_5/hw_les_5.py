
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint

driver = webdriver.Chrome()
driver.get('https://mvideo.ru')

driver.implicitly_wait(10)

element = driver.find_element(By.TAG_NAME, 'mvid-shelf-group')
actions = ActionChains(driver)
actions.move_to_element(element).perform()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button/div/span[@class='title'"
                                                                      " and contains(.,'В тренде')]/../.."))).click()
names = element.find_elements(By.XPATH, ".//div[contains(@class, 'product-mini-card__name')]")
prices = element.find_elements(By.XPATH, ".//div[contains(@class, 'product-mini-card__price')]"
                                         "//span[@class='price__main-value']")
print(len(prices))
goods = []
for i in range(len(names)):
    good = {'name': names[i].text, 'price': prices[i].text}
    goods.append(good)

pprint(goods)
