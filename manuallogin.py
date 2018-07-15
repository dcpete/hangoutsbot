# As of July 2018, login doesn't work with the normal install.
# This will let you save the cookie
# You'll probably have to create the cache directory
# After, copy refresh_token.txt to /data/cookies.json
# https://github.com/tdryer/hangups/issues/350
import os, hangups, requests, appdirs

print('Open this URL:')
print(hangups.auth.OAUTH2_LOGIN_URL)

authorization_code = input('Enter oauth_code cookie value: ')

with requests.Session() as session:
    session.headers = {'user-agent': hangups.auth.USER_AGENT}
    access_token, refresh_token = hangups.auth._auth_with_code(
        session, authorization_code
    )

dirs = appdirs.AppDirs('hangups', 'hangups')
token_path = os.path.join(dirs.user_cache_dir, 'refresh_token.txt')
hangups.auth.RefreshTokenCache(token_path).set(refresh_token)
