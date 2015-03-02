import nmap


# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

class MainPage():
    def get(self):
        greetings_query = Greeting.query(ancestor=guestbook_key()).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        template = jinja_environment.get_template('index.html')
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout ' + users.get_current_user().nickname()
            self.response.out.write(template.render(greetings=greetings,
                                                    url=url,
                                                    url_linktext=url_linktext))
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            self.response.out.write(template.render(url=url,
                                                    url_linktext=url_linktext))


class Guestbook():
    def post(self):
        greeting = Greeting(parent=guestbook_key())

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()
        self.redirect('/')

nm = nmap.PortScanner()
nminfo = nm.scan(hosts='10.1.10.0/24', arguments='-sP')
print nminfo
