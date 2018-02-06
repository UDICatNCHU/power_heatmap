# power_heatmap
Draw_GR.py 為利用熱點影像顯示數據之程式(綠→紅)

Draw_GB.py 為利用熱點影像顯示數據之程式(綠→藍)

數據資料需到Google drive取得校園電力資料(https://drive.google.com/drive/folders/1_R7wtkN0JT0j2LJqtcMiRukqLjXPzQVc?usp=sharing)


# 電力資料視覺化異常分析(校園電力資料利用熱點影像顯示)

## 登入方式 :
* 開啟mobaXterm => 點選左上角Session => 點選SSH
* Remote host : 140.120.13.245
* Specify username : helen
* port : 1590
* 點選"OK"
* 輸入密碼 : helen
<img src="https://i.imgur.com/EpdwXkh.png" width="500px"/>
<img src="https://i.imgur.com/biZKfAX.png" width="500px"/>

## 合併電力資料、整理資料
* 電力資料每個樓層各4個蒐集器(data01~data04)，需加總合併後為某日某時某分某一秒該樓層的總用電量
* 時間格式需以yyyy/mm/dd為準，以每分鐘、每十分鐘、每小時為時間單位區分(資料集需自行預處理)
* 檔案名稱為"樓層-時間區間.csv"

## 熱點影像顯示
接著執行Draw_GB.py或是Draw_GR.py，內容如下：

<img src="https://i.imgur.com/DDZU2Xe.png" width="500px"/>

* 輸入指定樓層(7~9)
* 輸入指定時間區間(60為每分鐘為一單位、600為每十分鐘為一單位，3600為每小時為一單位)
* 執行並另存圖片
* 是否繼續?[Y/n]
* 結果如下：
<img src="https://i.imgur.com/NaunGZs.jpg" width="500px"/>
