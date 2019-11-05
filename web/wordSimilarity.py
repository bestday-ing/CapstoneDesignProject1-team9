from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def wordSimilarity(comp1, comp2):
    option = Options()
    option.add_argument("--headless")
    option.add_argument("--window-size=1920x1980")
    option.add_argument("disable-gpu")

    try:
        driver = webdriver.Chrome(executable_path='./chromedriver_77.exe', options=option)  # 버전에 따라 수정해서
    except:
        driver = webdriver.Chrome(executable_path='/Users/yubin/ChromeDriver/chromedriver4', options=option)  # 맥 경로, 불필요시 주석 처리바람

    driver.get('https://wordsimilarity.com/word-similarity-api')
    driver.find_element_by_xpath('//*[(@id = "word1")]').send_keys(comp1)
    driver.find_element_by_xpath('//*[(@id = "word2")]').send_keys(comp2)
    driver.find_element_by_name("lang").send_keys('Korean')
    driver.find_element_by_class_name('btn.btn-primary.btn-large').click()  # 자동 클릭처리
    driver.implicitly_wait(2)
    results = driver.find_elements_by_class_name("col-md-4");
    p = results[1].text.split(" ")
    print(float(p[2]))
    return float(p[2])

wordSimilarity('김치', '불고기')