import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://store.steampowered.com/search/?term=gta'

def get_data(url):
    r = requests.get(url)
    return r.text

# processing data
def parser(data):
    result = []
    soup = BeautifulSoup(data, 'html.parser')
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass
    contents = soup.find('div', attrs={'id':'search_resultsRows'})
    games = contents.find_all('a')

    for game in games:
        link = game['href']
    

        # parsing data
        title = game.find('span', {'class':'title'}).text.strip().split('€')[0]
        price = game.find('div', {'class':'search_price'}).text.strip().split('€')[0]
        release = game.find('div', {'class':'search_released'}).text.strip().split('€')[0]

        if release == '':
            release = 'None'

        # sorting data
        data_dict = {
            'title':title,
            'price':price,
            'link':link,
            'realese':release,
        }

        # append
        result.append(data_dict)
    return result
# PROCESS CLEANED DATA FROM PARSER
def output(datas : list):
    for i in datas :
        print(i)

def generate_output_file(filename: str, extension: str, directory: str = 'output'):
    file = "%s.%s"%(filename, extension)
    print("file : %s"%(file))

    cwd = os.getcwd()
    print("cwd : %s"%(cwd))

    dir = os.path.join(cwd,directory)
    print("dir : %s"%(dir))

    is_directory_exist = os.path.exists(dir)

    if not is_directory_exist:
        os.mkdir(dir)

    path = os.path.join(cwd,directory,file)
    print(path)

    with open(path, 'a') as file:
        return file
    
def generate_data(result, filename):
    directory, csv, excel = 'output', 'csv', 'xlsx' 

    # generating csv and excel files
    generate_output_file(filename, csv, directory)
    generate_output_file(filename, excel, directory)

    generate_filename = lambda file: os.path.join(os.getcwd(), directory, file)

    csv_filepath = generate_filename("%s.%s"%(filename,csv))
    excel_filepath = generate_filename("%s.%s"%(filename,excel)) 
    
    try:
        df = pd.DataFrame(result)
        df.to_excel(excel_filepath)
        df.to_csv(csv_filepath, mode="a")
    except:
        raise
    finally:
        print(f"""
        Successfully write documents, you can find the results \n  
        csv: {csv_filepath}
        excel: {excel_filepath}
        """)

if __name__ == '__main__':
    data = get_data(url)
    final_data =  parser(data)
    filename = input("Specify your filename output: ")
    generate_data(final_data,filename)