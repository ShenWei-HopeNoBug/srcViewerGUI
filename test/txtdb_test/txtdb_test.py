# -*- coding: GB2312 -*-

import sys
from assets.txtDataBase import TxtDatabase

if __name__ == '__main__':
    path = './test.txt'
    savData = TxtDatabase(path)
    # print(savData.initTxtDb()['msg'])
    print(savData.fallback()['msg'])

    # print(savData.clearAll()['msg'])
    # -------------���Ԫ��
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
    #     '�й�',
    #     '',
    # ])
    # print(savData.printDatas()['data'])

    # -------------����
    print('------------>����')
    # findIndex = [3, 1, 2, -1, 100]
    # print('>>', findIndex)
    # print('=>', savData.findIndexData(findIndex)['data'])
    # print('=>', savData.findDatas(['two', 'one', 'three', '', '�й�', 'lala'])['data'])
    # print('=>', savData.findOneData('one')['data'])
    # print('=>', savData.findOneData('�й�')['data'])
    # print('=>', savData.findOneData('')['data'])
    # print(savData.printDatas()['data'])
    # -------------ɾ��
    print('------------>ɾ��')
    # print('=>', savData.deleteIndexData([-1, 4, 8, 13, 100, 6]))
    # print(savData.printDatas()['data'])
    # print('=>', savData.deleteDatas(['three', 'four', 'five', 'sss', 'one', '�й�', '']))
    # print(savData.printDatas()['data'])
    # print('=>', savData.deleteOneData('one'))
    # print('=>', savData.deleteOneData(''))
    # print(savData.printDatas()['data'])
    # -------------�޸�
    print('------------>�޸�')
    # modifyIndex = {
    #     3: '3',
    #     11: '11',
    #     2: '2',
    #     1000: 'wan',
    #     -1: '-1',
    #     9: '',
    #     5: '�й�'
    # }
    # print('>>', modifyIndex)
    # print('=>', savData.modifyIndexData(modifyIndex)['msg'])
    # print(savData.printDatas()['data'])
    # modifyData = {
    #     'one': '1',
    #     'two': '2',
    #     '�й�': 'ch',
    #     'tree': '4',
    #     '': '��'
    # }
    # print('>>', modifyData)
    # print('=>', savData.modifyDatas(modifyData)['msg'])
    # print(savData.printDatas()['data'])
    sys.exit(0)
