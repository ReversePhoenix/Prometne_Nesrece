import os


def ustvari_datoteko_txt(from_, to):
    if not os.path.exists("C:\\Users\\Jernej-Asus\\IdeaProjects\\Prometne_nesrece_02"):
        os.makedirs("C:\\Users\\Jernej-Asus\\IdeaProjects\\Prometne_nesrece_02")
    ime_datoteke = ""
    for i in range(from_, to):
        if i >= 10:
            ime_datoteke = "pno" + str(i) + ".txt"
            with open(os.path.join("C:\\Users\\Jernej-Asus\\IdeaProjects\\Prometne_nesrece_02", ime_datoteke),
                      "w") as temp:
                temp.write("")
        else:
            ime_datoteke = "pno0" + str(i) + ".txt"
        with open(os.path.join("C:\\Users\\Jernej-Asus\\IdeaProjects\\Prometne_nesrece_02", ime_datoteke),
                  "w") as temp:
            temp.write("")


ustvari_datoteko_txt(0, 16)
