# -*- coding: utf-8 -*-
# !/usr/bin/python
# @Time    : 2021-03-21
# @Author  : 409162075
# @FileName: zoomeye_url_get_urls.py
# version: 1.0.3


import requests
import config
import random

def main():

    cookies_use = config.__jsluid_s + ';' + config.Hm_lvt_3c8266fabffc08ed4774a252adcb9263 + ';' + config.Hm_lpvt_3c8266fabffc08ed4774a252adcb9263
    if cookies_use:
        pass
    else:
        print('请将cookies填入config文件')

    # 添加随机user-agent,哪颗需要，可以继续向列表中添加
    user_agent_list = [
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/527 (KHTML, like Gecko, Safari/419.3) Arora/0.6 (Change: )",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
        "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Opera/7.51 (Windows NT 5.1; U) [en]",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/28.0.1469.0 Safari/537.36"
    ]
    u_list = random.randint(0, len(user_agent_list)-1)
    user_agent_use = user_agent_list[u_list]


    header_config = {
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept": "application / json, text / plain, * / *",
        "Accept - Encoding": "gzip, deflate",
        "Cube-Authorization": config.Cube_Authorization,
        'User-Agent': user_agent_use,
        "Referer": "https: // www.zoomeye.org /",
        "Cookie": cookies_use
    }

    # 设置每页显示条数，默认为20,可以设置10，20，50
    page_size_config = 20

    search_url = input('[*] 请输入url：')
    search_url = search_url.replace('searchResult?q=', 'search?q=')

    page_start = input('[*] 请输入起始页面：')
    page_stop = input('[*] 请输入截止页面：')

    print()

    # 存储文件
    doc_result = open('result.txt', 'a+')

    ii = 0  # 总数据量
    # 页码范围内抓取
    for page_num in range(int(page_start), int(page_stop) + 1):
        try:
            search_url = search_url + '&page=' + str(page_num) + '&pageSize=' + str(page_size_config)
            html = requests.get(url=search_url, headers=header_config).json()
        except Exception as error:
            print(str(error.args))
            continue

        # 抓取页内数据
        try:
            data_limit = len(html['matches'])
        except Exception as error:
            print('发生错误' + str(error.args))
            print('请检查config文件是否已更新 或者因为抓取频率太高，需刷新网页填写验证码')
            continue

        re_duplicates = set()
        # 去重
        for i in range(0, data_limit):
            # print(i)
            try:
                ip_want = html['matches'][i]['ip']
                if 'portinfo' in html['matches'][i]:

                    port_want = html['matches'][i]['portinfo']['port']
                    service_want = html['matches'][i]['portinfo']['service']
                    data_source = str(service_want) + '://' + str(ip_want) + ':' + str(port_want)

                elif 'site' in html['matches'][i]:
                    data_source = html['matches'][i]['site']
                    raw_data_info = html['matches'][i]['headers']
                    # print(raw_data_info)
                    if 'HTTP/0.9' in raw_data_info:
                        service_info = 'http://'
                    elif 'HTTP/1.0' in raw_data_info:
                        service_info = 'http://'
                    elif 'HTTP/1.1' in raw_data_info:
                        service_info = 'http://'
                    elif 'HTTP/2' in raw_data_info:
                        service_info = 'https://'
                    else:
                        print('未知HTTP协议 请手动确认')
                    data_source = service_info + data_source
                else:
                    print('Error, please issues')
                    pass

                if data_source not in re_duplicates:
                    re_duplicates.add(data_source)
                    print('[+] ' + data_source)
                    doc_result.write(data_source + '\n')
                    i += 1
                else:
                    pass
            except Exception as error:
                print('[!] 发生错误：' + str(error.args))
                i += 1
                continue

        print()
        ii = ii + i
        print('[!] 第' + str(page_num) + '页抓取完毕  共抓取数据' + str(i) + '条\n')

    doc_result.close()
    print('-------抓取完毕------共抓取数据' + str(ii) + '条------' + '\n' * 2)


def logo():
    print(r'''
        __________                    ___________             
        \____    /____   ____   _____ \_   _____/__.__. ____  
          /     //  _ \ /  _ \ /     \ |    __)<   |  |/ __ \ 
         /     /(  <_> |  <_> )  Y Y  \|        \___  \  ___/ 
        /_______ \____/ \____/|__|_|  /_______  / ____|\___  >
                \/                  \/        \/\/         \/ 
                    zoomeye_url_get_urls  without_zoomeye_api
    ''')

if __name__ == '__main__':
    logo()
    main()
