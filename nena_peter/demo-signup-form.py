#!/usr/bin/python
# coding: latin-1

Site = 'Peter and Nena'

Timezone = 'Pacific/Honolulu'

Colors = '''
    base03:    #002b36;
    base02:    #073642;
    base01:    #586e75;
    base00:    #657b83;
     base0:    #839496;
     base1:    #93a1a1;
     base2:    #eee8d5;
     base3:    #fdf6e3;
    yellow:    #b58900;
    orange:    #cb4b16;
       red:    #dc322f;
   magenta:    #d33682;
    violet:    #6c71c4;
      blue:    #268bd2;
      cyan:    #2aa198;
     green:    #859900;
''' # - http://ethanschoonover.com/solarized

Analytics = '''<script>


</script>'''


# - HTML Page Code

main_page_html = '''<style>

</style>
<div class="page_html">
 <header class="hi"><span class="color_b">Hi</span></header>

</div><!-- - /page_html - -->'''

form_page_html = '''<style>
.form_wrap { margin-left: 55px; margin-top: 35px; outline: 1px solid #eee; width: 345px; padding: 45px; }
tr { height: 32px; }
td.label { font-size: 14px; text-align: right; padding-right: 10px; }
input[type="text"] { width: 200px; height: 16px; }
</style>
<div class="page_html">
 <header class="hi"><span class="color_b">Fill Out The Form</span></header>
  <article class="form_wrap">
    <form action="../../add_form" enctype="multipart/form-data" method="post">
      <table>
        <tr>
          <td class="label">Email Addess</td>
          <td class="input"><input type="text" name="email_address" /></td>
        </tr>
        <tr>
          <td class="label">User Name</td>
          <td class="input"><input type="text" name="user_name" /></td>
        </tr>
        <tr>
          <td></td>
          <td style="text-align:right"><input type="submit" value="Sign Up" /></td>
        </tr>
      </table>
    </form>
  </article><!-- - /form_wrap - -->
</div><!-- - /page_html - -->'''


entries_page_html = '''<style>
.text_wrap { margin-left: 65px; }
.fav {background-color: #F8BBD0; width: 300px; height: 50px;}
</style>
<div class="page_html">
 <header class="hi"><span class="color_b">Form Entries</span></header>
  <article class="text_wrap">
    <p>Sign in as an &nbsp; <b><span class="color_a">Admin User</span></b> &nbsp; to view form data</p>
  </article><!-- - /form_wrap - -->
</div><!-- - /page_html - -->'''


entries_page_html_admin = '''<style>
.list_wrap { margin-left: 25px; margin-top: 45px; }
.item_wrap { width: 400px; border-bottom: 1px solid #eee; padding: 15px; padding-bottom: 10px; margin-top: 45px; }
.item_wrap:hover { border-bottom: 1px solid #657b83; }
.right_wrap { float: right; text-align: right; font-size: 12px; }
.right_wrap a { color: #cb4b16; }
.right_wrap a:hover { text-decoration: underline; }
.id_wrap { padding-top 40px; color: #839496; }
.email_address { font-size: 14px; line-height: 20px; }
.your_name { font-size: 22px; color: #073642; }
</style>
<div class="page_html">
 <header class="hi"><span class="color_b">RSVPs</span></header>
  <article class="list_wrap">
    <div class="item_wrap" ng-repeat="item in items">
      <div class="item_data">

        <div class="right_wrap">
          <p><a href ng-click="delete(item.data_id)">Delete</a></p>
          <div class="id_wrap">[!item.data_id!]</div>
        </div><!-- - /right_wrap - -->

        <p><span class="id_wrap">[!item.rsvp_time!]</span>
        <br />
        <span class="your_name">[!item.your_name!]</span>
        <br />
        <span class="email_address">Response: [!item.response!]</span>
        <br />    
        <span class="email_address">[!item.email_address!]</span>
        <br />
        <span class="add_guest">Additional Guests: [!item.add_guest!]</span>
        </p>
        
      </div><!-- - /item_data - -->
    </div><!-- - /item_data - -->
  </article><!-- - /list_wrap - -->
</div><!-- - /page_html - -->'''


code_page_html = '''<style>
.link_wrap { margin-left: 85px; margin-top: 45px; }
</style>
<div class="page_html">
 <header class="hi"><span class="color_b">Code Link</span></header>
  <div class="link_wrap">
    <p>View on &nbsp; <a href="https://github.com/Kyle2501/App-Engine-Parts" target="_blank">GitHub</a></p>
  </div><!-- - /link_wrap - -->
</div><!-- - /page_html - -->'''


