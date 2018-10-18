# -*- coding: utf-8 -*-
from src.https import Http
from src.parse import Parse
from src.setting import headers
from src.setting import cookies
import time,random
import logging
import codecs
import sqlite3


logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s Process%(process)d:%(thread)d %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='diary.log',
                    filemode='a')


def getInfo(url, para):
    """
    获取信息
    """
    generalHttp = Http()
    htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
    generalParse = Parse(htmlCode)
    pageCount = generalParse.parsePage()
    print("总页数:{0}".format(pageCount))

    info = []
    for i in range(1, pageCount + 1):
        print('第%s页' % i)
        para['pn'] = str(i)
        time.sleep(random.randint(1,5))
        try:
            htmlCode = generalHttp.post(url, para=para, headers=headers, cookies=cookies)
            generalParse = Parse(htmlCode)
            info = info + getInfoDetail(generalParse)

            '''
            每5页向文件写一次
            
            '''
            dd = 5
            if(i % dd == 0):
                flag = processInfo(info, para)
                if flag:
                    print("文件写{0}~{1}页的信息".format((i-dd+1),i))
                    info=[]
            if (pageCount-i) < 5:
                flag = processInfo(info, para)
                time.sleep(5)
                if flag:
                    print("文件写{0}页的信息".format(i))
                    info = []

        except Exception as e:
            print(e)
        time.sleep(2)
    return flag


def getInfoDetail(generalParse):
    """
    信息解析
    """
    info = generalParse.parseInfo()
    return info


def processInfo(info, para):
    """
    信息存储
    """
    logging.error('Process start')
    try:
        title = '公司名称\t公司类型\t融资阶段\t标签\t公司规模\t公司所在地\t职位类型\t' \
                '学历要求\t福利\t薪资\t城市\tbusinessZones\t公司简称\t是否校招\tjobNature\t' \
                'positionLables\tpositionName\tresumeProcessDay\tresumeProcessRate\t' \
                'skillLables\tthirdType\tlatitude\tlongitude\tlinestaion\t工作经验\tcreateTime\n'
        file = codecs.open('%s职位.xls' % para['city'], 'a+', 'utf-8')
        file.write(title)
        for p in info:
            line = str(p['companyName']) + '\t' + \
                   str(p['companyType']) + '\t' + \
                   str(p['companyStage']) + '\t' + \
                   str(p['companyLabel']) + '\t' + \
                   str(p['companySize']) + '\t' + \
                   str(p['companyDistrict']) + '\t' + \
                   str(p['positionType']) + '\t' + \
                   str(p['positionEducation']) + '\t' + \
                   str(p['positionAdvantage']) + '\t' + \
                   str(p['positionSalary']) + '\t' + \
                   str(p['city']) + '\t' + \
                   str(p['businessZones']) + '\t' + \
                   str(p['companyShortName']) + '\t' + \
                   str(p['isSchoolJob']) + '\t' + \
                   str(p['jobNature']) + '\t' + \
                   str(p['positionLables']) + '\t' + \
                   str(p['positionName']) + '\t' + \
                   str(p['resumeProcessDay']) + '\t' + \
                   str(p['resumeProcessRate']) + '\t' + \
                   str(p['skillLables']) + '\t' + \
                   str(p['thirdType']) + '\t' + \
                   str(p['latitude']) + '\t' + \
                   str(p['longitude']) + '\t' + \
                   str(p['linestaion']) + '\t' + \
                   str(p['positionWorkYear']) + '\t' + \
                   str(p['createTime']) + '\n'

            file.write(line)
        file.close()
        return True
    except Exception as e:
        print(e)
        return None


def main(url, para):
    """
    主函数逻辑
    """
    logging.error('Main start')
    if url:
        flag = getInfo(url, para)  # 获取信息
        #flag = processInfo(info, para)  # 信息储存

        return flag
    else:
        return None


if __name__ == '__main__':
    kdList = [u'数据',u'算法',u'数据挖掘',u'数据分析',u'大数据']
    cityList = [u'北京']
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    for city in cityList:
        for kd in kdList:
            print('爬取: %s' % kd)
            para = {'first': 'true', 'pn': '1', 'kd': kd, 'city': city}
            flag = main(url, para)
            if flag:
                print('%s爬取成功' % city)
            else:
                print('%s爬取失败' % city)
