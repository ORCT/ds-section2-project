from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil
import time

try:
    shutil.rmtree(r'C:\chrometemp') #remove cookie, cache
except FileNotFoundError:
    pass

subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')#run chrome debugger mode

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]#get chrome driver version 
# chrome_ver = chromedriver_autoinstaller.get_chrome_version()

try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)#add options mean 'open debugger mode chrome only'
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)

driver.implicitly_wait(10)

url = 'https://tmi.nexon.com/kart/rank?mode=indi&speed=speedIndiCombine'
driver.get(url)
time.sleep(7)
'''
1,2,3위 호출한번 하고 그 다음에 반복문으로 쭉 불러내면 될 듯
//*[@id="base"]/div[2]/div[1]/div[1]/p[1]/a
//*[@id="base"]/div[2]/div[2]/div[1]/p[1]/a
//*[@id="base"]/div[2]/div[3]/div[1]/p[1]/a
//*[@id="4"]/span[2]/a
//*[@id="5"]/span[2]/a
//*[@id="6"]/span[2]/a
물론 xpath로 잘 불러지는지 확인을 해야겠지만

잘불러지는거 확인했고 이거 처음에 a 태그로 유저 이름 리스트를 미리 만들고 그거대로 해서 반복문 돌리는게
굳이 뒤로가기 누르는 버튼 안눌러도 돼서 좋을듯?
오케이 내일 함수화하자
'''
user_name_xpath = '//*[@id="base"]/div[2]/div[1]/div[1]/p[1]/a'
user_name_btn = driver.find_element_by_xpath(user_name_xpath)
user_name_btn.click()
time.sleep(1)
#일단 위에거로 잘 불러와지는거 확인했고 그리고 이제 데이터 모으는 작업 좀 하면 되겠네
#아 그리고 요즘 무한부스터전이 훨씬 인기 많으니까 스피드 개인 끝내고 나면 무부전도 모아서 해보자

#자 일단 이제 유저 이름 눌러서 창 들어왔다
#그 다음에는 이제 전적을 보면서 맵데이터집고 옆에 화살표 눌러서 열어가지고 순위, 카트, 랩 타임 이렇게 불러오고
#다 불러왔으면 어디 저장해놓은 다음에 밑으로 내려가면서 이 짓 반복
# //*[@id="inner"]/div[5]/div[2]/div/section[1]/div/p[3]
# //*[@id="inner"]/div[5]/div[2]/div/section[1]/div/p[3]/text()
track_xpath = '//*[@id="inner"]/div[5]/div[2]/div/section[1]/div/p[3]'
track_name = driver.find_element_by_xpath(track_xpath).get_attribute('innerText')
# 이제 트랙 이름도 불러왔으니까 요 트랙 이름으로 해당 매치 데이터에 트랙 이름이랑 슥슥 집어넣으면 되겠다
match_open_xpath = '//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[1]/p[6]'
match_open_btn = driver.find_element_by_xpath(match_open_xpath)
match_open_btn.click()
time.sleep(1)
#이걸로 옆에 버튼도 눌러서 순위표 표시했고
#다만 카트가 안보이는 경우를 결측치로 입력을 해야하는데 이게 어떤 에러가 날지를 잘 모르겠다 일단 해보자고
kart_1_xpath = '//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[2]/div/div[2]'#일단 카트데이터 아직 업데이트 안된 카트임 아마 리키?그 바이크일듯
# kart_2_xpath = '//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[3]/div/div[2]'#li옆에 숫자가 하나씩 오르네
kart_2_xpath = '//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[3]/div/div[2]/img'
kart_1_name = driver.find_element_by_xpath(kart_1_xpath).get_attribute('title')#없으면 그냥 빈칸이 되어버림, 이거 none이나 모름 같은거로 처리
kart_2_name = driver.find_element_by_xpath(kart_2_xpath).get_attribute('title')
# print(kart_1_name,'//',kart_2_name)

kart_1_user_xpath = '//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[2]/div/div[3]/a'
kart_1_user_name = driver.find_element_by_xpath(kart_1_user_xpath).get_attribute('innerText')
# print(kart_1_user_name)

