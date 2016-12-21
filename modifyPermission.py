''''' 
Author:司小幽 
time：2016-11-30 ~ 2016-12-1 
function:遍历GitLab上的项目，将每个项目中除Administrator用户外，其余具有master权限的用户更改为developer权限。 
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
  
#修改成员权限，并将更改权限的成员名输出至报表  
def modifyUserLevel(projectId):  
    getProjectMember(projectId)  
    for name in dict1:  
        if name != 'Administrator':  
            if dict1[name] == 40:  
                    urlPut='http://{Your Git Ip}/api/v3/projects/'+str(projectId)+'/members/'+str(dict[name])+'?access_level=30?private_token={Your Private token}'  
                    put=requests.put(urlPut)  
                    writer = csv.writer(csvfile)  
                    data=[]  
                    data.append(name)  
                    writer.writerows(data)  
#主方法  
csvfile = file('{Path}', 'wb')  
for projectId in idData:  
    modifyUserLevel(projectId["id"])  
csvfile.close()  
