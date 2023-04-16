from django.test.testcases import TestCase
from posts.models import Post, Tag
from .models_for_test import *

class Test_posts(TestCase):
    def setUp(self) -> None:
        Tag.objects.create(tag_name='tag1')
        self.post = create_post("militarywife_farmhouse_life",1)
        
    def test_check_creating(self):
        post = Post.objects.all()
        self.assertTrue(True if post[0].author == 'militarywife_farmhouse_life' else False)
        
    def test_add_alt_post(self):
        post = Post.objects.all()[0]
        post.alt_name = "test"
        post.save()
        self.assertTrue(True if post.alt_name == 'test' else False)
        
    def test_add_page_file_name_post(self):
        post = Post.objects.all()[0]
        post.file_name = "test"
        post.save()
        self.assertTrue(True if post.file_name == 'test' else False)
        
    def test_check_unique_field(self):
        post = Post.objects.all()[0]
        self.assertTrue(True if post.unique_field == 'militarywife_farmhouse_life_CUaON55FYpb' else False)
    
    def test_check_add_tag(self):
        post = Post.objects.all()[0]
        tag = Tag.objects.all()[0]
        post.tags.add(tag)
        self.assertTrue(True if post.tags.all()[0].tag_name == 'tag1' else False)
        
    def test_check_remove_tag(self):
        post = Post.objects.all()[0]
        tag = Tag.objects.all()[0]
        post.tags.add(tag)
        post.tags.remove(tag)
        self.assertTrue(True if len(post.tags.all()) == 0 else False)
        
    # grand test for testing all posibilites in fields
    def test_chenging_num_comments_posts(self):
        post = Post.objects.all()[0]
        numbers = [1, 0, -3, 2032321, -321, 3.4]
        try:
            for i in numbers:
                post.comments = i
                post.save()
            self.assertTrue(True)
        except:
            self.assertTrue(False)
    
    def test_chenging_num_likes_posts(self):
        post = Post.objects.all()[0]
        numbers = [1, 0, -3, 2032321, -321, 3.4]
        try:
            for i in numbers:
                post.likes = i
                post.save()
            self.assertTrue(True)
        except:

            self.assertTrue(False)