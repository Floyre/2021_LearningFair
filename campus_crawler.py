#
#               이 프로그램은 Microsoft Visual Studio Code 터미널에 최적화되어 있습니다.
#                                   https://code.visualstudio.com/download
#

from selenium import webdriver as webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import sys
import os
import os.path
import unicodedata

# Selenium WebDriver 관련 설정값
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
options.add_argument('--hide-scrollbars')
options.add_argument("--log-level=3")  # Log Only FATAL info = 3
options.add_experimental_option("excludeSwitches", ["enable-logging"]) # Suppress Console Logs
driver = webdriver.Chrome(executable_path="chromedriver.exe",options=options)  # WebDriver Location


#ASCII ART 변수
start = """
┌┬────────────────────────────────────────────┬┐
├┘                                            └┤
│  상명대학교 e-Campus 주차 과목별 항목 출력기 │
├┐                                            ┌┤
└┴────────────────────────────────────────────┴┘
"""
loginsuccess= """
┌─────────────────────────┐
│           PASS          │
├─────────────────────────┤
│   e-Campus 로그인 성공  │
└─────────────────────────┘
"""
loginfail= """
┌─────────────────────────┐
│          ERROR          │
├─────────────────────────┤
│   e-Campus 로그인 실패  │
└─────────────────────────┘
"""
fileloc="""
┌───────────────────────┐
│  txt 파일의 저장 위치 │
└───────────────────────┘
"""
secdetect="""
┌───────────────────────────────────────┐
│   Security.txt 파일이 감지되었습니다  │
└───────────────────────────────────────┘
"""
sectip="""
┌────────────────────────────────────────────────────────────────────────────────────┐
│  프로그램이 있는 폴더에 Security.txt 파일을 생성했습니다.                          │
│  해당 텍스트 파일의 첫번째 줄에는 e-Campus 아이디                                  │
│  두번째 줄에는 e-Campus 비밀번호를 입력 후 저장하시면                              │
│  저장된 DB를 기준으로 다음에 프로그램을 실행하셨을때 로그인을 자동으로 진행합니다. │
└────────────────────────────────────────────────────────────────────────────────────┘
"""
reqauth="""
┌─────────────────────────────────────────────────────────────────────────────┐
│                                   ERROR                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                      모바일 본인 인증이 필요합니다                          │
│  e-Campus 사이트에서 본인인증을 완료 후 프로그램을 재실행해주시길 바랍니다  │
└─────────────────────────────────────────────────────────────────────────────┘
"""
authdone="""
┌───────────────────┐
│        PASS       │
├───────────────────┤
│   본인 인증 완료  │
└───────────────────┘
"""
workdone="""
┌──────────────────────────┐
│   작업이 완료되었습니다  │
└──────────────────────────┘
"""
wrongans="""
┌──────────────────────┐
│         ERROR        │
├──────────────────────┤
│   잘못된 입력입니다  │
└──────────────────────┘
"""
bye="""
┌─────────────────────────────┐
│   이용해 주셔서 감사합니다  │
└─────────────────────────────┘
"""

def createFolder(directory): #폴더 생성 함수
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('디렉터리 생성에 오류가 발생했습니다. 해당 디렉터리 : ' +  directory)

def xpathchecker(xpath): #지금 보고있는 페이지에 입력받은 Xpath가 있는지 검증하는 함수
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException: #없으면 Return 0
        return 0;
    return 1; #있으면 Return 1

def checksec(directory):
    if os.path.isfile(directory): #security.txt의 유무를 검증
        security = open('security.txt','r',encoding='UTF-8') #만약 프로그램 파일이 있는 디렉터리에 security.txt가 있다면 해당 폴더를 UTF-8 인코더로 열기
        id = str(security.readline().strip()) #1번째 줄 아이디 변수에 할당
        pw = str(security.readline()) #2번째 줄 비밀번호 변수에 할당
        return id, pw
    else:
        security = open("security.txt","w") #만약 프로그램 파일이 있는 디렉터리에 security.txt가 없다면 해당 폴더에 security.txt 생성
        print(sectip)


secfile= 'security.txt'
checksec(secfile)
createFolder('학습목록')
securityfail = 0
print(start)

