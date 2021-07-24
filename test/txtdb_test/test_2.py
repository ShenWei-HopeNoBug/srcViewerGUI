import sys
from assets.txtDataBase import TxtDatabase

if __name__ == '__main__':
    path = './test.txt'
    savData = TxtDatabase(path)
    savData.clearAll()
    # -------------添加元素
    savData.addDatas([
        '游戏王',
        '',
        'three',
        'four',
        '',
        'six'
    ])
    oldList = savData.printDatas()['data']
    dataDict = {
        -1: '游戏王者',
        6: 'five'
    }
    # print(savData.modifyIndexData(dataDict))
    print(savData.modifyIndexData(dataDict))
    print('-' * 50)
    print('原数组：', oldList)
    print('修改后：', savData.printDatas()['data'])
