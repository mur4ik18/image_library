from posts.models import Post, Tag
from posts_collections.models import Collection
from approve.models import Non_approved


def create_post(author, id) -> object:
    obj = Non_approved.objects.get_or_create(name="militarywife_farmhouse_life")
    key = str(f'https://www.instagram.com/p/CUaON55FYpb{id}/').split('/')[-1]
    if len(key) <= 3:
        key = str(f'https://www.instagram.com/p/CUaON55FYpb/{id}').split('/')[-2]
    post = Post.objects.create(
        unique_field=author + '_' + key,
        author=author,
        post_url=f'https://www.instagram.com/p/CUaON55FYpb{id}/',
        image='imagines/images/militarywife_farmhouse_life770821500431.jpg',
        date='2021-09-29 17:57:50',
        likes='586',
        comments='99',
        image_field='Happy',
        caption='Happy hump',
        mentions='asa',
        text_comments='das',
        alt_name='',
        file_name='',
        changed=False,
        edited=False,
        accessed=True,
        )
    post.folder_buy_author.add(obj[0].id)
    return post


def create_collection(name) -> object:
    return Collection.objects.create(
        title = name
    )
