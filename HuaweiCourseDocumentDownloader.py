# coding: utf-8
#----------------------------------------------------------------------------
# created by: snow
# repo: https://github.com/penguin806/HuaweiCourseDocumentDownloader
# version: 1.0
# ---------------------------------------------------------------------------
import datetime
import gzip
import os
import requests


projectId = '____PROJECT_ID_HERE____'
documentId = '____DOCUMENT_ID_HERE____'
authorizationToken = '____AUTHORIZATION_TOKEN_HERE____'
savePath = './snow_downloads/'



requestHeaders = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'EDM-Authorization': authorizationToken,
    'Pragma': 'no-cache',
    'Referer': 'https://learning.huaweils.com/edm3client/static/index.html?lang=zh_CN&showDownload=hide&appid=snow_downloader',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

requestParams = {
    'docVersion': 'V1',
    'wmType': '',
    'renderDocType': '',
    'docFormat': '',
    'X-HW-ID': '',
    'X-HW-APPKEY': '',
    'X-IAM-SECRET': '',
    'X-IAM-ACCOUNT': '',
    'X-HIC-Info': '',
    'userId': '',
}

def getDocumentParameters():
    url = 'https://learning.huaweils.com/edm/projects/' + projectId + '/previewer/documents/' + documentId

    response = requests.get(url, params = requestParams, headers = requestHeaders)
    if(response.status_code == 200):
        return response.json()
    else:
        raise Exception('getDocumentParameters failed: ' + response.text)


def getDocumentSpecifiedPage(pageNum, totalPage):
    url = 'https://learning.huaweils.com/edm/projects/' + projectId + '/previewer/documents/' + documentId
    
    dataToPost = {
        'docFormat': 'src',
        'docId': documentId,
        'docVersion': 'V1',
        'documentIndex': 1,
        'pageNum': pageNum,
        'type': 'doc',
        'totalPage': totalPage,
    }

    response = requests.post(url, params = requestParams, headers = requestHeaders, json = dataToPost)
    if response.status_code == 200:
        return gzip.decompress(response.content)
    else:
        raise Exception('getDocumentSpecifiedPage failed: ' + response.text)


def savePageAsSvgFile(containerDir, svgContent, pageNum):
    fileName = containerDir + str(pageNum) + '.svg'
    with open(fileName, 'wb') as f:
        f.write(svgContent)



if __name__ == '__main__':
    print(r'''
      ___           ___           ___           ___     
     /\  \         /\__\         /\  \         /\__\    
    /::\  \       /::|  |       /::\  \       /:/ _/_   
   /:/\ \  \     /:|:|  |      /:/\:\  \     /:/ /\__\  
  _\:\~\ \  \   /:/|:|  |__   /:/  \:\  \   /:/ /:/ _/_ 
 /\ \:\ \ \__\ /:/ |:| /\__\ /:/__/ \:\__\ /:/_/:/ /\__\
 \:\ \:\ \/__/ \/__|:|/:/  / \:\  \ /:/  / \:\/:/ /:/  /
  \:\ \:\__\       |:/:/  /   \:\  /:/  /   \::/_/:/  / 
   \:\/:/  /       |::/  /     \:\/:/  /     \:\/:/  /  
    \::/  /        /:/  /       \::/  /       \::/  /   
     \/__/         \/__/         \/__/         \/__/    
    ''')
    print('-------------- Download Started --------------')
    print('Project ID: ' + projectId)
    print('Document ID: ' + documentId)

    try:
        docParams = getDocumentParameters()
        totalPage = docParams['totalPage']
        print('totalPage: ' + str(totalPage))

        containerDir = savePath + documentId + '_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '/'
        if not os.path.exists(containerDir):
            os.makedirs(containerDir)
        print('The document files will be saved to: ' + containerDir)

        for currentPage in range(1, totalPage + 1):
            pageContent = getDocumentSpecifiedPage(currentPage, totalPage)
            savePageAsSvgFile(containerDir, pageContent, currentPage)
            print(f'Retrieve Page {currentPage} of {totalPage}...  OK')

        # Todo: Combine all svg files into pdf

        print('-------------- Download Finished --------------')

    except Exception as e:
        print(e)