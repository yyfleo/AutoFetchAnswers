# coding = utf-8
from urllib import request
from http import cookiejar
from .GetTaskList import getCsrf
from bs4 import BeautifulSoup
import json

seewoClassLoginPath = "https://class.seewo.com/student/login"
seewoClassAnswerPath = "https://class.seewo.com/student/adpter.json?action=FETCH_ANSWERDETAILS_ST&method=POST"


def fetchAnswers(xToken: str, taskID: str, f, output=False, csrf=getCsrf()):
    """ Fetch the answers of a task, which was given its taskID. """
    c = cookiejar.CookieJar()
    headers = {"Content-Type": "application/json",
               "x-csrf-token": csrf,
               "Cookie": "csrfToken=" + csrf + "; "
               + "x-token=" + xToken}
    p = request.HTTPCookieProcessor(c)
    d = bytes(json.dumps({"actionName": "FETCH_ANSWERDETAILS_ST", "params": {
              "router": {"taskId": taskID}}}), encoding="utf-8")
    o = request.build_opener(p)
    req = request.Request(url=seewoClassAnswerPath, data=d, headers=headers)
    res = o.open(req).read().decode("utf-8")
    j = json.loads(res)
    if output:
        f.write("Result: ")
        f.write(str(j["code"]))
        f.write(" ")
        f.write(j["msg"])
        f.write("<br>")
        if j["code"] == 0:
            f.write("Answers:<br>")
            i = 1
            for ans in j["data"]:
                f.write(str(i))
                f.write(".")
                if ans["type"]["value"] == "填空题":
                    f.write("<br>")
                    e = 0
                    try:
                        for item in BeautifulSoup(ans["answer"], "html.parser").stripped_strings:
                            if not "分" in item:
                                f.write(item)
                        f.write("<br>")
                    except ValueError:
                        pass
                else:
                    f.write(" ")
                    f.write(ans["answer"])
                    f.write("<br>")
                i = i + 1
    return res
