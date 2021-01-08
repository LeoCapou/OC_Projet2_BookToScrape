
import requests, re, time
from bs4 import BeautifulSoup
import csv
import urllib.request
import os
import lxml
import cchardet
import cProfile


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

# exctraction infos d un livre 
def page_produit(url):

    ctx = {
        'upc' : None,
        'prixHT' : None,
        'prixTTC' : None,
        'disponibilite' : None,
        'titre' : None,
        'description' : None,
        'image_url' : None,
        'notation' : None,
        'url_produit' : None,
    }

    response = requests.get(url)

    if response.ok:

        ctx['url_produit'] = url

        soup = BeautifulSoup(response.content, 'lxml')

        # UPC
        tab = soup.find_all('td')
        ctx['upc'] = tab[0].text

        # Prix HT
        ctx['prixHT'] = tab[2].text

        # Prix TTC
        ctx['prixTTC'] = tab[3].text

        # Disponibilite
        availability = tab[5].text
        nb = re.findall(r'\d+', availability)
        ctx['disponibilite'] = int(nb[0]) # exctraction nombre

        # Titre
        ctx['titre'] = (soup.find('h1')).text

        # Description
        description = soup.find_all('p')
        description = description[3].text
        ctx['description'] = description.replace("\u203d","").replace("\u2028","").replace("\ufb01","").replace("\ufb02","")

        # Image url
        image = soup.find_all('img')
        image_url = image[0].get('src')
        ctx['image_url'] = image_url.replace("../../","https://books.toscrape.com/")

        # Notation
        element = soup.find('div',{'class':"col-sm-6 product_main"})
        if element.find('p',{'class':"star-rating Zero"}):
            rating = 0
        elif element.find('p',{'class':"star-rating One"}):
            rating = 1
        elif element.find('p',{'class':"star-rating Two"}):
            rating = 2
        elif element.find('p',{'class':"star-rating Three"}):
            rating = 3
        elif element.find('p',{'class':"star-rating Four"}):
            rating = 4
        elif element.find('p',{'class':"star-rating Five"}):
            rating = 5

        ctx['notation'] = rating     
        
        return(ctx)        

    else:

        print("Page livre Fail")

# exctraction tous les livres d une categorie 
def categorie_extraction(url):

    ctx = [] # liste liens livres
    
    response = requests.get(url)

    if response.ok:

        soup = BeautifulSoup(response.content, 'lxml')

        for product_pod in soup.findAll('article',{'class':"product_pod"}):
            ctx.append( str(product_pod.findAll('a')[1]['href']).replace("../../../","https://books.toscrape.com/catalogue/") ) # lien livre

        # plusieurs pages dans categorie
        i = 2
        url_page_suivante = url.replace('index','page-2') 
        while requests.get(url_page_suivante).ok :

            response = requests.get(url_page_suivante)
            soup = BeautifulSoup(response.content, 'lxml')

            for product_pod in soup.findAll('article',{'class':"product_pod"}):
                ctx.append( str(product_pod.findAll('a')[1]['href']).replace("../../../","https://books.toscrape.com/catalogue/") ) # lien livre

            i += 1
            page = "page-" + str(i)
            url_page_suivante = url.replace('index', page)

    else:

        print("Page catégorie Fail")

    return(ctx)    

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
 
            time.sleep(0.1)
            # Update Progress Bar
            printProgressBar(i + 1, l, prefix = category_title, suffix = 'Complete', length = 50)
            i += 1

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
    cProfile.run('main()')
