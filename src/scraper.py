
class Scraper:

  def extract_job_title_from_result(self, soup): 
    jobs = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
      for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        jobs.append(a['title'])
    return(jobs)

  def extract_company_from_result(self, soup): 
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

  def extract_location_from_result(self, soup): 
    locations = []
    spans = soup.findAll('span', attrs={'class': 'location'})
    for span in spans:
      locations.append(span.text)
    return(locations)

  def extract_date_from_result(self, soup):
    dates = []
    spans = soup.findAll('span', attrs={'class': 'date'})
    for span in spans:
      dates.append(span.text)
    return(dates)

  def extract_summary_from_result(self, soup): 
    summaries = []
    spans = soup.findAll('div', attrs={'class': 'summary'})
    for span in spans:
      summaries.append(span.text.strip())
    return(summaries)

  def extract_urls_from_result(self, soup):
    urls = []
    for div in soup.find_all(name='div', attrs={'class':'row'}):
      for a in div.find_all(name='a', attrs={'data-tn-element':'jobTitle'}):
        urls.append("https://www.indeed.ca/{}".format(a['href']))
    return(urls)

  def extract_number_of_results(self, soup):
    result_str = soup.find(name='div', attrs={'id':'searchCount'}).text.strip().split()
    return int(result_str[3])