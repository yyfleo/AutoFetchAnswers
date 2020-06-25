import os
import json
import time
import glob
from SeewoClassApi import GetCookies, GetTaskList, GetAnswer, GetTaskList

print("Seewo eClass Fetch Reference Answer Tool Embed")
print("V2.2 Embed in Github Actions")
print("By yyfleo.")
print("Build 20200625\n")
print("请注意：")
print("本软件仅供学习与交流使用，查到的答案也仅供作业校对订正时参考，请勿使用于非法用途！")
print("使用本软件所产生的一切后果由使用者承担，软件编写者不负任何责任！")
print("使用本软件即代表你同意以上条款，否则请立即关闭本软件！")

if not os.path.exists("docs"):
    os.makedirs("docs")
csrf = GetTaskList.getCsrf()
token = os.environ["x-token"]
j = json.loads(GetTaskList.getAccountUndoneTasks(token, False, csrf))

print("\nGot tasks list success! Fetching answers list sequentially......")
i = 1
for item in j["data"]:
    print(str(i) + ".", item["taskName"])
    taskid = j["data"][i - 1]["taskId"]
    with open("docs/" + item["taskName"] + ".html", "w") as f:
        f.write("<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>The reference answers for ")
        f.write(item["taskName"])
        f.write("</title></head>")
        f.write("<body>")
        f.write(item["taskName"])
        f.write("<br>Last updated on ")
        f.write(time.asctime(time.localtime(time.time())))
        f.write(" (UTC)<br>")
        GetAnswer.fetchAnswers(token, taskid, f, True, csrf)
        f.write("</body></html>")
    i = i + 1

print("\nFetched all answers successfully. Generating index.html......")
with open("docs/index.html", "w") as f:
    f.write("<!DOCTYPE html><html><head><meta charset=\"utf-8\"><title>The fetched answers list</title></head>")
    f.write("<body><h2>Fetched answers list:</h2><i>Updates on 4, 10, 15 UTC every day</i><br><i>Last updated on ")
    f.write(time.asctime(time.localtime(time.time())))
    f.write(" (UTC)</i>")
    count = 1
    for filename in sorted(glob.glob(os.getcwd() + "/docs/*.html")):
        temp = filename.split("/")
        if temp[len(temp) - 1] == "index.html":
            continue
        f.write(str(count))
        f.write(". ")
        f.write("<a href=\"" + temp[len(temp) - 1] + "\">")
        i = 1
        temp = temp[len(temp) - 1].split(".")
        for item in temp:
            if not i == len(temp):
               f.write(item)
            i = i + 1
        f.write("</a><br>")
        count = count + 1
    f.write("<h5>Powered by Seewo eClass Fetch Reference Answer Tool Embed, powered by Github Actions and Seewo Class Api, deployed on Github Pages.</h5>")
    f.write("</body></html>")
