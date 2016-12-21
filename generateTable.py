''''' 
Author:司小幽 
TIME：2016-11-30 ~ 2016-12-1 
function:以”GitLab项目名 用户名 用户权限“的格式将GitLab上的对应数据写入.csv文件（除了Administrator) 
'''  
  
  
import requests  
import json  
import csv  
  
#获取projectId  
urlId = 'http://{Your Git Ip}/api/v3/projects?private_token={Your Private token}'  
projectId = requests.get(urlId)  
idData=json.loads(projectId.text)  
dict={}  
dict1={}  
  
#将项目成员名分别和id以及access_level建立两种映射关系  
def getProjectMember(projectId):  
    urlMember = 'http://{Your Git Ip}/api/v3/projects/'+str(projectId)+'/members?private_token={Your Private token}'  
    projectMember=requests.get(urlMember)  
    membersData=json.loads(projectMember.text)  
    for j in membersData:  
        dict[j["name"]] = j["id"]  
        dict1[j["name"]]=j["access_level"]  
  
#未降权前的除Adminstrator用户的其余项目所有用户以“项目名 用户名 权限”格式输出至报表  
csvfile = file('{Path}', 'wb')  
for projectId in idData:  
    getProjectMember(projectId["id"])  
    for name in dict1:  
        if name != 'Administrator':  
            writer = csv.writer(csvfile)  
            data=[]  
            data.append((projectId["name"], name, dict1[name]))  
            writer.writerows(data)  
csvfile.close()  
