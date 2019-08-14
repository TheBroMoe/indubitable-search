import requests
import bs4
from bs4 import BeautifulSoup
import webbrowser
import pandas as pd
import time
import os
from datetime import datetime
from scraper import Scraper

class Command_Line_Iterface:

    def __init__(self, url):
        # Variables
        self.base_url = url
        self.initialize_data_structure()
        self.scraper = Scraper()
        self.exit = False
        self.save_all = False
        self.save_cities = False
        self.save_page = False
        self.next_city = False
        self.next_page = False
        self.given_job_title = ""
        self.city_set = list()
        self.current_city = dict()
        self.city_result_count = 0

        self.current_date = str(datetime.today()).split()[0]


        # Constants
        self.search_increment = 20
    
    def initialize_data_structure(self):

        self.city_jobs_dict = dict()
        
        self.city_jobs_dict["title"] = list()
        self.city_jobs_dict["company"] = list()
        self.city_jobs_dict["location"] = list()
        self.city_jobs_dict["date"] = list()
        self.city_jobs_dict["summary"] = list()
        self.city_jobs_dict["url"] = list() 

    def start(self):
        '''
        Starts Main Loop
        '''
        while True:
            self.given_job_title = ""
            self.city_set = list()
            self.exit = False
            self.clear_function()
            self.display_title()

            self.get_initial_parameters()
            
            if self.exit:
                break

            self.start_job_search()

        self.save_to_csv()
        print("Happy Hunting!")
    
    def clear_function(self):
        os.system('cls||clear')

    def display_title(self):
        print("Welcome to the Indubitable Search!")
        print("Today's Date: {}".format(self.current_date))
        print("Enter X to exit program")
        print("=========================")
    
    def get_initial_parameters(self):
        self.get_job_title()

        if self.exit:
            return
        
        self.get_city_set()

    def get_job_title(self):
        print("Enter Job Title:")
        while True:
            self.given_job_title = input()
            if self.given_job_title.strip() == "":
                print("Error: Enter a Job Title")
            elif self.given_job_title.lower() == "x":
                self.exit = True
                return
            else:
                return
        
    def get_city_set(self):
        print("Enter List of Cities (Press enter to continue after): ")
        while True:
            given_city = input()
            if given_city.strip() == "":
                if len(self.city_set) > 0:
                    break
                else:
                    print("Error: Enter at least one city")
            elif given_city.lower() == "x":
                self.exit = True
                break
            else:
                self.city_set.append(given_city)

    def replace_symbols(self, given_str):
        given_str = given_str.replace(" ", "+")
        given_str = given_str.replace(",", "%2C")
        return given_str

    def start_job_search(self):
        self.save_all = False
   
        print("Extracting...")

        for city in self.city_set:
            if self.exit:
                return
            self.city_search(city)

    def city_search(self, city):
        self.save_cities = False
        self.next_city = False
        self.get_city_result_count(city)
        print("Results Found for '{}': {}".format(city, self.city_result_count))
        for page_index in range(0, self.city_result_count, self.search_increment):
            if self.exit:
                return
            self.page_search(city, page_index)
            time.sleep(1)

    def get_city_result_count(self, city):
        url = self.generate_url(city)
        soup = self.generate_soup_object(url)
        self.city_result_count = self.scraper.extract_number_of_results(soup)

    def generate_url(self, city, page_index=0):
        return "{}/jobs?q={}&l={}&start={}".format(self.base_url, self.replace_symbols(self.given_job_title), self.replace_symbols(city), page_index)
    
    def generate_soup_object(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
    
    def page_search(self, city, page_index):
        self.save_page = False
        self.next_page = False
        current_url = self.generate_url(city, page_index)
        current_soup = self.generate_soup_object(current_url)
            
        # Use methods to extract to lists
        self.extract_current_page_lists(current_soup)
        for index in range(0, len(self.current_city['location'])):
            self.current_index = index
            if self.exit:
                return
            if not self.save_all:
                if not self.save_cities and not self.next_city:
                    if not self.save_page and not self.next_page:
                        self.display_current_job()
                        self.prompt_user_job_options()
                    else:
                        if self.save_page:
                            self.save_post()
                else:
                    if self.save_page:
                        self.save_post()
            else:
                self.save_post()
                    
    def prompt_user_job_options(self):
        self.display_job_prompt_message()
        while True:
            self.user_response = input()
            
            # Go to next 
            if self.user_response.lower() == "p":
                # Save post to dict
                response = self.prompt_user_next_options()
            
                # Set flag to save the rest of the posts
                if response == "p":
                    print("skipping...")
                    self.next_page = True
                    return
            
                elif response == "c":
                    print("skipping...")
                    self.next_city = True
                    return
                
                elif response == "b":
                    return
            
            elif self.user_response.lower() == "n":
                return

            # Open page
            elif self.user_response.lower() == "v":
                print("opening in browser now")
                self.open_browser_to_url(self.current_city['url'][self.current_index])
            
            # Save post to dict
            elif self.user_response.lower() == "s":
                response = self.prompt_user_save_options()
            
                # Set flag to save the rest of the posts
                if response == "p":
                    print("Posts Saved!")
                    self.save_page = True
                    return
            
                elif response == "c":
                    print("Saving posts, this will take a few seconds...")
                    self.save_cities = True
                    return

                elif response == "a":
                    print("Saving posts, this will take a few seconds...")
                    self.save_all = True
                    return
                
                elif response == "b":
                    return
                
                
            elif self.user_response.lower() == "b":
                self.exit = True
                print("Returning...")
                return

            else:
                print("Invalid Input! Try again")

    def prompt_user_save_options(self):
        self.display_save_prompt_message()
        while True:
            self.user_response = input()
            
            if self.user_response.lower() == "p":
                return "p"
            
            elif self.user_response.lower() == "c":
                return "c"

            elif self.user_response.lower() == "a":
                return "a"
            
            elif self.user_response.lower() == "b":
                return "b"
            else:
                print("Invalid Input! Try again")

    def prompt_user_next_options(self):
        self.display_next_prompt_message()
        while True:
            self.user_response = input()
            
            if self.user_response.lower() == "p":
                return "p"
            
            elif self.user_response.lower() == "c":
                return "c"

            elif self.user_response.lower() == "a":
                return "a"
            
            elif self.user_response.lower() == "b":
                return "b"
            else:
                print("Invalid Input! Try again")

    def open_browser_to_url(self, url):
        webbrowser.open(url, new = 2)
            
    def display_job_prompt_message(self):
        print("What do you want to do?")
        print("[N]ext Post | [V]iew Post | [S]ave | Ski[P] | [B]ack")
    
    def display_next_prompt_message(self):
        print("Where do you want to skip?")
        print("[P]age | [C]ity | [B]ack")
    
    def display_save_prompt_message(self):
        print("What do you want to save?")
        print("[P]age Posts | [C]ity Posts | [A]ll Posts | [B]ack")

    def display_current_job(self):
        print("=========================")
        print("Job Title: {}".format(self.current_city["title"][self.current_index]))
        print("Company Name: {}".format(self.current_city["company"][self.current_index]))
        print("Location: {}".format(self.current_city["location"][self.current_index]))
        print("Date Posted: {}".format(self.current_city["date"][self.current_index]))
        print("Summary: {}".format(self.current_city["summary"][self.current_index]))
        print("=========================")

    def save_post(self):
        try:
            self.city_jobs_dict["title"].append(self.current_city["title"][self.current_index])
            self.city_jobs_dict["company"].append(self.current_city["company"][self.current_index])
            self.city_jobs_dict["location"].append(self.current_city["location"][self.current_index])
            self.city_jobs_dict["date"].append(self.current_city["date"][self.current_index])
            self.city_jobs_dict["summary"].append(self.current_city["summary"][self.current_index])
            self.city_jobs_dict["url"].append(self.current_city["url"][self.current_index])
        except IndexError:
            return

    def extract_current_page_lists(self, current_soup):
        self.initialize_current_city()

        self.current_city["title"] = self.scraper.extract_job_title_from_result(current_soup)
        self.current_city["company"] = self.scraper.extract_company_from_result(current_soup)
        self.current_city["location"] = self.scraper.extract_location_from_result(current_soup)
        self.current_city["date"] = self.scraper.extract_date_from_result(current_soup)
        self.current_city["summary"] = self.scraper.extract_summary_from_result(current_soup)
        self.current_city["url"] = self.scraper.extract_urls_from_result(current_soup)

    def initialize_current_city(self):
        self.current_city["title"] = list()
        self.current_city["company"] = list()
        self.current_city["location"] = list()
        self.current_city["date"] = list()
        self.current_city["summary"] = list()
        self.current_city["url"] = list() 

    def save_to_csv(self):
        directory = "jobs"
        if not os.path.exists(directory):
            os.makedirs(directory)
        current_date_filename = "{}/{}.csv".format(directory, self.current_date)
        print("Saving to {}".format(current_date_filename))  
        jobs_dataframe = pd.DataFrame.from_dict(self.city_jobs_dict)
        jobs_dataframe.to_csv(current_date_filename, index=False)




