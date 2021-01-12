import requests, re
from bs4 import BeautifulSoup

# exctraction infos d un livre 
def page_produit(url):
    """
    Extrait toutes les infos d'un livre à partir de l'url de sa page produit
    @parametres:
        url : url de la page produit
    """    

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

        soup = BeautifulSoup(response.content, 'lxml', from_encoding="utf-8")

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
        ctx['description'] = description.replace("\u203d","").replace("\u2028","").replace("\ufb01","").replace("\ufb02","").replace("\ufeff","").replace("\u2015","")

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
    """
    Extrait toutes les url page produit pour chaque livre de la categorie
    @parametres:
        url : url de la page categorie
    """        

    ctx = [] # liste liens livres
    
    response = requests.get(url)

    if response.ok:

        soup = BeautifulSoup(response.content, 'lxml', from_encoding="utf-8")

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