# https://www.indeed.ca/jobs?q=data+scientist+%2420%2C000&l=Edmonton%2C+AB
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time

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

if __name__ == "__main__":
  print("Reading...")

  URL = "https://www.indeed.ca/jobs?q=data+scientist+%2420%2C000&l=Edmonton%2C+AB"

  #conducting a request of the stated URL above:
  page = requests.get(URL)

  soup = BeautifulSoup(page.text, 'html.parser')

  max_results_per_city = 100
  city_set = ['New+York','Chicago','San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta', 'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']
  columns = ['city', 'job_title', 'company_name', 'location', 'summary', 'salary']
  
  # Use methods to extract to lists
  job_title_list = extract_job_title_from_result(soup)
  company_name_list = extract_company_from_result(soup)
  locations_list = extract_location_from_result(soup)
  # PROPERLY IMPLEMENT
  salaries_list = extract_salary_from_result(soup)
  summaries_list = extract_summary_from_result(soup)

  print(salaries_list)
