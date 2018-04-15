import time
import get_data
import save_collect_data
import pandas as pd
import mysql.connector
from selenium import webdriver
import setting

#time_to_collect = [9, 14, 21]
def timing_to_get_data(driver, filename, time_to_collect):
	d = pd.read_excel(filename)
	name = d.name
	shop_url = d.shop_url
	shop_url_list = {}
	for i in range(len(name)):
		shop_url_list[name[i]] = shop_url[i]
	print("shop_url_list", shop_url_list)
	while True:
		time.sleep(60)
		l_time = time.localtime()
		date_str, time_str = get_data.get_localtime_str()
		conn = mysql.connector.connect(user = setting.MYSQL_USER, password = setting.MYSQL_PASSWORD, database = "tm")
		cursor = conn.cursor()
		start_time = time_str[:time_str.find(":")] + ":00:00"
		print("start_time", start_time, "end_time", time_str)
		cursor.execute("select * from shop where date = %s and TIME(time) between %s and %s;", [date_str, start_time, time_str])
		r = cursor.fetchall()
		conn.commit()
		cursor.close()
		if l_time.tm_hour in time_to_collect and r == []:
			print("这个时间点还没爬取，现在开始爬取")
			shop_list = []
			for name in shop_url_list.keys():
				shop = get_data.get_ww_state(driver, shop_url_list[name], name)
				print("shop", shop)
				shop_list.append(shop)
			save_collect_data.save_ww_state(shop_list)





if __name__ == "__main__":
	driver = webdriver.PhantomJS(executable_path = setting.EXECUTABLE_PATH)
	filename = "data/shop_url.xlsx"
	time_to_collect = [9, 14, 23]
	timing_to_get_data(driver, filename, time_to_collect)