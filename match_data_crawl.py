from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil
import time
import pandas as pd

def make_ranker_list():
    '''
    ## Function that return the ranker list using element's xpath in url.\n
    Rank 1 to 3 are diffrent form of xpath from 4 to end.\n
    #### ❗️Be care that xpaths may change depending on the circumstances of the site.\n
    '''
    ranker_list = []
    
    for i in range(1, 4):
        ranker_name_xpath = f'//*[@id="base"]/div[2]/div[{i}]/div[1]/p[1]/a'
        user_name = driver.find_element_by_xpath(ranker_name_xpath).get_attribute('innerText')
        ranker_list.append(user_name)
    
    for i in range(4, 41):
        try:
            ranker_name_xpath = f'//*[@id="{i}"]/span[2]/a'
            user_name = driver.find_element_by_xpath(ranker_name_xpath).get_attribute('innerText')
            ranker_list.append(user_name)
        except:
            continue
        
    return ranker_list

def get_match_data(match_id):
    '''
    ## Function that return the dictionary of each ranker's match data.
    ### The return dict is composed of these form; match_id : (track_name, internal_match_rank, kart_name, user_name, lap_time)
    
    - Map Data Format
        - //*[@id="inner"]/div[5]/div[2]/div/section[{index}]/div/p[3]
        - index limit 1 to 201
    
    - Match Data Format
        - //*[@id="inner"]/div[5]/div[2]/div/section[{index}]/div/p[6]
        - index limit 1 to 201

    - Kart Name Data Format
        - //*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[{index}]/div/div[2]/img
        - index limit 2 to 10

    - User Name Data Format
        - //*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[{index}]/div/div[3]/a
        - index limit 2 to 10
        
    - Lap Time Data Format
        - //*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[{index}]/div/div[4]
        - index limit 2 to 10

    - Match Rank Data:
        - index - 1
        
    #### ❗️Be care the retired user.\n
    '''
    match_data_dict = {}
    
    for i in range(1,101):
        try:
            track_xpath = f'//*[@id="inner"]/div[5]/div[2]/div/section[{i}]/div/p[3]'
            track_name = driver.find_element_by_xpath(track_xpath).get_attribute('innerText')
            match_data_dict[match_id+'/'+str(i)] = []
            print(match_id+'/'+str(i))
            
            match_open_xpath = f'//*[@id="inner"]/div[5]/div[2]/div/section[{i}]/div/p[6]'
            match_open_btn = driver.find_element_by_xpath(match_open_xpath)
            match_open_btn.click()
            # time.sleep(0.1)
        except:
            continue
            
        for j in range(2,6):
            try:
                kart_xpath = f'//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[{j}]/div/div[2]/img'
                kart_name = driver.find_element_by_xpath(kart_xpath).get_attribute('title')
                
                kart_user_xpath = f'//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[{j}]/div/div[3]/a'
                kart_user_name = driver.find_element_by_xpath(kart_user_xpath).get_attribute('innerText')
                
                kart_time_xpath = f'//*[@id="inner"]/div[5]/div[2]/div/section[1]/div[2]/ul/li[{j}]/div/div[4]'
                kart_time_value = driver.find_element_by_xpath(kart_time_xpath).get_attribute('innerText')
                
                match_data_dict[match_id+'/'+str(i)].append((track_name, j-1, kart_name, kart_user_name, kart_time_value))
            except:
                continue
    
    return match_data_dict

def get_result_dict(ranker_list):
    '''
    ## Function that return the result dictionary of all crawled match data.
    '''
    result_dict = {}
    
    for i in ranker_list:
        try:
            ranker_url = f'https://tmi.nexon.com/kart/user?nick={i}&matchType=indi'
            driver.get(ranker_url)
            time.sleep(1)
            match_data_dict = get_match_data(str(i))
            result_dict.update(match_data_dict)
        except:
            continue
        
    return result_dict

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
time.sleep(3)

ranker_list = make_ranker_list()
remove_name = ['멈구리군단병', 'Racing프로', 'CN1v7Go', '아야노코찌', '키보드무선임',
               '봉봉봉상', '그냥핑크빈', '밥은율', '빠름제왕', '핑튀어요', '미흡충',
               'Scamper성욱s', 'D9G림보', '마달모시', '초심돌아오자']

for i in remove_name:
    try:
        ranker_list.remove(i)
    except:
        continue

result_dict = get_result_dict(ranker_list)

print(result_dict)

with open('data_dict.txt','w',encoding='UTF-8') as f:
    for key, value in result_dict.items():
        f.write(f'{key} : {value}\n')

df = pd.DataFrame(result_dict)
df.to_csv('./kartrider_match_data.csv', index=False)

driver.quit()