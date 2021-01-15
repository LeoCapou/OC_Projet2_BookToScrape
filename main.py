import requests, time, sys
from bs4 import BeautifulSoup
import csv
import urllib.request
import os
import lxml
from fonctions import *


def main():

    response = requests.get("https://books.toscrape.com/index.html")

    if not response.ok:
        # Quitte le programme si erreur impossible
        sys.exit("Probleme acces au site Book to Scrape")

    # Creation repertoire contenant les CSV
    try:
        os.mkdir("CSV")
        print("Repertoire CSV cree")
    except FileExistsError:
        print("Repertoire CSV existe deja")

    # Creation repertoire contenant les Images
    try:
        os.mkdir("Images")
        print("Repertoire IMAGES cree")
    except FileExistsError:
        print("Repertoire IMAGES existe deja")

    # parcours toutes les categories
    soup = BeautifulSoup(response.content, "lxml")
    nav_list = soup.find("ul", {"class": "nav nav-list"})
    category_list = nav_list.find("ul")

    l = len(category_list.find_all("a"))  # progression

    for category in category_list.find_all("a"):
        category_title = category.text
        category_title = category_title.strip()
        category_link = "https://books.toscrape.com/" + category["href"]

        print(category_title)

        # export csv
        titre_csv = category_title.replace(" ", "_") + ".csv"
        with open("./CSV/" + titre_csv, "w") as f:
            fnames = [
                "product_page_url",
                "upc",
                "title",
                "price_including_tax",
                "price_excluding_tax",
                "number_available",
                "product_description",
                "category",
                "review_rating",
                "image_url",
            ]
            writer = csv.DictWriter(f, fieldnames=fnames)
            writer.writeheader()

            # parcours livres de la categorie
            for livre in categorie_extraction(category_link):
                infos_livre = page_produit(livre)
                writer.writerow(
                    {
                        "product_page_url": str(infos_livre["url_produit"]),
                        "upc": str(infos_livre["upc"]),
                        "title": str(infos_livre["titre"]),
                        "price_including_tax": str(infos_livre["prixTTC"]),
                        "price_excluding_tax": str(infos_livre["prixHT"]),
                        "number_available": str(infos_livre["disponibilite"]),
                        "category": category_title,
                        "review_rating": str(infos_livre["notation"]),
                        "image_url": str(infos_livre["image_url"]),
                        "product_description": str(
                            infos_livre["description"]
                        ).encode("ascii", "ignore"),
                    }
                )

                # telechargement image livre
                nom_image = str(page_produit(livre)["titre"]) + ".jpg"
                nom_image = re.sub(r'[\\\\/*?:"<>|]', "", nom_image)
                urllib.request.urlretrieve(
                    str(page_produit(livre)["image_url"]), "./Images/" + nom_image
                )


if __name__ == "__main__":
    main()
