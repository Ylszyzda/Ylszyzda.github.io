#-*- coding: utf-8 -*-
#    __                     
#   / /    _  __        ____   _____
#  / /    | |/_/______ / __ \ / ___/
# / /___ _>  < /_____// /_/ /(__  ) 
#/_____//_/|_|        \____//____/  

import os
import sys
import time
import  json
import pywifi
import requests

url_version = 'https://ylszyzda.github.io/version.json'
url_py = 'https://ylszyzda.github.io/OS.py'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61'}

try:
    with open("config.json","r") as json_file:
        config = json.load(json_file)

except:
    print('[Error] json file is not configured')
    print('Setting config...')
    errorname = input('Please input your username: ')
    configuredjson = open("config.json",'a+')
    print('waiting...')
    print("{\"userconfig\":{\"language\":\"EN\",\"version\":\""+config["userconfig"]['version']+"\",\"username\":\"None\",\"firstusing\":\"True\"}}",file=configuredjson)
    print('down!')
    configuredjson.close()
    with open("config.json","r") as json_file:
        config = json.load(json_file)


class mainOS:

    def init():
        username = config["userconfig"]["username"]
        print('Hello! '+username)
        print('Welcome to use Lx-OS v'+config["userconfig"]["version"])
        if config["userconfig"]["language"] == "EN":
            print('input \'help\' for help')
        else:print('输入 \'help\' 获取帮助')
        if config["userconfig"]["firstusing"] == "True":
            jsfile1 = open("config.json","w")
            print('If you first use it,please read \'README\'')
            language = input("choose your language(简体中文(输入Chinese) or English):").capitalize()
            if language == 'Chinese':
                config["userconfig"]["language"] = "CH"
            else:
                config["userconfig"]["language"] = "EN"
            config["userconfig"]["firstusing"] = "False"
            print("{\"userconfig\":{\"language\":"+"\""+config['userconfig']['language']+"\""+",\"version\":\""+config["userconfig"]['version']+"\",\"username\":\""+config["userconfig"]['username']+"\",\"firstusing\":\""+config["userconfig"]["firstusing"]+"\"}"+"}",file=jsfile1)
    
    def documentsshow():
        file1 ='.\\file\\'
        for root,dirs,files in os.walk(file1):
            for name in files:
                print(os.path.join(name))

    def documentopen(documentname):
        file1 ='.\\file\\'
        i = 0
        elseable = 0
        for root,dirs,files in os.walk(file1):
            for name in files:
                i += 1
                if documentname == name:
                    elseable = 1
                    if config["userconfig"]["language"] == "EN":
                        print('found the document successfully')
                        dmchc = input('choose the type of opening\ninput read or write or remove:\n')
                    else:
                        print('已成功找到文件')
                        dmchc = input('选择文件操作类型\n输入 read 或 write 或 remove:\n')
                    
                    if dmchc == 'read':
                        filepath = open('file\\'+documentname,'r')
                        txt = filepath.read()  
                        print('\n')
                        print(txt)
                        print('\n')
                        filepath.close()
                    if dmchc == 'write':
                        filepath = open('file\\'+documentname,'a')
                        if config["userconfig"]["language"] == "EN":
                            txt2 = input('Please write the document down.\n')
                        else:
                            txt2 = input('请输入要写入的文件内容\n')
                        print('\n'+txt2,file=filepath)
                        filepath.close
                        if config["userconfig"]["language"] == "EN":
                            print('write successfully')
                        else:
                            print('成功写入')
                    if dmchc == 'remove':
                        filepath = open('file\\'+documentname,'w') 
                        print('',file=filepath)
                        filepath.close()
                else:
                    if elseable == 0:
                        if config["userconfig"]["language"] == "EN":
                            print("Matching files..."+"("+str(i)+")" " maybe can not find the document")
                        else:
                            print("匹配文件中..."+"("+str(i)+")" " 可能无法找到文件")

    def run(documentname):
        try:
            os.system('python file\\'+documentname)
        except FileNotFoundError:
            if config["userconfig"]["language"] == "EN":
                print('[Error]Can not open \'' + documentname + ' \'')
            else:
                print('[Error]未能打开文件 \''+documentname+' \'')

    def app():
        if config["userconfig"]["language"] == "EN":
            chc2 = input('choose to input applist or apprun:\n')
        else:
            chc2 = input('输入 applist 或 apprun:\n')
        if chc2 == 'applist':
            file2 ='.\\apps\\'
            print('\n')
            for root,dirs,files in os.walk(file2):
                for name in files:
                    print(os.path.join(name))
        if chc2 == 'apprun':
            if config["userconfig"]["language"] == "EN":
                appname = input('input appname:\n')
            else:
                appname = input("输入应用名称:\n")
            os.system('python apps\\'+appname)

    def warn(e):
        print("warn:"+str(e))

    def wifi():
        print('interface\nscan\nconnect [ssid] [password]')

        def wifi_interfaces():
            wifi = pywifi.PyWiFi()
            ifaces=wifi.interfaces()[0]
            if ifaces.status() in[pywifi.const.IFACE_CONNECTED,pywifi.const.IFACE_CONNECTING]:
                print('interface: %s connected'% ifaces.name())
            else:
                print("interface: %s disconnected"% ifaces.name())

        def wifi_scan():
            wifi = pywifi.PyWiFi()
            ifaces = wifi.interfaces()[0]
            ifaces.scan()
            results = ifaces.scan_results()
            for name in results:
                print('wifi:%s' % name.ssid)

        def wifi_connect(ssid,password):
            wifi = pywifi.PyWiFi()
            ifaces = wifi.interfaces()[0]
            ifaces.disconnect()
            time.sleep(3)
            profile_info=pywifi.Profile()
            profile_info.ssid=ssid
            profile_info.auth=pywifi.const.AUTH_ALG_OPEN
            profile_info.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
            profile_info.cipher = pywifi.const.CIPHER_TYPE_CCMP
            profile_info.key = password
            ifaces.remove_all_network_profiles()
            tmp_profile = ifaces.add_network_profile(profile_info)
            ifaces.connect(tmp_profile)
            print('Wait...')
            time.sleep(5)
            if ifaces.status()==pywifi.const.IFACE_CONNECTED:
                print('Okay!')
            else:
                print('Error!')

        c = input('>> ')
        s = c.split(' ')
        if s[0] == 'interface':
            wifi_interfaces()
        elif s[0] == 'scan':
            wifi_scan()
        elif s[0] == 'connect':
            wifi_connect(ssid=s[1],password=s[2])

