#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import tweepy
import shelve
import json
import pprint

### Functions
def yes_no_prompt(text):
    choice = raw_input(text)
    if choice in ['y', 'yes']:
        return True
    elif choice in ['n', 'no']:
        return False

def update_consumer_key():
    # Open database file
    d = shelve.open('keys.shelve')

    temp_ck = raw_input('CONSUMER KEY: ')
    temp_cs = raw_input('CONSUMER SECRET: ')
    d['consumer_key'] = temp_ck
    d['consumer_secret'] = temp_cs
    print "API keys are registered successfully."
    d.close()

def update_access_token():
    # Open database file
    d = shelve.open('keys.shelve')

    if not ((d.has_key('consumer_key')) or (d.has_key('consumer_secret'))):
        print "Please register API key(menu 1) in advance."
        d.close()
        sys.exit()

    # Consumer Key
    CONSUMER_KEY = d['consumer_key']
    # Consumer Secret
    CONSUMER_SECRET = d['consumer_secret']

    # Create OAuthHandler Instance
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    print "Access:", auth.get_authorization_url()
    verifier = raw_input('Verifier:')
    auth.get_access_token(verifier)

    # Construct the API instance
    api = tweepy.API(auth)
    me = api.me()
    screen_name = str(me._json['screen_name'])

    if d.has_key(screen_name):
        if not yes_no_prompt("Token for @" + screen_name + " is found.\n" "Do you update access token for @" + screen_name + "? (y/n)"):
            d.close()
            sys.exit()

    tokens = {"access_token":auth.access_token, "access_token_secret":auth.access_token_secret}
    d[screen_name] = tokens
    print "Updated access token for @" + screen_name + " successfully."

    # Close database file
    d.close()

def show_access_token():
    # Open database file
    d = shelve.open('keys.shelve')
    pprint.pprint(d.items())

while True:
    choice = raw_input("Please select mode.\n\t1 Update API keys\n\t2 Update Access tokens\n\t3 Show access tokens\n\tq Exit\n")

    if choice in ['1']:
        update_consumer_key()
        print "\n"
    elif choice in ['2']:
        update_access_token()
        print "\n"
    elif choice in ['3']:
        show_access_token()
        print "\n"
    elif choice in ['q', 'Q']:
        sys.exit()
    else:
        print "Invalid value.\n"
