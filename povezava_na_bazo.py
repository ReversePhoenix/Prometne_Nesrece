import csv
import pyodbc as pyd
from format_fun import *

cnxn = pyd.connect("DRIVER={MySQL ODBC 5.3 Unicode Driver};SERVER=localhost;DATABASE=prometne_nesrece;UID=root;PWD=abc")
cursor = cnxn.cursor()

sql_01 = "INSERT INTO nesreca (id_nesrece, klas_nesrece, st_ue, datum, ura, x, y) VALUES (?, ?, ?, ? ,?,?,?)"

sql_02 = "INSERT INTO zunanje_razmere (id_nesrece, vreme, stanje_prometa, stanje_vozisca, stanje_povrsine) VALUES (?, ?, ?, ?, ?)"

# idikator manjka
sql_03 = "INSERT INTO krajevne_lastnosti (id_nesrece, odsek, sifra_oznaka, kraj_nesrece, hisna_st, prizorisce, vzrok, tip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

sql_04 = "INSERT INTO  osebni_Podatki(id_nesrece, oseba_je, starost, spol, drzavljanstvo, poskodba_osebe, vrsta_udelezenca, varnost, izkusenost, alkotest, strokovni_pregled) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"


def fill_in(sql, insert):
    cursor.execute(sql, insert)
    cursor.commit()


cursor.execute("SET FOREIGN_KEY_CHECKS=0")
cursor.commit()


# funkcija za polnenje baze
def fill_base(start=0, end=0):
    ending = ".csv"
    for i in range(start, end):
        file = "pn0" + str(i) if i < 10 else "pn" + str(i)
        print(file)
        print("STARTING! " + file)
        with open("csv_datoteke/PN/" + file + ending, encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for _, row in enumerate(reader, start=1):
                fill_in(sql_01, (row["id"],
                                 row["klasifikacija nesreče glede na posledice"],
                                 row["upravna enota"],
                                 to_date_format(row["datum nesrece"]),
                                 to_time_format(row["ura nesreče"]),
                                 vstavi_koordinato(row["x"]),
                                 vstavi_koordinato(row["y"])))
            print("DONE " + file)


fill_base(15, 16)


# nesreca(za koordinate)
# (row["id"],
#  row["klasifikacija nesreče glede na posledice"],
#  row["upravna enota"],
#  to_date_format(row["datum nesrece"]),
#  to_time_format(row["ura nesreče"]),
#  vstavi_koordinato(row["x"]),
#  vstavi_koordinato(row["y"])))

# nesreca
# (row["01. ID nesrece"],
# row["02. Klasifikacija nesrece"],
# row["03. Upravne enote"],
# to_date_format(row["04. Datum"]),
# to_time_format(row["05. Ura"]))

# zunanje razmere

# (row["01. ID nesrece"],
# row["16. Vremenske okoliscine"],
# row["17. Stanje prometa"],
# row["18. Stanje vozisca"],
# row["19. Stanje povrsine"])

# krajevne lastnosti

# (row["01. ID nesrece"],
# row["06. Indikator mesta"],
# row["07. Kategorija ceste"],
# row["08. 0znaka ceste "],
# row["09. Kraj nesrece"],
# row["12. Hišna številka"],
# row["13. Opis prizorisca"],
# row["14. Vzrok nesrece"],
# row["15. Tip nesrece"])

# osebni podatki

# (row["01. ID nesrece"],
# row["02. Oseba"],
# row["03. Starost"],
# row["04. Spol"],
# row["06. Državljanstvo"],
# row["07. Poškodba ceste"],
# row["08. Vrsta udeleženca"]
# row["09. Varovanje"]
# row["10. Staž"]
# row["11. Vrednost alkotesta"]
# row["12. Vrednost strokovenga preizkusa"])

# (row["01. ID nesrece"],
#  udelezenec(row["02. Oseba"]),
#  row["03. Starost"],
#  doloci_spol(row["04. Spol"]),
#  row["05. Državljanstvo"],
#  poskoda(row["06. Poškodba osebe"]),
#  tip_u(row["07. Vrsta udeleženca"]),
#  varovanje(row["08. Varovanje"]),
#  izkusenost(row["09. Izkušenost voznika"]),
#  preizkusi(row["10. Vrednost alkotesta"]),
#  preizkusi(row["11. Vrednost strkovnega preizkusa"])))
