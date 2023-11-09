from flask import Flask, render_template, session, request, redirect, url_for
import mysql.connector
from datetime import timedelta
from PIL import Image
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "心がカギ"
app.permanent_session_lifetime = timedelta(minutes=30)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

# TOP-------------------------------------------------------------------------------------------


@app.route("/", methods=["GET"])
def top():
    sql = "SELECT * FROM goods;"

    result = select(sql)

    if "nickname" in session:
        res = {"icon": session["icon"]}
        return render_template("topLogin.html", result=result, res=res)
    else:
        return render_template("top.html", result=result)


# Login処理-------------------------------------------------------------------------------------------


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/loginCheck", methods=["POST"])
def loginCheck():
    result = {}
    test = request.form

    sql = (
        'SELECT pass,nick,icon,profile,mail FROM user WHERE mail ="'
        + test["mail"]
        + '";'
    )

    print(sql)

    result = select(sql)
    print(result[0])

    for rec in result:
        print(rec["pass"])
        print(rec["icon"])
        nickname = rec["nick"]
        icon = rec["icon"]

    if not test["pass"] == rec["pass"]:
        return render_template("login.html", result=result)

    session["nickname"] = nickname
    session["icon"] = icon
    session["profile"] = rec["profile"]
    session["mail"] = rec["mail"]

    return render_template("/loginComplete.html", nickname=nickname, icon=icon)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return render_template("/logoutComplete.html")


# 新規登録-------------------------------------------------------------------------------------------


@app.route("/MRegister")
def MRegister():
    err = {}
    result = session.copy()

    return render_template("MRegister.html", result=result, err=err)


@app.route("/check", methods=["POST"])
def check():
    err_count = 0
    vtbl = {
        "mail": "メールアドレス",
        "pass": "パスワード",
        "check": "パスワード確認用",
        "news": "お知らせ",
        "nick": "ニックネーム",
        "sei": "姓",
        "sei2": "セイ",
        "mei": "名",
        "mei2": "メイ",
        "post": "郵便番号",
        "pref": "都道府県",
        "home": "番地",
        "phone": "電話番号",
        "addr": "住所",
        "bname": "建物名",
        "sex": "性別",
    }
    result = request.form

    err = {}

    for key, value in result.items():
        if not value:
            err[key] = "入力されていません"
            err_count += 1
        else:
            err[key] = ""

    if not err_count == 0:
        return render_template("MRegister.html", result=result, err=err)

    if not result["pass"] == result["check"]:
        err["pas"] = "パスワードが一致しません"
        return render_template("MRegister.html", result=result, err=err)

    for key, value in result.items():
        session[key] = value

    return render_template("check.html", result=result, vtbl=vtbl)


@app.route("/checkMail", methods=["POST"])
def checkMail():
    result = session.copy()


    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        sql = """
    INSERT INTO user 
        (mail,pass,nick,news,sei,sei2,mei,mei2,post,pref,addr,home,bname,phone,sex)
    VALUES 
        (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s)
    """
        data = [
            (
                result["mail"],
                result["pass"],
                result["nick"],
                result["news"],
                result["sei"],
                result["sei2"],
                result["mei"],
                result["mei2"],
                result["post"],
                result["pref"],
                result["addr"],
                result["home"],
                result["bname"],
                result["phone"],
                result["sex"],
            )
        ]
        cur.executemany(sql, data)
        con.commit()

        print("records inserted.")

    except mysql.connector.errors.ProgrammingError as e:
        print("***DB接続エラー***")
        print(type(e))
        print(e)
    except Exception as e:
        print("***システム運行プログラムエラー***")
        print(type(e))
        print(e)
    finally:
        cur.close()
        con.close()

    session.clear()

    return render_template("checkMail.html", result=result)


# ユーザー-------------------------------------------------------------------------------------------


@app.route("/user", methods=["GET"])
def user():
    sql = "SELECT * FROM goods;"

    result = select(sql)

    if "nickname" in session:
        res = {
            "nickname": session["nickname"],
            "icon": session["icon"],
            "profile": session["profile"],
            "mail": session["mail"],
        }
        return render_template("user.html", result=result, res=res)
    else:
        return render_template("top.html", result=result)


@app.route("/profileUp")
def profileUp():
    res = {
        "nickname": session["nickname"],
        "icon": session["icon"],
        "profile": session["profile"],
        "mail": session["mail"],
    }

    return render_template("profileUp.html", res=res)


