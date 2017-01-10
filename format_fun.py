import datetime
import decimal
import unittest


def to_date_format(s):
    if "." in s:
        s = s.split(".")
    else:
        s = s.split("/")
    return datetime.date(int(s[2]), int(s[1]), int(s[0]))


def to_time_format(s):
    if "." in s:
        s = s.split(".")
        return datetime.time(int(s[0]), int(s[1]))
    return datetime.time(int(s), 00)


def replace_with_zero(n):
    return n if n.isnumeric() else 0


def is_real(o):
    return None if not o.isnumeric() else o


def test_value(value_of):
    return value_of if value_of.replace(",", "", 1).isdigit() else None


# spremeni meseca in leta v leto tako, da zaokrožimo eno leto navzgor če je star več kot pol leta tekočega leta
def spremeni_leta(vrednost_leta):
    if len(vrednost_leta) == 4:
        leto, meseci = int(vrednost_leta[:2]), int(vrednost_leta[2:4])
        return leto + 1 if meseci >= 6 else leto
    else:
        return int(vrednost_leta)


# ustvari slovar, ki vsebuje šifro države kot ključ in državo kot vrednost
def drzavljanstvo(datoteka):
    drzave = {}
    celotna_datoteka = open(datoteka, "r", encoding="utf-8")
    for vrstica in celotna_datoteka:
        sifra, drzava = vrstica.split(None, 1)
        drzava = drzava.strip("\n")
        drzave[sifra] = drzava
    return drzave


def izpelji_drzavljanostv(sifra):
    d = drzavljanstvo("drzavljanstvo.txt")
    return d[sifra]


# vozniški staž oz. čas vozniškega dovolenja
def izkusenost(izkusnje):
    if "-" in izkusnje:
        leto, meseci = izkusnje.split("-")
        return int(leto) + 1 if int(meseci) >= 6 else int(leto)
    leto, meseci = int(izkusnje[:2]), int(izkusnje[2:4])
    return int(leto) + 1 if int(meseci) >= 6 else int(leto)


def preizkusi(vrednost):
    if "," in vrednost:
        vrednost = vrednost.replace(",", ".")
    return decimal.Decimal(vrednost)


# določi spol 1 == moški, 2 == ženska, neznan == 0
# funkcija naj vrača
def doloci_spol(spol):
    s = {"NEZNAN": 0, "MOŠKI": 1, "ŽENSKI": 2}
    return s[spol]


def vstavi_koordinato(k):
    if k:
        return decimal.Decimal(k)
    else:
        return 0


def udelezenec(u):
    s = {"UDELEŽENEC": 1, "POVZROČITELJ": 0}
    return s[u]


def poskoda(p):
    s = {"BREZ POŠKODBE": "B",
         "HUDA TELESNA POŠKODBA": "H",
         "LAŽJA TELESNA POŠKODBA": "L",
         "SMRT": "S",
         "BREZ POŠKODBE-UZ": "U",
         "NI VNEŠENO": "N"}

    return s[p]


def varovanje(v):
    s = {"DA": 1, "NE": 2, "NEZNAN": 0, "NI PODATKA": 3}
    return s[v]


voz = {"AV": "VOZNIK AVTOBUSA",
       "DS": "VOZNIK DELOVNEGA STROJA",
       "KM": "VOZNIK KOLESA Z MOTORJEM",
       "KO": "KOLESAR",
       "KR": "X-KRŠITELJ - JRM",
       "KV": "VOZNIK KOMBINIRANEGA VOZILA",
       "LK": "VOZNIK LAHKEGA ŠTIRIKOLESA",
       "MK": "VOZNIK MOTORNEGA KOLESA",
       "MO": "VOZNIK MOPEDA",
       "OA": "VOZNIK OSEBNEGA AVTOMOBILA",
       "OD": "ODGOVORNA OSEBA",
       "OS": "OSTALO",
       "PE": "PEŠEC",
       "PO": "PRAVNA OSEBA",
       "PT": "POTNIK",
       "SD": "POSAMEZNIK, S.P., KI SAMOSTOJNO OPRAVLJA DEJAVNOST IN ZAPOSLUJE DRUGE",
       "SK": "VOZNIK ŠTIRIKOLESA",
       "SM": "SKRBNIK MLADOLETNIKA",
       "SP": "SAMOSTOJNI PODJETNIK",
       "SV": "VOZNIK SPECIALNEGA VOZILA",
       "TK": "VOZNIK TRIKOLESA",
       "TR": "VOZNIK TRAKTORJA",
       "TV": "VOZNIK TOVORNEGA VOZILA",
       "NI": "NI VNEŠENO"}


def tip_u(ud):
    s = dict((beseda, ac) for ac, beseda in voz.items())
    return s[ud]


# naredi teste ze vse možne funkcije
class PrometneNesrece(unittest.TestCase):
    def test_datum(self):
        self.assertEqual(to_date_format("09.02.2012"), datetime.date(2012, 2, 9))
        self.assertEqual(to_date_format("31.12.2000"), datetime.date(2000, 12, 31))
        self.assertEqual(to_date_format("16/2/2014"), datetime.date(2014, 2, 16))

    def test_time(self):
        self.assertEqual(to_time_format("11.50"), datetime.time(11, 50))
        self.assertEqual(to_time_format("12"), datetime.time(12, 00))
        self.assertEqual(to_time_format("3"), datetime.time(3, 00))

    def test_drzavljanstvo(self):
        self.assertEqual(izpelji_drzavljanostv("005"), "SLOVENIJA")
        self.assertEqual(izpelji_drzavljanostv("211"), "ITALIJA")
        self.assertEqual(izpelji_drzavljanostv("444"), "EKVATORIALNA GVINEJA")
