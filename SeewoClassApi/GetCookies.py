# coding = utf-8
from urllib import request
from urllib import parse
from http import cookiejar
import json
import hashlib

seewoLoginPath = "https://id.seewo.com/login"


def login(username: str, password: str, output=False):
    """ Log in and return the cookies. """
    m = hashlib.md5(password.encode("utf-8"))
    d = bytes(parse.urlencode(
        {"username": username, "password": m.hexdigest()}), encoding="utf-8")
    c = cookiejar.CookieJar()
    h = request.HTTPCookieProcessor(c)
    res = request.build_opener(h).open(
        seewoLoginPath, d).read().decode("utf-8")
    if output:
        j = json.loads(res)["data"]
        print("Result:", end="")
        print(str(j["statusCode"]) + " " + j["message"])
        print("\nCookies:")
        for item in c:
            print(item.name + " " + item.value)
        if j["statusCode"] == 200:
            # success
            print("\nUser info:")
            for item in j["data"]["user"]:
                print(item + ":" + str(j["data"]["user"][item]))
            print("\nLogin info:")
            for item in j["data"]:
                if item != "user":
                    print(item+":" + str(j["data"][item]))
    return c


def getToken(username: str, password: str, output=False):
    """ Return an x-token of the given account. """
    cookies = login(username, password, output)
    for cookie in cookies:
        if cookie.name == "x-token":
            return cookie.value
    raise AttributeError(
        "x-token not found! Maybe your username or password is wrong.")


if __name__ == "__main__":
    u = input("username:")
    p = input("password:")
    login(u, p, True)
