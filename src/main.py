import requests
import bs4
from bs4 import BeautifulSoup
import webbrowser
import pandas as pd
import time
import os
from datetime import datetime



def extract_job_title_from_result(soup): 
  jobs = []
  for div in soup.find_all(name='div', attrs={'class':'row'}):
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
      jobs.append(a['title'])
  return(jobs)

def extract_company_from_result(soup): 
  companies = []
  for div in soup.find_all(name='div', attrs={'class':'row'}):
    company = div.find_all(name='span', attrs={'class':'company'})
    if len(company) > 0:
      for b in company:
        companies.append(b.text.strip())
    else:
      sec_try = div.find_all(name='span', attrs={'class':'result-link-source'})
      for span in sec_try:
        companies.append(span.text.strip())
  return(companies)

def extract_location_from_result(soup): 
  locations = []
  spans = soup.findAll('span', attrs={'class': 'location'})
  for span in spans:
    locations.append(span.text)
  return(locations)

def extract_date_from_result(soup):
  dates = []
  spans = soup.findAll('span', attrs={'class': 'date'})
  for span in spans:
    dates.append(span.text)
  return(dates)

def extract_summary_from_result(soup): 
  summaries = []
  spans = soup.findAll('div', attrs={'class': 'summary'})
  for span in spans:
    summaries.append(span.text.strip())
  return(summaries)

def extract_urls_from_result(soup):
  urls = []
  for div in soup.find_all(name='div', attrs={'class':'row'}):
    for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
      urls.append("https://www.indeed.ca/{}".format(a['href']))
  return(urls)

def extract_number_of_results(soup):
  result_str = soup.find(name='div', attrs={'id':'searchCount'}).text.strip().split()
  return int(result_str[3])


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
      result_count = extract_number_of_results(soup)

      print("Results Found for '{}': {}".format(city, result_count))

      for index in range(0, result_count, 20):
        if exit_requested:
          break

        current_URL = "https://www.indeed.ca/jobs?q={}&l={}&start={}".format(given_job_title, city, str(index))
        # Conducting a request of the stated URL above:
        current_page = requests.get(current_URL)
        current_soup = BeautifulSoup(current_page.text, 'html.parser')
            
        # Use methods to extract to lists
        current_titles = extract_job_title_from_result(current_soup)
        current_companies = extract_company_from_result(current_soup)
        current_locations = extract_location_from_result(current_soup)
        current_dates = extract_date_from_result(current_soup)
        current_summaries = extract_summary_from_result(current_soup)
        current_urls = extract_urls_from_result(current_soup)

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

  
  
