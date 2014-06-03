#!/usr/bin/env python

import os
import json
import urllib
import jinja2
import oauth2
import webapp2
import urllib2
import logging
import ConfigParser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def yelp_request(self, url_params):
        # Read keys and tokens
        config = ConfigParser.ConfigParser()
        config.read("config.ini")
        config_section = "yelp_keys"
        consumer_key = config.get(config_section, "consumer_key")
        consumer_secret = config.get(config_section, "consumer_secret")
        token = config.get(config_section, "token")
        token_secret = config.get(config_section, "token_secret")
        
        # Unsigned URL
        path = "http://api.yelp.com/v2/search"
        encoded_params = ""
        if url_params:
            encoded_params = urllib.urlencode(url_params)
        url = "%s?%s" % (path, encoded_params)
        logging.info(url)

        # Sign the URL
        consumer = oauth2.Consumer(consumer_key, consumer_secret)
        oauth_request = oauth2.Request("GET", url, {})
        oauth_request.update({"oauth_nonce": oauth2.generate_nonce(),
                        "oauth_timestamp": oauth2.generate_timestamp(),
                        "oauth_token": token,
                        "oauth_consumer_key": consumer_key})

        token = oauth2.Token(token, token_secret)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()
        #logging.info(signed_url)

        logging.info(url_params)
        
        # Connect
        try:
            conn = urllib2.urlopen(signed_url, None)
            try:
                response = json.loads(conn.read())
            finally:
                conn.close()
        except urllib2.HTTPError, error:
            response = json.loads(error.read())

        logging.info(response)
        return response
        
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("main.html")
        self.response.write(template.render())
    
    def post(self):
        jsonstring = self.request.body
        jsonobject = json.loads(jsonstring)
        
        # TODO error handling
        params = {}
        params["term"] = "restaurants"
        params["ll"] = "{},{}".format(str(jsonobject["latitude"]),str(jsonobject["longitude"]))
        params["radius_filter"] = "1000"
        logging.info(params)
        
        response = self.yelp_request(params)
        
        logging.info(type(response))
        
        response = json.dumps(response)             
        self.response.write(response)
            
app = webapp2.WSGIApplication([
    ("/", MainHandler)
], debug=True)