# - System
import os
import urllib
import wsgiref.handlers
import webapp2
import json
# - 
from google.appengine.api import users
from google.appengine.api import mail
# -
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
# -
from urlparse import urlparse
# -
import time
import datetime
from pytz.gae import pytz


class Form_db(db.Model):
    addTime = db.DateTimeProperty(auto_now_add=True)
    data_id = db.StringProperty()
  #
    response = db.StringProperty()
    your_name = db.StringProperty()
    email_address = db.StringProperty()
    add_guest = db.StringProperty()
    rsvp_time = db.StringProperty()

class addForm_db(webapp2.RequestHandler):
    def post(self):
        date_time = datetime.datetime.now(pytz.timezone(Timezone)).strftime("%Y%m%d_%H%M%S")
        data_id = date_time
        item = Form_db(key_name=data_id)
        item.data_id = data_id
      # - -
        item.response = self.request.get('response')
        item.your_name = self.request.get('your_name')
        item.email_address = self.request.get('email_address')
        item.add_guest = self.request.get('add_guest')

        item.rsvp_time = datetime.datetime.now(pytz.timezone(Timezone)).strftime("%x")


      #
        item.put()
        time.sleep(1)
        self.redirect('/map')



class deleteData(webapp2.RequestHandler):
    def get(self):
        page_address = self.request.uri
        base = os.path.basename(page_address)
        data_id = base.split('?')[1]
        if users.is_current_user_admin():
            item = db.Query(Form_db).filter('data_id =', data_id).get()
        item.delete()
        time.sleep(1)
        self.redirect('../../list/entries')

invite_page_html = '''

<style>

.page { text-align: center; font-family:'Pacifico'; width: 475px; padding: 20px;}
.heading, span .and, .end, .at, .address, .date, .info  { font-family:'Pacifico'; font-size: 1.25em;}
.reception {font-family: 'Pacifico'; font-size: 1.5em;}
.name { font-family: 'Pacifico'; font-size: 2.5em;}
.place {font-family: 'Pacifico'; font-size: 2em;}
.attire, .attire_info {font-family: 'Pacifico'; font-size: 1em;}


</style>


 <div class="page">
   <img src="../../pics/Wedding_Invites_Final.jpg" style="width:475px; height:650px" />
   
  </div>
'''



rsvp_page_html = '''

<style>
.form_wrap { margin-left: 55px; margin-top: 35px; outline: 5px double #F8BBD0; width: 360px; padding: 45px;}
tr { height: 32px; }
td.label { font-size: 14px; text-align: right; padding-right: 10px; }
input[type="text"] { width: 200px; height: 16px; border: 1px solid #002242;}
.label { font-family: 'Pacifico';}
header {text-align: center;}


</style>

<div class="page">
 <header>Please RSVP Below:</header>
  <article class="form_wrap">
    <form action="../../add_form" enctype="multipart/form-data" method="post">
      <table>
        <tr>
          <td class="label">Your Name</td>
          <td class="input"><input type="text" name="your_name" /></td>
        </tr>
        <tr>
          <td class="label">Email Address</td>
          <td class="input"><input type="text" name="email_address" /></td>
        </tr>
        <tr>
          <td class="label">Will You Be Joining Us?</td>
          <td class="input"><input type="text" name="response" /></td>
        </tr>
        <tr>
          <td class="label">RSVP for Another Guest</td>
          <td class="input"><input type="text" name="add_guest" /></td>
        </tr>

        <tr>
          <td></td>
          <td style="text-align:right"><input type="submit" value="RSVP" /></td>
        </tr>
      </table>
    </form>
  </article><!-- - /form_wrap - -->

</div><!-- - /page_html - -->

'''

