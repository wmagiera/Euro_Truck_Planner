
###################
# file_name to pełna ścieżka do pliku
# destination to katalog gdzie mają pojawić się rozpakowane elementy
# catalogs to lista z nazwami katalogów, które chcę zachować, pozostałe usuwamy
#
# Tworzy katalog destination/"tmp"
# Rozpakowuje do niego plik scs
# Kopiuje zawartość katalogów z catalogs z destination/"tmp" do destination
# Usuwa katalog destination/"tmp"
###################
def rozpakuj_plik_scs(file_name,destination,catalogs):
    pass

###################
# directory to katalog z plikami scs
# avoid to lista nazw plikow scs, które nie mają być analizowane
# destination to katalog gdzie mają pojawić się rozpakowane elementy
# catalogs to lista z nazwami katalogów, które chcę zachować, pozostałe usuwamy
#
# Tworzy katalogi z listy catalogs w katalogu directory
# Dla każdego pliku scs w katalogu directory sprawdza, czy jego nazwa nie jest na liście avoid
# Jeżeli nie, wywołuje dla niego rozpakuj_plik_scs()
###################
def rozpakuj_pliki_scs(directory,aviod,destination,catalogs):
    pass

###################
# file_name wynikowy plik csv (pełna ścieżka) z zawartością (osobny wpis dla każdej pary cargo,body_type):
# cargo,body_type
# acetylene,container
# acetylene,flatbed_cont
# acid,chemtank
###################
def przygotuj_cargo_list(file_name):
    pass

###################
# file_name wynikowy plik csv (pełna ścieżka) z zawartością (osobny wpis dla każdej pary cargo,body_type):
# company,cargo,direction,body_types
# aaa,motorcycles,in,curtainside
# aaa,motorcycles,out,curtainside
# aaa,motorcycles,in,dryvan
# aaa,motorcycles,out,dryvan
###################
def przygotuj_company_cargo_io(file_name):
    pass