from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

# 이거해결하고 [0]에 대한 프린트인데 여러개에 대한 프린트 하고 우선순위 정렬하면됨 ㅇㅇㅇㅇㅇ 그러고 태윤 ㄱㄱ

# 크롬이랑 맞는 버전의 크롬드라이버 설치 후 이거를 작업파일과 같은위치에 exe파일로 넣어야함
#driver = webdriver.Chrome() 이렇게만 하면 시스템에 부착된 장치가 작동하지 않는다는 오류 종종 떠서 구글링해서 코드바꿈
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
################################################################
driver.get("https://shopping.naver.com/") # 크롤링할 대상 사이트명
elem = driver.find_element_by_name("query") # 클래스로도 가능 driver.find 하면 여러개 나옴 ㅇㅇ
# 이건 이제 다룰 요소? 인데 검색창이다 그러면 검색창을 html 분석해서 클래스나 name 이름으로 찾은 후 그걸 넣어주면 됨 
elem.send_keys("조던") # 이건 키보드 입력을 전달하는 기능 (즉 검색할수있게 함)
time.sleep(1)
elem.send_keys(Keys.RETURN) # 엔터키 치는 기능
############################################
driver.find_elements_by_css_selector(".n_ico_npay_plus__1pi8I")[0].click()
# result = driver.find_elements_by_css_selector("._3SMi-TrYq2")
# print(result.text)

html = driver.page_source
soup = BeautifulSoup(html)
r = soup.select('._3Vox1DKZiA', features = 'html.parser')
for i in r:
    print(i.select_one('._3SMi-TrYq2').text)

driver.close()

# 여기까지 하면 검색이 된다. 이제 하나의 이미지를 클릭해보자.
# 먼저 이미지 클래스 태그 분석해주고 (클래스로 할때는 . 중간중간 잘 써주어야 함)
# driver.find_elements_by_css_selector(".rg_i.Q4LuWd")[0].click() # [0] : 첫번째꺼를 & 그리고 뒤에 .click()은 클릭기능
# 이건 이제 class로 검색하는방법 (class name도 있던데 뭔 차이지)
# 그리고 딱 하나만 할거면 element인데 여러개해서 리스트 담고 그럴거면 elements!