map_page_html = '''


<style>

.page { margin: auto;}
.direct {font-family: 'Pacifico'; font-size: 1.5em;}
.directions {padding-left: 75px;}
.header, .warn, header, .address { text-align:center;}
#gmap_canvas {text-align: center; padding-left: 50px;}
.map {padding-left: 60px;}



</style>

  <div class="page">
    <header>Directions</header>
    <p class="warn"><em>Please be aware that digital turn-by-turn directions to the house are often mistaken. We strongly advice guest to follow the directions provided below. Furthermore the house is not visible from the street.</em></p><br/>
  <div class="map">
    <script src='https://maps.googleapis.com/maps/api/js?v=3.exp'></script><div style='overflow:hidden;height:400px;width:500px;'><div id='gmap_canvas' style='height:400px;width:500px;'></div><div><small><a href="http://embedgooglemaps.com">                  embed google maps             </a></small></div><div><small><a href="http://www.autohuren.world/">auto huren</a></small></div><style>#gmap_canvas img{max-width:none!important;background:none!important}</style></div><script type='text/javascript'>function init_map(){var myOptions = {zoom:10,center:new google.maps.LatLng(34.16828,-118.045099),mapTypeId: google.maps.MapTypeId.ROADMAP};map = new google.maps.Map(document.getElementById('gmap_canvas'), myOptions);marker = new google.maps.Marker({map: map,position: new google.maps.LatLng(34.16828,-118.045099)});infowindow = new google.maps.InfoWindow({content:'<strong>The Malhotra Residence</strong><br>336 Sturtevant Dr. Sierra Madre, CA 91024<br>'});google.maps.event.addListener(marker, 'click', function(){infowindow.open(map,marker);});infowindow.open(map,marker);}google.maps.event.addDomListener(window, 'load', init_map);</script>
  </div> <br />

     <div class="direct">From the Westbound 210 Freeway:</div> 
        <p class="directions">Exit Santa Anita<br/>
        Immediate right on Santa Anita Ave. <br/>
        Left on Grand View Ave. <br/>
        Right on Mountain Trail Ave.<br/>
        Right on Sturtevant Dr.</p><br/>

      <div class="direct">From the Eastbound 210 Freeway:</div> 
        <p class="directions">Exit Baldwin <br/>
        Immediate left on Baldwin Ave.<br/>
        Right on Foothill Blvd. <br/>
        Left on San Carlos Rd. <br/>
        San Carlos Rd. becomes Mountain Trail Ave.;<br/> 
        continue onto Mountain Trail<br/>
        Right on Sturtevant Dr.</p><br/>

    </div>
<!-- - /page_html - -->



'''

travel_page_html = '''

<style>

.page {text-align: center; margin: auto;}
.travel {font-family: 'Pacifico'; font-size: 1.5em;}


</style>

<div class="page">

 <header>Travel</header><br />


  <div class="travel">Recommended Airports</div>

    <p>LAX (Los Angeles International Airport)<br/>
    Burbank Airport<br/>
    Long Beach Airport<br/></p>

  <div class="travel">Accommodations</div>

    <p><em>Many of our guests will have, at one time or another, stayed at Chez Malhotra, but unfortunately, we'll be fully booked up in August with family coming from out of town! Here are some alternatives: </em></p>

    <p><a href="">AirBnB ($ to $$$):</a>  If you're traveling in a group or would like to have an authentic Sierra Madre/Pasadena experience, you may enjoy renting a private apartment or space in a someone’s home. Please visit www.airbnb.com for openings. 

    <p><a href="">Rose Bowl Motel ($):</a>  Visitors on a budget may find it more affordable to stay in Eagle Rock (where, after all, Nena and Peter met) than in Sierra Madre or Pasadena. Don't be deterred: Eagle Rock is just a 15-to-20 minute drive from Sierra Madre, and the food scene in the area is fantastic!</p>

    <p><a href="">The Langham ($$$$):</a> Out-of-towners wishing to luxuriate will enjoy this elegant hotel’s expansive gardens, innumerable amenities, and highly attentive staff.</p>






</div><!-- - /page_html - -->


'''

