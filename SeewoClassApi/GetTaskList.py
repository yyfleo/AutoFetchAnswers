# coding = utf-8
from urllib import request
from http import cookiejar
import json
import time

seewoClassLoginPath = "https://class.seewo.com/student/login"
seewoClassUndoneTasksGetPath = "https://class.seewo.com/student/adpter.json?action=FETCH_HOME_TASK&method=POST"
seewoClassTeachersGetPath = "https://class.seewo.com/student/adpter.json?action=FETCH_TASKS_FILTER&method=POST"
seewoClassTasksGetPath = "https://class.seewo.com/student/adpter.json?action=FETCH_TASKS&method=POST"
seewoClassUserInfoGetPath = "https://class.seewo.com/student/adpter.json?action=FETCH_FRIDAY_INFO&method=POST"

def getCsrf():
    """ Fetch the csrfToken of this session. """
    c = cookiejar.CookieJar()
    h = request.HTTPCookieProcessor(c)
    request.build_opener(h).open(seewoClassLoginPath)
    for item in c:
        if item.name == "csrfToken":
            return item.value
    return ""


def generateRequest(operation: str, xToken: str, csrf=getCsrf(), url=""):
    """ Generate a request and return the result.\n
        Vaild operations: FETCH_HOME_TASK, FETCH_TASKS_FILTER, FETCH_TASKS, FETCH_FRIDAY_INFO """
    c = cookiejar.CookieJar()
    headers = {"x-csrf-token": csrf,
               "Cookie": "csrfToken=" + csrf + "; "
               + "x-token=" + xToken}
    p = request.HTTPCookieProcessor(c)
    d = bytes(json.dumps({"actionName": operation}), encoding="utf-8")
    o = request.build_opener(p)
    if operation == "FETCH_HOME_TASK":
        req = request.Request(
            url=seewoClassUndoneTasksGetPath, data=d, headers=headers)
    elif operation == "FETCH_TASKS_FILTER":
        req = request.Request(
            url=seewoClassTeachersGetPath, data=d, headers=headers)
    elif operation == "FETCH_TASKS":
        req = request.Request(
            url=seewoClassTasksGetPath, data=d, headers=headers)
    elif operation == "FETCH_FRIDAY_INFO":
        req = request.Request(
            url=seewoClassUserInfoGetPath, data=d, headers=headers)
    elif url != "":
        req = request.Request(url=url, data=d, headers=headers)
    else:
        raise AttributeError("Operation Invaild.")
    res = o.open(req).read().decode("utf-8")
    return res


def getAccountTeachers(xToken: str, output=False, csrf=getCsrf()):
    """ Print the list of teachers who have sent the given account homework. """
    res = generateRequest("FETCH_TASKS_FILTER", xToken, csrf)
    if output:
        j = json.loads(res)
        print("Result:", j["code"], j["msg"])
        if j["code"] == 0:
            print("Subjects:")
            for s in j["data"]["subjects"]:
                print(s["text"])
            print("Teachers:")
            for s in j["data"]["teachers"]:
                print(s["value"], s["text"])
    return res


def getAccountUndoneTasks(xToken: str, output=False, csrf=getCsrf()):
    """ Print the undone homework list of the given account. """
    res = generateRequest("FETCH_HOME_TASK", xToken, csrf)
    if output:
        j = json.loads(res)
        print("Result:", j["code"], j["msg"])
        if j["code"] == 0:
            print("Count:", len(j["data"]))
            i = 1
            for item in j["data"]:
                print("")
                print("==========")
                print(str(i) + "." + item["taskName"] + ": " + item["subjectName"])
                print("taskId:", item["taskId"])
                print("questionNum:", item["questionNum"])
                print("publisher:", item["publisher"])
                print("studentNum:", item["studentNum"])
                print("finishExercisesNum:", item["finishExercisesNum"])
                print("createTime:", time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.localtime(item["createTime"]/1000)))
                print("updateTime:", time.strftime("%Y-%m-%d %H:%M:%S",
                                                   time.localtime(item["updateTime"]/1000)))
                print("closeTaskTime:", time.strftime("%Y-%m-%d %H:%M:%S",
                                                      time.localtime(item["closeTaskTime"]/1000)))
                print("learningNum:", item["learningNum"])
                # real learning number is learningNum - finishExercisesNum
                print("exhibitAnswer:", item["exhibitAnswer"])
                # if it will display answers after done the homework
                i = i + 1
    return res


# if __name__ == "__main__":
#     print("Homeworks undone:")
#     settings = SCASettings()
#     for account in settings.getAccountsList():
#         print("==========", account, "==========")
#         csrf = getCsrf()
#         getAccountTeachers(settings.readSettings(account), csrf)
#         getAccountUndoneTasks(settings.readSettings(account), csrf)
#         print("")
