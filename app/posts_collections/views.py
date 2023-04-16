from django.shortcuts import render
from django.views.generic import ListView
from .models import Collection
from django.db.models.aggregates import Count
from posts.models import *
from django.http import HttpResponse, HttpResponseRedirect
from .download_collections import download_data
from django.db.models import Q
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

class Collections(ListView):
    model = Collection
    template_name = 'collections/collections.html'

    def get_queryset(self):
        collections = self.model.objects.annotate(
            posts_count = Count('posts', filter=Q(
                posts__accessed=True))
        ).order_by('-title')
        return collections

    def post(self,request, *args, **kwargs):
        if 'create_collection_name' in request.POST:
            title = request.POST.get('create_collection_name')
            Collection.objects.get_or_create(title=str(title))
            return self.get(request,*args, **kwargs)

class Collections_solo(ListView):
    template_name = 'collections/one_collection_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['writers'] = User.objects.filter(groups__name='writer')
        context['title'] = obj.title
        context['collection_id'] = obj.id
        context['collection_writer'] = obj.members.all()
        return context

    def get_object(self):
        obj = Collection.objects.get(pk=self.kwargs.get('pk'))
        return obj

    def get_queryset(self):
        collections= self.get_object().posts.all().filter(accessed=True).prefetch_related('tags', 'collections').order_by('author')
        return collections

    def post(self, request,*args, **kwargs):
        if 'rename_input' in request.POST:
            coll = self.get_object()
            coll.title = request.POST.get("rename_input")
            coll.save()
            return self.get(request,*args, **kwargs)
        
        if 'delete_collection' in request.POST:
            coll = self.get_object()
            coll.delete()
            return HttpResponseRedirect('/collection/')
        
        if 'download_collection' in request.POST:
            obj=self.get_object()
            data = {}
            t=1
            for each_post in obj.posts.all():
                tags = []
                for i in each_post.tags.all():
                    tags.append(str(i))

                data['p'+str(t)] = {
                    'numbers': str(t),
                    'account': each_post.author,
                    'post_url': each_post.post_url,
                    'image': each_post.image,
                    'date': each_post.date,
                    'likes': str(each_post.likes),
                    'comments': str(each_post.comments),
                    'caption': each_post.caption,
                    'hashtags': each_post.hashtags,
                    'mentions': each_post.mentions,
                    'text_comments': each_post.text_comments,
                    'Image_credit': each_post.image_field,
                    'tags': ', '.join(tags)
                }
                t+=1
            download_data(obj.title, data)
            
            f = open(f'files/{obj.title}.xlsx', 'rb')
            response = HttpResponse(f.read(), content_type='application/excel')
            response['Content-Disposition'] = 'attachment; filename=%s' % f"{obj.title}.xlsx"
            return response
            return self.get(request,*args, **kwargs)

        if 'send_to_writer' in request.POST:
            user = request.POST.get('sellect_to_send')
            obj = self.get_object()
            obj.posts.all().update(edited=False,changed=False)
            obj.for_changing = True 
            obj.save()
            obj.members.add(User.objects.get(id=user))
            return HttpResponseRedirect('/collection/')
    
        if 'send_to_writer_non' in request.POST:
            user = request.POST.get('sellect_to_send')
            obj = self.get_object()
            obj.posts.all().update()
            obj.for_changing = True 
            obj.save()
            obj.members.add(User.objects.get(id=user))
            return HttpResponseRedirect('/collection/')


class Collections_experimental(Collections):
    template_name = 'collections/collections_exp.html'
    
class Collections_solo_experimental(Collections_solo):
    template_name = 'collections/one_collection_page_exp.html'