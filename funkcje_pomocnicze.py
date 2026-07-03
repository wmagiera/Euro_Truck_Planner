import pandas as pd

def completed_wyciagnij_wszystkie_punkty(completed):
    completed_from = completed[['company_from', 'city_from']].rename(columns={'company_from' : 'company',
                                                                              'city_from' : 'city'})
    completed_to = completed[['company_to', 'city_to']].rename(columns={'company_to' : 'company',
                                                                        'city_to' : 'city'})
    completed_all = pd.concat([completed_to, completed_from]).drop_duplicates()
    return completed_all
