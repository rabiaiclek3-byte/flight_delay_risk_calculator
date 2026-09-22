CEZA_ORANI_YUZDE = 3


def hesapla(kalkis_fiyati, varis_fiyati, ucus_suresi, tasinan_yuk_miktari):
    ekstra_yanan_yakit = tasinan_yuk_miktari * (CEZA_ORANI_YUZDE / 100) * ucus_suresi
    kazanc = tasinan_yuk_miktari * (varis_fiyati - kalkis_fiyati)
    maliyet = ekstra_yanan_yakit * kalkis_fiyati
    net_kar = kazanc - maliyet
    return ekstra_yanan_yakit, kazanc, maliyet, net_kar


def main():
    kalkis_fiyati = float(input("Kalkış havalimanı yakıt fiyatı (TL/kg): "))
    varis_fiyati = float(input("Varış havalimanı yakıt fiyatı (TL/kg): "))
    ucus_suresi = float(input("Uçuş süresi (saat): "))
    tasinan_yuk_miktari = float(input("Taşınan yük miktarı (kg): "))

    ekstra_yanan_yakit, kazanc, maliyet, net_kar = hesapla(kalkis_fiyati, varis_fiyati, ucus_suresi, tasinan_yuk_miktari)

    print(f"Ekstra yanan yakıt (ceza): {ekstra_yanan_yakit:.1f} kg")
    print(f"Yakıt fiyatı farkından kazanç: {kazanc:.2f} TL")
    print(f"Ekstra ağırlık taşıma maliyeti: {maliyet:.2f} TL")
    print(f"Net kar/zarar: {net_kar:.2f} TL")

    print("")
    if net_kar > 0:
        print(f"Bu rota karlı. (+{net_kar:.2f} TL)")
    else:
        print(f"Bu rota zararlı. ({net_kar:.2f} TL)")
        print("Varış havalimanında da yakıt almak daha mantıklı olabilir.")


if __name__ == "__main__":
    main()