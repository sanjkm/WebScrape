# Gets price for Tory Burch item that Jules is interested in

from bs4 import BeautifulSoup
import urllib2

from StringIO import StringIO
import gzip

import csv, os

# Opens URL to see if the item listed there has price less than or equal
# to the max_price inputted. If so, the item and its price are outputted
# to outfile. Otherwise, the program returns zero
def GetPriceData (url, max_price, outfile):

    site = url    
    hdr = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
           'Accept-Encoding': 'gzip, deflate, br',
           'Accept-Language': 'en-US,en;q=0.5',
           'Connection': 'keep-alive'}

    req = urllib2.Request(site, headers=hdr)
    page = urllib2.urlopen(req)
    
    if page.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(page.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        soup = BeautifulSoup (data, 'lxml')
    else:
        soup = BeautifulSoup (page, 'lxml')

    price_tag = 'data-number-price' # html tag with the item's price

    for link in soup.find_all('span'):  # price is the first tag with the below attributes
        if price_tag in link.attrs:
            curr_px = float(link.attrs[price_tag])

            if curr_px <= max_price:
                f = open(outfile, 'a')

                f.write(soup.title.string + '\n')
                f.write('Current Price: ' + str(curr_px) + '\n')
                f.write('Target Price: ' + str(max_price) + '\n\n')
                f.write(url + '\n\n')
                f.close()
            return 0
    return 0

def main():

    clothes_file = 'clothes_list.txt'

    cmd_file = './first_reminder.sh'
    CURR_DIR = '/home/smenon/Web/'
    outfile = 'Tory.txt'
    outfile = CURR_DIR + outfile
    
    f = open(outfile, 'w')
    f.close()
    
    with open(CURR_DIR + clothes_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            url, max_price = row['Link'], float(row['Target Price'])
            GetPriceData (url, max_price, outfile)

    os.system (CURR_DIR + cmd_file)

main()
    
