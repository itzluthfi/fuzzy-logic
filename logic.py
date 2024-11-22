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

# Fuzzy Debit Air
def FDA(x):
    return {
        "surut": kurva_linear_turun(40, 60, x),
        "sedang": segitiga(40, 60, 70, x),
        "penuh": kurva_linear_naik(60, 80, x),
    }

# Fuzzy Intensitas Hujan
def FIH(x):
    return {
        "rendah": kurva_linear_turun(40, 60, x),
        "sedang": segitiga(40, 60, 70, x),
        "tinggi": kurva_linear_naik(60, 80, x),
    }

# Fuzzy Kelembaban
def FK(x):
    return {
        "kering": kurva_linear_turun(40, 60, x),
        "agak lembab": segitiga(40, 60, 70, x),
        "lembab": kurva_linear_naik(60, 80, x),
    }

# Fungsi Z
def naik(a, b, x):
    return b - (x*(b-a))

def turun(a, b, x):
    return (x*(b-a)) + a

def defuzzify(alpha, z):
    alpha_values = [a["alpha"] for a in alpha]
    pembilang = sum(alpha_values[i] * z[i] for i in range(len(alpha)))
    penyebut = sum(alpha_values)
    return pembilang / penyebut

# Mesin Inferensi
def inferensi(DA_val, IH_val, K_val):
    DA = FDA(DA_val)
    IH = FIH(IH_val)
    K = FK(K_val)

    # Rules untuk Bukaan Pintu Air
    alphaDam = [
        {"alpha": min(DA["surut"], IH["rendah"]), "out": "lebar"},
        {"alpha": min(DA["surut"], IH["sedang"]), "out": "lebar"},
        {"alpha": min(DA["surut"], IH["tinggi"]), "out": "sempit"},
        {"alpha": min(DA["sedang"], IH["rendah"]), "out": "lebar"},
        {"alpha": min(DA["sedang"], IH["sedang"]), "out": "lebar"},
        {"alpha": min(DA["sedang"], IH["tinggi"]), "out": "sempit"},
        {"alpha": min(DA["penuh"], IH["rendah"]), "out": "sempit"},
        {"alpha": min(DA["penuh"], IH["sedang"]), "out": "sempit"},
        {"alpha": min(DA["penuh"], IH["tinggi"]), "out": "sempit"},
    ]

    # Rules untuk Durasi Irigasi
    alphaDurasi = [
        {"alpha": min(DA["surut"], K["kering"]), "out": "lama"},
        {"alpha": min(DA["surut"], K["agak lembab"]), "out": "lama"},
        {"alpha": min(DA["surut"], K["lembab"]), "out": "singkat"},
        {"alpha": min(DA["sedang"], K["kering"]), "out": "lama"},
        {"alpha": min(DA["sedang"], K["agak lembab"]), "out": "singkat"},
        {"alpha": min(DA["sedang"], K["lembab"]), "out": "singkat"},
        {"alpha": min(DA["penuh"], K["kering"]), "out": "singkat"},
        {"alpha": min(DA["penuh"], K["agak lembab"]), "out": "singkat"},
        {"alpha": min(DA["penuh"], K["lembab"]), "out": "singkat"},
    ]

    # Fuzzy Output
    zDam = [turun(0, 100, rule["alpha"]) if rule["out"] == "sempit" else naik(0, 100, rule["alpha"]) for rule in alphaDam]
    zDurasi = [turun(0, 60, rule["alpha"]) if rule["out"] == "singkat" else naik(0, 60, rule["alpha"]) for rule in alphaDurasi]

    # Defuzzification
    Dam = defuzzify(alphaDam, zDam)
    Durasi = defuzzify(alphaDurasi, zDurasi)

    return Dam, Durasi

# Input Data
DA_val = float(input("Masukkan nilai Debit Air (1-100): "))
IH_val = float(input("Masukkan nilai Intensitas Hujan (1-100): "))
K_val = float(input("Masukkan nilai Kelembaban (1-100): "))

# Output Hasil
Dam, Durasi = inferensi(DA_val, IH_val, K_val)
print(f"Tingkat Bukaan Pintu Air: {Dam:.2f} %")
print(f"Durasi Irigasi: {Durasi:.2f} Menit")