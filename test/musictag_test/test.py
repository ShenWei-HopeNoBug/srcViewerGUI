from assets.publicTools import getMusicInfo
import os

path = r'G:/音乐/RNB36 曲包/{}'.format("01.LOVE - 100年后のきみに.mp3")
infoDict = getMusicInfo(path)
title, artist, cover = infoDict['title'], infoDict['artist'], infoDict['cover']
print('title:', title)
print('artist:', artist)
# print('cover:', cover)
# print(cover.data)
print('----------------------')
print(type(cover))
# for key in dir(cover):
#     print(key)
print(cover['data'])
print(cover['ext'])
