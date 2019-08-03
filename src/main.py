import requests
import bs4
from bs4 import BeautifulSoup
import webbrowser
import pandas as pd
import time
import os
from datetime import datetime
from scraper import Scraper

def main():

  # Initialize Data Storage
  city_jobs_dict = dict()
  
  # Initialize Dictionary
  city_jobs_dict["title"] = list()
  city_jobs_dict["company"] = list()
  city_jobs_dict["location"] = list()
  city_jobs_dict["date"] = list()
  city_jobs_dict["summary"] = list()
  city_jobs_dict["url"] = list() 
  
  exit_requested = False

  scraper = Scraper()

  while True:

    save_all_posts = False

    if exit_requested:
        break
    
    os.system('cls||clear')
    print("Welcome to the job hunting app!")
    current_date = str(datetime.today()).split()[0]
    print("Today's Date: {}".format(current_date))
    print("Enter X to exit program")
    print("=========================")
  

    # Get job title
    given_job_title = input("Enter Job Title: ")
    
    if given_job_title.lower() == "x":
      break
    
    given_job_title = given_job_title.replace(" ", "+")

    # Get list of cities
    city_set = list()
    print("Enter List of Cities (Press enter to continue after): ")
    while True:
      given_city = input()
      if given_city == "":
        if len(city_set) > 0:
          break
        else:
          print("Error: Enter at least one city")
      else:
        given_city = given_city.replace(" ", "+")
        city_set.append(given_city)
    
    print("Extracting...")
    
    # Create Resulting URL
    for city in city_set:
      save_all_cities = False
      if exit_requested:
        break
      
      URL = "https://www.indeed.ca/jobs?q={}&l={}".format(given_job_title, city)
      
      # Conducting a request of the stated URL above:
      page = requests.get(URL)
      soup = BeautifulSoup(page.text, 'html.parser')
      result_count = scraper.extract_number_of_results(soup)

      print("Results Found for '{}': {}".format(city, result_count))
      
      for index in range(0, result_count, 20):
        if exit_requested:
          break

        current_URL = "https://www.indeed.ca/jobs?q={}&l={}&start={}".format(given_job_title, city, str(index))
        # Conducting a request of the stated URL above:
        current_page = requests.get(current_URL)
        current_soup = BeautifulSoup(current_page.text, 'html.parser')
            
        # Use methods to extract to lists
        current_titles = scraper.extract_job_title_from_result(current_soup)
        current_companies = scraper.extract_company_from_result(current_soup)
        current_locations = scraper.extract_location_from_result(current_soup)
        current_dates = scraper.extract_date_from_result(current_soup)
        current_summaries = scraper.extract_summary_from_result(current_soup)
        current_urls = scraper.extract_urls_from_result(current_soup)

        a_not_selected = True
        

        for i in range(0, len(current_locations)):
          if exit_requested:
            break
          
          if not save_all_posts:
            if not save_all_cities:

              if a_not_selected:
                # Print Posting
                print("=========================")
                print("Job Title: {}".format(current_titles[i]))
                print("Company Name: {}".format(current_companies[i]))
                print("Location: {}".format(current_locations[i]))
                print("Date Posted: {}".format(current_dates[i]))
                print("Summary: {}".format(current_summaries[i]))
                print("=========================")

                # Prompt User
                print("What do you want to do?")
                print("[N]ext Post | [V]iew Post | [S]ave post | Save all posts from [P]age | Save all posts from [C]ity | Save [A]ll posts from search | E[X]it Program")

                while True:
                  # Get user input
                  user_response = input()

                  # Go to next post
                  if user_response.lower() == "n":
                    break
                  
                  # Open page
                  elif user_response.lower() == "v":
                    webbrowser.open(current_urls[i], new = 2)
                  
                  # Save post to dict
                  elif user_response.lower() == "s":
                    try:
                      city_jobs_dict["title"].append(current_titles[i])
                      city_jobs_dict["company"].append(current_companies[i])
                      city_jobs_dict["location"].append(current_locations[i])
                      city_jobs_dict["date"].append(current_dates[i])
                      city_jobs_dict["summary"].append(current_summaries[i])
                      city_jobs_dict["url"].append(current_urls[i])
                    except IndexError:
                      break
                    print("Post Saved!")
                  
                  # Set flag to save the rest of the posts
                  elif user_response.lower() == "p":
                    print("Posts Saved!")
                    a_not_selected = False
                    break
                  
                  elif user_response.lower() == "c":
                    print("Saving posts, this will take a few seconds...")
                    save_all_cities = True
                    break

                  elif user_response.lower() == "a":
                    print("Saving posts, this will take a few seconds...")
                    save_all_posts = True
                    break
                  
                  elif user_response.lower() == "x":
                    exit_requested = True
                    break

                  else:
                    print("Invalid Input! Try again")
              
              else:
                try:
                  city_jobs_dict["title"].append(current_titles[i])
                  city_jobs_dict["company"].append(current_companies[i])
                  city_jobs_dict["location"].append(current_locations[i])
                  city_jobs_dict["date"].append(current_dates[i])
                  city_jobs_dict["summary"].append(current_summaries[i])
                  city_jobs_dict["url"].append(current_urls[i])
                except IndexError:
                  break
            else:
                try:
                  city_jobs_dict["title"].append(current_titles[i])
                  city_jobs_dict["company"].append(current_companies[i])
                  city_jobs_dict["location"].append(current_locations[i])
                  city_jobs_dict["date"].append(current_dates[i])
                  city_jobs_dict["summary"].append(current_summaries[i])
                  city_jobs_dict["url"].append(current_urls[i])
                except IndexError:
                  break
          else:
                try:
                  city_jobs_dict["title"].append(current_titles[i])
                  city_jobs_dict["company"].append(current_companies[i])
                  city_jobs_dict["location"].append(current_locations[i])
                  city_jobs_dict["date"].append(current_dates[i])
                  city_jobs_dict["summary"].append(current_summaries[i])
                  city_jobs_dict["url"].append(current_urls[i])
                except IndexError:
                  break

        time.sleep(1)

      time.sleep(1)

  current_date_filename = "jobs/{}.csv".format(current_date)

  print("Saving to {}".format(current_date_filename))  
  jobs_dataframe = pd.DataFrame.from_dict(city_jobs_dict)
  jobs_dataframe.to_csv(current_date_filename, index=False)

if __name__ == "__main__":
  main()

  
  
