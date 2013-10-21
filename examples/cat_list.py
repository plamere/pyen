import pyen

en = pyen.Pyen()

start = 0
page_size = 100

while True:
    response = en.get('catalog/list', start=start, results=page_size)
    catalogs = response['catalogs']
    for cat in catalogs:
        print "%s %5d %8s %s" % (cat['id'], cat['total'], cat['type'], cat['name'])

    if len(catalogs) < page_size:
        break
    else:
        start += page_size


