from django.shortcuts import redirect, render
from django.http import HttpResponse
from datetime import datetime
from matplotlib import colors
import twstock
import sqlite3
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import os
# Create your views here.

def index(request):
    return render(request,"Index.html",locals())

def searchstock(request):
    std = twstock.realtime.get(request.POST.get('Search'))     #從twstock上抓取股票即時資訊
    sname = std.get('info').get('name')                        #抓取股票簡稱
    scode = std.get('info').get('code')                        #抓取股票代號
    stime = std.get('info').get('time')                        #抓取資料時間
    sfullname = std.get('info').get('fullname')                #抓取股票全名
    last_price = std.get('realtime').get('latest_trade_price') #抓取即時股價(最後一次交易的股價)
    open_price = std.get('realtime').get('open')               #抓取當日開盤價
    high_price = std.get('realtime').get('high')               #抓取當日盤內最高價
    low_price = std.get('realtime').get('low')                 #抓取當日盤內最低價
    buy_price = std.get('realtime').get('best_bid_price')      #抓取即時最佳買入價
    buy_volume = std.get('realtime').get('best_bid_volume')    #抓取即時最佳買入數量
    buy=zip(buy_price,buy_volume)
    sell_price = std.get('realtime').get('best_ask_price')     #抓取即時最佳賣出價
    sell_volume = std.get('realtime').get('best_ask_volume')   #抓取即時最佳賣出數量
    sell = zip(sell_price,sell_volume)
    return render(request,"search.html",locals()) 

