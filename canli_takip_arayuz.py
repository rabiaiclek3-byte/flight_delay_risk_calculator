
import tkinter as tk
from tkinter import ttk
import requests


BILINEN_HAVAYOLLARI = {
    "Türk Hava Yolları (THY)": "THY",
    "Pegasus (PGT)": "PGT",
    "American Airlines (AAL)": "AAL",
    "Lufthansa (DLH)": "DLH",
    "Emirates (UAE)": "UAE",
}


def canli_verileri_cek():
    url = "https://opensky-network.org/api/states/all"
    try:
        cevap = requests.get(url, timeout=15)
        cevap.raise_for_status()
        return cevap.json(), None
    except requests.exceptions.RequestException as hata:
        return None, str(hata)


def havayolu_ucuslarini_bul(veri, on_ek):
    if veri is None or "states" not in veri or veri["states"] is None:
        return []

    sonuclar = []
    for durum in veri["states"]:
        callsign = durum[1]
        if callsign is None:
            continue
        callsign = callsign.strip()
        if callsign.startswith(on_ek):
            sonuclar.append({
                "callsign": callsign,
                "boylam": durum[5],
                "enlem": durum[6],
                "yukseklik_m": durum[7],
                "yerde_mi": durum[8],
                "hiz_ms": durum[9],
            })
    return sonuclar


pencere = tk.Tk()
pencere.title("Canlı Uçuş Takip")
pencere.geometry("520x480")


ust_cerceve = tk.Frame(pencere, padx=10, pady=10)
ust_cerceve.pack(fill="x")

tk.Label(ust_cerceve, text="Havayolu seç:").pack(side="left")

secilen_havayolu = tk.StringVar()
acilir_menu = ttk.Combobox(
    ust_cerceve,
    textvariable=secilen_havayolu,
    values=list(BILINEN_HAVAYOLLARI.keys()),
    state="readonly",
    width=28,
)
acilir_menu.current(0)  # İlk seçeneği varsayılan yap
acilir_menu.pack(side="left", padx=8)


metin_cercevesi = tk.Frame(pencere)
metin_cercevesi.pack(fill="both", expand=True, padx=10, pady=(0, 10))

kaydirma_cubugu = tk.Scrollbar(metin_cercevesi)
kaydirma_cubugu.pack(side="right", fill="y")

sonuc_kutusu = tk.Text(
    metin_cercevesi, wrap="word", yscrollcommand=kaydirma_cubugu.set
)
sonuc_kutusu.pack(fill="both", expand=True)
kaydirma_cubugu.config(command=sonuc_kutusu.yview)


def ara_butonuna_basildi():
    goruntulenen_isim = secilen_havayolu.get()
    on_ek = BILINEN_HAVAYOLLARI[goruntulenen_isim]

    sonuc_kutusu.delete("1.0", tk.END)  #
    sonuc_kutusu.insert(tk.END, "Canlı veri çekiliyor, lütfen bekleyin...\n")
    pencere.update()  

    veri, hata = canli_verileri_cek()

    sonuc_kutusu.delete("1.0", tk.END)

    if hata is not None:
        sonuc_kutusu.insert(tk.END, f"Veri alınamadı: {hata}\n")
        return

    ucuslar = havayolu_ucuslarini_bul(veri, on_ek)

    if not ucuslar:
        sonuc_kutusu.insert(
            tk.END, f"Şu anda '{on_ek}' ile başlayan aktif bir uçuş bulunamadı.\n"
        )
        return

    sonuc_kutusu.insert(tk.END, f"'{on_ek}' için {len(ucuslar)} aktif uçuş bulundu:\n\n")
    for u in ucuslar:
        durum_metni = "Yerde" if u["yerde_mi"] else "Havada"
        hiz_kmh = round(u["hiz_ms"] * 3.6) if u["hiz_ms"] else "bilinmiyor"
        yukseklik = round(u["yukseklik_m"]) if u["yukseklik_m"] else "bilinmiyor"
        sonuc_kutusu.insert(
            tk.END,
            f"Uçuş: {u['callsign']}\n"
            f"  Durum: {durum_metni}\n"
            f"  Yükseklik: {yukseklik} metre\n"
            f"  Hız: {hiz_kmh} km/s\n"
            f"  Konum: enlem {u['enlem']}, boylam {u['boylam']}\n\n",
        )


ara_butonu = tk.Button(ust_cerceve, text="Ara", command=ara_butonuna_basildi)
ara_butonu.pack(side="left", padx=8)


pencere.mainloop()