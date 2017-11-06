from facebook import GraphAPI
from urllib.parse import quote
import requests
import settings


# Creates a Bit.ly link, add utm info
def build_link(link):
    link = link.split('?')[0]
    link += '?utm_source=fact_checking_bot'
    url = link.replace(':', '%3A').replace('/', '%2F')
    token = settings.BITLY_TOKEN
    bitly_request = f'https://api-ssl.bitly.com/v3/shorten?access_token={token}&longUrl={url}'
    try:
        return requests.get(bitly_request).json()['data']['url']
    except KeyError:
        return link


def get_url_info(url):
    '''
    Capture opengraph data from links.
    It tries to get everything from Facebook.
    TO DO: Have a default image when no image is found
    '''
    token = settings.FACEBOOK_TOKEN
    fb_graph = GraphAPI(access_token=token, version='2.10')
    fb_info = fb_graph.get_object(
        id=quote(url),
        fields=['engagement,og_object{image,description,title,updated_time}']
        )
    if fb_info:
        try:
            return dict(
                thumbnail=fb_info['og_object']['image'][0]['url'],
                facebook_shares=fb_info['engagement']['share_count'],
                title=fb_info['og_object']['title'],
                description=fb_info['og_object']['description'],
                source=url.split('/')[2]
                )
        except KeyError:
            from webpreview import web_preview
            metadata = web_preview(url)
            return dict(
                thumbnail=metadata[2],
                facebook_shares=fb_info['engagement']['share_count'],
                title=metadata[0],
                description=metadata[1],
                source=url.split('/')[2]
                )
    else:
        return dict(
            thumbnail='', facebook_shares=0, title='',
            description='', source=url.split('/')[2]
            )
