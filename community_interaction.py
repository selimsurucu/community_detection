# -*- coding: utf-8 -*-
"""
Created on Wed May 27 00:17:13 2020

@author: selim
"""

import sys
import numpy as np
import os 
from datetime import datetime
import csv
import calendar

"""
PARAMETLERİN BULUNMASI
"""
communities_parametre = sys.argv [1]
retweet_folder= sys.argv [2]
communities_file= open(communities_parametre, "r")

"""
communities.txt okunarak communityler elde edildi.
"""
communities = np.array([])
for line in communities_file:
    my_split = line.split("=")
    communities = np.append(communities,my_split[1])
communities_file.close()



"""
İLK ATAMALAR 
"""
weekly_first_date=None
biweekly_first_date = None
montly_first_date = None
weekly_array= np.zeros((len(communities),len(communities)))
bi_weekly_array=np.zeros((len(communities),len(communities)))
monthly_array=np.zeros((len(communities),len(communities)))
code_first_run=True



"""
RETWEET DOSYALARI OKUNARAK TESPİT EDİLMEYE ÇALIŞILDIĞI KISIM.
TESPİT EDİLİRSE TRUE DÖNER. TESPİT EDİLMEZSE FALSE DÖNER
"""
def search_users_file(file,search):
     fhand = open(file.name)
     status = False
     for line in fhand:
         result=line.find(search+",")
         if result != -1 :
             status = True
             break
     return status
    

