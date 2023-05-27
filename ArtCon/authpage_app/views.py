from django.shortcuts import render, redirect
from django.contrib import auth
from .models import User
import re


def login(request):
    if request.method == "GET":
        return render(request, "authpage_app/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        res_data = {}
        if username == "" or password == "":
            res_data["error"] = "모든 칸을 다 입력해주세요."
        else:
            user = User.objects.get(username=username)
            if password == user.password:
                request.session["user"] = user.id
                ###########################
                ## 로그인 후 볼 화면 지정 필요 ##
                ###########################
                return redirect("/index")
            else:
                res_data["error"] = "비밀번호가 틀렸습니다."
    return render(request, "authpage_app/login.html", res_data)


# def login(request):
#     return render(request, "authpage_app/login.html")


# https://velog.io/@azzurri21/Django-%EC%A0%90%ED%94%84%ED%88%AC%EC%9E%A5%EA%B3%A0-%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8-%EC%B4%88%EA%B8%B0%ED%99%94
def findP(request):
    return render(request, "authpage_app/findPassword.html")


def register(request):
    userdb = User.objects.all()
    email_validation = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone_number_validation = re.compile("\d{2,3}-\d{3,4}-\d{4}")
    password_validation = re.compile(
        "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$"
    )
    if request.method == "GET":
        return render(request, "signUp.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        phone_number = request.POST["phone_number"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        res_data = {}
        if (
            username == ""
            or email == ""
            or firstname == ""
            or lastname == ""
            or phone_number == ""
            or password1 == ""
        ):
            res_data["empty_error"] = "모든 정보가 입력되지 않았습니다."
        elif password1 != password2:
            res_data["pw_error02"] = "비밀번호가 다릅니다."
        elif userdb.filter(username=username).exists():
            res_data["username_error"] = "이미 존재하는 아이디입니다."
        elif userdb.filter(phone_number=phone_number).exists():
            res_data["phone_number_error02"] = "이미 가입된 연락처입니다."
        elif email_validation.match(email) == None:
            res_data["email_error"] = "@와 .를 포함한 이메일형식이 아닙니다."
        elif phone_number_validation.match(phone_number) == None:
            res_data["phone_number_error"] = "-를 포함한 연락처 형식이 아닙니다."
        elif password_validation.match(password1) == None:
            res_data["pw_error01"] = "비밀번호 형식을 확인해주세요."
        else:
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
                email=request.POST["email"],
                first_name=request.POST["firstname"],
                last_name=request.POST["lastname"],
                phone_number=request.POST["phone_number"],
            )
            auth.login(request, user)
            res_data["success"] = "ok"

        return render(request, "authpage_app/register.html", res_data)


# def register(request):
#     return render(request, "authpage_app/register.html")
