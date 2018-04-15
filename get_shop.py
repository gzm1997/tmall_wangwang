import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


def get_shop_list(cla, shop_num):
    my_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-cn,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
        "cache-control": "max-age=0",
        "cookie": "_med=dw:1366&dh:768&pw:1366&ph:768&ist:0; UM_distinctid=15ef70c84ae4bc-078dc0844fe32e-c303767-100200-15ef70c84af380; cna=WKStEcvkV1UCAXjsrp3GgBCz; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=CN%7Czh-CN%7CCNY%7C156; t=f5c767e7f77260cdcbc0fc3639bb7c2d; _tb_token_=e5beb5e88eef5; cookie2=1f7d93cc81330fa2d5552517b6dabbb6; swfstore=250890; enc=kQSkRMMgDBCDmleHeN9tEfNsMhb6MZ3vufS8%2FITOYa6XsGDhQsd79XNo40S6d5ry%2FdVlVx0z3Qn%2BXyG2OzfpyQ%3D%3D; _m_h5_tk=5c49343c6f9aa8eeb9f062d4478fbbfd_1516519746412; _m_h5_tk_enc=2432fc31ddb3679e5717bd7865cb7304; skt=047683f2e8f0503f; whl=-1%260%260%260; x=__ll%3D-1%26_ato%3D0; tt=tmall-main; cq=ccp%3D1; res=scroll%3A1349*10587-client%3A1349*637-offset%3A1349*10587-screen%3A1366*768; pnm_cku822=098%23E1hvdpvUvbpvUvCkvvvvvjiPPLdZljr8nLFhgjEUPmPOzj1nRFMhljlhn2LWljtVRphvCvvvphvCvpvVvUCvpvvvKphv8vvvphvvvvvvvvCHhQvvvfgvvhZLvvmCvvvvBBWvvvH%2BvvCHhQvvv7AivpvUvvCCUVoYp9JEvpvVvpCmpYFWmphvLUmgKdIadb8reTt%2BCNLhjCywHFXXiXhpVE01Ux8x9CQaRfU6pwethboJ%2B3%2BdaNAwVtuOJyqhzE%2B7RqwiLO2v5fVQKoZHtR9t%2BFuTWDQPvpvhvv2MMTwCvvpvvhHh; isg=BFtbblCEhYbhQfoTc7Xv-5Xz6r9pIvHKJpLOY02Yfdp0LHsO1QD_gnmuwo6iDMcq",
        "referer": "https://list.tmall.com/search_product.htm?q=%C4%EA%D8%9B&type=p&spm=a220m.1000858.a2227oh.d100&from=.list.pc_1_searchbutton",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"        
    }
    base_url = "https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.7.59d0b76cP00U4B&q=" + cla + "&sort=s&style=w&from=mallfp..pc_1_searchbutton"
    shops_dict = {}
    count = 0
    url = base_url
    index = 0
    while count < shop_num - 1:
        #print("url", url)
        #print("index", index)
        s = requests.Session()
        r = s.get(url, headers = my_headers)
        s.keep_alive = False

        bobj = BeautifulSoup(r.text, "html.parser")
        r.close()
        #print(bobj)
        titles = bobj.find_all("a", {"class": "sHi-title"})
        shops = bobj.find_all("a", {"class": "sHe-shop"})
        length = len(titles)
        #print("shops", shops)
        mark = False
        #print("shops", shops)
        for i in range(length):
            if count == shop_num:
                mark = True
                #print("count", count, "shop_num", shop_num)
                break
            shops_dict[titles[i].get_text()] = "https:" + shops[i]["href"]
            count += 1
        #print("len of shops_dict", len(shops_dict))
        if mark:
            break
        else:
            url = "https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.7.59d0b76cP00U4B&s=" + str((index + 1) * 20) + "&q=" + cla + "&sort=s&style=w&from=.list.pc_1_searchbutton&type=pc#J_Filter"
            index += 1
            time.sleep(5)
        #print("len shops_dict", len(shops_dict))
    return shops_dict


def save_data_to_xlsx(shop_dict, filename):
    name = [k for k in shop_dict.keys()]
    shop_url = [shop_dict[k] for k in name]
    save = pd.DataFrame({"name": name, "shop_url": shop_url})
    save.to_excel(filename)


if __name__ == "__main__":
    cla = "鞋子"
    shops_dict = get_shop_list(cla, 45)
    print(shops_dict)
    save_data_to_xlsx(shops_dict, "data/shop_url.xlsx")
    #print(len(shops_dict))