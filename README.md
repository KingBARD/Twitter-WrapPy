Twitter WrapPy
=========

Twitter WrapPy is a twitter wrapper that **doesn't** use the offical API


Version
----


Alpha



List of current functions
--------------
* Login
* Tweet
* Retweet
* Favorite
* Delete Tweet
* Direct Message
* Get Tweets(Returns a list of tweets)
* Get Followers/Following(Returns a list of accounts)
* Get Trends (Returns a list of trends)
* Change Profile Settings (Location, Username Etc)


Login Example
--------------

```sh
    Twitter = TwitterClient.TwitterClient()

    if Twitter.login('account', 'passowrd'):
    	print('Signed into %s' %  Twitter.Account)
    else:
        print('Sign in failed')
```
Tweeting Example
---------------

```sh

    Twitter = TwitterClient.TwitterClient()

    Twitter.login('account', 'passowrd')
    
    Messages = ['First Tweet','Second Tweet','Third??']
    
    for Message in Messages:
        Twitter.tweet(Message)
        
```

License
----

MIT


