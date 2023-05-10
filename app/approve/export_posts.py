import csv

def download_all_data(data_):
    header_names = ['postID', 'account', 'post_url', 'image', 'date', 'likes', 'comments',
                            'caption', 'hashtags', 'mentions', 'text_comments', 'site_description','tags',
                            'alt_name','image_title','collections','edited','account_link']

    with open('files/export.csv', 'w', newline='') as csvfile:
        fieldnames = header_names
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in data_:
            writer.writerow({
                'postID': data['postID'],
                'account': data['author'],
                'post_url': data['post_url'],
                'image': data['custom_image'],
                'date': data['date'],
                'likes': data['likes'],
                'comments': data['comments'],
                'caption': data['caption'],
                'hashtags': data['hashtags'],
                'mentions': data['mentions'],
                'text_comments': data['text_comments'],
                'site_description': data['image_field'],
                'tags': ', '.join([i['tag_name'] for i in data['tags']]),
                'alt_name': data['alt_name'],
                'image_title': data['file_name'],
                'collections': ', '.join([i['title'] for i in data['collections']]),
                'edited': data['edit'],
                'account_link': data['account_link'],
            })
