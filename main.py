import os
from pathlib import Path

import pliki_scs
import pliki_save

def main():
    WINDOWS_SAVE_FILE = Path(r"C:\Users\wlady\OneDrive\Dokumenty\Euro Truck Simulator 2\profiles\7661647A696572\save\quicksave\game.sii")

    MAIN_DIR = Path('.')
    GAME_DATA = MAIN_DIR / "game_data"
    SAVE_FILES_DIR = GAME_DATA / "save_files"

    SAVE_FILE_BEGIN = "save_"
    SAVE_FILE_END = ".sii"
    GAME_TIME_FILE = GAME_DATA / "game_time.txt"
    COMPANY_POINTS_FILE = GAME_DATA / "company_points.csv"
    COMPLETED_FILE = GAME_DATA / "completed_routes.csv"
    CITY_COMPLETION_FILE = GAME_DATA / "city_completion.csv"

    with open(GAME_TIME_FILE) as f:
        game_time = int(f.read())

    ##################
    # dekodowanie nowego pliku save
    ##################
    game_time_new = pliki_save.kopiuj_i_dekoduj_plik_save(WINDOWS_SAVE_FILE,SAVE_FILES_DIR,SAVE_FILE_BEGIN,SAVE_FILE_END)
    ##################
    # aktualizacja game_time
    ##################
    if game_time_new > game_time:
        game_time = game_time_new
        with open(GAME_TIME_FILE,"w") as f:
            f.write(str(game_time))

    SAVE_FILE = SAVE_FILES_DIR / (SAVE_FILE_BEGIN + str(game_time) + SAVE_FILE_END)

    ##################
    ## obsługa plików save
    ##################
    ## aktualizacja dostępnych punktów na mapie
    ##################
    pliki_save.lista_company_points(SAVE_FILE,COMPANY_POINTS_FILE)
    ##################
    ## aktualizacja dostępnych punktów na mapie
    ##################
    pliki_save.aktualizuj_completed_routes(SAVE_FILE,COMPLETED_FILE)
    ##################
    ## aktualizacja wykonania miast
    ##################
    pliki_save.aktualizuj_city_completion(COMPANY_POINTS_FILE,COMPLETED_FILE,CITY_COMPLETION_FILE)

if __name__ == "__main__":
    main()