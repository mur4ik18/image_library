from posts.models import Post, Tag
from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.template import loader
from django.db.models.aggregates import Count
from posts_collections.views import Collection
from django.db.models import Q
from approve.models import Non_approved
from writers.models import PostHistory, CollectionsHistory
import requests
import json
from datetime import date
import os


def capitalaze(text):

    if len(text) < 2:
        return ""
    else:
        url = f"https://capitalize-my-title.p.rapidapi.com/title/ap/{text}"
        headers = {
            "X-RapidAPI-Key": os.environ.get("RapidAPI", 'no'),

            "X-RapidAPI-Host": "capitalize-my-title.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers)
        print(response.__dict__)
        if response.json()["code"] == 200:
            return response.json()["data"]["output"]
        else:
            return text


def delete_post(request):
    post_id = request.POST.get('post_id')
    get_object_or_404(Post, pk=post_id).delete()
    return JsonResponse({"success": True})


def approve_post(request):
    post_id = request.POST.get('post_id')
    obj = get_object_or_404(Post, pk=post_id)
    obj.accessed = True
    obj.save()
    return JsonResponse({"success": True})


def add_new_tag(request):
    post_id = request.POST.get('post_id')
    tag_name = request.POST.get('tag_name')
    tag = Tag.objects.get_or_create(tag_name=tag_name)
    obj = get_object_or_404(Post,pk=post_id)
    obj.tags.add(tag[0].id)
    obj.tags_list += f"|{tag_name}"
    obj.save()
    posts_html = loader.render_to_string('import/non_improved_tags.html', {'project':obj})
    output_data = {'posts_html': posts_html}
    return JsonResponse(output_data)

def delete_tag(request):
    post_id = request.POST.get('post_id')
    tag_name = request.POST.get('tag_name')
    tag = Tag.objects.get(tag_name=tag_name)
    obj = get_object_or_404(Post,pk=post_id)
    obj.tags.remove(tag.id)
    obj.tags_list = ''.join(obj.tags_list.split(f"|{tag_name}"))
    obj.save()
    posts_html = loader.render_to_string('import/non_improved_tags.html', {'project':obj})
    output_data = {'posts_html': posts_html}
    return JsonResponse(output_data)

def delete_post_form_collection(request):
    post_id = request.POST.get('post_id')
    collid = request.POST.get('collid')
    obj = get_object_or_404(Post, pk=post_id)
    obj.collections.remove(collid)
    return JsonResponse({"success":True})

def add_to_collection(request):
    post_id = request.POST.get('post_id')
    collid = request.POST.get('collection_id')
    obj = get_object_or_404(Post, pk=post_id)
    collection = Collection.objects.get(title=collid)
    obj.collections.add(collection.id)
    return JsonResponse({"success":True})


def delete_changing_folder():
    collections = Collection.objects.annotate(
        writer_post_count = Count('posts', filter=Q(
            posts__changed = 0,
            posts__edited = False
        )),
        admin_post_count = Count('posts', filter=Q(
            posts__changed = 1,
            posts__edited = False
        ))
    ).filter(for_changing=True)
    for i in collections:
        print(i.writer_post_count, i.admin_post_count)
        if i.writer_post_count == 0 and i.admin_post_count == 0:
            i.for_changing = False
            i.save()

def approve_writer(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post,pk=post_id)
    post.edited = True
    post.edited_data = date.today()
    post.save()
    delete_changing_folder()
    return JsonResponse({"success":True})

def send_to_revision(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post,pk=post_id)
    post.changed = False
    post.save()
    return JsonResponse({"success":True})

def collections_massive_add_tag(request):
    coll_id = request.POST.get('collid')
    name_tag = request.POST.get('tag')
    tag = Tag.objects.get_or_create(tag_name=name_tag)
    obj = get_object_or_404(Collection, pk=coll_id)
    for ob in obj.posts.all():
        ob.tags.add(tag[0].id)
        ob.tags_list += f"|{name_tag}"
        ob.save()

    return JsonResponse({"success" : True})

def collections_massive_add_tag_for_folders(request):
    coll_id = request.POST.get('collid')
    name_tag = request.POST.get('tag')
    tag = Tag.objects.get_or_create(tag_name=name_tag)
    obj = get_object_or_404(Collection, pk=coll_id)
    for ob in obj.posts.all():
        ob.tags.add(tag[0].id)
        ob.tags_list += f"|{name_tag}"
        ob.save()
    return JsonResponse({"success" : True})

def approve_massive_add_tag(request):
    coll_id = request.POST.get('collid')
    name_tag = request.POST.get('tag')
    tag = Tag.objects.get_or_create(tag_name=name_tag)
    obj = get_object_or_404(Non_approved, pk=coll_id)
    for ob in obj.posts_in_folder.all():
        ob.tags.add(tag[0].id)
        ob.tags_list += f"|{name_tag}"
        ob.save()
    return JsonResponse({"success" : True})

# massive collections add/del
def bulk_collection_add(request):
    posts = request.POST.get('posts_id')
    print(posts)
    collection_name= request.POST.get('collection_name')
    collection = Collection.objects.get(title=collection_name)
    for post_id in posts.split(','):
        post = Post.objects.get(pk=int(post_id))
        post.collections.add(collection.id)
    
    return JsonResponse({"success" : True})

def bulk_delete(request):
    posts = request.POST.get('posts_id')
    print(posts)
    for post_id in posts.split(','):
        post = Post.objects.get(pk=int(post_id))
        if post: post.delete()
    
    return JsonResponse({"success" : True})

def bulk_approve(request):
    posts = request.POST.get('postsid')
    print(posts)
    for post_id in posts.split(','):
        post = Post.objects.get(pk=int(post_id))
        post.accessed = True
        post.save()   
    return JsonResponse({"success" : True})






# Writers
# approuve and massive changes
def approve(request):
    arr = request.POST.get("result")
    res = json.loads(arr)
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post,pk=post_id)

    post.changed = True
    for box_box in res:
        box = res[box_box]
        if box["name"] == 'image_field_text':
            post.image_field = box["textaria"]
        elif box["name"] == 'page_file_name':
            # capitalaze(tank[0])
            post.file_name = capitalaze(box["textaria"])
        post.save()
    post.save()
    
    col = CollectionsHistory.objects.get_or_create(title=get_object_or_404(Collection, pk=request.POST.get('collection_id')).title)[0]
    
    ph = PostHistory.objects.create(
        post = get_object_or_404(Post,pk=post_id),
        writer = request.user,
        image_field = post.image_field,
        file_name = post.file_name
    )
    ph.collections.add(col.id)
    
    return JsonResponse({"success":True})

