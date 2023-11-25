from flask import Flask, render_template, session, request, redirect, url_for
import mysql.connector
from datetime import timedelta
from PIL import Image
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "心がカギ"
app.permanent_session_lifetime = timedelta(hours=24)
app.config["MAX_CONTENT_LENGTH"] = 8**20

# TOP-------------------------------------------------------------------------------------------


@app.route("/", methods=["GET"])
def top():
    sql = "SELECT * FROM goods ORDER BY rand();"

    result = select(sql)
    session.pop("name", None)
    session.pop("file", None)
    session.pop("price", None)
    session.pop("info", None)
    session.pop("gid", None)
    session.pop("photo", None)
    session.pop("id", None)

    if "nickname" in session:
        res = {"icon": session["icon"]}
        return render_template("topLogin.html", result=result, res=res)
    else:
        return render_template("top.html", result=result)


# Login処理-------------------------------------------------------------------------------------------


@app.route("/login", methods=["GET"])
def login():
    errmsg = {}
    test = {}
    return render_template("login.html", errmsg=errmsg, test=test)


@app.route("/loginCheck", methods=["POST"])
def loginCheck():
    result = {}
    test = request.form

    sql = (
        'SELECT pass,nick,icon,profile,mail FROM user WHERE mail ="'
        + test["mail"]
        + '";'
    )
    err = ""
    print(sql)
    result = select(sql)
    if not result:
        err = "メールアドレスまたはパスワードが違います"
        return render_template("login.html", err=err, test=test)

    print(result[0])

    for rec in result:
        print(rec["pass"])
        print(rec["icon"])
        nickname = rec["nick"]
        icon = rec["icon"]

    if not test["pass"] == rec["pass"]:
        err = "メールアドレスまたはパスワードが違います"
        return render_template("login.html", result=result, err=err, test=test)

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
    sql = 'SELECT * FROM goods WHERE mail ="' + session["mail"] + '";'

    result = select(sql)

    sql = 'SELECT money FROM user WHERE mail ="' + session["mail"] + '";'

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        userP = cur.fetchall()
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

    if "nickname" in session:
        res = {
            "nickname": session["nickname"],
            "icon": session["icon"],
            "profile": session["profile"],
            "mail": session["mail"],
        }
        return render_template("user.html", result=result, res=res, userP=userP)
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
    nick = request.form["nick"]
    profile = request.form["profile"]
    print(nick)

    # ***ファイルオブジェクト取得***
    file = request.files["file"]

    filename = file.filename
    # ***ファイル受信チェック***
    if not filename:
        sql = (
            'UPDATE user SET nick = "'
            + nick
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

    else:
        directory_path = "static/images/icon/"
        file_name = res["icon"]
        file_path = os.path.join(directory_path, file_name)
        if not file_name == "unknownUser.jpg":
            os.remove(file_path)

        # ***ファイルオープン***
        rec = extension_check(filename)
        if rec == "True":
            img = Image.open(file)
            img = crop_max_square(img)
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


# 残高追加-------------------------------------------------------------------------------------------
@app.route("/payment", methods=["GET"])
def payment():
    res = {}
    return render_template("payment.html", res=res)


@app.route("/paymentComplete", methods=["POST"])
def paymentComplete():
    res = {
        "mail": session["mail"],
    }
    code = request.form["code"]
    sql = 'SELECT money FROM prepaid WHERE CODE = "' + code + '";'

    result = select(sql)
    if not result:
        return render_template("payment.html", res=res)
    for rec in result:
        money = rec["money"]

    sql = 'SELECT money FROM user WHERE mail = "' + res["mail"] + '";'

    result = select(sql)
    for rec in result:
        Umoney = rec["money"]

    sumMoney = int(Umoney) + int(money)
    sumMoney = str(sumMoney)
    sql = (
        'UPDATE user SET money = "' + sumMoney + '" WHERE mail = "' + res["mail"] + '";'
    )
    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        con.commit()
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

    return render_template("paymentComplete.html", res=res, money=money)


# 商品登録-------------------------------------------------------------------------------------------


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

    if "file" in session:
        directory_path = "static/images/goods/"
        file_name = session["file"]
        file_path = os.path.join(directory_path, file_name)
        os.remove(file_path)
        session.pop("file", None)
        return render_template("GRegister.html", res=res, result=result, err=err)
    else:
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
    # ***ファイルオブジェクト取得***
    file = request.files["file"]

    filename = file.filename

    if filename:
        rec = extension_check(filename)
        if rec == "True":
            # ***ファイルオープン***
            img = Image.open(file)
            img = crop_max_square(img)
            # ***日時情報の取得***
            savedate = datetime.now().strftime("%Y%m%d_%H%M%S_")
            # ***安全なファイル名に変換***
            filename = savedate + secure_filename(filename)
            # ***保存用フルパス作成***
            os.path.join("./static/images/goods", filename)
            save_path = os.path.join("./static/images/goods/", filename)
            # ***ファイル保存***
            img.save(save_path, quality=90)
            images = filename
        else:
            images = "unknownGoods.jpeg"
    else:
        images = "unknownGoods.jpeg"

    for key, value in result.items():
        if not value:
            err[key] = "入力されていません"
            err_count += 1
        else:
            err[key] = ""

    if not err_count == 0:
        return render_template("GRegister.html", result=result, err=err, res=res)

    session["name"] = result["name"]
    session["category"] = result["category"]
    session["file"] = images
    session["price"] = result["price"]
    session["info"] = result["info"]

    return render_template(
        "GRegisterCheck.html", result=result, vtbl=vtbl, res=res, images=images
    )


@app.route("/GRegisterComplete", methods=["POST"])
def GRegisterComplete():
    res = {
        "nickname": session["nickname"],
        "icon": session["icon"],
        "profile": session["profile"],
        "mail": session["mail"],
    }

    result = session.copy()

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        sql = """
    INSERT INTO goods 
        (name,photo,price,info,category,mail)
    VALUES 
        (%s, %s, %s, %s, %s, %s)
    """
        data = [
            (
                result["name"],
                result["file"],
                result["price"],
                result["info"],
                result["category"],
                session["mail"],
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

    session.pop("name", None)
    session.pop("file", None)
    session.pop("category", None)
    session.pop("price", None)
    session.pop("info", None)

    return render_template("GRegisterComplete.html", result=result, res=res)


# 商品詳細-------------------------------------------------------------------------------------------


@app.route("/detail/<gid>", methods=["GET"])
def detail(gid):
    session.pop("gid", None)
    sql = 'SELECT * FROM goods WHERE GID = "' + gid + '";'

    result = select(sql)

    for rec in result:
        mail = rec["mail"]
        price = rec["price"]
    print(mail)
    price = f"{price:,}"

    sql = 'SELECT nick,icon,mail FROM user WHERE mail ="' + mail + '";'

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        userP = cur.fetchall()
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

    print(userP)

    session["gid"] = gid

    sql = "SELECT * FROM goods ORDER BY rand() LIMIT 8;"

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        goods = cur.fetchall()
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

    if "nickname" in session:
        res = {
            "nickname": session["nickname"],
            "icon": session["icon"],
            "mail": session["mail"],
        }
        if res["mail"] == mail:
            return render_template(
                "detailUser.html",
                result=result,
                userP=userP,
                goods=goods,
                res=res,
                price=price,
            )
        else:
            return render_template(
                "detailLogin.html",
                result=result,
                userP=userP,
                goods=goods,
                res=res,
                price=price,
            )
    else:
        return render_template(
            "detail.html", result=result, goods=goods, userP=userP, price=price
        )


# 商品編集-------------------------------------------------------------------------------------------


@app.route("/goodsEdit", methods=["GET"])
def goodsEdit():
    gid = session["gid"]
    sql = 'SELECT * FROM goods WHERE GID = "' + gid + '";'

    result = select(sql)

    for rec in result:
        session["photo"] = rec["photo"]

    return render_template("goodsEdit.html", result=result)


@app.route("/goodsEditComplete", methods=["POST"])
def goodsEditComplete():
    res = {
        "nickname": session["nickname"],
        "icon": session["icon"],
        "profile": session["profile"],
        "mail": session["mail"],
        "photo": session["photo"],
    }

    name = request.form["name"]
    price = request.form["price"]
    info = request.form["info"]
    category = request.form["category"]

    print(name)

    gid = session["gid"]
    # ***ファイルオブジェクト取得***
    file = request.files["file"]

    filename = file.filename
    # ***ファイル受信チェック***
    if not filename:
        sql = (
            'UPDATE goods SET name = "'
            + name
            + '", price = "'
            + price
            + '", info = "'
            + info
            + '", category = "'
            + category
            + '" WHERE gid = "'
            + gid
            + '";'
        )
        print("NOOOOOOOOOO" + sql)
        try:
            con = con_db()
            cur = con.cursor(dictionary=True)
            cur.execute(sql)
            con.commit()
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

    else:
        directory_path = "static/images/goods/"
        file_name = res["photo"]
        file_path = os.path.join(directory_path, file_name)
        if not file_name == "unknownGoods.jpg":
            os.remove(file_path)

        # ***ファイルオープン***
        rec = extension_check(filename)
        if rec == "True":
            img = Image.open(file)
            img = crop_max_square(img)
            # ***日時情報の取得***
            savedate = datetime.now().strftime("%Y%m%d_%H%M%S_")
            # ***安全なファイル名に変換***
            filename = savedate + secure_filename(filename)
            # ***保存用フルパス作成***
            os.path.join("./static/images/goods", filename)
            save_path = os.path.join("./static/images/goods", filename)
            # ***ファイル保存***

            img.save(save_path, quality=90)

        photo = filename
        print(photo)

        sql = (
            'UPDATE goods SET name = "'
            + name
            + '", price = "'
            + price
            + '", info = "'
            + info
            + '", photo = "'
            + photo
            + '", category = "'
            + category
            + '" WHERE gid = "'
            + gid
            + '";'
        )
        print("OKEEEEEEEEEEEEEEE" + sql)
        try:
            con = con_db()
            cur = con.cursor(dictionary=True)
            cur.execute(sql)
            con.commit()
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

    session.pop("gid", None)
    session.pop("photo", None)

    return render_template("goodsEditComplete.html", res=res)


# 商品削除-------------------------------------------------------------------------------------------


@app.route("/goodsDel", methods=["GET"])
def goodsDel():
    gid = session["gid"]
    sql = 'SELECT * FROM goods WHERE GID = "' + gid + '";'

    result = select(sql)

    return render_template("goodsDel.html", result=result)


@app.route("/goodsDelComplete", methods=["GET"])
def goodsDelComplete():
    gid = session["gid"]

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        sql = 'DELETE FROM goods WHERE gid = "' + gid + '";'

        cur.execute(sql)
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

    session.pop("gid", None)
    return render_template("goodsDelComplete.html")


# 購入処理-------------------------------------------------------------------------------------------


@app.route("/order", methods=["GET"])
def order():
    res = {
        "nickname": session["nickname"],
        "icon": session["icon"],
    }

    gid = session["gid"]
    mail = session["mail"]
    sql = 'SELECT * FROM goods WHERE GID = "' + gid + '";'

    result = select(sql)

    for rec in result:
        price = rec["price"]

    priceF = f"{price:,}"

    sql = 'SELECT * FROM user WHERE mail ="' + mail + '";'

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        userP = cur.fetchall()
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

    for item in userP:
        money = item["money"]
    moneyF = f"{money:,}"

    sumMoney = int(money) - int(price)
    sumMoneyF = f"{sumMoney:,}"
    sumMoneyF = str(sumMoneyF)

    return render_template(
        "order.html",
        result=result,
        userP=userP,
        priceF=priceF,
        moneyF=moneyF,
        res=res,
        sumMoneyF=sumMoneyF,
    )


@app.route("/orderComplete", methods=["POST"])
def orderComplete():
    res = {
        "nickname": session["nickname"],
        "icon": session["icon"],
    }
    gid = session["gid"]
    mail = session["mail"]

    sql = 'SELECT * FROM goods WHERE GID = "' + gid + '";'
    result = select(sql)
    for rec in result:
        price = rec["price"]

    sql = 'SELECT * FROM user WHERE mail ="' + mail + '";'
    result = select(sql)
    for rec in result:
        money = rec["money"]

    if price > money:
        return render_template("order.html", res=res)

    sql = 'SELECT * FROM masaru WHERE id ="1";'
    result = select(sql)
    for rec in result:
        mMoney = rec["money"]

    sumMoney = int(money) - int(price)
    mSumMoney = int(price) * 0.1
    masaruMoney = mMoney + mSumMoney
    print(masaruMoney)
    sellerMoney = int(price) * 0.9
    print(sellerMoney)

    sql = 'UPDATE user SET money = "' + str(sumMoney) + '" WHERE mail = "' + mail + '";'
    print(sql)
    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        con.commit()
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

    sql = 'SELECT * FROM goods WHERE gid ="' + gid + '";'
    result = select(sql)
    for rec in result:
        sellerUser = rec["mail"]

    sql = (
        'UPDATE user SET money = "'
        + str(sellerMoney)
        + '" WHERE mail = "'
        + sellerUser
        + '";'
    )
    print(sql)
    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        con.commit()
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

    sql = 'UPDATE masaru SET money = "' + str(masaruMoney) + '" WHERE id = "1";'
    print(sql)
    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        con.commit()
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

    sumMoney = f"{sumMoney:,}"

    return render_template("orderComplete.html", sumMoney=sumMoney)


# 出品者ページ-------------------------------------------------------------------------------------------


@app.route("/userProfile/<mail>", methods=["GET"])
def userProfile(mail):
    sql = 'SELECT icon,nick,profile FROM user WHERE mail = "' + mail + '";'

    print(sql)

    result = select(sql)

    sql = 'SELECT * FROM goods WHERE mail ="' + mail + '";'

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        goods = cur.fetchall()
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

    if "nickname" in session:
        res = {"nickname": session["nickname"], "icon": session["icon"]}
        return render_template(
            "userProfileLogin.html", result=result, goods=goods, res=res
        )
    else:
        return render_template("userProfile.html", result=result, goods=goods)


# お知らせ-------------------------------------------------------------------------------------------
@app.route("/news", methods=["GET"])
def news():
    sql = "SELECT * FROM news ORDER BY nid DESC;"

    result = select(sql)

    sql = "SELECT goods.gid,goods.name,goods.info,user.nick FROM goods JOIN user ON goods.mail = user.mail ORDER BY gid DESC;"

    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        cur.execute(sql)
        goods = cur.fetchall()
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

    return render_template("news.html", result=result, goods=goods)


# 管理者-------------------------------------------------------------------------------------------


@app.route("/admin", methods=["GET"])
def admin():
    test = {}
    session.pop("id", None)
    return render_template("adminLogin.html", test=test)


@app.route("/adminComplete", methods=["POST"])
def adminComplete():
    result = {}
    test = request.form

    sql = 'SELECT id,pass FROM admin WHERE id ="' + test["id"] + '";'
    print(sql)
    result = select(sql)
    if not result:
        return render_template("adminLogin.html", test=test)

    for rec in result:
        print(rec["id"])

    if not test["pass"] == rec["pass"]:
        return render_template("adminLogin.html", test=test)

    session["id"] = rec["id"]
    if not "id" in session:
        return render_template("adminLogin.html")

    return render_template("adminComplete.html")


@app.route("/administrator", methods=["POST"])
def administrator():
    if not "id" in session:
        return render_template("adminLogin.html")

    return render_template("administrator.html")


@app.route("/adminUser", methods=["GET"])
def adminUser():
    sql = "SELECT * FROM user;"

    result = select(sql)
    return render_template("adminUser.html", result=result)


@app.route("/adminGoods", methods=["GET"])
def adminGoods():
    sql = "SELECT * FROM goods;"

    result = select(sql)
    return render_template("adminGoods.html", result=result)


@app.route("/adminNews", methods=["GET"])
def adminNews():
    sql = "SELECT * FROM news;"

    result = select(sql)
    return render_template("adminNews.html", result=result)


@app.route("/adminNewsAdd", methods=["POST"])
def adminNewsAdd():
    sql = "SELECT * FROM news;"

    result = select(sql)
    return render_template("adminNewsAdd.html", result=result)


@app.route("/adminNewsAddComplete", methods=["POST"])
def adminNewsAddComplete():
    result = request.form

    day = datetime.now().strftime("%Y%m%d")
    try:
        con = con_db()
        cur = con.cursor(dictionary=True)
        sql = """
    INSERT INTO news 
        (title,data,day)
    VALUES 
        (%s, %s, %s)
    """
        data = [(result["title"], result["data"], day)]
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

    return render_template("adminNewsComplete.html")


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


def extension_check(filename):
    Extension = ["jpg", "png", "gif"]

    if "." in filename:
        ext = filename.rsplit(".", 1)[1]
        ext = ext.lower()
        print(ext)
    # root, ext = os.path.splitext(filename)
    # print(root)
    # print(ext)
    if ext in Extension:
        rec = "True"
    else:
        rec = "False"
    return rec


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(
        (
            (img_width - crop_width) // 2,
            (img_height - crop_height) // 2,
            (img_width + crop_width) // 2,
            (img_height + crop_height) // 2,
        )
    )


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


@app.errorhandler(413)
def error413(error):
    errmsg = {"code": error.code, "msg": "アカウント名またはパスワードが違います"}
    return render_template("login.html", errmsg=errmsg), 413


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
    # app.run(host="localhost", port=5000)
