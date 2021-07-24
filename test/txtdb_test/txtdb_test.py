# -*- coding: GB2312 -*-

import sys
from assets.txtDataBase import TxtDatabase

if __name__ == '__main__':
    path = './test.txt'
    savData = TxtDatabase(path)
    # print(savData.initTxtDb()['msg'])
    print(savData.fallback()['msg'])

    # print(savData.clearAll()['msg'])
    # -------------添加元素
    # savData.addDatas([
    #     'one',
    #     'two',
    #     'three',
    #     'four',
    #     'five',
    #     'six'
    # ])
    # savData.addDatas([
    #     'seven',
    #     'eight',
    #     'nine',
    #     'ten',
    #     'one',
    #     '',
    #     '中国',
    #     '',
    # ])
    # print(savData.printDatas()['data'])

    # -------------查找
    print('------------>查找')
    # findIndex = [3, 1, 2, -1, 100]
    # print('>>', findIndex)
    # print('=>', savData.findIndexData(findIndex)['data'])
    # print('=>', savData.findDatas(['two', 'one', 'three', '', '中国', 'lala'])['data'])
    # print('=>', savData.findOneData('one')['data'])
    # print('=>', savData.findOneData('中国')['data'])
    # print('=>', savData.findOneData('')['data'])
    # print(savData.printDatas()['data'])
    # -------------删除
    print('------------>删除')
    # print('=>', savData.deleteIndexData([-1, 4, 8, 13, 100, 6]))
    # print(savData.printDatas()['data'])
    # print('=>', savData.deleteDatas(['three', 'four', 'five', 'sss', 'one', '中国', '']))
    # print(savData.printDatas()['data'])
    # print('=>', savData.deleteOneData('one'))
    # print('=>', savData.deleteOneData(''))
    # print(savData.printDatas()['data'])
    # -------------修改
    print('------------>修改')
    # modifyIndex = {
    #     3: '3',
    #     11: '11',
    #     2: '2',
    #     1000: 'wan',
    #     -1: '-1',
    #     9: '',
    #     5: '中国'
    # }
    # print('>>', modifyIndex)
    # print('=>', savData.modifyIndexData(modifyIndex)['msg'])
    # print(savData.printDatas()['data'])
    # modifyData = {
    #     'one': '1',
    #     'two': '2',
    #     '中国': 'ch',
    #     'tree': '4',
    #     '': '空'
    # }
    # print('>>', modifyData)
    # print('=>', savData.modifyDatas(modifyData)['msg'])
    # print(savData.printDatas()['data'])
    sys.exit(0)