def updata():

    r1 = requests.get(url=url_version,headers=header)
    version = r1.json()['v']

    def download():
        try:
            jsfile1 = open("config.json","w")
            r2 = requests.get(url=url_py,headers=header,allow_redirects=True)
            open('OS_new.py',"wb").write(r2.content)
            if config["userconfig"]["language"] == "EN":
                print('Successfully download \'OS_new.py\'')
            else:
                print('成功下载\'OS_new.py\',请手动删除旧文件并运行新版本文件')
            print("{\"userconfig\":{\"language\":"+"\""+config['userconfig']['language']+"\""+",\"version\":\""+version+"\",\"username\":\""+config["userconfig"]['username']+"\",\"firstusing\":\""+config["userconfig"]["firstusing"]+"\"}"+"}",file=jsfile1)
            jsfile1.close()
        except Exception as e:
            print(f'[Error: {e}]')

    if config["userconfig"]["version"] != version:
        if config["userconfig"]["language"] == "EN":
            print('find new version')
            c = input('download new version?y/n:')
            if c == 'y':
                download()
        else:
            print("找到了新版本")
            c = input('是否下载新版本?y/n:')
            if c == 'y':
                download()
    if config["userconfig"]["version"] == version:
        if config["userconfig"]["language"] == "EN":
            print('cannot find new version')
        else:
            print('当前版本已为最新版本')

