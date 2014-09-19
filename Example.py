import TwitterClient

def main():

    Twitter = TwitterClient.TwitterClient()

    if Twitter.login('account, password'):
    	print('Signed into %s' %  Twitter.Account)
    else:
    	print('Sign in failed')
    
if __name__ == '__main__':
    main()
