'''
Date: 2021-08-22 15:18:09
LastEditors: Steve Li
LastEditTime: 2021-08-22 16:07:24
FilePath: \baidurecordingquery\api\index.py
'''
from requests import *
from re import *
from json import dumps
from http.server import BaseHTTPRequestHandler
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin',"*")
        self.send_header('Content-type','application/json')
        self.end_headers();
        try:
            domain = compile(r'domain=([^?&=]*)').findall(self.path);
            if len(domain)==0:
                self.wfile.write(dumps({
                    "code": 0,
                    "msg": "未传入请求参数！"
                }).encode())
                return;
            resp = get("https://www.baidu.com/s?ie=UTF-8&wd="+domain[0]+"&usm=3&rsv_idx=2&rsv_page=1",headers={
                "Host": "www.baidu.com",
                "Content-Type":"application/x-www-form-urlencoded",
                "Connection":"keep-alive",
                "Referer":"https://www.baidu.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"
            }).text
            if resp.find("没有找到")!=-1 or resp.find("很抱歉")!=-1:
                self.wfile.write(dumps({
                    "code": 403,
                    "msg": "该域名暂时未被百度收录！"
                }).encode())
                return;
            else:
                number = 0;
                try:
                    number =  int(resp[ resp.find('''<span class="nums_text">百度为您找到相关结果约''')+35: resp.find('''个</span>''')].replace(',',''))
                except Exception as e:
                    number = 0;
                finally:
                    pass;
                if number==0:
                    self.wfile.write(dumps({
                        "code": 0,
                        "msg": "获取百度收录失败！"
                    }).encode())
                    return;
                self.wfile.write(dumps({
                        "code": 200,
                        "msg": "该域名已被百度收录！",
                        "number": str(number)
                    }).encode())
                return;
        except Exception as e:
            self.wfile.write(dumps({
                        "code": 0,
                        "msg": "获取百度收录失败！"
                    }).encode())
            return;
        finally:
            return;
    def do_POST(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin',"*")
        self.send_header('Content-type','application/json')
        self.end_headers();
        self.wfile.write(dumps({
            "code":500,
            "msg":"Method Not Allowed"
        }))
        return;
