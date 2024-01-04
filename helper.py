from bs4 import BeautifulSoup
import pandas as pd

def get_url_and_name(div_item):
    a_tag = div_item.find('a')
    url = a_tag['href']
    name = a_tag.text
    return url, name

def load_html_file(f):
    soup = BeautifulSoup(f)
    div = soup.find_all('div', class_='pam')
    output = {get_url_and_name(div_item) for div_item in div}
    return output

def make_clickable(url, text):
    return f'<a target="_blank" href="{url}">@{text}</a>'

def get_people_who_unfollow_me(follow, following):
    follower_set = load_html_file(follow)
    following_set = load_html_file(following)
    unfollowers = (following_set - follower_set)
    unfollowers = [make_clickable(i[0], i[1]) for i in unfollowers]
    output = pd.DataFrame(unfollowers, columns=['Users'])
    output = output.sort_values(by=['Users']).reset_index(drop=True)
    
    return output
