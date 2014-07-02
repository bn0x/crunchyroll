crunchyroll
===========

crunchyroll api library in python
very basic..

```python
import crunchyroll

instance = crunchyroll.Crunchyroll('YOUR EMAIL OR USER', 'YOUR PASSWORD')
getPopular = instance.batch()
firstItemOfPopular = getPopular['data'][0]['body']['data'][0]
print("Name: %s"%firstItemOfPopular['name'])
series_id = firstItemOfPopular['series_id']
print("Series ID: %s"%series_id)
collection_id = instance.list_collections(series_id=series_id)['data'][0]['collection_id']
print("Collection ID: %s"%collection_id)
media_id = instance.list_media(collection_id=collection_id)['data'][1]['media_id']
print("Media ID: %s"%media_id)
episode_url = instance.get_episodes(media_id=media_id)
print("You can watch the episode at: %s" % 
episode_url['data'][1]['body']['data']['stream_data']['streams'][0]['url'])
```
