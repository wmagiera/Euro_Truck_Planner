import shutil

import pandas as pd
import os
import re

import funkcje_pomocnicze as fp

###################
# file_begin - początek nazwy plików do wyszukania
# directory - katalog, gdzie należy szukać
#
# Zwraca DataFrame z nazwami plików zaczynających się od file_begin
###################
def zwroc_liste_plikow(file_begin,directory):
    file_tab = []
    for file in os.listdir(directory):
        if file.startswith(file_begin):
            file_tab.append({
                "file_name": os.path.join(directory, file)
            })
    file_pd = pd.DataFrame(file_tab)
    return file_pd

###################
# available - DataFrame z dostępnymi trasami
# completed - DataFrame ze zrobionymi trasami
#
# Usuwa wszystkie trasy, które zaczynają się lub kończą w obsłużonym punkcie
# Zwraca DataFrame
###################
def usun_trasy_z_do_obsluzonych_punktow(available,completed):
    completed_all = fp.completed_wyciagnij_wszystkie_punkty(completed)
    available = available.merge(
        completed_all.rename(columns={'city' : 'city_from', 'company' : 'company_from'}),
        on=["company_from", "city_from"],
        how="left",
        indicator=True
    ).query('_merge == "left_only"').drop(columns="_merge")
    available = available.merge(
        completed_all.rename(columns={'city' : 'city_to', 'company' : 'company_to'}),
        on=["company_to", "city_to"],
        how="left",
        indicator=True
    ).query('_merge == "left_only"').drop(columns="_merge").drop_duplicates(subset = ["company_from", "city_from", "company_to", "city_to", "cargo"])
    return available

###################
# available - DataFrame z dostępnymi trasami
# completed - DataFrame ze zrobionymi trasami
#
# Usuwa wszystkie trasy, które mają produkt już dla danej firmy obsłużony
# Zwraca DataFrame
###################
def usun_trasy_z_do_obsluzonymi_produktami(available,completed):
    available = available.merge(
        completed[['company_from', 'cargo']],
        on=["company_from", "cargo"],
        how="left",
        indicator=True
    ).query('_merge == "left_only"').drop(columns="_merge")
    available = available.merge(
        completed[['company_to', 'cargo']],
        on=["company_to", "cargo"],
        how="left",
        indicator=True
    ).query('_merge == "left_only"').drop(columns="_merge").drop_duplicates(subset = ["company_from", "city_from", "company_to", "city_to", "cargo"])
    return available

###################
# available - DataFrame z dostępnymi trasami
# completed - DataFrame ze zrobionymi trasami
#
# Usuwa wszystkie trasy, które mają punkt startowy w nieznanym mieście
# Zwraca DataFrame
###################
def usun_trasy_z_nieznanego_miasta(available, completed):
    completed_all = fp.completed_wyciagnij_wszystkie_punkty(completed)
    available = available.merge(
        completed_all[["city"]].rename(columns={'city' : 'city_from'}),
        on=["city_from"],
        how="left",
        indicator=True
    ).query('_merge == "both"').drop(columns="_merge").drop_duplicates(subset = ["company_from", "city_from", "company_to", "city_to", "cargo"])
    return available

###################
# available - DataFrame z dostępnymi trasami
# completed - DataFrame ze zrobionymi trasami
#
# Usuwa wszystkie trasy, które mają punkt końcowy w znanym mieście
# Zwraca DataFrame
###################
def usun_trasy_do_znanego_miasta(available, completed):
    completed_all = fp.completed_wyciagnij_wszystkie_punkty(completed)
    available = available.merge(
        completed_all[["city"]].rename(columns={'city' : 'city_to'}),
        on=["city_to"],
        how="left",
        indicator=True
    ).query('_merge == "left_only"').drop(columns="_merge").drop_duplicates(subset = ["company_from", "city_from", "company_to", "city_to", "cargo"])
    return available

###################
# r - DataFrame z danymi do przygotowania
###################
def przygotuj_opis_trasy(r,game_time):
    t = "job_offer_data : " + r["job_ID"] + " {\n"
    t = t + " target: \"" + r["company_to"] + "." + r["city_to"] + "\"\n"
    t = t + " expiration_time: " + str(game_time + 10000) + "\n"
    t = t + " urgency: " + str(r["urgency"]) + "\n"
    t = t + " shortest_distance_km: " + str(r["shortest_distance_km"]) + "\n"
    t = t + " ferry_time: " + str(r["ferry_time"]) + "\n"
    t = t + " ferry_price: " + str(r["ferry_price"]) + "\n"
    t = t + " cargo: cargo." + r["cargo"] + "\n"
    t = t + " company_truck: " + r["company_truck"] + "\n"
    t = t + " trailer_variant: " + r["trailer_variant"] + "\n"
    t = t + " trailer_definition: " + r["trailer_definition"] + "\n"
    t = t + " units_count: " + str(r["units_count"]) + "\n"
    t = t + " fill_ratio: " + str(r["fill_ratio"]) + "\n"
    t = t + " trailer_place: " + str(r["trailer_place"]) + "\n}\n"
    return t

###################
# naglowek
# job_ID
# opis
# save_file
###################
def uzupelnij_plik_o_trase(naglowek,job_ID,opis,save_file,game_time,WINDOWS_SAVE_FILE):
    with open(save_file) as f:
        text = f.read()
    game_time_file = int(re.search(r'game_time: (\d+)',text).group(1))
    if game_time_file == game_time:
        # znaleziona trasa w aktualnym pliku, modyfikuję expiration_time
        ind = text.find("job_offer_data : " + job_ID)
        ind = text.find("expiration_time:",ind+1)
        ind = text.find(" ",ind+1)
        ind2 = text.find("\n",ind+1)
        text = text[:ind+1] + str(game_time + 15000) + text[ind2:]
        print("znaleziona trasa w aktualnym pliku")
    elif text.find(job_ID) > -1:
        # w najnowszym pliku jest już takie job_ID
        print("jest konflikt job_ID z najnowszym plikiem save - coś trzeba zrobić")
        return
    else:
        # dodaje trase do pliku
        print("nie ma, trzeba dodać trasę do pliku")
        ind = text.find(naglowek)
        ind = text.find("job_offer:",ind+1)
        ind = text.find(" ",ind+1)
        ind2 = text.find("\n", ind + 1)
        ilosc = int(text[ind:ind2])+1
        text = text[:ind+1] + str(ilosc) + text[ind2:]
        ind = text.find("cargo",ind)
        text = text[:ind] + "job_offer[" + str(ilosc-1) + "]: " + job_ID + "\n " + text[ind:]
        ind = text.find("}",ind)
        for _ in list(range(ilosc-1)):
            ind = text.find("}", ind+1)
        ind = ind + 3
        text = text[:ind] + opis + "\n" + text[ind:]
    with open("tmp2.csv", "w") as f:
        f.write(text)
    ### TODO
    dest = shutil.copyfile("tmp2.csv",WINDOWS_SAVE_FILE)
    # skopiować plik wynikowy do katalogu z save-ami
