import pandas as pd
veri = pd.read_csv("Airline_Delay_Cause.csv") 
print(veri.head())
print(veri.columns)
toplam_gecikme = veri["weather_delay"].sum() + veri["nas_delay"].sum() + veri["security_delay"].sum() + veri["late_aircraft_delay"].sum() + veri["carrier_delay"].sum()
hava_orani = veri["weather_delay"].sum() / toplam_gecikme * 100
print("Hava durumu kaynaklı gecikme oranı: %", round(hava_orani, 1))
print("=== Rötar Risk ve Fiyat Hesaplayıcı ===")

print("Rota: 1) İç Hat-Kısa  2) İç Hat-Uzun  3) Dış Hat-Avrupa  4) Dış Hat-Kıta")
rota = int(input("Numara: "))

ay = int(input("Ay (1-12): "))

print("Gün: 1)Pzt 2)Sal 3)Çar 4)Per 5)Cum 6)Cmt 7)Paz")
gun = int(input("Numara: "))

saat = int(input("Kalkış saati (0-23): "))
ilk_sefer = input("Günün ilk seferi mi? (e/h): ")

print("Hava: 1)Açık 2)Parçalı 3)Yağmur 4)Kar/Sis 5)Fırtına")
hava = int(input("Numara: "))

aktarma = input("Aktarmalı mı? (e/h): ")

print("Yoğunluk: 1)Düşük 2)Orta 3)Yüksek")
kalkis_yog = int(input("Kalkış için numara: "))
varis_yog = int(input("Varış için numara: "))

print("Bilete kaç gün kaldı: 1)0-3 2)4-14 3)15-45 4)45+")
rezervasyon = int(input("Numara: "))

hava_puan = {1: 0, 2: 3, 3: 15, 4: 30, 5: 45}
hava_neden = {
    1: "Açık havada ek risk yok.",
    2: "Parçalı bulutluluk küçük risk katar.",
    3: "Yağmur pist kayganlığını etkiler.",
    4: "Kar/sis buzlanma ve görüş riskini artırır.",
    5: "Fırtınada kalkış/iniş onayları gecikebilir.",
}
rota_puan = {1: 3, 2: 6, 3: 8, 4: 12}
rota_fiyat = {1: (1000, 2500), 2: (1800, 3800), 3: (3500, 9000), 4: (8000, 25000)}
yog_puan_kalkis = {1: 0, 2: 8, 3: 16}
yog_puan_varis = {1: 0, 2: 6, 3: 12}
rez_carpan = {1: 1.40, 2: 1.15, 3: 1.00, 4: 0.85}

hafta_sonu = gun == 5 or gun == 7
kis = ay in (12, 1, 2)
yaz = ay in (6, 7, 8)

puan = 5 

if 5 <= saat <= 8:
    saat_puan = 0
elif 9 <= saat <= 13:
    saat_puan = 5
elif 14 <= saat <= 17:
    saat_puan = 10
elif 18 <= saat <= 21:
    saat_puan = 18
else:
    saat_puan = 8
puan = puan + saat_puan

puan = puan + (0 if ilk_sefer == "e" else 12)
puan = puan + hava_puan[hava]
puan = puan + (10 if hafta_sonu else (5 if gun == 1 else 0))
puan = puan + (12 if kis else (10 if yaz else 0))
puan = puan + yog_puan_kalkis[kalkis_yog]
puan = puan + yog_puan_varis[varis_yog]
puan = puan + (20 if aktarma == "e" else 0)
puan = puan + rota_puan[rota]

puan = min(puan, 95)

if puan <= 25:
    seviye = "Düşük"
elif puan <= 50:
    seviye = "Orta"
elif puan <= 75:
    seviye = "Yüksek"
else:
    seviye = "Çok Yüksek"

rotar_min = round(puan * 0.5)
rotar_max = round(puan * 1.6) + 15


fiyat_min, fiyat_max = rota_fiyat[rota]
carpan = 1.0
if yaz:
    carpan = carpan * 1.20
elif kis:
    carpan = carpan * 0.95
if hafta_sonu:
    carpan = carpan * 1.10
carpan = carpan * rez_carpan[rezervasyon]

fiyat_min = round(fiyat_min * carpan)
fiyat_max = round(fiyat_max * carpan)

print("")
print("=== SONUÇ ===")
print("Risk Skoru:", puan, "/ 100  -  Seviye:", seviye)
print("Tahmini Rötar:", rotar_min, "-", rotar_max, "dakika")
print("Tahmini Fiyat:", fiyat_min, "-", fiyat_max, "TL")

print("")
print("=== Nedenler ===")
print("-", hava_neden[hava])
if saat_puan >= 18:
    print("- Akşam saatinde önceki uçuşlardan rötar birikir.")
if ilk_sefer != "e":
    print("- Günün ilk seferi olmadığı için önceki rötar devralınabilir.")
if hafta_sonu:
    print("- Hafta sonu yolcu yoğunluğu artar.")
if kis:
    print("- Kışın buzlanma/kar riski artar.")
elif yaz:
    print("- Yazın tatil sezonu yoğunluğu riski artırır.")
if yog_puan_kalkis[kalkis_yog] >= 16:
    print("- Kalkış havalimanı çok yoğun.")
if yog_puan_varis[varis_yog] >= 12:
    print("- Varış havalimanı çok yoğun.")
if aktarma == "e":
    print("- Aktarmalı uçuşta bağlantı kaçırma riski var.")

print("")
print("=== Öneriler ===")
if puan > 50:
    print("- Risk yüksek, yedek uçuş düşün.")
if aktarma == "e":
    print("- En az 90-120 dakika katman süresi bırak.")
if hava >= 4:
    print("- Uçuştan bir gün önce hava durumunu kontrol et.")
print("- Uçuş durumunu kalkıştan birkaç saat önce tekrar kontrol et.")
