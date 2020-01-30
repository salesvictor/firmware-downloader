import bs4
import os
import urllib.request


def parsed_url(url: str):
    raw_html = urllib.request.urlopen(url)
    soup_html = bs4.BeautifulSoup(raw_html, features='html.parser')
    return soup_html


url = 'https://www.tp-link.com/us/support/download/'
soup_html = parsed_url(url)
routers_table = soup_html.find_all(attrs={'data-class':'wi-fi-routers'})[0]
routers_tags = routers_table.find_all('a')
routers = [{'link':_['href'], 'name':_.text} for _ in routers_tags]
for router in routers:
    print(f"Downloading firmare for router {router['name']}\n")
    router_url = f"https://www.tp-link.com{router['link']}#Firmware"
    soup_html = parsed_url(router_url)
    tables = soup_html.find_all('table')
    downloads = [table.find_all(attrs={'class':'download ga-click'}) for table in tables]
    downloads = [_ for _ in downloads if _]
    files = [_[0]['href'] for _ in downloads]
    print(f'Found {len(files)} files\n')
    for idx, file in enumerate(files):
        print(f'Downloading file {idx+1}/{len(files)}')
        link = file.replace(' ', '%20')
        urllib.request.urlretrieve(link, os.path.basename(file))
