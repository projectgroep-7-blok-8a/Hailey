# -*- coding: UTF-8 -*-
#Author: Sanne Schroduer
#Date: 3-6-2019
#Funcionality: This part of the application executes the textmining by searching for co-occurence in the title & abstract of the extraced articles.


import json
import re


def get_diseases():
    """This function reads the diseases.txt file,
    and saves all the diseases in a list.

    :return: diseases_list: a list of all the diseases
    """
    diseases_list = []
    diseases = open("diseases.txt", "r")
    lines = diseases.readlines()

    for line in lines:
        diseases_list.append(line.strip())
    return diseases_list

def get_compounds():
    """This function reads the compounds.txt file,
    and ssaves alle the compounds in a list.

    :return: compounds_list: a list of all the compounds
    """
    compound_list = []
    compounds = open("compounds.txt", "r")
    lines = compounds.readlines()

    for line in lines:
        compound_list.append(line.strip())
    return compound_list


def find_co_occurrence(diseases, compounds):
    """This function searches for co-occurrence in the title & abstract of the extracted articles.
    With the use of for-loops, for every disease-compound combination is determined
    if this co-occcurrence is found in one of the extracted articles.
    When a co-occurrernce is found, a score is assigned to the article, and the article is saved in a dictionary.
    :param diseases: a list of all the diseases of interest
    :param compounds: a list of all the compounds of interest

    Output: the output of this function is two JSON files that are saved:
    - icicle.json: containing all the co-occurrences, with only the amount of times this co-occurrence was found.
    This file is used for the visualisation in JavaScript.
    - 2raw_text_mining_results.json: in this file, the dictionary is saved.
    This file is used for extracting the results in the application_result.html.
    """
    text_mining_results = {}
    icicle_results = {}

    with open("bg_articles.json") as json_file:
        articles = json.load(json_file)

    for disease in diseases:
        count_per_disease = {}
        regex_d = "[ ]"+disease+"[ s.,:;]"
        compound_results = {}

        for compound in compounds:
            regex_c = "[ ]"+compound+"[ .,:;]"
            compound_data = []

            for key, value in articles.items():
                title = value[1].lower()
                abstract = value[2].lower()
                score = 0

                if re.search(regex_d, title) and re.search(regex_c, title):
                    score += 10
                if re.search(regex_d, abstract) and re.search(regex_c, abstract):
                    score += 5
                if re.search(regex_d, title) and re.search(regex_c, abstract):
                    score += 4
                if re.search(regex_d, abstract) and re.search(regex_c, title):
                    score += 4
                elif score > 0:
                    compound_data.append([value[0], value[1], score, value[3]])
                    compound_results[compound] = compound_data

                number_of_results = len(compound_data)
                if number_of_results> 0:
                    count_per_disease[compound] = number_of_results

        text_mining_results[disease] = compound_results
        icicle_results[disease] = count_per_disease

    final_icicle_results ={}
    final_icicle_results["Bitter Gourd"] = icicle_results

    with open("text_mining_results.json", 'w') as outfile:      #file used for displaying the articles in the application_result.html
        json.dump(text_mining_results, outfile, indent=4)

    with open("icicle_results.json", 'w') as outfile:           #file used for the visualisation in JS
        json.dump(final_icicle_results, outfile, indent=4)