stay_page_html = '''

<style>
.page {text-align: center; margin: auto;}
.la {font-family: 'Pacifico'; font-size: 1.5em;}
</style>

<div class="page">

 <header>Enjoy your Stay</header> <br />

   <div class="la">Arts, Culture, Hiking, and Entertainment In the San Gabriel Valley</div><br />


    <div class="intro"><em>Visitors may be pleasantly surprised to find that they don't have to travel to Central or West L.A. to get a taste of the history, natural beauty, and culture of the Southland.</em></div>

      <p><a href="">The Gamble House:</a> A 1907 architectural gem designed, from foundation to teacup, by the renowned Greene brothers. The home's woodwork is as breathtaking as its history. At 23, Nena was the youngest docent the Gamble House had ever trained.</p>

      <p><a href="">The Huntington Library and Gardens:</a> Peter and Nena fell in love with</p> 

      <p><a href="">Heritage Square Museum:</a> Most of L.A.'s Victorian homes and buildings have been destroyed or fallen into disrepair, but Heritage Square has done a remarkable job of</p>

      <p><a href="">The Norton Simon Museum:</a> Despite its modest size, the Norton Simon is one of Peter and Nena's favorite museums. It has an impressive collection of 19th- and 20th-century Western art, as a vast collection of Asian art, and rotating exhibitions. Be sure to take a stroll through the sculpture garden.</p>

      <p><a href="">The Hollywood Bowl:</a> This  legendary outdoor concert venue hosts a variety of musical concerts to suit every taste. If you're attending a classical or jazz concert, we suggest taking a little picnic and bottle of wine for a magical evening. Some concerts end with fireworks! The Hollywood Bowl is, as its name suggests, in the heart of Hollywood. If you plan to attend one of the many diverse concerts or shows, we recommend taking a shuttle instead of driving and parking, which is often time consuming and expensive.</p>

      <p><a href="">The Academy Theater, Pasadena:</a> This theater, a fixture from Nena's childhood, may not show new movies as soon as they're released, but the tickets are a mere $2/each every day before 6 p.m., and $3 after 6 p.m.!</p>

      <p><a href="">The Laemmle Playhouse 7, Pasadena:</a> If you're after independent, foreign, or critically acclaimed films, look no further. The Laemmle is a small theater that seeks to show good movies regardless of their appeal to the mass market.</p>

      <p><a href="">Hiking:</a> Have $5 in cash on hand if you plan to hike anywhere in Southern California; most trails require a $5 permit to park.</p>

      <p><a href="">Chantry Flats:</a> Follow the trail to Sturtevant Falls for a moderately challenging but rewarding hike.</p>

      <p><a href="">Eaton Canyon:</a> Incredible views from cliffs above a vast ravine. If you're planning on taking children, please take care in ensuring that you keep them away from crumbly cliff edges.</p>
           
  <div class="la">Shopping, Groceries, and Necessities</div>
   
      <p><a href="">Flea Markets ($ to $$$):</a> L.A. has had a love affair with antique vintage goods since well before the dawn of hipsterdom. Whether you're seeking to furnish your home gracefully or pick up a kitschy souvenir, we highly recommend the Pasadena City College (PCC) and Rose Bowl Flea Markets. Arrive early for the best selection or later for the best deals. The PCC market is open the first Sunday of every month, and the Rose Bowl market is open the second Sunday of every month.</p>

      <p><a href="">Old Town Pasadena ($$$):</a> Home to a host of well-known shops like Tiffany's, Lululemon, and Urban Outfitters. There are also a few local shops worth checking out, like the Mexican handicrafts store The Folk Tree.</p>

      <p><a href="">Taylor's Market:</a> Good for produce, meat, and dry goods. Conveniently located in the heart of Sierra Madre's charming downtown.</p>
                
      <p><a href="">Gasoline/Petrol:</a> Arco offers the lowest prices in our neighborhood. There's one at the corner of Foothill Blvd. and Santa Anita Blvd. in Arcadia, and another at the corner of Foothill and Rosemead in Pasadena. Both are a short drive from Sierra Madre.</p> 

      <p><a href="">Westfield Santa Anita ($ to $$$):</a> The Santa Anita mall is a five-minute drive from Sierra Madre.</p>

      <p><a href="">Hastings Ranch ($ to $$$):</a> This neighborhood in north Pasadena--just a short drive from Sierra Madre--is home to Trader Joe's, Rite Aid drug store, Whole Foods Market, Nordstrom Rack, Best Buy, and other major retailers.</p>
           
 </div>
<!-- - /page_html - -->


'''
dining_page_html = '''

<style>
  .page {text-align: center; margin: auto;}
</style>
 <div class="page">

  <header>Recommended Local Dining</header><br/>

    <p><a href="">Mary's Market ($):</a> This cozy and welcoming Sierra Madre sandwich counter opened its doors in 1922 and hasn’t closed since. Go for the food and stick around for the proprietress’ conversation. Open for breakfast and lunch.</p>

    <p><a href="">Bean Town Coffee ($):</a> A Sierra Madre establishment with a dedicated local following. Serves a nice cup of coffee or tea. Open all day and into the evening.</p> 

    <p><a href="">Auntie Em's Kitchen ($$):</a> American comfort food with a local-seasonal twist. Auntie Em's is best known for its baked goods, and hile most will recommend the cupcakes, we suggest you try the seasonal treats--like pluot upside-down cake or strawberry bread pudding. Open for breakfast and lunch. Expect a moderate wait if you go for brunch on a weekend.</p>

    <p><a href="">Cacao Mexicatessen ($$):</a> A trip to L.A. is incomplete without the kind of Mexican meal that feels like a hug from your best friend. Cacao blends authentic cuisine from various regions of Mexico with California fare. Caters to vegetarians and carnivores alike. Open for breakfast, lunch, and dinner.</p>

    <p><a href="">La Grande Orange Cafe ($$):</a> A beautiful old restaurant located near Pasadena's Old Town. With painted vaulted ceilings and roomy booths, you'll get the feel of early-20th century California architecture with your serving of California cuisine. We love the tacos and the key lime pie. Great for dinner. Expect a moderate wait if you go for dinner on a weekend.</p>

    <p><a href="">Din Tai Fung ($$):</a> This dumpling house is as popular with Arcadia's Sanghainese denizens as it is with everyone else. Open for lunch and dinner. Expect a long wait if you go for lunch or dinner of a weekend.</p>

    <p><a href="">Tender Greens ($$):</a>  A great lunch or casual dinner spot. Offers a variety of wonderful salads, vegetable side dishes, sandwiches, and hot dishes. Great for carnivores, vegetarians, and the gluten-free. and Open for lunch and dinner.</p> 

    <p><a href="">Bulgarini Gelato ($$$):</a> This unassuming little gelateria has the best gelati, sorbetti, and granita in L.A. While a </p>

 </div><!-- - /form_wrap - -->
<!-- - /page_html - -->

'''

