# https://www.indeed.ca/jobs?q=data+scientist+%2420%2C000&l=Edmonton%2C+AB
import requests
import bs4
from bs4 import BeautifulSoup
import webbrowser
import pandas as pd
import time
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

def extract_salary_from_result(soup): 
  salaries = []
  for div in soup.find_all(name='div', attrs={'class':'row'}):
    try:
      salaries.append(div.find('nobr').text)
    except:
      try:
        div_two = div.find(name='div', attrs={'class':'sjcl'})
        div_three = div_two.find('div')
        salaries.append(div_three.text.strip())
      except:
        salaries.append('N/A')
  return(salaries)

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

if __name__ == "__main__":

  # Build URL
  
  given_job_title = input("Enter Job Title: ").replace(" ", "+")

  city_set = list()

  while True:
    given_city = input("Enter List of Desired Cities (Press enter to continue after): ")

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
  URL = "https://www.indeed.ca/jobs?q={}&l={}".format(given_job_title, city_set[0])

  #conducting a request of the stated URL above:
  page = requests.get(URL)


  soup = BeautifulSoup(page.text, 'html.parser')

  result_count = extract_number_of_results(soup)
  
  print(result_count)

  columns = ['city', 'job_title', 'company_name', 'location', 'summary', 'url']

  sample_dataframe = pd.DataFrame(columns = columns)
  
  # Use methods to extract to lists
  job_title_list = extract_job_title_from_result(soup)
  company_name_list = extract_company_from_result(soup)
  locations_list = extract_location_from_result(soup)
  summaries_list = extract_summary_from_result(soup)
  urls_list = extract_urls_from_result(soup)

  #webbrowser.open(urls_list[0], new = 2)

  
  
