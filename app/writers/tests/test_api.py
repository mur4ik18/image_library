from django.test import TestCase
from django.test import Client
from api.views import *
from posts.models import Post, Tag
from posts_collections.models import Collection
from approve.models import Non_approved

class Importing(TestCase):
    def setUp(self):
        author = "alex"
        id = 0
        obj = Non_approved.objects.get_or_create(name="militarywife_farmhouse_life")
        key = str(f'https://www.instagram.com/p/CUaON55FYpb{id}/').split('/')[-1]
        if len(key) <=3 :
            key = str(f'https://www.instagram.com/p/CUaON55FYpb/{id}').split('/')[-2]
        post = Post.objects.create(
            unique_field = author + '_' + key,
            author= author,
            post_url = f'https://www.instagram.com/p/CUaON55FYpb{id}/',
            image = 'imagines/images/militarywife_farmhouse_life770821500431.jpg',
            date = '2021-09-29 17:57:50',
            likes = '586',
            comments = '99',
            image_field = 'Happy',  
            caption = 'Happy hump',
            mentions = 'asa',
            text_comments = 'das',
            alt_name = '',
            file_name = '',
            changed = False,
            edited = False,
            accessed = True,
        )
        post.folder_buy_author.add(obj[0].id)
    
    def tearDown(self):
        pass
    
    # massive_post_data_update
    def test_massive_post_data_update_1_normal_good_request(self):
        # data = {"0": { "name": "page_file_name","id": "0", "collection_id": "0", "gram": "", "textaria": "test1",}, "1": {"name": "page_file_name","id": "1","collection_id": "0","gram": "test","textaria": '',}}
        # c = Client() #above, from django.test import TestCase,Client
        # #optional, but may be necessary for your configuration: c.login("username","password")
        # response = c.post('/api/massive_save_for_writers', data, follow=True)
        # self.assertEqual(response.status_code, 200)
        pass

    def test_massive_post_data_update_2_with_slash(self):
        pass
    
    def test_massive_post_data_update_3_with_back_slash(self):
        pass
    
    def test_massive_post_data_update_4_with_not_accepted_keys(self):
        pass