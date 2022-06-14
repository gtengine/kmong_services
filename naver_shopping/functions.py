from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pyperclip
import time
import pyautogui
import os

##################################################

def sleep(sec=1):
    time.sleep(sec)


def driver_instance():
    """드라이버 열기"""
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 불필요한 로그를 프린트하지 않음.
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    driver.implicitly_wait(10) # 요청한 페이지의 정보가 모두 넘어올 때까지 최대 10초 기다림. drive를 열고 한 번만 정의하면 됨.
    sleep()
    
    return driver



def log_in(driver, user_id, user_pw):
    """네이버 로그인"""
    driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
    
    id_element = driver.find_element(by='id', value='id') # id 적는 칸.
    pw_element = driver.find_element(by='id', value='pw') # password 적는 칸.
    
    # 네이버는 원격으로 로그인 시, 보안 문자 입력 때문에 사실 상 selenium으로 로그인이 불가능.
    # 따라서 우회하는 방법을 써야 하는데, selenium을 통해 직접 입력하지 않고, id 와 pw를 [복사 + 붙여넣기] 하는 방법으로 로그인.
    id_element.click()
    pyperclip.copy(user_id)
    id_element.send_keys(Keys.CONTROL, 'v')
    sleep()
    
    pw_element.click()
    pyperclip.copy(user_pw)
    pw_element.send_keys(Keys.CONTROL, 'v')
    sleep()
    
    driver.find_element('id', value='log.login').click()
    sleep()
    
    return driver



def shopping(driver, shop_url):
    """특정 쇼핑사이트의 상품 구매 (네이버 페이 비밀번호 입력 전 까지의 단계)"""
    driver.get(shop_url)
    sleep()
    
    # ### 옵션 선택 부분
    # driver.find_element(by='xpath', value='//*[@id="content"]/div/div[2]/div[2]/fieldset/div[6]/div/a').click()
    # sleep(1)
    # driver.find_element(by='xpath', value='//*[@id="content"]/div/div[2]/div[2]/fieldset/div[6]/div/ul/li[10]/a').click()
    # sleep(1)
    # ###
    
    driver.find_element(by='xpath', value='//*[@id="content"]/div/div[2]/div[2]/fieldset/div[9]/div[1]/div/a').click() # 구매하기 버튼
    sleep()
    driver.find_element(by='xpath', value='//*[@id="orderForm"]/div/div[7]/button').click() # 결제하기 버튼
    sleep(5)
    
    return driver



def click_pay_pw(password):
    """이미지 인식을 통해 네이버 페이 비밀번호 클릭 (결제)"""
    pyautogui.PAUSE = 0.5
    img_dir = os.path.join(os.getcwd(), 'images')
    
    for i in str(password):
        img_path = os.path.join(img_dir, f'{i}.png')
        img = pyautogui.locateCenterOnScreen(img_path)
        pyautogui.click(img)
    sleep(10)



def wait(driver, by, value):
    """특정 element가 완전히 렌더링 될 때까지 기다림"""
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((by, value))) # 특정 element가 표시될 때까지 최대 15초 기다림.
    return driver



def cancel_purchase(driver):
    """구매한 상품 주문 취소하고 드라이버 닫기"""
    driver.find_element(by='xpath', value='//*[@id="order"]/div[5]/div/div[2]/div/button[2]').click()
    sleep()
    driver.find_element(by='xpath', value='//*[@id="order"]/div[2]/div[7]/button[1]').click()
    
    wait(driver, By.XPATH, '//*[@id="content"]/div/table/tbody/tr/td[6]/a')
    sleep(2)
    driver.find_element(by='xpath', value='//*[@id="content"]/div/table/tbody/tr/td[6]/a').click()
    
    wait(driver, By.XPATH, '//*[@id="batchReqReason.claimReqReason"]')
    sleep(2)
    driver.find_element(by='xpath', value='//*[@id="batchReqReason.claimReqReason"]').click()
    sleep()
    driver.find_element(by='xpath', value='//*[@id="batchReqReason.claimReqReason"]/option[2]').click()
    sleep()
    driver.find_element(by='xpath', value='//*[@id="content"]/div/div[3]/a[1]').click()
    sleep(5)
    
    driver.quit() # 드라이버 닫기