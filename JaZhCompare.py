# -*- coding: utf-8 -*-

import urllib
import requests  # 抓取網頁
from bs4 import BeautifulSoup  # 分析HTML
import time  # 製造時間間格
import os  # 建立資料夾
# import pdb  # 除錯用，建立斷點


def create_dir(dir_name):
    if (os.path.exists(dir_name) is False):  # 檢查資料夾存在與否
        os.mkdir(dir_name)
        print '建立資料夾', dir_name
    elif (os.path.exists(dir_name) is True):
        print '資料夾已存在'


def file_save(filename, filetxt, fileEncode=None):
    f02 = open(filename, 'w')
    if fileEncode is not None:
        filetxt = filetxt.encode(fileEncode)
    f02.write(filetxt)
    print 'save:', filename
    f02.close()


def read_file(filePath):
    f = open(filePath, "r")
    file_text = f.read()
    f.close()
    return file_text


def read_dir(dir_path):
    cur_path = os.getcwd()  # 得知目前路徑
    cur_path = cur_path + '\\' + dir_path
    list00 = []
    for root, dirs, files in os.walk(cur_path):
        for f in files:
            list00.append(os.path.join(root, f))
            print os.path.join(root, f)
    return list00


def exciteTranlate01(string00, loop_time=0):
    urlFront = "http://www.excite.co.jp/world/fantizi/?wb_lp=JACH&big5=yes&before="
    res = urllib.quote(string00)
    url00 = urlFront + res
    print '計時10秒'
    for time_sec in range(10, 0, -1):
        time.sleep(1)
        print '倒數 ' + str(time_sec) + ' 秒'
    print '10秒結束'
    print '傳送翻譯資料'

    try:  # 第一次除錯
        response00 = requests.get(url00, timeout=1).content
        print '接收已翻譯資料'
        html00 = BeautifulSoup(response00, 'html.parser')
        result00 = html00.find(id="after").string
    except:
        if loop_time == 10:
            print '翻譯失敗'
        else:
            print 'try除錯區，loop次數：', loop_time
            result00 = exciteTranlate01(string00, loop_time + 1)

    # print '片段翻譯結果：'
    # print result00
    return result00


def removeTopEnd(conbile_txt):
    conbile_txt = conbile_txt.strip('[TOP][ALLTOP]')
    conbile_txt = conbile_txt.strip('[ALLEND][END]')
    conbile_txt = conbile_txt.replace('[END][TOP]', '')
    conbile_txt = conbile_txt.replace('[TOP]', '')
    conbile_txt = conbile_txt.replace('[END]', '')
    conbile_txt = conbile_txt.replace('[ALLTOP]', '')
    conbile_txt = conbile_txt.replace('[ALLEND]', '')
    return conbile_txt

#############################################################

trans_limit = 700

ja_txt = read_file('trans_ja.txt')
ja_txt = '[ALLTOP]' + ja_txt + '[ALLEND]\n'
print '總字數', len(ja_txt)
LineBreakIdxPre = 0
LineBreakIdxNext = 0

ja_dir_path = 'trans_ja'
create_dir(ja_dir_path)

i = 0
while (LineBreakIdxNext >= 0):
    i = i + 1
    print '=========================================='
    LineBreakIdxNext = ja_txt.find('\n', (LineBreakIdxPre + trans_limit))
    transText = ja_txt[LineBreakIdxPre:LineBreakIdxNext]
    print '片段字數：', len(transText)

    if(len(transText) > 0):
        print '分割片段：'
#        print transText
        transText = '[TOP]' + transText + '[END]'
        LineBreakIdxPre = LineBreakIdxNext
        print LineBreakIdxNext
        cut_name = ja_dir_path + '\\trans_ja_' + str(i).zfill(3) + '.txt'
        file_save(cut_name, transText)
    else:
        print '沒東西'
    print '=========================================='

zh_dir_path = 'trans_zh'
create_dir(zh_dir_path)

for ja_cut_file in read_dir(ja_dir_path):
    zh_cut_file = zh_dir_path + '\\trans_ja_' + ja_cut_file.split('_')[-1]

    if (os.path.isfile(zh_cut_file) is True):  # 檢查檔案存在與否
        print zh_cut_file, '已存在'
        continue

    ja_cut_txt = read_file(ja_cut_file)
    zh_cut_txt = exciteTranlate01(ja_cut_txt)
    file_save(zh_cut_file, zh_cut_txt, 'utf-8')

zh_txt = ''
for zh_cut_file in read_dir(zh_dir_path):
    zh_txt += read_file(zh_cut_file)

zh_txt = removeTopEnd(zh_txt)
file_save('trans_zh.txt', zh_txt)

ja_txt = read_file('trans_ja.txt')
zh_txt = read_file('trans_zh.txt')

jpTxtList = ja_txt.split('\n')
zhTxtList = zh_txt.split('\n')
jpTxtLines = len(jpTxtList)
zhTxtLines = len(zhTxtList)
print 'ja行數', jpTxtLines
print 'zh行數', zhTxtLines

table_jpzh = ''
if(jpTxtLines == zhTxtLines):
    j01 = 0
    while(j01 < jpTxtLines):
        table_jpzh += '<tr><td lang="ja" class="jaTD">' + jpTxtList[j01] + '</td>'
        table_jpzh += '<td lang="zh" class="zhTD">' + zhTxtList[j01] + '</td></tr>'
        j01 = j01 + 1
    table_jpzh = '<table>' + table_jpzh + '</table>'
    table_jpzh = table_jpzh.replace('<tr><td lang="ja" class="jaTD"></td><td lang="zh" class="zhTD"></td></tr><tr><td lang="ja" class="jaTD"></td><td lang="zh" class="zhTD"></td></tr><tr><td lang="ja" class="jaTD"></td><td lang="zh" class="zhTD"></td></tr>','<tr><td lang="ja" class="jaTD"></td><td lang="zh" class="zhTD"></td></tr><tr><td lang="ja" class="jaTD">space_line</td><td lang="zh" class="zhTD">space_line</td></tr><tr><td lang="ja" class="jaTD"></td><td lang="zh" class="zhTD"></td></tr>')
    table_jpzh = table_jpzh.replace('<tr><td lang="ja" class="jaTD">space_line</td><td lang="zh" class="zhTD">space_line</td></tr>','<tr><td lang="ja" class="jaTD"></td><td lang="zh" class="zhTD"></td></tr>')

html_jpzh = BeautifulSoup(table_jpzh, 'html.parser').prettify()
#    html_jpzh = BeautifulSoup(html_jpzh, 'html.parser')

pathHTML = 'trans_jazh.html'
file_save(pathHTML, html_jpzh, 'utf-8')
