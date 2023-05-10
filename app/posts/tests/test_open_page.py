from django.test import Client, TestCase
from posts.models import Post, Tag
from .models_for_test import *

# # написать тесты для всех запросов по апи

class Test_open_page(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = create_post("militarywife_farmhouse_life",1)
        self.collection = create_collection("test")
        self.post.collections.add(self.collection.id)

    def test_post_page(self):
        response = self.client.get(f'/post/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_import_non_approved(self):
        response = self.client.get(f'/import/non_approved/?accessed=0')
        self.assertEqual(response.status_code, 302)

    def test_import_approved(self):
        response = self.client.get(f'/import/non_approved/?accessed=1')
        self.assertEqual(response.status_code, 302)

    def test_queue_writer_admin(self):
        response = self.client.get(f'/writer/?w=1')
        self.assertEqual(response.status_code, 302)

    def test_queue_writer(self):
        response = self.client.get(f'/writer/?w=0')
        self.assertEqual(response.status_code, 302)

    def test_collections_all_(self):
        response = self.client.get(f'/collection/')
        self.assertEqual(response.status_code, 403)

    def test_collections_all(self):
        response = self.client.get(f'/collection/{self.collection.id}/')
        self.assertEqual(response.status_code, 200)