while(True):
    if (os.path.getsize('security.txt') > 0 and securityfail == 0): #security.txt에 1글자라도 글자가 감지되면 AND securityfail 변수 0 (프로그램 실행 시 최초 1번만 돌아감. 런 한 다음 통과하면 그냥 그대로 통과되지만, 실패해서 Return 하게 되면 securityfail이 1이라 입력으로 넘어감
        print(secdetect)
        id, pw = checksec(secfile)
        print('【 로그인에 사용할 ID :',id,'】')
        print('【 로그인에 사용할 PW :',pw,'】')
        securityfail = 1
    elif(os.path.getsize('security.txt') == 0 or securityfail == 1): #security.txt의 내용이 0 글자라면 OR securityfail 변수 1 (security.txt 감지 되었는데 ID/비밀번호 오류 시 입력 가능하게 돌아옴) 
        id = str(input("상명대학교 e-Campus ID를 입력해주세요 : "))
        pw = str(input("상명대학교 e-Campus PW를 입력해주세요 : "))

    driver.get('https://ecampus.smu.ac.kr/login.php/') 
    driver.find_element_by_name('username').send_keys(id) #ID입력
    driver.find_element_by_name('password').send_keys(pw) #PW 입력
    driver.find_element_by_xpath('//*[@id="region-main"]/div/div/div/div[1]/div[1]/div[2]/form/div[2]/input').click() #로그인 버튼 클릭
    if(xpathchecker('//*[@id="region-main"]/div/div/div/div[1]/div[1]/div[2]/form/p') == 0): #로그인 화면에서 '아이디 또는 패스워드가 잘못 입력되었습니다.' 의 Xpath가 감지되지 않으면 0, 감지되면 1
        print(loginsuccess)
        break
    else:
        print(loginfail)
        print("【 아이디 또는 패스워드가 잘못 입력되었습니다 】")
        print("\n【 시도된 ID :",id,"】\n【 시도된 PW :",pw,"】\n")
        continue

course_links = driver.find_elements_by_class_name('course_label_re') #본인인증 필요성 확인용
course_links[0].click() #0(1)번째 교과 과목을 클릭했을 때
if(xpathchecker('//*[@id="btn-stonepass"]')==1): #일일 인증 버튼의 Xpath가 있는가?
    print(reqauth)
    quit()
else: #없으면 메인화면으로 복귀
    print(authdone)
    driver.get('https://ecampus.smu.ac.kr/')
while(True):
    while(True):
        week = str(input("크롤링하고 싶은 주차를 입력해주세요. : "))
        if(week.isnumeric() == False):
            print(wrongans)
            continue
        else:
            break
    filename = ('학습목록/' + week + '주차_학습목록.txt')
    f = open(filename,'wt',encoding='UTF-8')
    print(fileloc)
    print('▶ ',filename,'◀\n')
    section = '//*[@id="section-'+week+'"]/div[3]/ul'

    # 본인의 수업 개수가 몇 개인지 불러오기
    course_link_list=[]
    course_links=course_link_list
    course_links_div_element = driver.find_elements_by_class_name('course_label_re')
    for divElem in course_links_div_element:
        course_link_list.append(divElem.find_elements_by_class_name('course_link'))

    for i in range(len(course_links)):
        # 페이지가 새로 고쳐지면 각 element의 고유 id가 변하기 때문에 새로고침 시에 매번 배열을 불러옴.
        course_links = driver.find_elements_by_class_name('course_label_re')
        course_links[i].click()

        content = [e.text for e in driver.find_elements_by_xpath(section)] # xPath로 긁어와야되는 내용 (과제, 수업)

        # 이번주차 , n주차 section 2개 중복되는 것 삭제 루프
        new_list = [] 
        for v in content:
            if v not in new_list:
                new_list.append(v)

        titlepath = '//*[@id="page-header"]/nav/div/div[3]'
        title = [e.text for e in driver.find_elements_by_xpath(titlepath)]
        print('▼───────────────────────────────────────▼\n강의 제목 :', title[0],'\n')
        f.write('\n\n▼───────────────────────────────────────▼')
        f.write('\n\n강의 제목 : ')
        f.write(title[0])
        f.write('\n\n')
        
        #e-Campus의 항목별 아이콘 이름 앞에 있는 줄바꿈 구문을 삭제
        if not new_list:
            print("항목이 없습니다.")
            f.write("항목이 없습니다.")
        else:
            fix_list = new_list[0].replace('\n게시판',' 게시판 ')
            new_list[0] = fix_list
            fix_list = new_list[0].replace('\n파일\n',' 파일 ')
            new_list[0] = fix_list
            fix_list = new_list[0].replace('\n과제\n',' 과제 ')
            new_list[0] = fix_list
            fix_list = new_list[0].replace('\n퀴즈\n',' 퀴즈 ')
            new_list[0] = fix_list
            fix_list = new_list[0].replace('\n동영상\n',' 동영상 ')
            new_list[0] = fix_list
            fix_list = new_list[0].replace('\n화상강의\n',' 화상강의 ')
            new_list[0] = fix_list
            fix_list = new_list[0].replace('\n이러닝콘텐츠\n',' 이러닝콘텐츠 ')
            fix_list = unicodedata.normalize('NFC',fix_list) # 한글 자소분리 버그 해결 - https://1023labs.com/posts/python-korean-unicodedata/
            print(fix_list)
            f.write(fix_list)
        driver.get('https://ecampus.smu.ac.kr') # 메인화면으로 복귀
    print('■───────────────────────────────────────■')
    f.write('\n\n■───────────────────────────────────────■')
    print(workdone)
    f.close()
    
    while(True):
        quitcheck=input('다른 주차 과목을 출력하고 싶으시다면 Y, 종료하고 싶으시다면 N 을 입력해주세요. : ')
        if (quitcheck== 'Y' or quitcheck == 'y'):
            driver.get('https://ecampus.smu.ac.kr')
            print('\n')
            break
        elif(quitcheck=='N' or quitcheck == 'n'):
            print(bye)
            driver.quit()
            quit()
        else:
            print(wrongans)
            continue