from selenium import webdriver
from bs4 import BeautifulSoup
import setting
import time


def get_localtime_str():
    l_time = time.localtime()
    year = l_time.tm_year
    month = l_time.tm_mon
    day = l_time.tm_mday
    hour = l_time.tm_hour
    minute = l_time.tm_min
    second = l_time.tm_sec
    date_str = str(year) + "-" + str(month) + "-" + str(day);
    time_str = str(hour) + ":" + str(minute) + ":" + str(second)
    return date_str, time_str


def get_ww_state(driver, shop_url, name):
    driver.get(shop_url)
    time.sleep(1)
    while True:
        count = 0
        try:
            ww = driver.find_element_by_class_name("ww-inline")
        except:
            time.sleep(0.2)
            count += 1
            if count >= 3:
                break
        else:
            break;
    #print("ww", ww)
    #print("class", ww.get_attribute("class"))
    date_str, time_str = get_localtime_str()
    if  "ww-online" in ww.get_attribute("class"):
        return {"name": name, "state": 1, "date": date_str, "time": time_str}
    elif "ww-offline" in ww.get_attribute("class"):
        return {"name": name, "state": 0, "date": date_str, "time": time_str}
    else:
    	return {"name": name, "state": 0.5, "date": date_str, "time": time_str}


if __name__ == "__main__":
    executable_path = setting.EXECUTABLE_PATH
    driver = webdriver.PhantomJS(executable_path = executable_path)
    shop_url = 'https://store.taobao.com/shop/view_shop.htm?spm=a220m.1000858.1000725.3.7db040c17SlhK8&user_number_id=2929817125&rn=09837e0542dd7e42c00899865c41d2a9'
    name = "galaxy格莱仕旗舰店"
    print(get_ww_state(driver, shop_url, name))