def mainloop():
    chc = str(input('> '))

    if chc == 'help':
        if config["userconfig"]["language"] == "EN":
            print('\n************************************************************\ninput these commands to implement\ndocuments:show the documents name that you save in /file/\nopen:open a document and changing or reading it\nrun:run a document which type is .py\napp:check the list of app and run them\nsetting:change settings\nquit\n************************************************************\n')
        else:
            print('\n************************************************************\n输入以下命令来执行\ndocuments:显示你保存在路径/file/中的文件\nopen:打开一个文件并且更改或读取它\nrun:运行一个类型为\'.py\'的程序\napp:查看应用列表并且允许它们\nsetting:更改设置\nquit:退出OS\n************************************************************\n')

    if chc == 'documents':
        mainOS.documentsshow()

    if chc == 'open':
        if config["userconfig"]["language"] == "EN":
            mainOS.documentopen(documentname=input('Please input document name:\n'))
        else:
            mainOS.documentopen(documentname=input('请输入文件名:\n'))

    if chc == 'run':
        if config["userconfig"]["language"] == "EN":
            mainOS.run(input('input document name:\n'))
        else:
            mainOS.run(input('请输入文件名:\n'))

    if chc == 'app':
        mainOS.app()

    if chc == 'setting':
        jsfile1 = open("config.json","w")
        if config["userconfig"]["language"] == "EN":
            print('1.username\n2.language\n')
            chc4 = input('please input the number:\n')
            if chc4 == '1':
                config["userconfig"]['username'] = input('input the new username:\n')
                print("{\"userconfig\":{\"language\":"+"\""+config['userconfig']['language']+"\""+",\"version\":\""+config["userconfig"]['version']+"\",\"username\":\""+config["userconfig"]['username']+"\",\"firstusing\":\""+config["userconfig"]["firstusing"]+"\"}"+"}",file=jsfile1)
            if chc4 == '2':
                config["userconfig"]["language"] = input('input CH or EN\n')
                print("{\"userconfig\":{\"language\":"+"\""+config['userconfig']['language']+"\""+",\"version\":\""+config["userconfig"]['version']+"\",\"username\":\""+config["userconfig"]['username']+"\",\"firstusing\":\""+config["userconfig"]["firstusing"]+"\"}"+"}",file=jsfile1)
        else:
            print('1.username\n2.language\n')
            chc4 = input('请输入序号:\n')
            if chc4 == '1':
                config["userconfig"]['username'] = input('输入新用户名:\n')
                print("{\"userconfig\":{\"language\":"+"\""+config['userconfig']['language']+"\""+",\"version\":\""+config["userconfig"]['version']+"\",\"username\":\""+config["userconfig"]['username']+"\",\"firstusing\":\""+config["userconfig"]["firstusing"]+"\"}"+"}",file=jsfile1)
            if chc4 == '2':
                config["userconfig"]["language"] = input('输入 CH 或 EN\n')
                print("{\"userconfig\":{\"language\":"+"\""+config['userconfig']['language']+"\""+",\"version\":\""+config["userconfig"]['version']+"\",\"username\":\""+config["userconfig"]['username']+"\",\"firstusing\":\""+config["userconfig"]["firstusing"]+"\"}"+"}",file=jsfile1)

    if chc == 'quit':
        if config["userconfig"]["language"] == "EN":
            chc3 = input('input y/n:')
        else:
            chc3 = input('输入 y或n:')
        if chc3 =='y':
            json_file.close()
            sys.exit()

    if chc == 'updata':
        updata()

    if chc == 'wifi':
        mainOS.wifi()

    if chc != 'help' and chc != 'documents' and chc !='open' and chc != 'run' and chc != 'app' and chc != 'quit' and chc != 'setting' and chc !='updata' and chc !='wifi':
        if config["userconfig"]["language"] == "EN":
            print('================\nunknown command!\n================')
        else:
            print("================\n未知命令!\n================")

if __name__ == "__main__":
    mainOS.init()
    while True:
        mainloop()
