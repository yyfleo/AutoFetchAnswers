# coding = utf-8
from urllib import request
from http import cookiejar
from .GetTaskList import getCsrf, generateRequest
import json
import time
import ctypes
import os

seewoClassTaskInfoPath = "https://class.seewo.com/student/adpter.json?action=FETCH_STUDENT_TASK&method=POST"
seewoClassCacheExamPath = "https://class.seewo.com/student/adpter.json?action=CACHE_EXAM&method=POST"
seewoClassExamSubmitPath = "https://class.seewo.com/student/adpter.json?action=CONFIRM_SAVE_EXAM&method=POST"


def getUserInfo(xToken: str, output=False, csrf=getCsrf()):
    res = generateRequest("FETCH_FRIDAY_INFO", xToken, csrf)
    if output:
        j = json.loads(res)
        print("Result:", j["code"], j["msg"])
        if j["code"] == 0:
            for item in j["data"]:
                print(item + ":" + str(j["data"][item]))
    return res


def getUserId(xToken: str, output=False, csrf=getCsrf()):
    res = getUserInfo(xToken, output, csrf)
    j = json.loads(res)
    if j["code"] == 0:
        return j["data"]["userId"]
    else:
        raise AttributeError(
            "userId not found! Maybe your x-token is wrong or expired.")


def generateRequestWithTaskId(operation: str, xToken: str, taskID: str, csrf=getCsrf(), url=""):
    c = cookiejar.CookieJar()
    headers = {"Content-Type": "application/json",
               "x-csrf-token": csrf,
               "Cookie": "csrfToken=" + csrf + "; "
               + "x-token=" + xToken}
    p = request.HTTPCookieProcessor(c)
    d = bytes(json.dumps({"actionName": operation, "params": {
              "router": {"taskId": taskID}}}), encoding="utf-8")
    o = request.build_opener(p)
    if operation == "FETCH_STUDENT_TASK":
        req = request.Request(url=seewoClassTaskInfoPath,
                              data=d, headers=headers)
    elif operation == "CONFIRM_SAVE_EXAM":
        req = request.Request(url=seewoClassExamSubmitPath,
                              data=d, headers=headers)
    elif url != "":
        req = request.Request(url=url, data=d, headers=headers)
    else:
        raise AttributeError("Operation Invaild.")
    res = o.open(req).read().decode("utf-8")
    return res


def getTaskInfo(xToken: str, taskID: str, output=False, csrf=getCsrf()):
    res = generateRequestWithTaskId("FETCH_STUDENT_TASK", xToken, taskID, csrf)
    if output:
        j = json.loads(res)
        print("Result:", j["code"], j["msg"])
        if j["code"] == 0:
            for item in j["data"]:
                print(item + ":" + str(j["data"][item]))
    return res


def getQuestionNum(xToken: str, taskID: str, output=False, csrf=getCsrf()):
    res = getTaskInfo(xToken, taskID, output, csrf)
    j = json.loads(res)
    if j["code"] == 0:
        return j["data"]["questionNum"]
    else:
        raise AttributeError(
            "questionNum not found! Maybe your x-token or taskId is wrong.")


def cacheAnswers(xToken: str, taskID: str, answers: list, usedTime: int, output=False, csrf=getCsrf()):
    tmp = {"actionName": "CACHE_EXAM", "params": {"answers": answers, "commitTime": int(time.time(
    )*1000), "taskId": taskID, "usedTime": usedTime, "userId": getUserId(xToken, False, csrf)}}
    c = cookiejar.CookieJar()
    headers = {"Content-Type": "application/json",
               "x-csrf-token": csrf,
               "Cookie": "csrfToken=" + csrf + "; "
               + "x-token=" + xToken}
    p = request.HTTPCookieProcessor(c)
    # to solve the code of Chinese
    # s = json.dumps(tmp).encode("unicode_escape").decode("unicode_escape")
    # d = bytes(s.replace("'", "\\\""), encoding="utf-8")
    d = bytes(json.dumps(tmp).replace("'", "\\\""), encoding="utf-8")
    print(d)
    o = request.build_opener(p)
    req = request.Request(url=seewoClassCacheExamPath, data=d, headers=headers)
    res = o.open(req).read().decode("utf-8")
    print(res)
    j = json.loads(res)
    if output:
        print("Result:", j["code"], j["msg"])
    return res


def handInExam(xToken: str, taskID: str, output=False, csrf=getCsrf()):
    res = generateRequestWithTaskId("CONFIRM_SAVE_EXAM", xToken, taskID, csrf)
    if output:
        j = json.loads(res)
        print("Result:", j["code"], j["msg"])
        if j["code"] == 0:
            for item in j["data"]:
                print(item + ":" + str(j["data"][item]))
    return res
