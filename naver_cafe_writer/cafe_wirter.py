from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgbox
from tkinter import filedialog

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

import pyperclip
import time
# import base64
import requests
import urllib.request
import urllib.parse
import random

##################################################

root = Tk()
root.title('네이버 카페 포스팅')

### 유저 아이디, 비밀번호
user_info = LabelFrame(master=root, text='사용자 정보')
user_info.pack(fill='x', padx=5, pady=5)

# frame
user_frame = Frame(user_info)
user_frame.pack(fill='x', padx=5, pady=5)

# id 
id_label = Label(master=user_frame, text="     네이버 아이디 :")
id_label.pack(side='left', fill='x', padx=5, pady=5)

id_entry = Entry(master=user_frame, width=20)
id_entry.pack(side="left", fill="x")

# password 
pw_entry = Entry(master=user_frame, width=20)
pw_entry.pack(side="right", fill="x")

pw_label = Label(master=user_frame, text="네이버 비밀번호 :")
pw_label.pack(side='right', fill='x', padx=5, pady=5)

# client frame
client_frame = Frame(user_info)
client_frame.pack(fill='x', padx=5, pady=5)



# client_id entry
client_id_label = Label(master=client_frame, text="클라이언트 아이디 :")
client_id_label.pack(side='left', fill='x', padx=5, pady=5)

client_id_entry = Entry(master=client_frame, width=20)
client_id_entry.pack(side="left", fill="x")

# client_password 
client_pw_entry = Entry(master=client_frame, width=20)
client_pw_entry.pack(side="right", fill="x")

client_pw_label = Label(master=client_frame, text="클라이언트 비밀번호 :")
client_pw_label.pack(side='right', fill='x', padx=5, pady=5)

### 포스팅 카페 정보
cafe_info = LabelFrame(master=root, text='카페 정보')
cafe_info.pack(fill='x', padx=5, pady=5)

club_id_frame = Frame(cafe_info)
club_id_frame.pack(fill='x', padx=5, pady=5)

club_id_label = Label(club_id_frame, text='카페 고유 아이디')
club_id_label.pack(side='left', fill='x', padx=5, pady=5)

club_id_entry = Entry(club_id_frame, width=20)
club_id_entry.pack(side='left', fill='x')

menu_id_entry = Entry(club_id_frame, width=20)
menu_id_entry.pack(side='right', fill='x', padx=5, pady=5)

menu_id_label = Label(club_id_frame, text='카페 메뉴 아이디')
menu_id_label.pack(side='right', fill='x', padx=5, pady=5)


# 포스팅할 텍스트 파일
# frame
posting_files_frame = LabelFrame(master=root, text="텍스트 파일 등록")
posting_files_frame.pack(fill="x", padx=5, pady=5)
# listbox
file_list = Listbox(master=posting_files_frame, selectmode="extended", height=3)
file_list.pack(side="left", fill="both", expand=True, pady=10)


def add_image_files():
    """파일 추가"""
    file_list.delete(0, END)
    text_files = filedialog.askopenfilenames(
        title="텍스트 파일을 선택하세요",
        filetypes=(("모든 파일", "*.*"), ("TXT 파일", "*.txt")),
        initialdir=r"C:\\") # 최초 경로 - C:\\
    # 사용자가 선택한 파일 목록
    for text_file in text_files:
        file_list.insert(END, text_file.replace("/", "\\"))

# file selection button
find_file_btn = Button(master=posting_files_frame, text="선택", width=7, command=add_image_files)
find_file_btn.pack(side="top", padx=5, pady=3)


def del_image_files():
    """선택한 파일 삭제"""
    for index in reversed(file_list.curselection()):
        file_list.delete(index)


# file deletion button
del_file_btn = Button(master=posting_files_frame, text="삭제", width=7, command=del_image_files)
del_file_btn.pack(side="bottom", padx=5, pady=3)


# 포스팅
posting = LabelFrame(root)
posting.pack(fill='x', padx=5, pady=5)

n_posting_label = Label(posting, text='등록 파일 당 발행 수 : ')
n_posting_label.pack(side='left', fill='x', padx=5, pady=5)

n_posting_entry = Entry(posting, width=5)
n_posting_entry.pack(side='left', fill='x', padx=5, pady=5)

