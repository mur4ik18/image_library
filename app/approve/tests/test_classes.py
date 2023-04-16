from django.test import TestCase
from posts.models import Post, Tag
from approve.upload import *
import glob
from advanced_search.models import IgnoreList 
# Create your tests here.

class Importing(TestCase):
    def setUp(self):
        # IgnoreList.objects.create(title="Alex")
        pass
    
    def tearDown(self):
        pass
    
    # file type
    def test_upload_ignore_list_csv(self):
        print("test_upload_ignore_list_csv")
        file = "test_ignore_list.csv"
        self.assertFalse(check_if_excel(file))
    
    def test_upload_ignore_list_txt(self):
        print("test_upload_ignore_list_csv")
        file = "test_ignore_list.csv"
        self.assertFalse(check_if_excel(file))
    
    def test_upload_ignore_list_xlsx(self):
        print("test_upload_ignore_list_xlsx")
        file = "test_ignore_list.xlsx"
        self.assertTrue(check_if_excel(file))
        
    def test_upload_ignore_list_xlsm(self):
        print("test_upload_ignore_list_xlsm")
        file = "test_ignore_list.xlsm"
        self.assertTrue(check_if_excel(file))
    
    def test_upload_ignore_list_xlsx(self):
        print("test_upload_ignore_list_xltx")
        file = "test_ignore_list.xltx"
        self.assertTrue(check_if_excel(file))
    
    def test_upload_ignore_list_xltm(self):
        print("test_upload_ignore_list_xltm")
        file = "test_ignore_list.xltm"
        self.assertTrue(check_if_excel(file))
    
    # check if uploading works
    def test_upload_ignore_list(self):
        print("test_upload_ignore_list")
        file = "test_files/test_ignore_list.xlsx"
        lis = IgnoreListUpload(file, 1).parse_data()
        self.assertEqual(len(lis), 2)