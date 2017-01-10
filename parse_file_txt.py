from pandas import DataFrame
import csv
import xlrd


# odpre datoteko in se znebi znakov, ki bi morali predstavljati č, š, ž
def odpri_datoteko(datoteka):
    vse_nesrece = []
    with open(datoteka, "r", encoding="utf-8", errors="ignore") as vrstice:
        for vrstica in vrstice:
            vrstica = vrstica.replace("¬", "Č").replace("ć", "Š").replace("¦", "Ž")
            vse_nesrece.append(vrstica)
    return vse_nesrece


# skrbi za prvo bazo PROMETNE NESREČE (PN) 19 spremenjivk
# funkcija skrbi za tiste datoteke, ki niso ločene s presledki, ampak izlušči podatke preko indeksov.
def parse_one_line_pn(vrstica):
    id_nesrece = vrstica[0:9]
    klasifikacija = vrstica[9:10]
    ui = vrstica[10:14]
    datum = vrstica[14:24]
    ura = vrstica[24:29]
    # D pomeni, da se je nesreča zgodila v naselju in N pomeni, da se je zgodila izven.
    indikator_mesta = vrstica[29:30]
    kategorija_ceste = vrstica[30:31]
    oznaka_ceste = vrstica[31:36]
    kraj_nesrece = vrstica[36:61].strip(" ")
    sifra_ulica = vrstica[61:66]
    ulica = vrstica[66:91].strip(" ")
    hisna_stevilka = vrstica[91:95]
    opis_prizorisca = vrstica[95:96]
    vzrok_nesrece = vrstica[96:98]
    tip_nesrece = vrstica[98:100]
    vremenske_okoliscine = vrstica[100:101]
    stanje_prometa = vrstica[101:102]
    stanje_vozisca = vrstica[102:104]
    stanje_površine = vrstica[104:106]
    return id_nesrece, klasifikacija, ui, datum, ura, indikator_mesta, kategorija_ceste, \
           oznaka_ceste, kraj_nesrece, sifra_ulica, ulica, hisna_stevilka, opis_prizorisca, \
           vzrok_nesrece, tip_nesrece, vremenske_okoliscine, stanje_prometa, stanje_vozisca, stanje_površine


# skrbi za drugo bazo PROMETNE NESREČE OSEBNO (PNO) 12 spremenljivk
def parse_one_line_pnose(vrstica):
    if len(vrstica) < 10:
        pass
    else:
        p = 0
        id_nesrece = vrstica[0:9]
        oseba_je = "1" if vrstica[9:10] == "D" else "0"
        if vrstica[10] == " ":
            starot = vrstica[11:15]
            p += 1
        else:
            starot = vrstica[10:14]
        try:
            if vrstica[15] == " " and vrstica[16] == "1" or vrstica[16] == "2":
                spol = vrstica[16:17]
                p += 1
            else:
                spol = vrstica[14 + p:15 + p]
        except:
            spol = vrstica[14 + p:15 + p]
        obcina_prebi = vrstica[15 + p:19 + p]
        drzavljanstvo = vrstica[19 + p:22 + p]
        poskodba_osebe = vrstica[22 + p:23 + p]
        vrsta_udeleženca = vrstica[23 + p:25 + p]
        varovanje = vrstica[25 + p:26 + p]
        staz = vrstica[26 + p:30 + p]
        v_alko_test = vrstica[30 + p:34 + p]
        v_strokovni_p = vrstica[34 + p:38 + p]
        return id_nesrece, oseba_je, starot, spol, obcina_prebi, drzavljanstvo, \
               poskodba_osebe, vrsta_udeleženca, varovanje, staz, v_alko_test, v_strokovni_p


# skrbi za PN
def zapisi_v_tabele(pot_datoteke):
    global temp
    temp = [[] for _ in range(19)]
    celotna_datoteka = odpri_datoteko(pot_datoteke)
    for vrstica in celotna_datoteka:
        st = 0
        for atribut in parse_one_line_pn(vrstica):
            temp[st].append(atribut)
            st += 1


# skrbi za PNO
def zapisi_v_tabele_1(pot_datoteke):
    global temp
    temp = [[] for _ in range(13)]
    celotna_datoteka = odpri_datoteko(pot_datoteke)
    for vrstica in celotna_datoteka:
        st = 0
        vrstica = parse_one_line_pnose(vrstica)
        if vrstica:
            for v in vrstica:
                entry = v.replace("\n", "")
                temp[st].append(entry)
                st += 1


# skrbi za novejše podatke z $ vrednostmi >= 2001
def zapisi_v_tabele_2(pot_datoteke):
    global temp
    temp = [[] for _ in range(19)]
    celotna_datoteka = odpri_datoteko(pot_datoteke)
    for vrstica in celotna_datoteka:
        st = 0
        vrstica = vrstica.split("$")
        for v in vrstica:
            v = v.lstrip(" ")
            temp[st].append(v)
            st += 1


# za PNO starješe < 2001
# df = DataFrame({"01. ID nesrece": temp[0],
#                 "02. Oseba": temp[1],
#                 "03. Starost": temp[2],
#                 "04. Spol": temp[3],
#                 "05. Obcina prebivalca": temp[4],
#                 "06. Državljanstvo": temp[5],
#                 "07. Poškodba osebe": temp[6],
#                 "08. Vrsta udeleženca": temp[7],
#                 "09. Varovanje": temp[8],
#                 "10. Staž": temp[9], "11. Vrednost alko testa": temp[10],
#                 "12. Vrednost strkovnega preizkusa": temp[11]
#                 })


