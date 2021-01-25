# Intuitive Webscraper

- [Intuitive Webscraper](#intuitive-webscraper)
  - [Overview](#overview)
  - [Components](#components)
  - [Installation and Usage](#installation-and-usage)
  - [Project Architecture](#project-architecture)
  - [Author](#author)

## Overview
A webscraper and stock watchlist app that scrapes stock data. Users can
add new stocks to the watchlist via searching the ticker catalog for a
ticker symbol or public company to add or simply inputting the ticker
symbol. The watchlist can be managed by the user and is updated every day
to reflect the newest information and open and closing prices for the stocks.
Users can add, delete, and browse ticker symbols using this app.


## Components
The scraper utilizes Beautiful Soup to scrap data, while using Flask app 
as a backend and frontend to the application


## Installation and Usage
The requirements of the project are all included in the `requirements.txt` file.  
Create an environment for the project via `venv`, and run `pip install -r requirements.txt`
to install the requirements.  
To run the application, simply run `app.py` in the project directory.

To install and run, run in the project directory:
```
$ python3 -m venv env
$ source env/bin/activate(MacOS / Linux) or $ .\env\Scripts\activate(Windows)
$ pip install -r requirements.txt
$ python3 -m app.py
```

## Project Architecture
```
IntuitiveWebscraper
│   README.md
│   app.py
|   requirements.txt
│
└───intuitive_webscraper
|   |   utils.py
│   │   cache.py
|   |   parse_stocks.py
|   |   parse_tickers.py
│   │   process_stocks.py
|
└───templates
|
└───static
|
└───cache
```
`./intuitive_webscraper` serves as the src for this project, 
including all the source code.  
`./templates` stores all the html page templates  
`./static` stores the css stylesheets  
`./cache` stores all cache files and components  

## Author
Alex Chen  
I am a student studying Information Systems and Robotics at 
Carnegie Mellon University.