kart_1_time_xpath = '//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[2]/div/div[4]'
kart_1_time_value = driver.find_element_by_xpath(kart_1_time_xpath).get_attribute('innerText')
print(kart_1_time_value)
# 뭐 이제 이걸로 맵 데이터 부르기 완료했고, 카트 데이터, 유저, 시간 부르기 완료했고
# 반복을 위해서 이제 각각의 규칙을 좀 찾아보자고
# 일단 먼저 가장 큰거 맵데이터에 xpath를 한 번 비교해보자고
'''
맵데이터 비교:
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[1]/p[3]
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div/p[3]
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[1]/p[3]
이거 삼각형 눌러서 순위 데이터 열어버리면 div[1]이라고 인덱스가 붙어버리니까 알아두면 좋을듯 무시해도 물론 크리티컬한 문제는 없음 
//*[@id="inner"]/div[5]/div[2]/div/section[2]/div/p[3]
//*[@id="inner"]/div[5]/div[2]/div/section[3]/div/p[3]
//*[@id="inner"]/div[5]/div[2]/div/section[200]/div/p[3]
정리 : section에서 숫자가 하나씩 늘어난다, 딱 200매치까지 보여주는건가?

카트데이터(확실하게 이미지 누른거로):
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[2]/div/div[2]/img
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[3]/div/div[2]/img
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[4]/div/div[2]/img
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[8]/div/div[2]/img
정리 : li 인덱스가 커진다, 최대 인덱스는 9(1번이 #임)다만 인원수가 8명이 가득 안찼을 때는 빈칸에서 아마 에러가 날 것임 해당 파트를 주의할것

유저이름:
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[2]/div/div[3]/a
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[3]/div/div[3]/a
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[4]/div/div[3]/a
정리 : 이거도 li 인덱스, 아마 타임도 마찬가지일거임

타임:
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[2]/div/div[4]
//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[3]/div/div[4]
정리 : 동일, - 는 리타이어임 이걸로 나중에 구분할 방법이 생길것임

순위:
사실 이거는 딱히 크롤링을 할 생각은 없고 일단은 칼럼으로 넣긴 할텐데 아마 안쓸수도 있음
랩타임에 순위가 그렇게나 중요하진 않을 것 같아서
칼럼으로 넣을거면 그냥 저거 데이터 불러올 때 어디 리스트든 어디든 저장할테니까
그거 리스트 인덱스 +1 하면 되겠지 기록 없으면 무시해도 되고

'''

#그거도 다 끝나면 이제 나간 다음에 모든 유저들 대상으로 반복



# #user_nick = a에서 이제 닉을 읽어오는 거지 자바스크립트 어쩌구 뒤에 유저 닉이 나오니까 이걸 따서 user_url에다 써넣어서 해당 url로 갈 수 있는거지 
# user_url = f'https://tmi.nexon.com/kart/user?nick={user_nick}&matchType=indi'
# 유저 url 들어갔을 때 가끔 닉변한 놈 때문에 에러 뜨기도 하니까 에러나면 스킵하는 코드도 필요함


# #반복문으로 태그를 변경해나갈수있을까
# #태그는 a인거 같은데 a인거를 하나씩 다 클릭해나가는 방식으로 하면 될까?
# #크롤링 다 하고 생각해도 되는 부분일거 같은데 카트가 아직 집계가 안되는 놈이 있다. 아마 메타데이터에 안들어있는 신규출시 카트일 가능성이 높음
# #익시드 때문에 x만 하든지, v1만 하든지 해야할 거 같아(사실 익시드 이게 제일 문제야 요즘이야 공략이 나와서 거의 쓰는 타이밍이 비슷해졌지만 여전히 타이밍이 다들 다르니까 또 오히려 사고 회복을 빠르게 하는데에 익시드가 사용되니까 랩 타임 기준에서는 이상치가 조금 줄어들지도)

# login_btn_xpath = '//*[@id="root"]/div/div/div[3]/div/div/div/div[2]/button[1]'
# login_btn = driver.find_element_by_xpath(login_btn_xpath)
# login_btn.click()

# driver.find_element_by_name('email')
# driver.find_element_by_name('password')

# login_btn1_xpath = '//*[@id="login-form"]/fieldset/div[8]/button[1]'
# login_btn1 = driver.find_element_by_xpath(login_btn1_xpath)
# login_btn1.click()