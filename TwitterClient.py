import requests, re, urllib

POSTHEADERS = {'Host': 'twitter.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Referer': 'https://twitter.com/',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': 0,
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
        }

USERAGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'}

Session = requests.session()

global Password
global Account
global Token

class TwitterClient():

    ##What a piece of shit this is
    def getFollowing(self, link, followers = False):

        Links = []

        if not followers:
            link = 'https://mobile.twitter.com/{0}/following'.format(link)
        else:
            link = 'https://mobile.twitter.com/{0}/followers'.format(link)

        def get(url):

            S = Session.get(url)

            Source = S.text.encode('utf-8')

            return Source

        def Regex(source):

            pattern = re.compile(r'<a href="/(.*?)"><span class="username"><span>@</span>(.*?)</span></a>',re.MULTILINE) 

            for (a,b) in re.findall(pattern,source):
                Links.append('https://www.twitter.com/' + a)

            if 'Show more people' in source:
                patt = re.compile(r'<div class="w-button-more"><a href="(.*?)">Show more people</a></div>',re.MULTILINE)
                nextPage = re.search(patt, source).group(1)
                nextPage = 'https://mobile.twitter.com' + nextPage
                Regex(get(nextPage)) 

        Source = get(link)

        Regex(Source)

        return Links

                

    ##Also a piece of shit
    def getAllTweetLinks(self, link):

        Links = []

        link = 'https://mobile.twitter.com/' + link

        def getTimeline(url):
            try:
                S = Session.get(url)

                Source = S.text.encode('utf-8')

                return Source

            except:  
                pass

        def Regex(source):

            pattern = re.compile(r'<a name="(.*?)" href="(.*?)">(.*?)</a>', re.MULTILINE)
            
            for (a,l,c) in re.findall(pattern, source):
                Links.append('http://www.twitter.com' + l)

            if 'Load older' in source:
                patt = re.compile(r'<a href="(.*?)">Load older Tweets</a></div>',re.MULTILINE)

                a = re.search(patt, source).group(1)

                Regex(getTimeline(a)) 

        Source = getTimeline(link)

        Regex(Source)

        return Links

    def changeUrl(self, url):

        data = {
            'authenticity_token':self.Token,
            'page_context':'me',
            'section_context':'profile',
            'user[url]':url
        }

        response = Session.post('https://twitter.com/i/profiles/update',headers=POSTHEADERS,data=data,allow_redirects=False)

        if 'Url is not valid' in response.text:
            return False

        elif 'user_url' in response.text:
            return True

    def changeLocation(self, loc):

        data = {
            'authenticity_token':self.Token,
            'page_context':'me',
            'section_context':'profile',
            'user[location]':loc
        }

        response = Session.post('https://twitter.com/i/profiles/update',headers=POSTHEADERS,data=data)

        if 'Thanks, your settings have been saved.' in response.text:
            return True
        else:
            return False

    def changeDescription(self, desc):

        data = {
                'authenticity_token':self.Token,
                'page_context':'me',
                'section_context':'profile',
                'user[description]':desc
            }

        response = Session.post('https://twitter.com/i/profiles/update', headers=POSTHEADERS, data=data)

        if 'Thanks, your settings have been saved.' in response.text:
            return True
        else:
            return False


    def changeUsername(self, newusername):

        data = {
                '_method':'PUT',
                'authenticity_token':self.Token,
                 'user[screen_name]': newusername,
                 'auth_password':self.Password
                }

        response = Session.post('https://twitter.com/settings/accounts/update', data=data, headers=POSTHEADERS)


        if 'That username has been taken. Please choose another.' in response.text:
            return False
        elif 'Thanks, your settings have been saved.' in response.text:
            return True
        else:
            return False



    def changeEmail(self, email):

        data = {'_method':'PUT',
        'authenticity_token': self.Token,
        'user[screen_name]': self.Account,
         'user[email]':email,
         'auth_password': self.Password}

        response = Session.post('https://twitter.com/settings/accounts/update', data=data, headers=POSTHEADERS)

        if 'This email address is already registered.' in response.text:
            return False
        elif 'A message has been sent to you to confirm your new email address.' in response.text:
            return True
        else:
            return False


    def directMessage(self, user, message):

        data = {'authenticity_token': self.Token,
        'lastMsgId':'',
        'screen_name':user,
        'scribeContext[component]':'dm_existing_conversation_dialog',
        'text':message
        }

        response = Session.post('https://twitter.com/i/direct_messages/new', data=data, headers=POSTHEADERS)

        if message in response.text:
            return True
        elif response.status_code == 404:
            return False

    def deletetweet(self, tweet):
        
        tweet = tweet.split('/')[5]

        data = {'_method':'DELETE',
        'authenticity_token': self.Token,
        'id':tweet
        }

        response = Session.post('https://twitter.com/i/tweet/destroy',data=data, headers=POSTHEADERS, allow_redirects=False)
 
        if 'Your tweet has been deleted.' in response.text:
            return True
        elif response.status_code == 404:
            return False
        else:
            return False

    def fav(self, tweet, delete = False):

        tweet = tweet.split('/')[5]
        print(tweet)
        if delete:
            url = 'https://twitter.com/i/tweet/unfavorite'
        else:
            url = 'https://twitter.com/i/tweet/favorite'

        data = {'authenticity_token': self.Token,
                    'id': tweet
                }

        response = Session.post(url, headers=POSTHEADERS, data=data)

        if 'Favorited 1 time' in response.text:
            return True
        else:
            return False

    def follow(self, user, follow = True):

        if not follow:
            url = 'https://twitter.com/i/user/unfollow'
        else:
            url = 'https://twitter.com/i/user/follow'

        request = Session.get('https://www.twitter.com/{0}'.format(user))

        userID = re.search('<div class="ProfileNav" role="navigation" data-user-id="(.*?)">',request.text).group(1)

        data = {'authenticity_token': self.Token,
        'challenges_passed':'false',
        'handles_challenges':'1',
        'inject_tweet':'false',
        'user_id':userID}


        response = Session.post(url, headers=POSTHEADERS, data=data)

        if response.status_code == 404:
            return False
        if response.status_code == 200:
            return True


    def getTrends(self):#Login not required

        request = requests.get('https://mobile.twitter.com/trends')
        trends = []
        pattern = re.compile('<a href=\"/search(.*?)">\n(.*?)\n')

        for match in re.findall(pattern, request.text):
            a = match[1]
            a = a.strip()
            trends.append(a)

        return trends

    def reTweet(self, tweet, retweet = True):

        tweet = tweet.split('/')[5]

        if not retweet:
            url = "https://twitter.com/i/tweet/unretweet"
        else:
            url = 'https://twitter.com/i/tweet/retweet'

        data = {'authenticity_token':self.Token,
                'id':tweet
                }

        response = Session.post(url,headers=POSTHEADERS,data=data)

        if 'Tweets' in response.text:
            return True
        else:
            return False


    def tweet(self, message, reply = False, statusID = str):

        data = {'authenticity_token': self.Token,
                'place_id':'',
                'tagged_users':''
        }

        if reply:
            user = statusID.split('/')[3]
            statusID = statusID.split('/')[5]
            data.update({'in_reply_to_status_id':statusID})
            message = '@{0} '.format(user + message)
            data.update({'status':message})

        else:
            data.update({'status':message})

        response = Session.post('https://twitter.com/i/tweet/create', data=data, headers=POSTHEADERS)

        errmsg = 'Oh dear! You already tweeted that'

        if errmsg in response.text or response.status_code == 404:
            return False
        elif response.status_code == 200:
            return True
        

    def login(self, account, password):

        account = account.lower()

        request = Session.get('https://www.twitter.com/',
                            headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Host': 'twitter.com',})
        
        Account,self.Account = account,account
        Password,self.Password = password,password
        Token,self.Token = re.search('value="(.*?)">',request.text).group(1),re.search('value="(.*?)">',request.text).group(1)

        data = urllib.urlencode({

            'authenticity_token': urllib.quote(self.Token),
            'redirect_after_login':'/',
            'scribe_log': '',
            'return_to_ssl':'true',
            'session[password]': urllib.quote(password),
            'session[username_or_email]': urllib.quote(account),
            })


        response = Session.post('https://www.twitter.com/sessions', headers=POSTHEADERS, data=data)

        pageSource = response.text.lower()

        if 'user-style-' + account in pageSource:
            return True
        else:
            return False