"""
TÜM MATRİSLER X,Y= I,J KOORDİNATLARINA GÖRE SET EDİLİR.
"""
def set_matris_result(i,j):
    weekly_array[i][j]  = int(weekly_array[i][j]) +1 
    bi_weekly_array[i][j]  = int(bi_weekly_array[i][j]) +1 
    monthly_array[i][j]  = int(monthly_array[i][j]) +1 
    print(i,j,monthly_array[i][j])

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
COMMUNİTY'LER ARASINDAKİ İLİŞKİLERİN TESPİT EDİLDİĞİ KISIM.
İLİŞKİ TESPİT EDİLDİĞİNDE MATRİS'LER GÜNCELLENİR.
"""
def found_com_relations(file):
    #print("user = ", file)
    community_count = len(communities)
    for i in range(0,community_count):
        users = eval(communities[i])
        for user in users:
            for j in range(0,community_count):
                    if i == j :
                        continue
                    for o_user in eval(communities[j]):
                        result = search_users_file(file,user+","+o_user) 
                        if result == True:
                            set_matris_result(i,j)

                            
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
CSV dosyalarını ilk başta oluşturulduğu kısım
"""                    
def createdCsvFile():
    fieldnames = np.array(["first_date,last_date"])
    for i in range(0,len(communities)):
        for j in range(0,len(communities)):
            if i == j:
                continue
            else:
                fieldnames= np.append(fieldnames, str(i)+"-"+str(j))
    with open('results/weekly.csv', mode='w+',newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    with open('results/bi_weekly.csv', mode='w+',newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    with open('results/monthly.csv', mode='w+',newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
    print(fieldnames)
createdCsvFile()









# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
# CSV dosyasına yazma işlemleri bu fonksiyonda yapılır.
# ilk parametre Fonksiyonun çağrıldığı yerdeki son tarih ,
# ikinci parametre ise tip 
# Tip =  0 Weekly / Tip = 1 Biweekly / tip = 2 Montly
"""
def writeToCsvFile(last_date,tip):
   
    if tip == 0 : # Weekly
        arr = np.array([weekly_first_date,last_date])
        for i in range(0,len(communities)):
            for j in range(0,len(communities)):
                if i == j:
                    continue
                arr = np.append(arr, int(weekly_array[i,j]))
        with open('results/weekly.csv', mode='a',newline='') as csv_file:
             filewriter = csv.writer(csv_file, delimiter=',',
                            quoting=csv.QUOTE_MINIMAL)
             filewriter.writerow(arr)
    elif tip == 1 : # Bi weekly
        arr = np.array([biweekly_first_date,last_date])
        for i in range(0,len(communities)):
            for j in range(0,len(communities)):
                if i == j:
                    continue
                arr = np.append(arr, int(bi_weekly_array[i,j]))
        with open('results/bi_weekly.csv', mode='a',newline='') as csv_file:
            filewriter = csv.writer(csv_file, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(arr)
    elif tip == 2 : # Monthly
        arr = np.array([montly_first_date,last_date])
        for i in range(0,len(communities)):
            for j in range(0,len(communities)):
                if i == j:
                    continue
                arr = np.append(arr, int(monthly_array[i,j]))
        with open('results/monthly.csv', mode='a',newline='') as csv_file:
            filewriter = csv.writer(csv_file, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(arr)
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


# MAIN 
files_count = 0
for path in os.listdir(retweet_folder):
    if os.path.isfile(os.path.join(retweet_folder, path)):
        files_count += 1

print("Retweet Dosya Sayısı = " , files_count)

count = 0 
for entry in os.listdir(retweet_folder):
    print('reading retweet edges from file ('+entry+')...')
    if os.path.isfile(os.path.join(retweet_folder, entry)):
        count +=1 
        fhand = open(os.path.join(retweet_folder, entry))
        str_date =entry.split(".txt")
        datetime_obj = datetime.strptime(str_date[0], '%Y%m%d')
        writedFile=False # Dosyaya yazıldıysa tekrar yazılmasın diye eklendi.
        
        # Kod ilk çalıştırıldıysa ilk dosya tarihini weekly,biweekly,montly ye ilk gün olarak ataması yapılıyor. Değilse None atılıyor.
        if code_first_run:
            weekly_first_date = datetime_obj.date()
            biweekly_first_date = datetime_obj.date()
            montly_first_date = datetime_obj.date()
            code_first_run = False
        
       # Dizileri Sıfırlama işlemleri
        if(datetime_obj.date().weekday() == 0): 
            weekly_array.fill(0)
            weekly_first_date = datetime_obj.date()
            #print(weekly_array)
            #print("Mon") # 0 = Mon / 6 = Sun
            
        if datetime_obj.day == 1: # Her ayın 1 i hem ayın hem de biweekly nin başlayacağı tarih
            bi_weekly_array.fill(0)
            monthly_array.fill(0)
            biweekly_first_date = datetime_obj.date()
            montly_first_date = datetime_obj.date()
        elif datetime_obj.day == 15 : # her ayın 15 i biweekly nin başlayacağı tarih
            bi_weekly_array.fill(0)
            bi_weekly_array = datetime_obj.date()
            
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        found_com_relations(fhand)
        # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        
        
        if(datetime_obj.date().weekday()==6) and writedFile == False: # Haftanın son günü
            writedFile = True
            writeToCsvFile(datetime_obj.date(),0) # = weekly
        if datetime_obj.day == 14 and writedFile == False:
            writedFile = True
            writeToCsvFile(datetime_obj.date(),1) # = biweekly
        elif  datetime_obj.day == calendar.monthrange(datetime_obj.year, datetime_obj.month)[1] and writedFile == False: # Ayın son günü
            # Son günü olduğu için Hem monthly hem de biweekly csv dosyalarına yazdırılması gerekiyor.
            writedFile = True
            writeToCsvFile(datetime_obj.date(),1) # = biweekly
            writeToCsvFile(datetime_obj.date(),2) # = Monthly
       
        if files_count == count and writedFile == False : # Dosya son ise Bütün csv dosyalarının yazdırılması gerekiyor. 
             writedFile = True 
             writeToCsvFile(datetime_obj.date(),0) # = weekly
             writeToCsvFile(datetime_obj.date(),1) # = biweekly
             writeToCsvFile(datetime_obj.date(),2) # = Monthly