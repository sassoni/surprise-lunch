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
        logging.info("LocationHandler")
        #logging.info(self.request)
        
        jsonstring = self.request.body
        jsonobject = json.loads(jsonstring)
        logging.info(jsonstring)
        #for key, value in self.request.iteritems():
        #    logging.info(value)
        #request = json.loads(self.request)
        #logging.info(request)
        
        # TODO error handling
        params = {}
        params["term"] = "restaurants"
        params["ll"] = "{},{}".format(str(jsonobject["latitude"]),str(jsonobject["longitude"]))
        params["radius_filter"] = "1000"
        logging.info(params)
        
        response = self.yelp_request(params)
        
        logging.info("TYPEEEEEE")
        logging.info(type(response))
        
        response = json.dumps(response)              # dumpt it out as json
        #response = json.loads(response)  
        #content = json.dumps(content)  
        #logging.info(type(response))
        
        #self.response.headers["Content-Type"] = "application/json"
        self.response.write(response)
        
        
        #logging.info(response1)
        
        #self.response.headers["Content-Type"] = "text/plain"
            #response = handle_request(self.request)
    #print("Content-Type: application/json", end="\n\n")
    #json.dump(response, sys.stdout, indent=2)
            
        jsonResponse = """{
            "businesses": [
            {
            "id": "the-neighborhood-restaurant-somerville",
            "snippet_image_url": "http://s3-media2.ak.yelpcdn.com/photo/wZNbRB792ShRoHGOUZU0WA/ms.jpg",
            "rating_img_url_large": "http://s3-media2.ak.yelpcdn.com/assets/2/www/img/ccf2b76faa2c/ico/stars/v1/stars_large_4.png",
            "image_url": "http://s3-media1.ak.yelpcdn.com/bphoto/FOPOXdbX9DoW18KvKlF4KA/ms.jpg",
            "location": {
                "state_code": "MA",
                "postal_code": "02143",
                "country_code": "US",
                "address": [
                "25 Bow St"
                ],
                "display_address": [
                "25 Bow St",
                "Somerville, MA 02143"
                ],
                "city": "Somerville"
            },
            "display_phone": "+1-617-628-2151",
            "categories": [
                [
                "Bakeries",
                "bakeries"
                ],
                [
                "Breakfast & Brunch",
                "breakfast_brunch"
                ],
                [
                "Portuguese",
                "portuguese"
                ]
            ],
            "phone": "6176282151",
            "rating": 4.0,
            "is_closed": "false",
            "rating_img_url_small": "http://s3-media4.ak.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png",
            "url": "http://www.yelp.com/biz/the-neighborhood-restaurant-somerville",
            "review_count": 499,
            "name": "The Neighborhood Restaurant",
            "snippet_text": "I don't know if i've ever been as satisfied after eating SO much breakfast. The first time I went here, I had already eaten breakfast, was slightly hungover...",
            "is_claimed": "true",
            "distance": 1085.2387197179728,
            "mobile_url": "http://m.yelp.com/biz/the-neighborhood-restaurant-somerville",
            "rating_img_url": "http://s3-media4.ak.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png"
            },
            {
            "id": "ebi-sushi-bar-somerville",
            "snippet_image_url": "http://s3-media3.ak.yelpcdn.com/photo/4pPbN3LySSXKykvrXKGEsw/ms.jpg",
            "rating_img_url_large": "http://s3-media2.ak.yelpcdn.com/assets/2/www/img/ccf2b76faa2c/ico/stars/v1/stars_large_4.png",
            "image_url": "http://s3-media3.ak.yelpcdn.com/bphoto/fI1gRmWl5uJTq4vNrq5ADw/ms.jpg",
            "location": {
                "state_code": "MA",
                "postal_code": "02143",
                "country_code": "US",
                "address": [
                "290 Somerville Ave"
                ],
                "display_address": [
                "290 Somerville Ave",
                "Somerville, MA 02143"
                ],
                "city": "Somerville"
            },
            "display_phone": "+1-617-764-5556",
            "categories": [
                [
                "Sushi Bars",
                "sushi"
                ],
                [
                "Japanese",
                "japanese"
            ]
            ],
            "phone": "6177645556",
            "rating": 4.0,
            "is_closed": "false",
            "rating_img_url_small": "http://s3-media4.ak.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png",
            "url": "http://www.yelp.com/biz/ebi-sushi-bar-somerville",
            "review_count": 123,
            "name": "Ebi Sushi Bar",
            "snippet_text": "This place is by far one of the best Sushi restaurants I know. Their selection is plentiful and everything on their menu is worth a taste at least...",
            "is_claimed": "true",
            "distance": 745.6286391808283,
            "mobile_url": "http://m.yelp.com/biz/ebi-sushi-bar-somerville",
            "rating_img_url": "http://s3-media4.ak.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png"
            },
            {
            "menu_date_updated": 1387613124,
            "snippet_image_url": "http://s3-media2.ak.yelpcdn.com/photo/UQyqDtooh5IgAYLKwv1oig/ms.jpg",
            "rating_img_url_large": "http://s3-media2.ak.yelpcdn.com/assets/2/www/img/ccf2b76faa2c/ico/stars/v1/stars_large_4.png",
            "menu_provider": "single_platform",
            "id": "emmas-pizza-cambridge",
            "image_url": "http://s3-media1.ak.yelpcdn.com/bphoto/2hQL7fOJBbvDRFwyjZFoig/ms.jpg",
            "location": {
                "state_code": "MA",
                "postal_code": "02139",
                "country_code": "US",
                "address": [
                "40 Hampshire St"
                ],
                "display_address": [
                "40 Hampshire St",
                "Kendall Square/MIT",
                "Cambridge, MA 02139"
                ],
                "neighborhoods": [
                "Kendall Square/MIT"
                ],
                "city": "Cambridge"
            },
            "display_phone": "+1-617-864-8534",
            "categories": [
                [
                "Pizza",
                "pizza"
                ]
            ],
            "phone": "6178648534",
            "rating": 4.0,
            "is_closed": "false",
            "rating_img_url_small": "http://s3-media4.ak.yelpcdn.com/assets/2/www/img/f62a5be2f902/ico/stars/v1/stars_small_4.png",
            "url": "http://www.yelp.com/biz/emmas-pizza-cambridge",
            "review_count": 393,
            "name": "Emma's Pizza",
            "snippet_text": "Amazing pizza IF you buy by the pie and not by the slice.  The by the slice pizza has a thicker crust, and the sauce and cheese is a bit disappointing.Get...",
            "is_claimed": "true",
            "distance": 717.6735284455011,
            "mobile_url": "http://m.yelp.com/biz/emmas-pizza-cambridge",
            "rating_img_url": "http://s3-media4.ak.yelpcdn.com/assets/2/www/img/c2f3dd9799a5/ico/stars/v1/stars_4.png"
            }
        ],
        "region": {
            "span": {
            "latitude_delta": 0.016601640000004636,
            "longitude_delta": 0.012890020000014601
            },
            "center": {
            "longitude": -71.09150969999999,
            "latitude": 42.3739441
            }
        },
        "total": 3
        }"""
        
        #content = json.dumps(jsonResponse)              # dumpt it out as json
        #content = json.loads(str(jsonResponse))  
        #content = json.dumps(content)  
        
        #self.response.headers["Content-Type"] = "application/json"
        #self.response.write(content)
        
        #logging.info(content["total"])    
            
app = webapp2.WSGIApplication([
    ("/", MainHandler)
], debug=True)
