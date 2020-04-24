import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Read the excel file with pandas
data = pd.read_excel('index.xlsx')

# Loop through pandas dataframe
for index, row in data.iterrows():
    no = row['No.']
    title = row['Book Title'].replace('\n', ' ')
    category = row['Subject/Category'].replace('\n', ' ')
    url = row['OpenURL']

    # Get the page from url wih requests
    response = requests.get(url)

    # Read the page with beautifulsoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Search for download link with beautifulsoup
    result = soup.find('a', attrs={'title' : 'Download this book in PDF format'})
    download_link = result['href']

    # Download the pdf file with requests
    pdf = requests.get('https://link.springer.com' + download_link)
    with open (f'ebook/{category}/{title}.pdf', 'wb') as writer:
        print(f'{time.strftime("%H:%M:%S")}: Saving ebook no.{no} - title "{title}" in category "{category}"...')
        writer.write(pdf.content)

    # To prevent IP been blocked cause by access their server simultaneously
    time.sleep(60)
