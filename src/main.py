import unirest

if __name__ == "__main__":
    print("testing...")
    response = unirest.get("https://indeed-indeed.p.rapidapi.com/apisearch?q=java&v=2&format=json&radius=25&l=austin%2C+tx",
  headers={
    "X-RapidAPI-Host": "indeed-indeed.p.rapidapi.com",
    "X-RapidAPI-Key": "EnS71G18D3mshXpTsIY2efZriZdxp1FzHAJjsnnH2b4gdJrwOh"
    } 
    )
    print("response received:\n{}".format(response.body))
