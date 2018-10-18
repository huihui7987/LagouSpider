# -*- coding: utf-8 -*-
import re
import demjson


class Parse:
    '''
    解析网页信息
    '''

    def __init__(self, htmlCode):
        self.htmlCode = htmlCode
        self.json = demjson.decode(htmlCode)
        pass

    def parseTool(self, content):
        '''
        清除html标签
        '''
        if type(content) != str: return content
        sublist = ['<p.*?>', '</p.*?>', '<b.*?>', '</b.*?>', '<div.*?>', '</div.*?>',
                   '</br>', '<br />', '<ul>', '</ul>', '<li>', '</li>', '<strong>',
                   '</strong>', '<table.*?>', '<tr.*?>', '</tr>', '<td.*?>', '</td>',
                   '\r', '\n', '&.*?;', '&', '#.*?;', '<em>', '</em>']
        try:
            for substring in [re.compile(string, re.S) for string in sublist]:
                content = re.sub(substring, "", content).strip()
        except:
            raise Exception('Error ' + str(substring.pattern))
        return content

    def parsePage(self):
        '''
        解析并计算页面数量
        :return: 页面数量
        '''
        totalCount = self.json['content']['positionResult']['totalCount']  # 职位总数量
        resultSize = self.json['content']['positionResult']['resultSize']  # 每一页显示的数量
        pageCount = int(totalCount) // int(resultSize) + 1  # 页面数量
        if pageCount>200:
            pageCount = 200
        return pageCount

    def parseInfo(self):
        '''
        解析信息
        '''
        info = []
        for position in self.json['content']['positionResult']['result']:
            i = {}
            i['city'] = position['city']
            i['businessZones'] = position['businessZones']
            i['companyShortName'] = position['companyShortName']
            i['companyName'] = position['companyFullName']
            i['companyDistrict'] = position['district']
            i['companyLabel'] = position['companyLabelList']
            i['companySize'] = position['companySize']
            i['companyStage'] = position['financeStage']
            i['companyType'] = position['industryField']
            i['industryLables'] = position['industryLables']
            i['positionType'] = position['firstType']
            i['positionEducation'] = position['education']
            i['positionAdvantage'] = position['positionAdvantage']
            i['positionSalary'] = position['salary']
            i['positionWorkYear'] = position['workYear']

            i['isSchoolJob'] = position['isSchoolJob']
            i['jobNature'] = position['jobNature']
            i['positionLables'] = position['positionLables']
            i['positionName'] = position['positionName']
            i['resumeProcessDay'] = position['resumeProcessDay']
            i['resumeProcessRate'] = position['resumeProcessRate']
            i['secondType'] = position['secondType']
            i['skillLables'] = position['skillLables']
            i['thirdType'] = position['thirdType']
            i['latitude'] = position['latitude']
            i['longitude'] = position['longitude']
            i['linestaion'] = position['linestaion']
            i['createTime'] = position['createTime']

            info.append(i)
        return info
