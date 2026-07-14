import pandas as pd

import wyszukiwanie_trasy_funkcje as wt

###################
# Planner A: (Z current city do nowego punktu)
# Usuń trasy z / do punktów w których już byłem
# Usuń trasy przewożące produkty z / do, które już dla danej firmy są przewiezione
# Wybierz najkrótszą trasę
# Po wybraniu, skopiuj do nowego pliku save_game opis trasy i podmień w katalogu z zapisami
###################
def planner_A(available_begin,directory,completed_file,current_city_file,game_time,save_file):
    file_list = wt.zwroc_liste_plikow(available_begin,directory)
    completed = pd.read_csv(completed_file)
    with open(current_city_file) as f:
        current_city = f.read()
    available_all = []
    for _,f in file_list.iterrows():
        available = pd.read_csv(f["file_name"])
        available = wt.usun_trasy_z_do_obsluzonych_punktow(available,completed)
        available = wt.usun_trasy_z_do_obsluzonymi_produktami(available,completed)
        available = available[available["city_from"] == current_city]
        if len(available_all) == 0:
            available_all = available
        else:
            available_all = pd.concat([available_all,available])
    print("planner_A - własna ciężarówka")
    if len(available_all) == 0:
        print("Nie ma trasy zgodnie z algorytmem")
        return -1
    available_all = available_all.sort_values(by=["shortest_distance_km"]).reset_index(drop=True)
    available_all.to_csv("tmp.csv")
    naglowek = "company: company.volatile." + available_all.iloc[0]["company_from"] + "." + available_all.iloc[0]["city_from"]
    print(naglowek)
    print(available_all.iloc[0]["job_ID"])
    opis = wt.przygotuj_opis_trasy(available_all.iloc[0],game_time)
    print(opis)
    wt.uzupelnij_plik_o_trase(naglowek,available_all.iloc[0]["job_ID"],opis,save_file,available_all.iloc[0]["game_time"])
    with open(current_city_file, "w") as f:
        f.write(str(available_all.iloc[0]["city_to"]))
    return 0

###################
# Planner B: (Z znanego city do nowego city)
# Usuń trasy z / do punktów w których już byłem
# Usuń trasy przewożące produkty z / do, które już dla danej firmy są przewiezione
# Wybierz najkrótszą trasę
# Po wybraniu, skopiuj do nowego pliku save_game opis trasy i podmień w katalogu z zapisami
###################
def planner_B(available_begin,directory,completed_file,game_time,save_file,WINDOWS_SAVE_FILE):
    file_list = wt.zwroc_liste_plikow(available_begin,directory)
    completed = pd.read_csv(completed_file)
    available_all = []
    for _,f in file_list.iterrows():
        available = pd.read_csv(f["file_name"])
        available = wt.usun_trasy_z_do_obsluzonych_punktow(available,completed)
        available = wt.usun_trasy_z_do_obsluzonymi_produktami(available,completed)
        available = wt.usun_trasy_z_nieznanego_miasta(available,completed)
        available = wt.usun_trasy_do_znanego_miasta(available,completed)
        if len(available_all) == 0:
            available_all = available
        else:
            available_all = pd.concat([available_all,available])
    print("planner_B - szybkie trasy")
    if len(available_all) == 0:
        print("Nie ma trasy zgodnie z algorytmem")
        return -1
    available_all = available_all.sort_values(by=["shortest_distance_km"]).reset_index(drop=True)
    available_all = available_all.drop_duplicates(subset = ["company_from", "city_from", "company_to", "city_to", "cargo"]).reset_index(drop = True)
    available_all.to_csv("tmp.csv",index=False)
    for i in range(len(available_all)):
        print("Wybor: " + str(i))
        print(available_all.loc[i])
    wyb = int(input("Podaj trase: "))
    naglowek = "company : company.volatile." + available_all.iloc[wyb]["company_from"] + "." + available_all.iloc[wyb]["city_from"]
    print(naglowek)
    print(available_all.iloc[wyb]["job_ID"])
    opis = wt.przygotuj_opis_trasy(available_all.iloc[wyb],game_time)
    print(opis)
    wt.uzupelnij_plik_o_trase(naglowek,available_all.iloc[wyb]["job_ID"],opis,save_file,available_all.iloc[wyb]["game_time"],WINDOWS_SAVE_FILE)
