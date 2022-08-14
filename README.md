# Scraping Whoscored Event Data
![alt text](https://github.com/Stat-Peekers/Scrape-Whoscored-Event-Data/blob/main/logo.jpg "Whoscored")

Now you can get **FREE!!** match event data from [Whoscored](http://whoscored.com/ "Whoscored")'s chalkboard using **Selenium**. 

Pre-requisites:
1. **Clone repository**
   1. Clone this repo in your local system -> [How to?](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
2. **Work in a conda / python environment**\
   (Proceed to Step 3 if you don't want to work in an environment)
   1. _Preferred_ -> Create a new python environment
   2. Docs for creating and activating environment in conda -> [How to?](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)
   3. Activate the environment -> [How to?](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment)
3. **Installing required libraries**
   1. Using Anaconda prompt / terminal
      1. Open Anaconda prompt / terminal
      2. Go to local folder where cloned/downloaded repository
      4. Run this code `pip install -r requirements.txt`\
4. **Driver for chrome**
   1. Check browser version
      1. Open Chrome
         1. In the chrome address bar enter -> chrome://settings/help
         2. OR Open Chrome Click `⋮` -> Help -> About Google Chrome
      2. Download driver
         1. [Download from here](https://chromedriver.chromium.org/downloads)
         2. Choose the one that matches your current version as obtained in step `i`
         3. A zip file will be downloaded. Extract the file inside it into the cloned local folder.\

      NOTE: If you use any other browser than chrome, kindly go through [this](https://selenium-python.readthedocs.io/installation.html#drivers) and you will also have to change the code accordingly. I will be doing this in future updates
   

To get the data:
1. Data for one match: 
   1. Get the match url from [Whoscored](http://whoscored.com/ "Whoscored")
   2. Run file: `single_match_scrape.py`
   3. Enter the url for data from the desired match as obtained in Step `i`
2. Data for a tournament in a particular season:
   - Run file: `all_matches_in_comp.py`
   - Select desired tournament and season
   - Sit back and let the code do the work for you :smiley:

Reach me [here](https://twitter.com/StatPeekers) for any kind of help :) 

CREDITS:
Code is adapted from [Ali Hasan Khan](https://github.com/Ali-Hasan-Khan/Scrape-Whoscored-Event-Data) ([Reach out here](https://twitter.com/rockingAli5)) \
LICENCE: Original licence is also preserved / maintained as developed by [Ali Hasan Khan](https://github.com/Ali-Hasan-Khan/Scrape-Whoscored-Event-Data)
