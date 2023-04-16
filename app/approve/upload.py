import os
import sys

from posts_collections.models import Collection
import stat
from .models import Non_approved
os.environ['DJANGO_SETTINGS_MODULE'] = 'text_project.settings'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
import django
django.setup()
from posts.models import Post
import openpyxl
import requests
import shutil
import random
import time
from tutorial.settings import *
from advanced_search.models import IgnoreList  
import logging
from django.core.exceptions import BadRequest
logger = logging.getLogger(__name__)

def check_if_excel(uploaded_file):
        if ".xlsx" in uploaded_file or ".xlsm" in uploaded_file or ".xltx" in uploaded_file or ".xltm" in uploaded_file:
            return True
        else:
            return False

class Upload():
    def __init__(self, uploaded_file, test):
        if not test:
            uploaded_file = uploaded_file.get("file")
        self.postes = []
        self.file_name = self.get_file(uploaded_file)
        self.author = self.file_name
        self.wb = openpyxl.load_workbook(uploaded_file)
        # i use it for parsing 
        self.ws = self.wb.active

    def get_file(self, uploaded_file):
        return str(uploaded_file).split('.xlsx')[0]
        
class IgnoreListUpload(Upload):
    def parse_data(self):
        '''
            for row in self.ws:
                if row[0].value:
                    IgnoreList.objects.get_or_create(title=row[0].value)
        '''
        return [IgnoreList.objects.get_or_create(title=row[0].value) for row in self.ws if row[0].value]
            
class UploadingProducts(Upload):
    def parse_data(self):
        data = []
        t = 1
        z = 0
        obj = Non_approved.objects.get_or_create(name=self.author)
        for row in self.ws:
            if z == 0:
                z+=1
                continue
            if row[2].value:
                # download image
                key = str(row[1].value).split('/')[-1]
                if len(key) <=3 :
                    key = str(row[1].value).split('/')[-2]
                unique_field = self.author+ '_' + key
                print(t)
                post = Post.objects.filter(unique_field = unique_field)
                if len(post) == 0:
                    try:
                        web = row[12].value if row[12].value != None else "0"
                    except IndexError as e:
                        web = "0"
                    response = requests.get(row[2].value, stream=True)
                    image_name = self.author+str(random.randint(0,1000000000000))
                    with open(f'mediafiles/imagines/images/{image_name}.jpg', 'wb') as out_file:
                        shutil.copyfileobj(response.raw, out_file)
                    del response
                    
                        
                    post = Post.objects.create(
                        unique_field = unique_field,
                        author = self.author if row[0].value == '' or row[0].value == None else row[0].value,
                        post_url = row[1].value,
                        image = f'imagines/images/{image_name}.jpg',
                        date = str(row[3].value),
                        likes = row[4].value if row[4].value != None else 0,
                        comments = 0 if row[5].value == None else row[5].value,
                        image_field = '' if row[6].value == None else row[6].value,
                        caption = '' if type(row[7].value) != str else row[7].value,
                        mentions = '' if type(row[9].value) != list else row[9].value,
                        text_comments = row[10].value,
                        changed = False,
                        edited = False,
                        accessed = False,
                        hashtags = row[8].value if row[8].value != None else '',
                        website = web,
                    )
                    t+=1
                    
                    post.folder_buy_author.add(obj[0].id)


def decode_utf8(input_iterator):
    for l in input_iterator:
        yield l.decode('utf-8')

        
import csv
class UploadingCollections(object):
    def __init__(self, request) -> None:
        self.request = request
        self.parse_data()            

    def parse_data(self):
        data = []
        rows = csv.DictReader(decode_utf8(self.request.FILES['file']))
        for row in rows:
            data.append(Collection(id=row['id'],title=row['title']))
        Collection.objects.bulk_create(data)


class UploadingRelations(object):
    def __init__(self, request) -> None:
        self.request = request
        self.parse_data()            

    def parse_data(self):
        data = []
        rows = csv.DictReader(decode_utf8(self.request.FILES['file']))
        for row in rows:
            post = Post.objects.filter(id=int(row['post_id']))
            if len(post)==1:
                coll = Collection.objects.filter(id=int(row['coll_id']))
                if len(coll)==1:
                    post[0].collections.add(coll[0])

class UploadingPosts(object):
    def __init__(self, request) -> None:
        self.request = request
        self.parse_data()            

    def parse_data(self):
        data = []
        rows = csv.DictReader(decode_utf8(self.request.FILES['file']))
        for row in rows:
            key = row['post_url'].split('/')[-1]
            if len(key) <=3 :
                key = row['post_url'].split('/')[-2]
                
            data.append(Post(
                id = row['id'],
                author = row['author'],
                post_url = row['post_url'],
                image = row['image'],
                date = row['date'],
                likes = row['likes'],
                comments = row['comments'],
                image_field = row['image_field'],
                caption = row['caption'],
                mentions = row['mentions'],
                text_comments = row['text_comments'],
                hashtags = row['hashtags'],
                alt_name = row['alt_name'],
                file_name = row['file_name'],
                changed = row['edited'],
                edited = row['edited'],
                accessed = 1,
                unique_field = row['author'] + "_" + key,
                ))
        Post.objects.bulk_create(data,ignore_conflicts=True)