def massive_post_data_update(request):
    arr = request.POST.get("result")
    res = json.loads(arr)
    for box_box in res:
        box = res[box_box]
        post = get_object_or_404(Post,pk=box["id"])
        if box["name"] == 'image_field_text':
            post.image_field = box["textaria"]
        elif box["name"] == 'page_file_name':
            # capitalaze(tank[0])
            post.file_name = box["textaria"] #capitalaze(box["textaria"])
        post.save()
    return JsonResponse({"success":True})

def change_post_data(request):
    # result = {
    #   name
    #   id
    #   collection_id
    #   textaria 
    # }
    arr = request.POST.get("result")
    res = json.loads(arr)
    
    post_id = res["id"]
    name = res["name"]
    text = res["textaria"]
    post = get_object_or_404(Post,pk=post_id)

    if name == 'image_field_text':
        post.image_field = text
        post.save()
        return JsonResponse({"success":True, "text": text})   
    elif name == 'page_file_name':
        if request.POST.get("admin"):
            post.file_name = text
            post.save()
            return JsonResponse({"success":True, "text": text})     
        else:
            r = text #capitalaze(text)
            post.file_name = r
            post.save()
            return JsonResponse({"success":True, "text": r})     
    post.save()

    return JsonResponse({"success":True})

def massive_save_for_writers(request):
    # result[$(el).data('post_id')] = {
    #     "name": $(el).attr('name'),
    #     "id": $(el).data('post_id'),
    #     "collection_id": $(el).data('coll_id'),
    #     "gram": $(el).val(),
    #     "textaria": $(el).find("textarea").val(),
    #   }
    # box["name"], box["id"], box["collection_id"], box["gram"], box["textaria"]
    arr = request.POST.get("result")
    res = json.loads(arr)    
    for box_box in res:
        box = res[box_box]
        if box["gram"] == "" and box["textaria"] == "":
            continue
        else:
            text = box["gram"] if box["gram"] != "" else box["textaria"] if box["textaria"] != "" else ""
            if text == "":
                continue
            
            post = get_object_or_404(Post,pk=box["id"])
            if box["name"] == "page_file_name":
                post.file_name = box["textaria"] #capitalaze(text)
            elif box["name"] == "image_field_text":
                post.image_field = text
            post.save()
    return JsonResponse({"success":True})


"""
from posts.models import Post, Tag
for i in Post.objects.all():
    if len(i.tags.all()) > 0:
        for j in i.tags.all(): 
            i.tags_list += f"|{j.tag_name}"
            i.save()
            print(f"{i.tags.all()} > {i.tags_list}" )

"""
