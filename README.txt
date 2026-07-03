Wczytywanie danych z plików save
Mapa połączeń (odległości) - potem

Planner A: (Z current city do nowego punktu)
# Usuń trasy z / do punktów w których już byłem
# Usuń trasy przewożące produkty z / do, które już dla danej firmy są przewiezione
Wypisz wszystkie trasy, z current city
# Po wybraniu, skopiuj do nowego pliku save_game opis trasy i podmień w katalogu z zapisami

Planner B: (Z pośród dostępnych tras znajdź najkrótszą do nowego miasta jako quick route)
# Usuń trasy z / do punktów w których już byłem
# Usuń trasy przewożące produkty z / do, które już dla danej firmy są przewiezione
Zostaw trasy ze znanego miasta do nowego miasta.
Posortuj po długości trasy.
Wybierz najkrótszą.
# Po wybraniu, skopiuj do nowego pliku save_game opis trasy i podmień w katalogu z zapisami


TODO w Polsce
Plik pliki_scs.py
1. Wczytywanie danych z plików scs
2. Tam są dane o rodzajach cargo, naczepach, co która firma akceptuje
3. Tłumaczenie naczep z tego co w plikach available na to, co w pliku company cargo io

TODO w Polsce
Plik pliki_save.py
- def kopiuj_i_dekoduj_plik_save
