'''
    shows all genres
'''
import pyen

en = pyen.Pyen()
response = en.get('genre/list', bucket=['description'])
for g in response['genres']:
    print g['name'], '-', g['description']