exit_btn = Button(posting, text='종료', width=10, height=3, command=root.quit)
exit_btn.pack(side='right', padx=5, pady=5)



def open_driver():
    """드라이버 열기"""
    options = Options()
    # options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 불필요한 로그를 프린트하지 않음.
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.minimize_window()
    # driver = webdriver.Chrome('.\\chromedriver.exe', options=options)
    driver.implicitly_wait(10) # 요청한 페이지의 정보가 모두 넘어올 때까지 최대 10초 기다림. drive를 열고 한 번만 정의하면 됨.
    
    return driver



def check_access_token(client_id, client_secret, user_id, user_password):
    """엑세스 토큰 받아오기"""
    
    redirect_uri = 'https://localhost:8888/'
    url = f'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri=https://localhost:8888/&state=REWERWERTATE'
    
    driver = open_driver()
    driver.get(url)
    time.sleep(1)
    
    id_element = driver.find_element(by='id', value='id') # id 적는 칸.
    pw_element = driver.find_element(by='id', value='pw') # password 적는 칸.
    
    # 네이버는 원격으로 로그인 시, 보안 문자 입력 때문에 사실 상 selenium으로 로그인이 불가능.
    # 따라서 우회하는 방법을 써야 하는데, selenium을 통해 직접 입력하지 않고, id 와 pw를 [복사 + 붙여넣기] 하는 방법으로 로그인.
    id_element.click()
    pyperclip.copy(user_id)
    id_element.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    
    pw_element.click()
    pyperclip.copy(user_password)
    pw_element.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    
    driver.find_element('id', value='log.login').click()
    
    url = driver.current_url
    code = url.split('code=')[1].split('&')[0]
    
    url = f'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri=https://localhost:8888/&code={code}&state=REWERWERTATE'
    driver.get(url)
    res = driver.page_source
    access_token = res.split('"access_token":"')[1].split('",')[0]
    driver.quit()
    
    return access_token


### 진행 상황 확인
# label frame
progress_label_frame = LabelFrame(root, text='진행 상황')
progress_label_frame.pack(fill='x', padx=5, pady=5)

p_var = DoubleVar()
progressbar = ttk.Progressbar(progress_label_frame, maximum=100, variable=p_var)
progressbar.pack(fill='x', padx=5, pady=5)



def naver_cafe_post():
    """네이버 카페 글쓰기"""
    try:
        files = file_list.get(0, END)
        n_posting = int(n_posting_entry.get().strip())
        
        progress = 0
        count = 0
        p_var.set(progress)
        progressbar.update()
        for txt in files:
            with open(txt, 'r', encoding='utf-8') as t:
                sentences = t.readlines()
                
            title = sentences[0]
            subject = urllib.parse.quote(title)
            
            body = ''.join(sentences[1:])
            content = urllib.parse.quote(body).replace('%0A', '\n')
            
            for _ in range(0, n_posting):
                token = check_access_token(
                    client_id_entry.get().strip(),
                    client_pw_entry.get().strip(),
                    id_entry.get().strip(),
                    pw_entry.get().strip()
                    )
                
                header = "Bearer " + token # Bearer 다음에 공백 추가
                clubid = club_id_entry.get().strip() # 카페의 고유 ID값
                menuid = menu_id_entry.get().strip() # (상품게시판은 입력 불가)
                url = "https://openapi.naver.com/v1/cafe/" + clubid + "/menu/" + menuid + "/articles"
                
                data = {"subject": subject, "content": f'{content}\n\n\n{random.random()}'}
                headers = {"Authorization": header}
                response = requests.post(url, headers=headers, data=data)
                rescode = response.status_code
                if(rescode==200):
                    print(response.text)
                else:
                    print(rescode)
                
                count += 1
                progress = count / (len(files) * n_posting) * 100
                p_var.set(progress)
                progressbar.update()
    except Exception as e:
        msgbox.showerror('에러', e)
        return
    
    msgbox.showinfo('알림', f'작업을 종료하였습니다.\n작업 파일: {len(files)}, 총 발행 수: {count}')



start_btn = Button(posting, text='시작', width=10, height=3, command=naver_cafe_post)
start_btn.pack(side='right', padx=5, pady=5)

root.mainloop()

# https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri=https://localhost:8888/&state=REWERWERTATE

# https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri=https://localhost:8888/&code={code}&state=REWERWERTATE

# 30761183