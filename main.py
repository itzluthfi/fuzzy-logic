# Fuzzy Curve
def kurva_linear_naik(a, b, x):
    if x <= a:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return 1

def kurva_linear_turun(a, b, x):
    if x <= a:
        return 1
    elif a < x <= b:
        return (b - x) / (b - a)
    else:
        return 0

def segitiga(a, b, c, x):
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

# Fuzzy Jarak Lokasi
def FJL(x):
    return {
        "dekat": kurva_linear_turun(20, 50, x),
        "sedang": segitiga(30, 50, 70, x),
        "jauh": kurva_linear_naik(50, 80, x),
    }

# Fuzzy Biaya Perjalanan
def FBP(x):
    return {
        "murah": kurva_linear_turun(200, 400, x),
        "sedang": segitiga(300, 500, 700, x),
        "mahal": kurva_linear_naik(600, 800, x),
    }

# Fuzzy Fasilitas Wisata
def FFW(x):
    return {
        "sedikit": kurva_linear_turun(1, 50, x),
        "cukup": segitiga(30, 50, 70, x),
        "lengkap": kurva_linear_naik(50, 100, x),
    }


# Fungsi Z
def naik(a, b, alpha):
    return b - (alpha * (b - a))

def turun(a, b, alpha):
    return (alpha * (b - a)) + a

def defuzzify(alpha, z):
    alpha_values = [a["alpha"] for a in alpha]
    pembilang = sum(alpha_values[i] * z[i] for i in range(len(alpha)))
    penyebut = sum(alpha_values)
    if penyebut == 0:  # Cegah pembagian nol
        return sum(z) / len(z)  # Nilai default (rata-rata domain output)
    return pembilang / penyebut

# Mesin Inferensi
# Mesin Inferensi
def inferensi(JL_val, BP_val, FW_val):
    JL = FJL(JL_val)
    BP = FBP(BP_val)
    FW = FFW(FW_val)

    # Rules untuk Tingkat Kelayakan
    alphaKelayakan = [
        {"alpha": min(JL["dekat"], BP["murah"], FW["lengkap"]), "out": "sangat layak"},
        {"alpha": min(JL["dekat"], BP["sedang"], FW["cukup"]), "out": "layak"},
        {"alpha": min(JL["dekat"], BP["mahal"], FW["sedikit"]), "out": "tidak layak"},
        {"alpha": min(JL["sedang"], BP["murah"], FW["cukup"]), "out": "layak"},
        {"alpha": min(JL["sedang"], BP["sedang"], FW["sedikit"]), "out": "tidak layak"},
        {"alpha": min(JL["jauh"], BP["mahal"], FW["sedikit"]), "out": "tidak layak"},
    ]

    # Rules untuk Tingkat Kepuasan
    alphaKepuasan = [
        {"alpha": min(JL["dekat"], FW["lengkap"]), "out": "sangat puas"},
        {"alpha": min(JL["sedang"], FW["cukup"]), "out": "puas"},
        {"alpha": min(JL["jauh"], FW["sedikit"]), "out": "tidak puas"},
    ]

    # Fuzzy Output
    zKelayakan = [turun(0, 50, rule["alpha"]) if rule["out"] == "tidak layak" else 
                  turun(50, 80, rule["alpha"]) if rule["out"] == "layak" else 
                  naik(80, 100, rule["alpha"]) for rule in alphaKelayakan]
    zKepuasan = [turun(0, 50, rule["alpha"]) if rule["out"] == "tidak puas" else 
                 turun(50, 80, rule["alpha"]) if rule["out"] == "puas" else 
                 naik(80, 100, rule["alpha"]) for rule in alphaKepuasan]

    # Defuzzification
    Kelayakan = defuzzify(alphaKelayakan, zKelayakan)
    Kepuasan = defuzzify(alphaKepuasan, zKepuasan)

    return Kelayakan, Kepuasan


# Fungsi untuk menentukan status berdasarkan nilai
def status_from_value(value, jenis):
    if jenis == "kelayakan":
        if value >= 80:
            return f"{value:.2f}% (sangat layak)"
        elif value >= 50:
            return f"{value:.2f}% (layak)"
        else:
            return f"{value:.2f}% (tidak layak)"
    elif jenis == "kepuasan":
        if value >= 80:
            return f"{value:.2f}% (sangat puas)"
        elif value >= 50:
            return f"{value:.2f}% (puas)"
        else:
            return f"{value:.2f}% (tidak puas)"

# Program Utama 
while True:
    # Input Data
    JL_val = float(input("Masukkan jarak lokasi (km, 20-80): "))
    BP_val = float(input("Masukkan biaya perjalanan (ribu, 200-800): "))
    FW_val = float(input("Masukkan nilai fasilitas wisata (1-100): "))

    # Output Hasil
    Kelayakan, Kepuasan = inferensi(JL_val, BP_val, FW_val)

    # Menambahkan status berdasarkan hasil defuzzifikasi
    status_kelayakan = status_from_value(Kelayakan, "kelayakan")
    status_kepuasan = status_from_value(Kepuasan, "kepuasan")

    print(f"Tingkat Kelayakan Pariwisata: {status_kelayakan}")
    print(f"Tingkat Kepuasan Wisatawan: {status_kepuasan}")

    # Opsi untuk menjalankan ulang
    ulang = input("Apakah Anda ingin mencoba lagi? (y/n): ").lower()
    if ulang != 'y':
        print("Program selesai. Terima kasih!")
        break
