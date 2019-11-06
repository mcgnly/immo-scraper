## Immobilien-scraper
#### stay in your Kiez

**purpose:** 

Collect some data over time about home prices in your neighborhood

**current state:** 

This was built to work with https://www.immobilienscout24.de/ as it is structured in November 2019- this structure can change and then throw off the location of data or the ability to load subsequent pages, so keep an eye on things...

**usage:**

- this was made with python 3.6.0, but likely works with many 
versions

1. clone locally
2. install local dependencies with 
```pip install -r requirements.txt```
3. create a .env file according to the ```example.env``` where BASE_URL contains the url for the search you have run for your specific situation- the more specific the better
4. run with ```python scraper.py```

In the end, this will create a text file containing JSON describing all the items which matched your search: ID, price, square-meters, rooms, and price per m2. If you choose to run this at regular intervals with a cron job (at your own risk, generally websites don't love being scraped), it will update items when the IDs match and add only new IDs. 