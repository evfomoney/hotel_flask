from flask import Blueprint, render_template, request, redirect, \
    session, url_for
from .model import User


user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/")
def u_index():
    return "<h1>This is user_index</h1>"


@user_bp.route("/login/", methods=["GET", "POST"])
def log_fn():
    if session.get("identifier"):
        return "<h1>欢迎回来</h1>"
    else:
        if request.method == "POST":
            if request.form.get("status") == "0":
                result = User.isPass(request.form)
                if not result:
                    return """
                        <h1>登录失败</h1>
                    """
                else:
                    # 登录成功, 并缓存其身份
                    session["identifier"] = User.isAdmin(request.form)
                    if session.get("identifier") == "1":
                        return redirect(url_for("user.f_admin"))
                    else:
                        return "<h1>酒店介绍页面</h1>"

            elif request.form.get("status") == "1":
                result = User.register(request.form)
                if not result:
                    return """
                        <h1>注册失败</h1>
                    """
                else:
                    return """
                        <h1>注册成功</h1>
                    """
            else:
                return """
                    <h3>错误进入</h3>
                """

        return """
            <h1>log</h1>
            <form action='/user/login' method='post'>
                姓名:<input type='text' name='name'>
                密码:<input type='password' name='pwd'>
                ---------------------------------------------------------
                注册账号:<input type='text' name='name'>
                注册密码:<input type='password' name='pwd'>
                身份证号:<input type='text' name='passID'>
                ---------------------------------------------------------
                <input type='text' name='status'>


                <input type='submit'>
            </form>
        """


@user_bp.route("/logout/", methods=["GET"])
def f_logout():
    session.pop("identifier")
    return "<h1>退出成功</h1>"


@user_bp.route("/admin", methods=["GET", "POST"])
def f_admin():
    from apps.records import Records

    if request.method == "POST":
        # print(request.form)  # 数据库操作
        if request.form.get("status") == "1":
            Records.create_rc(request.form)
        elif request.form.get("status") == "2":
            Records.modify_rc(request.form)
        elif request.form.get("status") == "3":
            Records.delete_rc(request.form)

    return render_template("user/admin.html")
