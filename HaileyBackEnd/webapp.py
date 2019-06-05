# -*- coding: utf-8 -*-
#Author: Sanne Schroduer
#Date: 3-6-2019
#Funcionality: This application extracts Bitter Gourd-related articles from PubmMed,
# and searches for the co-occurence of a disease and a compound in these articles.


from searchPubmed import get_names, get_bg_articles
from textminer import get_diseases, get_compounds, find_co_occurrence


def main():
    """This function calls all the functions of the searchPubmed module and textminer module.

    Note: the output of get_bg_articles and find_co_occurrence are JSON files that will be saved.
    Because of that, there are no return statements present in these functions.
    """
    names_list = get_names()
    get_bg_articles(names_list)
    diseases_list = get_diseases()
    compounds_list = get_compounds()
    find_co_occurrence(diseases_list, compounds_list)

main()
