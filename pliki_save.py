import re
import pandas as pd

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
def kopiuj_i_dekoduj_plik_save(origin_save_file,destination,file_name_begin,file_name_end):
    return 0

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
    completed_from = completed[['company_from', 'city_from']].rename(columns={'company_from' : 'company',
                                                                              'city_from' : 'city'})
    completed_to = completed[['company_to', 'city_to']].rename(columns={'company_to' : 'company',
                                                                        'city_to' : 'city'})
    completed_all = pd.concat([completed_to, completed_from]).drop_duplicates()
    completed_grouped = completed_all.groupby('city').count().rename(columns={'company' : 'visited'})
    city_completion = pd.merge(points_grouped,completed_grouped,on='city',how='left').fillna(0)
    # merge tworzy dane float gdy jest NaN, więc zamieniam na int
    city_completion['visited'] = city_completion['visited'].astype(int)
    city_completion['unvisited'] = city_completion['all_points'] - city_completion['visited']
    city_completion = city_completion.drop(['all_points'],axis=1)
    print(city_completion)
    city_completion.to_csv(city_completion_file)