def searchhistory(request):
    conn = sqlite3.connect('db.sqlite3')         #連接資料庫
    c = conn.cursor()

    s = int(request.POST.get('choose_stock'))    #輸入的股票代號
    inputtime = request.POST.get('choose_month') #輸入的搜尋時間
    cursor = conn.execute("SELECT code,shortname,dealnumber,price,openprice,high,low,closeprice,change,transcount,dealdate from STOCK3")
    for i,row in enumerate(cursor):          #判斷是不是搜尋的股票
        if(s != row[0]):
            continue
        code = row[0]                        #股票代號為資料庫第一欄
        shortname = row[1]                   #股票代號為資料庫第二欄
        low = []                             #儲存轉型後的資料
        high = []
        open = []
        close = []
        o = row[4].split("[")[1].split("]")[0].split(",") #將一串文字分割成每個項目獨立的串列
        for t in o:
            open.append(float(t))             #將文字轉成浮點數型態存入
        c = row[7].split("[")[1].split("]")[0].split(",") #將一串文字分割成每個項目獨立的串列
        for t in c:
            close.append(float(t))             #將文字轉成浮點數型態存入
        l = row[6].split("[")[1].split("]")[0].split(",") #將一串文字分割成每個項目獨立的串列
        for t in l:
            low.append(float(t))             #將文字轉成浮點數型態存入
        h = row[5].split("[")[1].split("]")[0].split(",") #將一串文字分割成每個項目獨立的串列
        for t in h:
            high.append(float(t))             #將文字轉成浮點數型態存入
        #計算KD值
        rsv = []              #建立空串列儲存RSV值
        for i in range(len(close)):     #計算RSV值
            if(i>7):
                Min = 0.0
                Max = 0.0
                Min = min([low[i-8],low[i-7],low[i-6],low[i-5],low[i-4],low[i-3],low[i-2],low[i-1],low[i]])    #找出9日內最低價
                Max = max([high[i-8],high[i-7],high[i-6],high[i-5],high[i-4],high[i-3],high[i-2],high[i-1],high[i]])   #找出9日內最高價
                Rsv = ((close[i]-Min)/(Max-Min))*100    #計算RSV值
                rsv.append(Rsv)
        k_list = [50]                 #建立串列儲存K值，初始值設為50
        for num,rsv in enumerate(rsv):            #計算K值
                k_yesterday = k_list[num]
                k_today = (2/3)*k_yesterday+(1/3)*rsv   #K值公式
                k_list.append(k_today)
        k_list = k_list[1:]          #將初始值拿掉
        d_list=[50]                  #建立串列儲存D值，初始值設為50
        for num,k in enumerate(k_list):           #計算D值
                d_yesterday = d_list[num]
                d_today = 2/3*d_yesterday+1/3*k   #D值公式
                d_list.append(d_today)
        d_list = d_list[1:]          #將初始值拿掉
        dtime = []               #建立空串列儲存日期
        dealdate = row[10].split("[")[1].split("]")[0].split(",") #將一串文字分割成每個項目獨立的串列
        for t in dealdate:
            if (t[0] != "'"):
                y = t[2:6]
                m = t[6:8]
                d = t[8:10]
            else:
                y = t[1:5]
                m = t[5:7]
                d = t[7:9]
            st = y+"-"+m+"-"+d     #將文字轉成YYYY-mm-dd的型態
            dtime.append(datetime.strptime(st,"%Y-%m-%d"))   #存入時間型態的變數
        #計算均價
        ma5 = [close[0],close[1],close[2],close[3]]           #建立儲存MA5的串列，前四天的值設為每日收盤價
        ma10 = [close[0],close[1],close[2],close[3]]           #建立儲存MA10的串列，前四天的值設為每日收盤價
        ma20 = [close[0],close[1],close[2],close[3]]           #建立儲存MA20的串列，前四天的值設為每日收盤價
        ma60 = [close[0],close[1],close[2],close[3]]           #建立儲存MA60的串列，前四天的值設為每日收盤價
        for t in range(len(close)):
            if(t>3 and t <= 8):      #若天數小於10天
                ma5.append((close[t]+close[t-4]+close[t-3]+close[t-2]+close[t-1])/5)  #計算MA5
                ma10.append(ma5[-1])       #5~9天的值設為MA5的值
                ma20.append(ma5[-1])       #5~9天的值設為MA5的值
                ma60.append(ma5[-1])       #5~9天的值設為MA5的值
            if(t>8 and t<=18):
                ma5.append((close[t]+close[t-4]+close[t-3]+close[t-2]+close[t-1])/5)  #計算MA5
                ma10.append((close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/10)  #計算MA10
                ma20.append(ma10[-1])       #10~19天的值設為MA10的值
                ma60.append(ma10[-1])       #10~19天的值設為MA10的值
            if(t>18 and t<=58):
                ma5.append((close[t]+close[t-4]+close[t-3]+close[t-2]+close[t-1])/5)  #計算MA5
                ma10.append((close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/10)  #計算MA10
                ma20.append((close[t-19]+close[t-18]+close[t-17]+close[t-16]+close[t-15]+close[t-14]+close[t-13]+close[t-12]+close[t-11]+close[t-10]+close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/20)  #計算MA20
                ma60.append(ma20[-1])       #20~59天的值設為MA20的值
            if(t>58):
                ma5.append((close[t]+close[t-4]+close[t-3]+close[t-2]+close[t-1])/5)  #計算MA5
                ma10.append((close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/10)  #計算MA10
                ma20.append((close[t-19]+close[t-18]+close[t-17]+close[t-16]+close[t-15]+close[t-14]+close[t-13]+close[t-12]+close[t-11]+close[t-10]+close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/20)  #計算MA20
                ma60.append((close[t-59]+close[t-58]+close[t-57]+close[t-56]+close[t-55]+close[t-54]+close[t-53]+close[t-52]+close[t-51]+close[t-50]+close[t-49]+close[t-48]+close[t-47]+close[t-46]+close[t-45]+close[t-44]+close[t-43]+close[t-42]+close[t-41]+close[t-40]+close[t-39]+close[t-38]+close[t-37]+close[t-36]+close[t-35]+close[t-34]+close[t-33]+close[t-32]+close[t-31]+close[t-30]+close[t-29]+close[t-28]+close[t-27]+close[t-26]+close[t-25]+close[t-24]+close[t-23]+close[t-22]+close[t-21]+close[t-20]+close[t-19]+close[t-18]+close[t-17]+close[t-16]+close[t-15]+close[t-14]+close[t-13]+close[t-12]+close[t-11]+close[t-10]+close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/60)  #計算MA60
        if(inputtime == "2020/08~2021/06"):     #若查詢整年份的資料
            #顯示資料為2020/08~2021/06是因為2020/05~2020/07沒有MA60的資料
            #繪圖
            plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
            plt.rcParams['axes.unicode_minus'] = False
            row_pd = pd.DataFrame(row)
            fig = plt.figure(figsize=(10,4))     #設定圖片大小
            ax = plt.gca()                       #設定座標軸
            ax.set_facecolor('#202732')          #設定座標軸內顏色
            ax.tick_params(colors = 'w')         #設定座標軸顏色
            fig.patch.set_facecolor('#202732')   #設定圖片背景顏色
            plt.plot(dtime[59:],close[59:],color='blue',label="收盤")     #繪製每條曲線
            plt.plot(dtime[59:],open[59:],color='orange',label="開盤")
            plt.plot(dtime[59:],ma5[59:],color='m',label='MA5')
            plt.plot(dtime[59:],ma10[59:],color='green',label='MA10')
            plt.plot(dtime[59:],ma20[59:],color='cyan',label='MA20')
            plt.plot(dtime[59:],ma60[59:],color='red',label='MA60')
            plt.title(str(row[1])+"開盤收盤均價曲線",loc='right',color = 'w')   #設定圖片標題及位置、顏色 
            plt.xlabel('日期',color = 'w')     #設定座標軸名稱及顏色
            plt.ylabel('價格',color = 'w')     #設定座標軸名稱及顏色
            plt.grid(True,axis='y')
            plt.legend()
            plt.savefig(os.path.join('c:/Users/WEIZHE/Desktop/stock/static/image/historySearch.jpg'))   #儲存圖片
            plt.close()
            fig = plt.figure(figsize=(10,4))    #開啟一張新畫布，設定圖片大小
            ax = plt.gca()
            ax.set_facecolor('#202732')
            ax.tick_params(colors = 'w')
            fig.patch.set_facecolor('#202732')
            plt.plot(dtime[59:],k_list[51:],color = 'blue',label="K")    #繪製KD曲線圖
            plt.plot(dtime[59:],d_list[51:],color = 'orange',label = "D")
            plt.title(str(row[1])+"KD圖",loc = 'right',color = 'w')
            plt.xlabel('日期',color = 'w')
            plt.ylabel('百分比',color = 'w')
            plt.grid(True,axis='y')
            plt.legend()
            plt.savefig(os.path.join('c:/Users/WEIZHE/Desktop/stock/static/image/historyKD.jpg'))
            plt.close()
            
        else:
            iyear = inputtime[0:4]       #擷取輸入時間的年份
            itime = inputtime[-2::1]     #擷取輸入時間的月份
            #儲存KD值
            dtimem = []
            closem = []
            openm = []
            kvalue = []
            dvalue = []
            MA5m = []
            MA10m = []
            MA20m = []
            MA60m = []
            for t in range(len(dtime)):
                date = datetime.strftime(dtime[t],"%Y%m%d")
                y = date[0:4]
                m = date[4:6]
                if(itime == '05' or itime == '06'):     #若查詢5月或6月資料
                    if(m == itime and y == iyear):      #需判斷年份是否為查詢時間
                        dtimem.append(dtime[t])         #此筆資料是查詢範圍內資料，存入串列
                        closem.append(close[t])
                        openm.append(open[t])
                        MA5m.append(ma5[t])
                        MA10m.append(ma10[t])
                        MA20m.append(ma20[t])
                        MA60m.append(ma60[t])
                        kvalue.append(k_list[t])
                        dvalue.append(d_list[t])
                elif(m == itime):                      #若月分與查詢時間相同
                    dtimem.append(dtime[t])            #此筆資料是查詢範圍內資料，存入串列
                    closem.append(close[t])
                    openm.append(open[t])
                    MA5m.append(ma5[t])
                    MA10m.append(ma10[t])
                    MA20m.append(ma20[t])
                    MA60m.append(ma60[t])
                    kvalue.append(k_list[t])
                    dvalue.append(d_list[t])
            plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
            plt.rcParams['axes.unicode_minus'] = False
            row_pd = pd.DataFrame(row)
            time = []
            fig = plt.figure(figsize=(10,4))     #設定圖片大小
            ax = plt.gca()                       #設定座標軸
            ax.set_facecolor('#202732')          #設定座標軸內顏色
            ax.tick_params(colors = 'w')         #設定座標軸顏色
            fig.patch.set_facecolor('#202732')   #設定圖片背景顏色
            plt.plot(dtimem[:-1],closem[:-1],color='blue',label="收盤")    #繪製每條曲線
            plt.plot(dtimem[:-1],openm[:-1],color='orange',label="開盤")
            plt.plot(dtimem[:-1],MA5m[:-1],color='m',label='MA5')
            plt.plot(dtimem[:-1],MA10m[:-1],color='green',label='MA10')
            plt.plot(dtimem[:-1],MA20m[:-1],color='cyan',label='MA20')
            plt.plot(dtimem[:-1],MA60m[:-1],color='red',label='MA60')
            plt.title(str(row[1])+"開盤收盤曲線",loc='right',color = 'w')
            plt.xlabel('日期',color = 'w')     #設定座標軸名稱及顏色
            plt.ylabel('價格',color = 'w')     #設定座標軸名稱及顏色
            plt.grid(True,axis='y')
            plt.legend()
            plt.savefig(os.path.join('c:/Users/WEIZHE/Desktop/stock/static/image/historySearch.jpg'))  #儲存圖片
            fig = plt.figure(figsize=(10,4))    #開啟一張新畫布，設定圖片大小
            ax = plt.gca()
            ax.set_facecolor('#202732')
            ax.tick_params(colors = 'w')
            fig.patch.set_facecolor('#202732')
            plt.plot(dtimem[:-1],kvalue[:-1],color='blue',label="K")    #繪製KD曲線圖
            plt.plot(dtimem[:-1],dvalue[:-1],color='orange',label='D')
            plt.title(str(row[1])+"KD值曲線",loc='right',color = 'w')
            plt.ylabel('百分比',color = 'w')
            plt.legend()
            plt.savefig(os.path.join('c:/Users/WEIZHE/Desktop/stock/static/image/historyKD.jpg')) #儲存圖片
            plt.close()
        break
    
    return render(request,"historysearch.html",locals()) 


