#!/usr/bin/python

# Copyright (C) 2006 Peter Poeml.  All rights reserved.
# This program is free software; it may be used, copied, modified
# and distributed under the terms of the GNU General Public Licence,
# either version 2, or (at your option) any later version.


"""
This file is provided because urllib2 doesn't have support for the DELETE and
PUT methods.

"""

import httplib 
import base64 
import os 
import urlparse

BLOCKSIZE=1024

def delfile(url, file, username, password):

    auth_string = base64.encodestring('%s:%s' % (username, password)).strip()

    u = urlparse.urlparse(url)
    host = u[1]
    path = u[2]

    conn = httplib.HTTP(host) 
    conn.putrequest('DELETE', '%s' % path) 
    conn.putheader('Host', host)
    conn.putheader('Authorization', 'Basic %s' % auth_string) 
    conn.endheaders() 


    reply, msg, headers = conn.getreply() 

    if reply == 200:
        #print 'done'
        pass
    else:
        print 'error deleting %s' % file
        print 'upload-DELETE reply=', reply, ' msg=', msg, 'headers=', headers

def putfile(url, file, username, password):

    size = os.stat(file)[6] 

    auth_string = base64.encodestring('%s:%s' % (username, password)).strip()

    u = urlparse.urlparse(url)
    host = u[1]
    path = u[2]

    conn = httplib.HTTP(host) 
    conn.putrequest('PUT', '%s' % path) 
    conn.putheader('Host', host)
    conn.putheader('Content-Type', 'text/plain') 
    conn.putheader('Content-Length', str(size)) 
    conn.putheader('Authorization', 'Basic %s' % auth_string) 
    conn.endheaders() 

    fp = open(file, 'rb') 
    n = 0 
    while 1: 
        buf = fp.read(BLOCKSIZE) 
        n+=1 
        if n % 10 == 0: 
            #print 'upload-sending blocknum=', n 
            #print '.',
            pass

        if not buf: break 
        conn.send(buf) 
    fp.close() 

    reply, msg, headers = conn.getreply() 

    if reply == 200:
        pass
        #print 'done'
    else:
        print 'error uploading %s' % file
        print 'upload-PUT reply=', reply, ' msg=', msg, 'headers=', headers


def main():
    import sys 

    username = 'yourusername' 
    password = 'yourpassword' 
    file = sys.argv[1]
    url = 'http://api.opensuse.org/source/exim/exim/%s' % os.path.basename(file)
    
    putfile(url, file, username, password)

    delfile(url, file, username, password)


if __name__ == '__main__':
    main()
