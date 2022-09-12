from datetime import datetime
from django.shortcuts import render
import sqlite3
from matplotlib import colors
from numpy import split
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.indexes.base import Index
import datetime

def stock():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    s = 2330
    inputtime = 'y'
    cursor = conn.execute("SELECT code,shortname,dealnumber,price,openprice,high,low,closeprice,change,transcount,dealdate from STOCK3")
    for i,row in enumerate(cursor):
        if(s != row[0]):
            continue
        code = row[0]
        shortname = row[1]
        low = []
        high = []
        open = []
        close = []
        o = row[4].split("[")[1].split("]")[0].split(",")
        for t in o:
            open.append(float(t))
        c = row[7].split("[")[1].split("]")[0].split(",")
        for t in c:
            close.append(float(t))
        l = row[6].split("[")[1].split("]")[0].split(",")
        for t in l:
            low.append(float(t))
        h = row[5].split("[")[1].split("]")[0].split(",")
        for t in h:
            high.append(float(t))
        rsv = []
        for i in range(len(close)):
            if(i>7):
                Min = 0.0
                Max = 0.0
                Min = min([low[i-8],low[i-7],low[i-6],low[i-5],low[i-4],low[i-3],low[i-2],low[i-1],low[i]])
                Max = max([high[i-8],high[i-7],high[i-6],high[i-5],high[i-4],high[i-3],high[i-2],high[i-1],high[i]])
                Rsv = ((close[i]-Min)/(Max-Min))*100
                rsv.append(Rsv)
        k_list = [50]
        for num,rsv in enumerate(rsv):
                k_yesterday = k_list[num]
                k_today = (2/3)*k_yesterday+(1/3)*rsv
                k_list.append(k_today)
        k_list = k_list[1:]
        d_list=[50]
        for num,k in enumerate(k_list):
                d_yesterday = d_list[num]
                d_today = 2/3*d_yesterday+1/3*k
                d_list.append(d_today)
        d_list = d_list[1:]
        dtime = []
        dealdate = row[10].split("[")[1].split("]")[0].split(",")
        for t in dealdate:
            if (t[0] != "'"):
                y = t[2:6]
                m = t[6:8]
                d = t[8:10]
            else:
                y = t[1:5]
                m = t[5:7]
                d = t[7:9]
            st = y+"-"+m+"-"+d
            dtime.append(datetime.datetime.strptime(st,"%Y-%m-%d"))
        #計算均價
        ma5 = [close[0],close[1],close[2],close[3]]
        ma10 = [close[0],close[1],close[2],close[3]]
        ma20 = [close[0],close[1],close[2],close[3]]
        ma60 = [close[0],close[1],close[2],close[3]]
        for t in range(len(close)):
            if(t>3 and t <= 8):
                ma5.append((close[t]+close[t-4]+close[t-3]+close[t-2]+close[t-1])/5)
                ma10.append(ma5[-1])
                ma20.append(ma5[-1])
                ma60.append(ma5[-1])
            if(t>8 and t<=18):
                ma5.append((close[t]+close[t-4]+close[t-3]+close[t-2]+close[t-1])/5)
                ma10.append((close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/10)
                ma20.append(ma10[-1])
                ma60.append(ma10[-1])
            if(t>18 and t<=58):
                ma5.append((close[t]+close[t-4]+close[t-3]+close[t-2]+close[t-1])/5)
                ma10.append((close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/10)
                ma20.append((close[t-19]+close[t-18]+close[t-17]+close[t-16]+close[t-15]+close[t-14]+close[t-13]+close[t-12]+close[t-11]+close[t-10]+close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/20)
                ma60.append(ma20[-1])
            if(t>58):
                ma5.append((close[t]+close[t-4]+close[t-3]+close[t-2]+close[t-1])/5)
                ma10.append((close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/10)
                ma20.append((close[t-19]+close[t-18]+close[t-17]+close[t-16]+close[t-15]+close[t-14]+close[t-13]+close[t-12]+close[t-11]+close[t-10]+close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/20)
                ma60.append((close[t-59]+close[t-58]+close[t-57]+close[t-56]+close[t-55]+close[t-54]+close[t-53]+close[t-52]+close[t-51]+close[t-50]+close[t-49]+close[t-48]+close[t-47]+close[t-46]+close[t-45]+close[t-44]+close[t-43]+close[t-42]+close[t-41]+close[t-40]+close[t-39]+close[t-38]+close[t-37]+close[t-36]+close[t-35]+close[t-34]+close[t-33]+close[t-32]+close[t-31]+close[t-30]+close[t-29]+close[t-28]+close[t-27]+close[t-26]+close[t-25]+close[t-24]+close[t-23]+close[t-22]+close[t-21]+close[t-20]+close[t-19]+close[t-18]+close[t-17]+close[t-16]+close[t-15]+close[t-14]+close[t-13]+close[t-12]+close[t-11]+close[t-10]+close[t-9]+close[t-8]+close[t-7]+close[t-6]+close[t-5]+close[t-4]+close[t-3]+close[t-2]+close[t-1]+close[t])/60)
        if(inputtime == "y"):
            #繪圖
            plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
            plt.rcParams['axes.unicode_minus'] = False
            row_pd = pd.DataFrame(row)
            time = []
            fig1 = plt.figure(figsize=(10,4))
            ax = plt.gca()
            ax.tick_params(colors = 'w')
            fig1.patch.set_facecolor('#202732')
            plt.plot(dtime[59:],close[59:],color='blue',label="收盤")
            plt.plot(dtime[59:],open[59:],color='orange',label="開盤")
            plt.plot(dtime[59:],ma5[59:],color='m',label='MA5')
            plt.plot(dtime[59:],ma10[59:],color='green',label='MA10')
            plt.plot(dtime[59:],ma20[59:],color='cyan',label='MA20')
            plt.plot(dtime[59:],ma60[59:],color='black',label='MA60')
            plt.title(str(row[1])+"開盤收盤均價曲線",loc='right',color = 'w')
            plt.ylim(min(low),max(high))
            plt.xlabel('日期')
            plt.ylabel('價格')
            plt.grid(True,axis='y')
            plt.legend()
            plt.savefig('historySearch.jpg',edgecolor = '#202732')
            plt.close()
            fig2 = plt.figure(figsize=(10,4))
            ax = plt.gca()
            ax.tick_params(colors = 'w')
            fig2.patch.set_facecolor('#202732')
            plt.plot(dtime[59:],k_list[51:],color = 'blue',label="K")
            plt.plot(dtime[59:],d_list[51:],color = 'orange',label = "D")
            print(d_list[51:])
            plt.title(str(row[1])+"KD圖",loc = 'right',color = 'w')
            plt.xlabel('日期')
            plt.ylabel('百分比')
            plt.grid(True,axis='y')
            plt.legend()
            plt.savefig('historyKD.jpg',edgecolor = '#202732')
            plt.close()
            
        else:
            iyear = inputtime[0:4]
            itime = inputtime[-2::1]
            #計算KD值
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
                date = datetime.datetime.strftime(dtime[t],"%Y%m%d")
                y = date[0:4]
                m = date[4:6]
                if(itime == '05' or itime == '06'):
                    if(m == itime and y == iyear):
                        dtimem.append(dtime[t])
                        closem.append(close[t])
                        openm.append(open[t])
                        MA5m.append(ma5[t])
                        MA10m.append(ma10[t])
                        MA20m.append(ma20[t])
                        MA60m.append(ma60[t])
                        kvalue.append(k_list[t])
                        dvalue.append(d_list[t])
                elif(m == itime):
                    dtimem.append(dtime[t])
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
            fig = plt.figure(figsize=(10,4))
            ax = plt.gca()
            ax.tick_params(colors = 'w')
            fig.patch.set_facecolor('#202732')
            plt.plot(dtimem[:-1],closem[:-1],color='blue',label="收盤")
            plt.plot(dtimem[:-1],openm[:-1],color='orange',label="開盤")
            plt.plot(dtimem[:-1],MA5m[:-1],color='m',label='MA5')
            plt.plot(dtimem[:-1],MA10m[:-1],color='green',label='MA10')
            plt.plot(dtimem[:-1],MA20m[:-1],color='cyan',label='MA20')
            plt.plot(dtimem[:-1],MA60m[:-1],color='black',label='MA60')
            plt.ylim(min(low),max(high))
            plt.title(str(row[1])+"開盤收盤曲線",loc='right',color = 'w')
            plt.xlabel('日期')
            plt.ylabel('價格')
            plt.grid(True,axis='y')
            plt.legend()
            plt.savefig("historySearch.jpg", edgecolor = '#202732')
            fig = plt.figure(figsize=(10,4))
            ax = plt.gca()
            ax.tick_params(colors = 'w')
            fig.patch.set_facecolor('#202732')
            plt.plot(dtimem[:-1],kvalue[:-1],color='blue',label="K")
            plt.plot(dtimem[:-1],dvalue[:-1],color='orange',label='D')
            plt.title(str(row[1])+"KD值曲線",loc='right',color = 'w')
            plt.ylabel('百分比')
            plt.legend()
            plt.savefig('historyKD.jpg',edgecolor = '#202732')
            plt.close()