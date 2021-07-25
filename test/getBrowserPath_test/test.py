# -*- coding: GB2312 -*-
import winreg, os
import webbrowser
import sys


# ȡ��������İ�װ·��
def get_path(mainkey, subkey):
    try:
        key = winreg.OpenKey(mainkey, subkey)
    except FileNotFoundError:
        return 'None'
    value, type = winreg.QueryValueEx(key, "")  # ��ȡĬ��ֵ
    full_file_name = value.split(',')[0]  # ��ȥ���ź���Ĳ���
    # print(full_file_name)
    # [dir_name, file_name] = os.path.split(full_file_name)  # �����ļ�����·��
    return full_file_name


# ��ʼ������
ico_ie = r"SOFTWARE\Clients\StartMenuInternet\IEXPLORE.EXE\DefaultIcon"
ico_firefox = r"SOFTWARE\Clients\StartMenuInternet\FIREFOX.EXE\DefaultIcon"
ico_360js = r"SOFTWARE\Clients\StartMenuInternet\360Chrome\DefaultIcon"
ico_google = r"SOFTWARE\Clients\StartMenuInternet\Google Chrome\DefaultIcon"
ico_edge = r"SOFTWARE\Clients\StartMenuInternet\Microsoft Edge\DefaultIcon"

print("IE : " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_ie))

print("��� : " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_firefox))

print("�ȸ� : " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_google))

print("360����: " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_360js))

print("Edge: " + get_path(winreg.HKEY_LOCAL_MACHINE, ico_edge))
url = '../../browser/html/index.html'
chromePath = get_path(winreg.HKEY_LOCAL_MACHINE, ico_google)
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chromePath))
b = webbrowser.get('chrome')
b.open(os.path.abspath(url), new=1, autoraise=True)
sys.exit(0)
