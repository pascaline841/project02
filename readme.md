<h1 align="center"> Web Scraping-  BOOKS TO SCRAPE</h1><br>
  
## OVERVIEW

Beta version of a system for tracking book prices at Books to Scrape, an on-demand runtime application aimed at retrieving prices at runtime.
<br>


## REQUISITORIES 

Python3<br>
beautifulsoup4 <br>
requests <br>
<br>
## INSTALLATION
Start by closing the repository :
```
git clone https://github.com/pascaline841/p02
```
Start access the project folder

## for Window
Create a virtual environment
```
python -m venv env
```
Enable the virtual environment
```
cd env/scripts
source activate
```

## for Linux or macOS
Create a virtual environment 
```
python3 -m venv env
```
Activate the virtual environment with 
```
source env/bin/activate 
```
## . . . 
Install the python dependencies to the virtual environment
```
pip install -r requirements.txt
```
## LAUNCH 

Run the program
```
python main.py
```
Creation of  a BooksToScrape repertory<br>
Creation of a folder named by the category containing : <br>
- a picture of all books 
- a csv file with all the books<br>
the additional informations are :<br>
- Product_page_url<br>
- Universal_produit_code (upc)<br>
- Title<br>
- Price_including_tax <br>
- Price_excluding_tax <br>
- Number_available <br>
- Product Description <br>
- Category <br>
- Review_rating <br>
- Image URL <br>
