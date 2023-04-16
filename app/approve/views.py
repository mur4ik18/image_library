from django.db.models.aggregates import Count
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.views import APIView
from posts.models import Post
import csv
import logging
from .upload import *
from posts_collections.models import Collection
from .models import Non_approved
from django.http import HttpResponse, HttpResponseRedirect
from .serializers import PostsSerializer 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from asgiref.sync import sync_to_async
logger = logging.getLogger(__name__)


def upload_file(object):
    UploadingProducts(object, 0).parse_data()


def ignore_list(object):
    IgnoreListUpload(object, 0 ).parse_data()


def imp(request):
    if request.user.has_perm('approve.add_non_approved'):
        pass
    else:
        raise PermissionDenied
    if request.POST and 'upload' in request.POST:
        logger.error('start')
        file = request.FILES.getlist('files')#['files']
        print(file)
        for i in file:
            async_function = sync_to_async(upload_file({"file":i}))
    if request.POST and 'ignore_list' in request.POST:
        file = request.FILES['file']
        async_function = sync_to_async(ignore_list({"file":file}))


    return render(request, 'import/load.html')
    
class ExportCSV(APIView):
    def get(self, request, *args, **kwargs):
        count = request.query_params.get('count')
        all = request.query_params.get('all')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        header_names = ['postID', 'account', 'post_url', 'image', 'date', 'likes', 'comments',
                            'caption', 'hashtags', 'mentions', 'text_comments', 'site_description','tags',
                            'alt_name','image_title','collections','edited','account_link']
        if all == '1' and all != None:
            if count!=None:
                posts = Post.objects.annotate(collections_num = Count('collections')).filter(edited=True).prefetch_related('collections','tags') 
                if len(posts) > int(count):
                    posts = posts[len(posts)-int(count):]
                else:
                    posts = posts
            else:
                posts = Post.objects.annotate(collections_num = Count('collections')).filter(edited=True).prefetch_related('collections','tags')
        elif all == 'all' and all != None:
            posts = Post.objects.annotate(collections_num = Count('collections')).prefetch_related('collections','tags')
        else:
            if count!=None:
                posts = Post.objects.exclude(edited_data__exact='').order_by('edited_data').annotate(collections_num = Count('collections')).filter(edited=True).prefetch_related('collections','tags') 
                if len(posts) > int(count):
                    posts = posts[len(posts)-int(count):]
                else:
                    posts = posts
            else:
                posts = Post.objects.exclude(edited_data__exact='').order_by('edited_data').annotate(collections_num = Count('collections')).filter(edited=True).prefetch_related('collections','tags')

        serializer = PostsSerializer(posts, many=True)
        fieldnames = header_names
        writer = csv.DictWriter(response, fieldnames=fieldnames)

        writer.writeheader()
        for data in serializer.data:
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
                'account_link': data['account_link']})
        return response

class NonApproved(LoginRequiredMixin,ListView):
    model = Non_approved
    template_name = 'import/non_impruved.html'
    context_object_name = 'name_folder'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['accessed'] = int(self.request.GET.get('accessed', 0))
        return context

    def get_queryset(self):
        if self.request.user.has_perm('approve.view_non_approved'):
            pass
        else:
            raise PermissionDenied 
        folders = self.model.objects.annotate(
            posts_count=Count('posts_in_folder', filter=Q(
                posts_in_folder__accessed=self.request.GET.get('accessed', True)))
        ).filter(posts_count__gte=0)
        return folders.order_by('name')


class Folder(LoginRequiredMixin,ListView):
    def get_template_names(self):
        if self.request.user.has_perm('approve.view_non_approved'):
            pass
        else:
            raise PermissionDenied 
        access = int(self.request.GET.get('accessed', 0))
        template_name = 'import/approved_solo.html' if access else 'import/non_improved_solo.html'
        return template_name

    def get_object(self):
        obj = Non_approved.objects.get(pk=self.kwargs.get('pk'))
        return obj

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['accessed'] = int(self.request.GET.get('accessed', 0))
        context['title'] = self.get_object().name
        context['pk'] = self.kwargs.get('pk')
        context['collections'] = Collection.objects.all().order_by('title')
        return context

    def get_queryset(self):
        return self.get_object().posts_in_folder.filter(accessed=self.request.GET.get('accessed', False)).prefetch_related("tags", "collections") 


    def post(self,request, *args, **kwargs):  
        if self.request.user.has_perm('approve.change_non_approved'):
            pass
        else:
            raise PermissionDenied 
        if 'Aprove_all' in request.POST:
            obj = self.get_object().posts_in_folder.filter(accessed=self.request.GET.get('accessed', False)).prefetch_related("tags")
            obj.update(accessed=True)
            return HttpResponseRedirect('/import/non_approved/?accessed=0')
        if "delete_collection" in request.POST:
            obj = self.get_object().posts_in_folder.filter(accessed=self.request.GET.get('accessed', False)).prefetch_related("tags")
            for i in obj:
                i.delete()
            return HttpResponseRedirect('/import/non_approved/?accessed=0')
        if "rename_button" in request.POST:
            obj = self.get_object()
            title = obj.name
            new_title = request.POST.get("rename_input")
            if new_title != "":
                posts = Post.objects.filter(author=title)
                for i in posts:
                    i.author = new_title
                    i.save()
                obj.name = new_title
                obj.save()
            return self.get(request, *args, **kwargs)
