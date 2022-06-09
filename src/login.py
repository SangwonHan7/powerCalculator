import requests
import getpass

def login(mb_id, mb_password):
    res= requests.post('http://nvj.ipdisk.co.kr:8001/apache/chinghobot1507/bbs/macro_login.php',{'mb_id':mb_id,'mb_password':mb_password}).text
    return res

def loginProcess():
    print('Login(칭호봇 홈페이지 ID,PW 입력)')
    while True:
        mb_id = input('ID : ')
        mb_password = getpass.getpass('PW : ')
    
        loginResult = login(mb_id, mb_password)
        if(loginResult=='fail'):
            print("로그인에 실패했습니다.")
        elif(int(loginResult)<0):
            print("권한이 부족합니다.")
        else:
            break