@app.route("/profile", methods=["POST"])
def profile():
    res = {
        "nickname": session["nickname"],
        "icon": session["icon"],
        "profile": session["profile"],
        "mail": session["mail"],
    }

    directory_path = "static/images/icon/"
    file_name = res["icon"]
    file_path = os.path.join(directory_path, file_name)
    os.remove(file_path)

    # ***ファイルオブジェクト取得***
    file = request.files["file"]

    filename = file.filename
    # ***ファイル受信チェック***
    if not filename:
        return render_template("profileUp.html")
    # ***ファイルオープン***
    img = Image.open(file)
    # ***日時情報の取得***
    savedate = datetime.now().strftime("%Y%m%d_%H%M%S_")
    # ***安全なファイル名に変換***
    filename = savedate + secure_filename(filename)
    # ***保存用フルパス作成***
    os.path.join("./static/images/icon", filename)
    save_path = os.path.join("./static/images/icon", filename)
    # ***ファイル保存***
    img.save(save_path, quality=90)

    nick = request.form["nick"]
    icon = filename
    profile = request.form["profile"]
    print(nick)

    sql = (
        'UPDATE user SET nick = "'
        + nick
        + '", icon = "'
        + icon
        + '", profile = "'
        + profile
        + '" WHERE mail = "'
        + res["mail"]
        + '";'
    )
    print(sql)

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        con.commit()
        session["nickname"] = nick
        session["icon"] = icon
        session["profile"] = profile
    except mysql.connector.errors.ProgrammingError as e:
        print("***DB接続エラー***")
        print(type(e))
        print(e)
    except Exception as e:
        print("***システム運行プログラムエラー***")
        print(type(e))
        print(e)
    finally:
        cur.close()
        con.close()

    return render_template("profileUpComplete.html", res=res)


# 商品-------------------------------------------------------------------------------------------


@app.route("/GRegister")
def GRegister():
    res = {
        "nickname": session["nickname"],
        "icon": session["icon"],
        "profile": session["profile"],
        "mail": session["mail"],
    }
    err = {}
    result = session.copy()

    return render_template("GRegister.html", res=res, result=result, err=err)


@app.route("/GRegisterCheck", methods=["POST"])
def GRegisterCheck():
    res = {
        "nickname": session["nickname"],
        "icon": session["icon"],
        "profile": session["profile"],
        "mail": session["mail"],
    }
    err_count = 0
    vtbl = {"name": "商品名", "file": "商品画像", "price": "値段", "info": "商品説明"}
    result = request.form

    err = {}

    for key, value in result.items():
        if not value:
            err[key] = "入力されていません"
            err_count += 1
        else:
            err[key] = ""

    if not err_count == 0:
        return render_template("GRegister.html", result=result, err=err,res=res)
    
    for key, value in result.items():
        session[key] = value

    return render_template("GRegisterCheck.html", result=result, vtbl=vtbl, res=res)

@app.route("/GRegisterComplete", methods=["POST"])
def GRegisterComplete():

    result = session.copy()

    # ***ファイルオブジェクト取得***
    file = request.files["file"]

    filename = file.filename
    # ***ファイル受信チェック***
    if not filename:
        return render_template("profileUp.html")
    # ***ファイルオープン***
    img = Image.open(file)
    # ***日時情報の取得***
    savedate = datetime.now().strftime("%Y%m%d_%H%M%S_")
    # ***安全なファイル名に変換***
    filename = savedate + secure_filename(filename)
    # ***保存用フルパス作成***
    os.path.join("./static/images/icon", filename)
    save_path = os.path.join("./static/images/icon", filename)
    # ***ファイル保存***
    img.save(save_path, quality=90)

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        sql = """
    INSERT INTO goods 
        (name,photo,price,info)
    VALUES 
        (%s, %s, %s, %s)
    """
        data = [
            (
                result["name"],
                filename,
                result["price"],
                result["info"],
            )
        ]
        cur.executemany(sql, data)
        con.commit()

        print("records inserted.")

    except mysql.connector.errors.ProgrammingError as e:
        print("***DB接続エラー***")
        print(type(e))
        print(e)
    except Exception as e:
        print("***システム運行プログラムエラー***")
        print(type(e))
        print(e)
    finally:
        cur.close()
        con.close()

    session.clear()

    return render_template("GRegisterComplete.html", result=result)


@app.route("/detail/<gid>", methods=["GET"])
def detail(gid):
    sql = 'SELECT * FROM goods WHERE GID = "' + gid + '";'

    result = select(sql)

    if "nickname" in session:
        res = {"nickname": session["nickname"], "icon": session["icon"]}
        return render_template("detailLogin.html", result=result, res=res)
    else:
        return render_template("detail.html", result=result)


# DB接続-------------------------------------------------------------------------------------------


def con_db():
    con = mysql.connector.connect(
        host="localhost", user="11user", passwd="11pass", db="furniture"
    )
    return con


def select(sql):
    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        result = cur.fetchall()
    except mysql.connector.errors.ProgrammingError as e:
        print("***DB接続エラー***")
        print(type(e))
        print(e)
    except Exception as e:
        print("***システム運行プログラムエラー***")
        print(type(e))
        print(e)
    finally:
        cur.close()
        con.close()
    return result


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
