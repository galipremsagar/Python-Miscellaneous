from BeautifulSoup import BeautifulSoup
import urllib2
import sys


def getItemName(tag,index):
    try:
        itemName = tag.find("span", {"id": "nameQA"+str(index+1)}).__getitem__('title')
    except AttributeError:
        itemName = tag.find("a", {"id": "nameQA" + str(index + 1)})
        if itemName == None:
            itemName = ""
        else:
            itemName = itemName.__getitem__('title')
    return itemName

def getItemMerchantName(tag):
    try:
        itemMerchantName = tag.find("a", {"class": "newMerchantName"}).text
    except AttributeError:
        itemMerchantName = tag.find("span", {"class": "newMerchantName"})
        if itemMerchantName == None:
            itemMerchantName = ""
        else:
            itemMerchantName = itemMerchantName.text
    return itemMerchantName

def getItemFreeShipping(tag):
    try:
        iTemFreeShipping = tag.find("span", {"class": "freeShip"})
        if iTemFreeShipping == None:
            iTemFreeShipping = tag.find("div", {"class": "freeShip"}).text
        else:
            iTemFreeShipping = iTemFreeShipping.text
    except AttributeError:
        iTemFreeShipping = tag.find("span", {"class": "calc"})
        if iTemFreeShipping == None:
            iTemFreeShipping = tag.find("div", {"class": "calc"})
        if iTemFreeShipping == None:
            iTemFreeShipping = "No Free Shipping"
        else:
            iTemFreeShipping = iTemFreeShipping.text
    return iTemFreeShipping

def getItemPrice(tag,index):
    try:
        iTemPrice = tag.find("a", {"id": "DCTmerchNameLnk"+str(index)}).text
    except AttributeError:
        iTemPrice = tag.find("span", {"id": "priceProductQA" + str(index+1)})
        if iTemPrice == None:
            iTemPrice = ""
        else:
            iTemPrice = iTemPrice.text
    return iTemPrice


def get_item_details(itemTag,index):

    itemName = getItemName(itemTag,index)
    itemMerchantName = getItemMerchantName(itemTag)
    itemFreeShipping = getItemFreeShipping(itemTag)
    iTemPrice = getItemPrice(itemTag,index)

    return {"itemName":itemName,"itemMerchantName":itemMerchantName,"iTemFreeShipping":itemFreeShipping,"iTemPrice":iTemPrice}


def get_page_result(url):
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html,convertEntities=BeautifulSoup.HTML_ENTITIES)
    results = soup.find("div", {"id" : "searchResultsContainer"})

    results_BS_object = BeautifulSoup(str(results))

    i = 1
    items_list = []
    while True:
        tmp = results_BS_object.find("div",{"id":"quickLookItem-"+str(i)})
        if tmp:
            items_list.append(tmp)
            i+=1
        else:
            break


    print "The number of items on this page are ", len(items_list)
    for index,item in enumerate(items_list):
        print index
        print get_item_details(item,index)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print "Usage is:"
        print "Query 1: (requires a single argument)\n`your_program <keyword>`"
        print "Query 2: (requires two arguments)\n`your_program <keyword> <page number>`"
    elif len(sys.argv) == 3:
        if type(int(sys.argv[2])).__name__ == 'int' and int(sys.argv[2]) > 0:
            url = "http://www.shopping.com/products~PG-"+str(sys.argv[2])+"?KW="+str(sys.argv[1])+""
            get_page_result(url)
        else:
            print "Please provide valid page number"
    elif len(sys.argv) == 2:
        url = "http://www.shopping.com/products?KW=" + str(sys.argv[1])
        get_page_result(url)
    else:
        print "Wrong usage"
        print "Usage is:"
        print "Query 1: (requires a single argument)\n`your_program <keyword>`"
        print "Query 2: (requires two arguments)\n`your_program <keyword> <page number>`"
