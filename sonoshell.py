#!/usr/bin/env python

import sys

from soco import SoCo

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print "Usage: sonoshell.py [speaker's IP] [cmd]"
        print ""
        print "Valid commands: play, pause, stop, volume, next, previous, and info"
        sys.exit()

    speaker_ip = sys.argv[1]
    cmd = sys.argv[2].lower()
    param1 = ''
    param2 = ''

    if (len(sys.argv) > 3):
        param1 = sys.argv[3]
    if (len(sys.argv) > 4):
        param2 = sys.argv[4]

    sonos = SoCo(speaker_ip)

    if (cmd == 'play'):
        print sonos.play()
    elif (cmd == 'pause'):
        print sonos.pause()
    elif (cmd == 'volume'):
        if(param1 != ''):
            print param1
            sonos.volume(int(param1))
        else:
            print sonos.volume()
    elif (cmd == 'eq'):
        if(param1 == 'bass'):
            if(param2 != ''):
                sonos.bass(int(param2))
            else:
                print sonos.bass()
        elif(param1 == 'treble'):
            if(param2 != ''):
                sonos.treble(int(param2))
            else:
                print sonos.treble()
        else:
            print 'Usage: sonoshell.py [speaker\'s IP] eq [bass|treble]'
    elif (cmd == 'stop'):
        print sonos.stop()
    elif (cmd == 'next'):
        print sonos.next()
    elif (cmd == 'previous'):
        print sonos.previous()
    elif (cmd == 'start_playlist'):
        print sonos.start_playlist()
    elif (cmd == 'set_playmode'):
        print sonos.set_playmode()
    elif (cmd == 'info'):
        track = sonos.get_current_track_info()

        print 'Artist: ' + track['artist'] + ', Current track:  ' + track['title'] + ', From album: ' + track['album'] + ', This is track number: ' + track['playlist_position'] + ' in the playlist. It is ' + track['duration'] + ' minutes long.'
    else:
        print "Valid commands: play, pause, stop, next, previous, and info"
