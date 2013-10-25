#
# Generates an acrostic playlist
#
# This was built at the Tufts Hackathon Fall 2013
#
# Creates a playlist in the given genre, where the
# first letter in each song spells out a secret
# message


import sys
import pyen
import logging

found_songs = []
en = pyen.Pyen()

session_id = None

def get_more_songs(genre):
    ''' gets mores songs in the genre
    '''
    global session_id

    if session_id == None:
        response = en.get('playlist/dynamic/create', type='genre-radio', genre=genre)
        session_id = response['session_id']
    response = en.get('playlist/dynamic/next', session_id=session_id, results=5)

    songs = []
    for song in response['songs']:
        song_name =  song['title'] + ' by ' + song['artist_name']
        songs.append(song_name)
        # print '      ', song['title'] + ' by' + song['artist_name']
    return songs
    
def find_song_that_starts_with_letter(genre, c):
    ''' tries to find a song that begins with the
        given letter
    '''
    max_tries = 200

    for s in found_songs:
        if s[0].lower() == c:
            found_songs.remove(s)
            return s

    tries = max_tries
    while tries > 0:
        songs = get_more_songs(genre)
        for song in songs:
            if song[0].lower()  == c:
                return song
            else:
                found_songs.append(song)
        tries -= 1

def build_acrostic(genre, sentence):
    ''' builds an acrostic for the given genre
    '''

    for c in sentence:
        if c.isalpha():
            song = find_song_that_starts_with_letter(genre, c)
            print song
        else:
            print

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "python acrostic.py  genre 'secret message'"
    else:
        build_acrostic(sys.argv[1], sys.argv[2].lower())
