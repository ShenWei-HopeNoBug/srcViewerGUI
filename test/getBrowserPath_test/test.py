# -*- coding: GB2312 -*-
import winreg, os
import webbrowser
import sys


# 取得浏览器的安装路径
def get_path(mainkey, subkey):
    try:
        key = winreg.OpenKey(mainkey, subkey)
    except FileNotFoundError:
        return 'None'
    value, type = winreg.QueryValueEx(key, "")  # 获取默认值
    full_file_name = value.split(',')[0]  # 截去逗号后面的部分
    # print(full_file_name)
    # [dir_name, file_name] = os.path.split(full_file_name)  # 分离文件名和路径
    return full_file_name


# 初始化变量
ico_ie = r"SOFTWARE\Clients\StartMenuInternet\IEXPLORE.EXE\DefaultIcon"
ico_firefox = r"SOFTWARE\Clients\StartMenuInternet\FIREFOX.EXE\DefaultIcon"
ico_360js = r"SOFTWARE\Clients\StartMenuInternet\360Chrome\DefaultIcon"
ico_google = r"SOFTWARE\Clients\StartMenuInternet\Google Chrome\DefaultIcon"
ico_edge = r"SOFTWARE\Clients\StartMenuInternet\Microsoft Edge\DefaultIcon"

print("IE : " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_ie))

print("火狐 : " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_firefox))

print("谷歌 : " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_google))

print("360极速: " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_360js))

print("Edge: " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_edge))
url = '../../browser/html/index.html'
chromePath = get_path(winreg.HKEY_LOCAL_MACHINE, ico_google)
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
b = webbrowser.get('chrome')
b.open(os.path.abspath(url), new=1, autoraise=True)
sys.exit(0)
