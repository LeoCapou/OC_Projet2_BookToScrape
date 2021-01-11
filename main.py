
import requests, time
from bs4 import BeautifulSoup
import csv
import urllib.request
import os
import lxml
from fonctions import *


def main():

    response = requests.get('https://books.toscrape.com/index.html')

    if response.ok:

        # Creation repertoire contenant les CSV
        try:
            os.mkdir('CSV')
            print("Repertoire CSV cree") 
        except FileExistsError:
            print("Repertoire CSV existe deja")

        # Creation repertoire contenant les Images
        try:
            os.mkdir('Images')
            print("Repertoire IMAGES cree") 
        except FileExistsError:
            print("Repertoire IMAGES existe deja")      

        # parcours toutes les categories
        soup = BeautifulSoup(response.content, 'lxml')
        nav_list = soup.find('ul',{'class':"nav nav-list"})
        category_list = nav_list.find('ul')

        l = len(category_list.find_all('a')) #progression

        i = 0
     
        for category in category_list.find_all('a'):
            category_title = category.text
            category_title = category_title.strip()
            category_link = "https://books.toscrape.com/" + category['href']

            print(category_title)
 
            #export csv
            titre_csv = category_title.replace(" ","_") + ".csv"
            f = open("./CSV/"+titre_csv, 'w')
            with f:           
                fnames = ['product_page_url','upc','title','price_including_tax','price_excluding_tax','number_available','product_description','category','review_rating','image_url']
                writer = csv.DictWriter(f, fieldnames=fnames)    
                writer.writeheader()  
                                      
                # parcours livres de la categorie
                for livre in categorie_extraction(category_link):
                    writer.writerow({'product_page_url' : str(page_produit(livre)['url_produit']),
                                    'upc': str(page_produit(livre)['upc']),
                                    'title': str(page_produit(livre)['titre']),
                                    'price_including_tax': str(page_produit(livre)['prixTTC']),
                                    'price_excluding_tax': str(page_produit(livre)['prixHT']),
                                    'number_available': str(page_produit(livre)['disponibilite']),                                  
                                    'category': category_title,
                                    'review_rating': str(page_produit(livre)['notation']),
                                    'image_url': str(page_produit(livre)['image_url']),
                                    'product_description': str(page_produit(livre)['description']),})

                    #telechargement image livre    
                    nom_image = str(page_produit(livre)['titre']).replace(":"," ").replace("/"," ").replace('\\'," ").replace('"'," ") + ".jpg"            
                    urllib.request.urlretrieve(str(page_produit(livre)['image_url']),"./Images/"+nom_image )                 

    else :
        print("Probleme de connexion au site")

if __name__ == "__main__":
    main()
