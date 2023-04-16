from django.db import models
# Create your models here.
smal_length = 250
big_length = 500
cap_length = 10000

class Tag(models.Model):
    tag_name = models.CharField(blank=True, max_length=250)
    def __str__(self) -> str:
        return f"{self.tag_name}"

class Post(models.Model):
    collections = models.ManyToManyField('posts_collections.Collection',blank=True, related_name='posts')
    author = models.CharField(max_length=smal_length)
    post_url = models.CharField(max_length=smal_length,blank=True)
    image = models.ImageField(upload_to = 'imagines/images/', blank=True)
    date = models.CharField(max_length=smal_length, blank=True)
    likes = models.IntegerField(blank=True, default=0)
    #likes = models.IntegerField(blank=True)
    comments = models.IntegerField(blank=True)
    image_field = models.TextField(max_length=big_length, blank=True)
    caption = models.TextField(max_length=cap_length, blank=True)
    mentions = models.CharField(max_length=cap_length, blank=True)
    text_comments = models.TextField(max_length=cap_length, blank=True)
    tags_list = models.TextField(max_length=cap_length, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tag_posts', blank=True)
    hashtags = models.CharField(max_length=cap_length, blank=True)
    
    # for adding new fields
    alt_name = models.TextField(max_length=150, blank=True)
    file_name = models.TextField(max_length=500,blank=True)
    
    changed = models.BooleanField(blank=True, default=False)
    
    # admin
    edited = models.BooleanField(blank=True, default=False)
    edited_data = models.CharField(max_length=smal_length, blank=True)
    
    accessed = models.BooleanField(blank=True, default=True)
    folder_buy_author = models.ManyToManyField('approve.Non_approved', related_name='posts_in_folder')
    unique_field = models.CharField(max_length=big_length, unique=True, default=f"{author}_{str(post_url).split('/')[-1]}")

    website = models.CharField(max_length=big_length, blank=True, default="0")
    
    #ai part
    ai_caption = models.TextField(max_length=cap_length, blank=True)
    ai_description = models.TextField(max_length=cap_length, blank=True)

    def __str__(self) -> str:
        return f"{self.author}{self.date}" 

    def change_unique_to_default(self):
        self.unique_field = f"{self.author}_{str(self.post_url).split('/')[-2]}"