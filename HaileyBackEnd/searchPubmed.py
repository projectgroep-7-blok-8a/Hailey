# -*- coding: UTF-8 -*-
#Author: Sanne Schroduer
#Date: 3-6-2019
#Funcionality: This part of the application connects to PubMed and extracts and saves all the Bitter Gourd related articles.

from Bio import Entrez
from Bio import Medline
import json

def get_names():
    """This function reads all the Bitter Gourd related terms in the names.txt file,
    and saves the names in a list.

    :return: names_list: a list of all the names
    """
    names_list = []
    terms = open("names.txt", "r")
    lines = terms.readlines()

    for line in lines:
        names_list.append(line.strip())
    return names_list

def get_bg_articles(names_list):
    """This function loops through the variable names_list.
    Per name, it calls the search_PM function, which extracts all the PubMed ID's per name in a list.
    For all the ID's in the list, de Medline information is extracted and saved in a dictionary.
    The following information is saved per article: PMID, Publication date, title, abstract, hyperlink to the article
    :param names_list: a list of all the names
    """
    all_pm_records = {}

    for name in names_list:
        print(name)
        pm_ids = search_PM(name)
        Entrez.email = "s.schroduer@hotmail,com"
        handle = Entrez.efetch(db="pubmed", id=pm_ids, rettype="medline", retmode="text")
        records = Medline.parse(handle)

        records = list(records)
        all_pm_records[name] = records
    bg_articles = {}

    for name, record in all_pm_records.items():
        for article in record:
            if 'PMID' in article.keys() and 'TI' in article.keys():
                pm_id = article['PMID']
                link = "https://www.ncbi.nlm.nih.gov/pubmed/?term="+pm_id
                if 'AB' in article.keys():
                    bg_articles[name+"-"+article['PMID']] = [article['DP'], article['TI'], article['AB'], link]

                else:
                    bg_articles[name+"-"+article['PMID']] = [article['DP'], article['TI'], "No abstract found", link]

    #saves all the articles in the result dictionary, without duplicates
    result = {}
    for key, value in bg_articles.items():
        if value not in result.values():
            result[key] = value

    with open("bg_articles.json", 'w') as outfile:
        json.dump(result, outfile, indent=4)


def search_PM(search_term):
    """This function is called from get_bg_articles.
    It executes a search on PubMed for each bitter gourd term, and saves all the PubMed ID's in a list.
    :param: search_term: a string of a bitter gourd term
    :return: pm_ids: a list of all the ID's belonging to one bitter gourd term.
    """
    Entrez.email = "s.schroder@hotmail.com"
    handle = Entrez.esearch(db="pubmed", term='\"'+search_term+'\"', retmax=1000000)
    record = Entrez.read(handle)
    handle.close()
    pm_ids = record["IdList"]

    return pm_ids

