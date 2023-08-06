from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
from selenium import webdriver
from time import sleep


class Scraper():
    '''This class creates the scraper used to scrape the webpage'''
    def __init__(self, URL: str):
        self.URL = URL
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get(URL)

    def accept_cookies(self):
        accept_cookies = self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/button[1]') 
        accept_cookies.click()

    def get_links(xpath:str) -> list:
        '''This method finds all the links leading to pages that will be individually scraped,
        since they contain all the data about each attack'''
        container=driver.find_elements_by_xpath(xpath)
        attack_links=[]
        for item in container:
            attack_link= item.find_element_by_tag_name('a').get_attribute('href')
            attack_links.append(attack_link)


    def create_dictionary(dict_attacks: dict) -> dict:
        '''This method creates a dictionary where scraped data about each attack will be added.
        The dictionary is populated with data from each link obtained through the method get_links.
        Multiple features of each attack are added (eg Title, Date etc).
        None is appended where a specific category of data, 
        corresponding to one of the dictionary keys, is missing.
        The method returns the resulting dictionary'''
        dict_attacks={'Title': [], 'Date': [], 'Affiliation': [], 'Description': [], 'Suspected Victims':[], 'Suspected State Sponsor':[], 'Type Of Incident': [], 'Target Category':[], 'Victim Government Reaction': [] }
        for attack_link in attack_links:
            driver.get(attack_link)
            sleep(5)
            try:
                title=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[2]/div/div[1]/div/div[1]').text
                dict_attacks['Title'].append(title)
            except:
                dict_attacks['Title'].append(None)
            try:
                date=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[3]/div/div/div/div/div[1]/div/ul/li').text
                dict_attacks['Date'].append(date)
            except:
                dict_attacks['Date'].append(None)
            try:
                affiliation=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/ul/li/a').text
                dict_attacks['Affiliation'].append(affiliation)
            except:
                dict_attacks['Affiliation'].append(None)
            try:
                description=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[4]/div/div/div/div/div/div').text
                dict_attacks['Description'].append(description)
            except:
                dict_attacks['Description'].append(None)
            try:
                suspected_victims=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[5]/div/div/div/div[2]/div/div/div/ul/li').text
                dict_attacks['Suspected Victims'].append(suspected_victims)
            except:
                dict_attacks['Suspected Victims'].append(None)
            try:
                suspected_state_sponsor=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[6]/div/div/div/div/div[1]/div/ul/li').text
                dict_attacks['Suspected State Sponsor'].append(suspected_state_sponsor)
            except:
                dict_attacks['Suspected State Sponsor'].append(None)
            try:
                type_of_incident=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[6]/div/div/div/div/div[2]/div/ul/li').text
                dict_attacks['Type Of Incident'].append(type_of_incident)
            except:
                dict_attacks['Type Of Incident'].append(None)
            try:
                target_category=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[6]/div/div/div/div/div[3]/div/ul/li').text
                dict_attacks['Target Category'].append(target_category)
            except:
                dict_attacks['Target Category'].append(None)
            try:
                victim_government_reaction=driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/section/div[2]/div/div/div[7]/div/div/div/div/div/div/ul/li').text
                dict_attacks['Victim Government Reaction'].append(victim_government_reaction)
            except:
                dict_attacks['Victim Government Reaction'].append(None)
        return dict_attacks


    def get_csv_from_dict(dict_attacks) -> pd.DataFrame:
        '''This method takes the dictionary obtained through the method create_dictionary and 
        converts it into a dataframe. A csv file containing the data is then generated from the dataframe'''
        df_attacks=pd.DataFrame.from_dict(dict_attacks)
        df_attacks.to_csv('csv_attacks')
        return df_attacks