from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgbox

from functions import *

#########################

root = Tk()
root.title("네이버 쇼핑 자동화")

### 유저 아이디, 비밀번호, 네이버 페이 비밀번호
user_info = LabelFrame(master=root, text='사용자 정보')
user_info.pack(fill='x', padx=5, pady=5)

# id frame
id_frame = Frame(user_info)
id_frame.pack(fill='x', padx=5, pady=5)
id_label = Label(master=id_frame, text="네이버 아이디 :")
id_label.pack(side='left', fill='x', padx=5, pady=5)

# id entry
id_entry = Entry(master=id_frame, width=20)
id_entry.pack(side="left", fill="x")

# pw frame
pw_frame = Frame(user_info)
pw_frame.pack(fill='x', padx=5, pady=5)
pw_label = Label(master=pw_frame, text="네이버 비밀번호 :")
pw_label.pack(side='left', fill='x', padx=5, pady=5)

# password entry
pw_entry = Entry(master=pw_frame, width=20)
pw_entry.pack(side="left", fill="x")

# pay number frame
pay_n_frame = Frame(user_info)
pay_n_frame.pack(fill='x', padx=5, pady=5)

# pay number label
pay_n_label = Label(master=pay_n_frame, text="네이버 페이 비밀번호 :")
pay_n_label.pack(side='left', fill='x', padx=5, pady=5)

# pay number entry
pay_n_entry = Entry(pay_n_frame, width=20)
pay_n_entry.pack(side='left', fill='x')


### 구매 상품 사이트
# url frame
url_frame = LabelFrame(master=root, text="자동화 URL 추가")
url_frame.pack(fill='x', padx=5, pady=5)

# url entry
url_entry = Entry(url_frame, width=50)
url_entry.pack(side='left', fill='x', padx=5, pady=5, expand=True)
url_entry.insert(0, '작업할 URL을 입력하고, "추가" 버튼을 누르세요.')

# add url button
def add_url():
    """자동화 작업할 url을 입력하여 listbox에 추가."""
    url = url_entry.get().strip()
    url_listbox.insert(END, url)
    url_entry.delete(0, END)
    
add_url_button = Button(url_frame, text='추가', command=add_url, width=5, height=2)
add_url_button.pack(side='right', padx=10, pady=5)

# url list frame
url_list_frame = LabelFrame(master=root, text="URL 리스트")
url_list_frame.pack(fill='x', padx=5, pady=5)

url_listbox = Listbox(master=url_list_frame, selectmode='extended', height=0, width=50)
url_listbox.pack(fill='x', padx=5, pady=5, expand=True)

# del url button
def del_url():
    """listbox의 url 중 선택한 url 삭제"""
    for idx in reversed(url_listbox.curselection()):
        url_listbox.delete(idx)

del_url_button = Button(url_list_frame, text='삭제', command=del_url, width=10)
del_url_button.pack(side='right', padx=10, pady=5)

### 진행 상황 확인
# label frame
progress_label_frame = LabelFrame(root, text='진행 상황')
progress_label_frame.pack(fill='x', padx=5, pady=5)

p_var = DoubleVar()
progressbar = ttk.Progressbar(progress_label_frame, maximum=100, variable=p_var)
progressbar.pack(fill='x', padx=5, pady=5)

### 시작, 종료 버튼
# frame
run_frame = Frame(master=root)
run_frame.pack(fill="x", padx=5, pady=5)

# close button
close_btn = Button(master=run_frame, text="종료", width=10, padx=5, pady=5, command=root.quit)
close_btn.pack(side="right", padx=5, pady=5)

# run button
def run():
    user_id = id_entry.get().strip()
    user_pw = pw_entry.get().strip()
    pay_pw = pay_n_entry.get().strip()
    
    n_urls = url_listbox.size()
    progress = 0
    count = 0
    p_var.set(progress)
    progressbar.update()
    
    urls = url_listbox.get(0, END)
    for url in urls:
        driver = driver_instance()
        driver = log_in(driver, user_id, user_pw)
        driver = shopping(driver, url.strip())
        click_pay_pw(pay_pw)
        cancel_purchase(driver)
        
        count += 1
        progress = count / n_urls * 100
        p_var.set(progress)
        progressbar.update()

run_btn = Button(master=run_frame, text="전송", width=10, padx=5, pady=5, command=run)
run_btn.pack(side="right", padx=5, pady=5)

root.mainloop()