registry_page_html = '''
<style>
  .page {text-align: center; margin: auto;}
</style>

  <div class="page">
   <header>Registry</header><br />
    <p class="gifts">Because we do not yet have a home to furnish, we will not be registering for gifts.</p>
  </div>

'''


class publicSite(webapp2.RequestHandler):
    def get(self):
      # - page url
        page_address = self.request.uri
        path_layer = urlparse(page_address)[2].split('/')[1]
        base = os.path.basename(page_address)
      # - user
        user = users.get_current_user()
        if users.get_current_user(): # - logged in
          login_key = users.create_logout_url(self.request.uri)
          gate = 'Sign out'
          user_name = user.nickname()
        else: # - logged out
          login_key = users.create_login_url(self.request.uri)
          gate = 'Sign in'
          user_name = 'No User'
      # - app data
        app = Site
        page_name = 'Main'
        page_id = 'main'
        analytics = Analytics
        page_html = invite_page_html
        admin = ''
        if users.is_current_user_admin():
            admin = 'true' 

        if path_layer == 'invite':
            page_id = 'invite'
            page_name = 'Invite'
            page_html = invite_page_html

        if path_layer == 'rsvp':
            page_id = 'rsvp'
            page_name = 'RSVP'
            page_html = rsvp_page_html

        if path_layer == 'map':
            page_id = 'map'
            page_name = 'Map'
            page_html = map_page_html

        if path_layer == 'travel':
            page_id = 'travel'
            page_name = 'Travel'
            page_html = travel_page_html

        if path_layer == 'stay':
            page_id = 'stay'
            page_name = 'Stay'
            page_html = stay_page_html

        if path_layer == 'dining':
            page_id = 'dining'
            page_name = 'Dining'
            page_html = dining_page_html

        if path_layer == 'registry':
            page_id = 'registry'
            page_name = 'Registry'
            page_html = registry_page_html



        if path_layer == 'entries':
            page_id = 'entries'
            page_name = 'Entries'
            if admin == 'true':         
                page_html = entries_page_html_admin #!
            else:
                page_html = entries_page_html

        if path_layer == 'code':
            page_id = 'code'
            page_name = 'Code'
            page_html = code_page_html
               
      # - template
        objects = {
            'Site': app,
            'analytics': analytics,
            'login_key': login_key,
            'gate': gate,
            'user_name': user_name,
            'admin': admin,
          # -
            'path_layer': path_layer,
            'base': base,
            'page_name': page_name,
            'page_id': page_id,
            'page_html': page_html,
            
        }
      # - render
        path = os.path.join(os.path.dirname(__file__), 'html/publicSite.html')
        self.response.out.write(template.render(path, objects))


class listData(webapp2.RequestHandler):
    def get(self):
        page_address = self.request.uri
        base = os.path.basename(page_address)
        if users.is_current_user_admin():
            if base == 'entries':
                q = db.Query(Form_db, projection=(
                  'data_id',
                  'rsvp_time', 
                  'email_address', 
                  'your_name',
                  'response', 
                  'add_guest'
                ))
                db_data = q.order('your_name').fetch(50)
        data = []
        for f in db_data:
            data.append(db.to_dict(f))
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(data))


app = webapp2.WSGIApplication([    # - Pages
    ('/', publicSite),
    ('/form/?', publicSite),
      ('/add_form/?', addForm_db),
      ('/delete/data/?', deleteData),
    ('/entries/?', publicSite),
      ('/list/entries/?', listData),
    ('/invite/?', publicSite),
    ('/rsvp/?', publicSite),
    ('/map/?', publicSite),
    ('/travel/?', publicSite),
    ('/stay/?', publicSite),
    ('/dining/?', publicSite),
    ('/registry/?', publicSite)


], debug=True)

