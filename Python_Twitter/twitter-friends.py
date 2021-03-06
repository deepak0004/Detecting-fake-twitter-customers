import pickle
import time
import sys
from Object import *
from twitter import *
import unicodedata

# twitter-friends: lists all of a given user's friends (ie, followees (following) ), the ones user is following

st = sys.argv[1]
print st
config = {}
execfile(st, config)
twitter = Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))

us_list = []
dictt = {}

inputt = open('users_less_followees.txt', 'r')
for line in inputt:
    us = str(line) 
    us_list.append(us) 

#outputt = open('user_following.txt', 'w', 0)
for username in us_list:
        username = username.strip() 
        username = username.strip('\n')
        #outputt.write(username + ",")
        flag = 0
        while( flag == 0 ):
            try:
                query = twitter.friends.ids(screen_name = username) 
                flag = 1

                # tell the user how many friends we've found.
                # note that the twitter API will NOT immediately give us any more 
                # information about friends except their numeric IDs...
                #outputt.write( str(len(query["ids"])) ) 
                print username, " ", len(query["ids"]), " ", len(username)
                dictt[ username ] = [] 
                if( len(query["ids"]) ):
                    # now we loop through them to pull out more info, in blocks of 100.
                    for n in range(0, len(query["ids"]), 98):
                        ids = [-1]
                        ids.extend( query["ids"][n:n+98] )
                        ids.append(-1)
                        #print len(ids)
                        #print ids
                        flag2 = 0
                        while( flag2 == 0 ):
                            try:
                                subquery = twitter.users.lookup(user_id = ids)
                                flag2 = 1
                            except Exception:
                                print 'yo2', " ", flag2
                                time.sleep(60) 
                        print len(ids), " ", len(subquery)
                        for user in subquery:
                            #print str(user["screen_name"]), 
                            #outputt.write( "," + str(user["screen_name"]) )
                            dictt[ username ].append( str(user["screen_name"]) ) 
                #outputt.write("\n")
                print len(dictt[username])
            except Exception:
                print 'yo', " ", flag
                time.sleep(60)

with open("user_and_who_he_following.dump", "wb") as fp:   #Pickling
    pickle.dump(dictt, fp)