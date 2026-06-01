#!/usr/bin/env python3

import requests
import time
import json
import sys

class DCodeXFriendRemover:
    def __init__(self, cookie):
        self.cookie = cookie
        self.session = requests.Session()
        self.session.cookies.set('.ROBLOSECURITY', cookie)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Origin': 'https://www.roblox.com',
            'Referer': 'https://www.roblox.com/',
            'Content-Type': 'application/json'
        })
        self.user_id = None
        self.csrf_token = None
        self.request_delay = 3.0
        
    def get_csrf_token(self):
        try:
            response = self.session.post('https://auth.roblox.com/v2/logout')
            if 'x-csrf-token' in response.headers:
                self.csrf_token = response.headers['x-csrf-token']
                return True
            else:
                return False
        except Exception as e:
            return False
    
    def get_user_info(self):
        try:
            headers = {}
            if self.csrf_token:
                headers['X-CSRF-TOKEN'] = self.csrf_token
                
            response = self.session.get('https://users.roblox.com/v1/users/authenticated', headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.user_id = data['id']
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def get_all_friends(self):
        friends = []
        cursor = None
        
        while True:
            try:
                url = f'https://friends.roblox.com/v1/users/{self.user_id}/friends'
                if cursor:
                    url += f'?cursor={cursor}'
                
                headers = {}
                if self.csrf_token:
                    headers['X-CSRF-TOKEN'] = self.csrf_token
                
                response = self.session.get(url, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'data' in data and data['data']:
                        friends.extend(data['data'])
                    
                    cursor = data.get('nextPageCursor')
                    if not cursor:
                        break
                    
                    time.sleep(0.5)
                else:
                    break
                    
            except Exception as e:
                break
        
        return friends
    
    def unfriend_user(self, friend_id, friend_name, retry_count=0):
        try:
            time.sleep(self.request_delay)
            
            headers = {'X-CSRF-TOKEN': self.csrf_token} if self.csrf_token else {}
            
            response = self.session.post(
                f'https://friends.roblox.com/v1/users/{friend_id}/unfriend',
                headers=headers
            )
            
            if response.status_code == 200:
                return True, None
            elif response.status_code == 429:
                if retry_count < 3:
                    wait_time = 5 * (retry_count + 1)
                    print(f'WAIT {wait_time}s - RATE LIMIT...')
                    time.sleep(wait_time)
                    return self.unfriend_user(friend_id, friend_name, retry_count + 1)
                else:
                    return False, 'RATE LIMITED'
            elif response.status_code == 403:
                if self.get_csrf_token():
                    headers = {'X-CSRF-TOKEN': self.csrf_token}
                    retry_response = self.session.post(
                        f'https://friends.roblox.com/v1/users/{friend_id}/unfriend',
                        headers=headers
                    )
                    if retry_response.status_code == 200:
                        return True, None
                    else:
                        return False, f'CSRF ERROR {retry_response.status_code}'
                else:
                    return False, 'CSRF TOKEN FAILED'
            else:
                return False, f'HTTP {response.status_code}'
                
        except Exception as e:
            return False, str(e)
    
    def remove_all_friends(self):
        if not self.get_csrf_token():
            print('CSRF TOKEN FAILED')
            return False
        
        if not self.get_user_info():
            print('AUTH FAILED')
            return False
        
        friends = self.get_all_friends()
        
        if not friends:
            print('NO FRIENDS FOUND')
            return False
        
        print(f'FRIENDS: {len(friends)}')
        
        confirm = input(f'REMOVE {len(friends)} FRIENDS? (yes/no): ')
        if confirm.lower() != 'yes':
            print('CANCELLED')
            return False
        
        removed = 0
        failed = 0
        
        for i, friend in enumerate(friends, 1):
            friend_id = friend['id']
            friend_name = friend.get('name', f'ID:{friend_id}')
            
            print(f'[{i}/{len(friends)}] REMOVING: {friend_name}... ', end='')
            
            success, error = self.unfriend_user(friend_id, friend_name)
            
            if success:
                removed += 1
                print('OK')
            else:
                failed += 1
                print(f'FAIL ({error})')
        
        print(f'REMOVED: {removed}')
        print(f'FAILED: {failed}')
        
        return removed > 0


def get_cookie_from_user():
    cookie = input('ENTER .ROBLOSECURITY COOKIE: ').strip()
    
    if not cookie:
        print('COOKIE EMPTY')
        return None
    
    return cookie


def main():
    cookie = get_cookie_from_user()
    if not cookie:
        input('PRESS ENTER TO EXIT...')
        sys.exit(1)
    
    remover = DCodeXFriendRemover(cookie)
    
    try:
        remover.remove_all_friends()
    except KeyboardInterrupt:
        print('INTERRUPTED')
    except Exception as e:
        print(f'ERROR: {e}')
    
    input('PRESS ENTER TO EXIT...')


if __name__ == '__main__':
    main()