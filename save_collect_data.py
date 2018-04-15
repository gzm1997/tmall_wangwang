import mysql.connector
import setting
import pandas as pd

#shop_list为列表类型，每个shop为字典类，包含name，state，time
def save_ww_state(shop_list):
    user = setting.MYSQL_USER
    password = setting.MYSQL_PASSWORD
    conn = mysql.connector.connect(user = user, password = password)
    cursor = conn.cursor()
    cursor.execute("create database if not exists tm;")
    cursor.execute("use tm;")
    cursor.execute("create table if not exists shop(name varchar(50), state tinyint, date varchar(50), time varchar(50), count int);")
    for shop in shop_list:
        cursor.execute("select * from shop where name = %s;", [shop["name"]])
        r = cursor.fetchall()
        if r == []:
            if shop["state"] == 0:
                cursor.execute("insert into shop value(%s, %s, %s, %s, 1);", [shop["name"], shop["state"], shop["date"], shop["time"]])
            else:
                cursor.execute("insert into shop value(%s, %s, %s, %s, 0);", [shop["name"], shop["state"], shop["date"], shop["time"]])
        else:
            if shop["state"] == 1:
                cursor.execute("update shop set state = 1, date = %s, time = %s, count = 0 where name = %s;", [shop["date"], shop["time"], shop["name"]])
            else:
                cursor.execute("update shop set state = 0, date = %s, time = %s, count = count + 1 where name = %s;", [shop["date"], shop["time"], shop["name"]])
    conn.commit()
    cursor.close()


#start_time为开始时间，end_time为截至日期，为字符串类型
def collect_ww_state(date):
    user = setting.MYSQL_USER
    password = setting.MYSQL_PASSWORD
    conn = mysql.connector.connect(user = user, password = password)
    cursor = conn.cursor(dictionary = True)
    cursor.execute("use tm;")
    cursor.execute('select * from shop where DATE(date) = %s;', [date])
    r = cursor.fetchall()
    for shop in r:
        if type(shop["name"]) == bytearray:
            shop["name"] = shop["name"].decode("utf-8")
        if type(shop["date"]) == bytearray:
            shop["date"] = shop["date"].decode("utf-8")   
        if type(shop["time"]) == bytearray:
            shop["time"] = shop["time"].decode("utf-8")
    return r


def convert_data_to_xlsx(shop_list, filename):
    name = [e["name"] for e in shop_list]
    state = [e["state"] for e in shop_list]
    date = [e["date"] for e in shop_list]
    time = [e["time"] for e in shop_list]
    count = [e["count"] for e in shop_list]
    save = pd.DataFrame({"name": name, "state": state, "date": date, "time": time, "count": count})
    save.to_excel(filename)


if __name__ == "__main__":
    
    shop_list = [
        {'name': 'galaxy格莱仕旗舰店', 'state': 1, "date": "2018-3-11", 'time': '13:38:46'}
    ]
    save_ww_state(shop_list)

    date = "2018-2-25"
    shop_list = collect_ww_state(date)
    print("shop_list", shop_list)
    print("len", len(shop_list))
    filename = "data.xlsx"
    convert_data_to_xlsx(shop_list, filename)