# za PNO novejšje > 2001
# df = DataFrame({"01. ID nesrece": temp[0],
#                 "02. Oseba": temp[1],
#                 "03. Starost": temp[2],
#                 "04. Spol": temp[3],
#                 "05. Obcina prebivalca": temp[4],
#                 "06. Državljanstvo": temp[5],
#                 "07. Poškodbe osebe": temp[6],
#                 "08. Vrsta udeleženca": temp[7],
#                 "09. Varovanje": temp[8],
#                 "10. Staž leto": temp[9],
#                 "11. Staž mesec": temp[10],
#                 "12. Vrednost alko testa:": temp[11],
#                 "13. Vrednost strkovnega preizkusa": temp[12]})

# za PN starejše do 2007
# df = DataFrame({"01. ID nesrece": temp[0],
#                 "02. Klasifikacija nesrece": temp[1],
#                 "03. Upravne enote": temp[2],
#                 "04. Datum": temp[3],
#                 "05. Ura": temp[4],
#                 "06. Indikator mesta": temp[5],
#                 "07. Kategorija ceste": temp[6],
#                 "08. 0znaka ceste ": temp[7],
#                 "09. Kraj nesrece": temp[8],
#                 "10. Sifra ulice": temp[9],
#                 "11. Ulica": temp[10],
#                 "12. Hišna številka": temp[11],
#                 "13. Opis prizorisca": temp[12],
#                 "14. Vzrok nesrece": temp[13],
#                 "15. Tip nesrece": temp[14],
#                 "16. Vremenske okoliscine": temp[15],
#                 "17. Stanje prometa": temp[16],
#                 "18. Stanje vozisca": temp[17],
#                 "19. Stanje povrsine": temp[18]
#                 })

# PN NOVEJŠE 2007 >=
# df = DataFrame({"01. ID nesrece": temp[0],
#                 "02. Klasifikacija nesrece": temp[1],
#                 "03. Upravne enote": temp[2],
#                 "04. Datum": temp[3],
#                 "05. Ura": temp[4],
#                 "06. Indikator mesta": temp[5],
#                 "07. Kategorija ceste": temp[6],
#                 "08. 0znaka ceste ": temp[7],
#                 "09. Sifra ulice": temp[8],
#                 "10. Kraj nesrece": temp[9],
#                 "11. Ulica": temp[10],
#                 "12. Hišna številka": temp[11],
#                 "13. Opis prizorisca": temp[12],
#                 "14. Vzrok nesrece": temp[13],
#                 "15. Tip nesrece": temp[14],
#                 "16. Vremenske okoliscine": temp[15],
#                 "17. Stanje prometa": temp[16],
#                 "18. Stanje vozisca": temp[17],
#                 "19. Stanje povrsine": temp[18]
#                 })


# PNO za novejše >= 2005
# df = DataFrame({"01. ID nesrece": temp[0],
#                 "02. Oseba": temp[1],
#                 "03. Starost": temp[2],
#                 "04. Spol": temp[3],
#                 "05. Državljanstvo": temp[4],
#                 "06. Poškodbe osebe": temp[5],
#                 "07. Vrsta udeleženca": temp[6],
#                 "08. Varovanje": temp[7],
#                 "09. Izkušenost voznika": temp[8],
#                 "10. Vrednost alkotesta:": temp[9],
#                 "11. Vrednost strkovnega preizkusa": temp[10]
#                 })


def from_excel_to_csv(excel_file, location):
    wb = xlrd.open_workbook(excel_file)
    sh = wb.sheet_by_name("sheet1")
    your_csv_file = open(location, "w", newline="", encoding="utf-8")
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    your_csv_file.close()


def call_all(start, end, type_of):
    ending = ".txt"
    for i in range(start, end):
        if i < 10:
            file_name = "pno0" + str(i)
        else:
            file_name = "pno" + str(i)
        print(file_name)
        # zapisi_v_tabele("tekstovne_datoteke\\PN\\" + file_name + ending)
        # zapisi_v_tabele_1("tekstovne_datoteke\\" + type_of + "\\" + file_name + ending)
        zapisi_v_tabele_2("tekstovne_datoteke\\PNO\\" + file_name + ending)
        print("Odpiram ...")
        df = DataFrame({"01. ID nesrece": temp[0],
                        "02. Oseba": temp[1],
                        "03. Starost": temp[2],
                        "04. Spol": temp[3],
                        "05. Državljanstvo": temp[4],
                        "06. Poškodba osebe": temp[5],
                        "07. Vrsta udeleženca": temp[6],
                        "08. Varovanje": temp[7],
                        "09. Izkušenost voznika": temp[8],
                        "10. Vrednost alkotesta": temp[9],
                        "11. Vrednost strkovnega preizkusa": temp[10]
                        })
        df.to_excel("excel_datoteke\\" + type_of + "\\" + file_name + ".xlsx", sheet_name="sheet1", index=False)
        print("EXCELE DATOTEKA KONČANA!")
        from_excel_to_csv("excel_datoteke\\" + type_of + "\\" + file_name + ".xlsx",
                          "csv_datoteke\\" + type_of + "\\" + file_name + ".csv")
        print("CSV DATOTEKA KONČANA!")
        print("KONČANO")


if __name__ == "__main__":
    call_all(8, 15, "PNO")
