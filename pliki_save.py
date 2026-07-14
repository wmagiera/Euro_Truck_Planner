import re
import shutil
import subprocess
import pandas as pd

import funkcje_pomocnicze as fp

###################
# TODO
# origin_save_file - nazwa pliku save
# destination - katalog do trzymania plików save
# file_name_begin - jak ma wyglądać początek pliku wynikowego
# file_name_end - jak ma wyglądać koniec pliku wynikowego
#
# Kopiuje zakodowany plik save z origin do destination
# Dekoduje plik
# Wyszukuje w pliku game_time
# Zmienia nazwę pliku na file_name_begin + game_time + file_name_end
# Zwraca game_time (w main uzupełnić, że aktualizuje plik game_time.txt)
###################
def kopiuj_i_dekoduj_plik_save(origin_save_file,destination,file_name_begin,file_name_end,decrypt_file,tmp_save_file):
    subprocess.run(
        [
            str(decrypt_file),
            str(origin_save_file),
            str(tmp_save_file)
        ],
        check=True
    )
    with open(tmp_save_file) as f:
        text = f.read()
    game_time = int(re.search(r'game_time: (\d+)',text).group(1))
    game_time_file = destination / (file_name_begin + str(game_time) + file_name_end)
    dest = shutil.copyfile(tmp_save_file,game_time_file)
    tmp_save_file.unlink()
    return game_time

###################
# save_file - plik save, z którego mam pobrać listę punktów
# destination - plik do którego mam zapisać punkty
#
# Zawartość destination:
# company,city
# medas,argostoli
###################
def lista_company_points(save_file,destination):
    with open(save_file) as f:
        text = f.read()
    points = re.findall(r'companies\[\d+]: company\.volatile\.(.+)\.(.+)',text)
    points_df = pd.DataFrame(points,columns=["company","city"])
    points_df.to_csv(destination, index=False)

###################
# save_file - plik save, z którego mam pobrać zrobione trasy
# completed_file - plik ze zrobionymi trasami do uzupelnienia
#
# Do pliku completed_file dopisuje na końcu nowo zrobione trasy.
# Wartość trailer ustawia na '???'
###################
def aktualizuj_completed_routes(save_file,completed_file):
    with open(save_file) as f:
        text = f.read()
    routes = re.findall(r'delivery_log_entry.*\{([\s\S]*?)}',text)
    completed = []
    for route in routes:
        data_from = re.search(r'params\[1]: \"company.volatile\.(.+)\.(.+)\"',route)
        if not data_from:
            continue
        data_to = re.search(r'params\[2]: \"company.volatile\.(.+)\.(.+)\"',route)
        cargo = re.search(r'params\[3]: \"cargo\.(.+)\"',route)
        distance = int(re.search(r'params\[4]: (.+)',route).group(1))
        completed.append({
            "company_from": data_from.group(1),
            "city_from": data_from.group(2),
            "company_to": data_to.group(1),
            "city_to": data_to.group(2),
            "distance": distance,
            "cargo": cargo.group(1),
            "trailer": '???'
        })
    completed_df = pd.DataFrame(completed)
    completed_old = pd.read_csv(completed_file)
    for ind,row in completed_old.iterrows():
        if not (
            completed_df.loc[ind,'company_from'] == row['company_from'] and
            completed_df.loc[ind,'company_to'] == row['company_to']
        ):
            print('Błąd w plikach completed_routes')
            break
        completed_df.loc[ind,'trailer'] = row['trailer']
    completed_df.to_csv(completed_file, index=False)

###################
# company_points_file
# completed_routes_file
# city_completion_file
#
# Tworzy plik, dla każdego miasta jest podane ile punktów obsłużono i ile zostało do obsłużenia
# city,visited,unvisited
# wroclaw,4,0
###################
def aktualizuj_city_completion(company_points_file, completed_routes_file, city_completion_file):
    points = pd.read_csv(company_points_file)
    completed = pd.read_csv(completed_routes_file)

    points_grouped = points.groupby('city').count().rename(columns={'company' : 'all_points'})
    #completed_from = completed[['company_from', 'city_from']].rename(columns={'company_from' : 'company',
    #                                                                          'city_from' : 'city'})
    #completed_to = completed[['company_to', 'city_to']].rename(columns={'company_to' : 'company',
    #                                                                    'city_to' : 'city'})
    #completed_all = pd.concat([completed_to, completed_from]).drop_duplicates()
    completed_all = fp.completed_wyciagnij_wszystkie_punkty(completed)
    completed_grouped = completed_all.groupby('city').count().rename(columns={'company' : 'visited'})
    city_completion = pd.merge(points_grouped,completed_grouped,on='city',how='left').fillna(0)
    # merge tworzy dane float gdy jest NaN, więc zamieniam na int
    city_completion['visited'] = city_completion['visited'].astype(int)
    city_completion['unvisited'] = city_completion['all_points'] - city_completion['visited']
    city_completion = city_completion.drop(['all_points'],axis=1)
    city_completion.to_csv(city_completion_file)

###################
# save_file
# available_file
#
# Wyciąga z save_file dane o wszystkich dostępnych trasach
###################
def available_z_pliku_save_do_pliku(save_file,available_file):
    with open(save_file) as f:
        text = f.read()
    game_time = int(re.search(r'game_time: (\d+)',text).group(1))
    companies_text = re.findall(r'company : company.volatile.([\s\S]*?)}',text)
    companies = []
    for c in companies_text:
        company, city = re.search(r'(^.*)\.(.*) \{[\s\S]*',c).groups()
        jobs = re.findall(r'job_offer\[.*',c)
        for j in jobs:
            companies.append({"game_time": game_time,
                              "job_ID" : j.split(" ")[1],
                              "company_from": company,
                              "city_from" : city
            })
    companies_df = pd.DataFrame(companies)
    jobs_text = re.findall(r'job_offer_data : ([\s\S]*?)}',text)
    jobs = []
    for j in jobs_text:
        job_ID = re.search(r'(.*?) ',j).group(1)
        shortest_distance_km = int(re.search(r'shortest_distance_km: (.*)',j).group(1))
        if shortest_distance_km > 1:
            company, city = re.search(r'target: "(.*?)\.(.*?)"',j).groups()
            jobs.append({"job_ID": job_ID,
                         "company_to": company,
                         "city_to": city,
                         "urgency": int(re.search(r'urgency: (.*)',j).group(1)),
                         "shortest_distance_km": shortest_distance_km,
                         "ferry_time": int(re.search(r'ferry_time: (.*)',j).group(1)),
                         "ferry_price": int(re.search(r'ferry_price: (.*)',j).group(1)),
                         "cargo": re.search(r'cargo: cargo\.(.*)',j).group(1),
                         "company_truck": re.search(r'company_truck: (.*)',j).group(1),
                         "trailer_variant": re.search(r'trailer_variant: (.*)',j).group(1),
                         "trailer_definition": re.search(r'trailer_definition: (.*)',j).group(1),
                         "units_count": int(re.search(r'units_count: (.*)',j).group(1)),
                         "fill_ratio": int(re.search(r'fill_ratio: (.*)',j).group(1)),
                         "trailer_place": re.search(r'trailer_place: (.*)',j).group(1)
            })
    jobs_df = pd.DataFrame(jobs)
    available = pd.merge(companies_df, jobs_df, on='job_ID', how='right')
    available.to_csv(available_file,index=False)
    print(available_file)
