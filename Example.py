import TwitterClient

def main():
    Twitter = TwitterClient.TwitterClient()

    if Twitter.login('account', 'passowrd'):
    	print('Signed into %s'%  Twitter.Account)
        
    	# for a in Twitter.getFollowing('leagues', True):
    	# 	print(a)

    	# Messages = ['Message 1','Message2']

    	# for Message in Messages:
    	# 	Twitter.directMessage('lol', Message)

    	# Accs ['lol','a','op']	

    	# for Acc in Accs:
    	# 	Twitter.follow(Acc)	
    else:
    	print('Sign in failed')


if __name__ == '__main__':
    main()
