from typing import List
from django.shortcuts import render
from django.db.models.aggregates import Count
from posts_collections.views import Collection
from django.db.models import Q
from django.views.generic import ListView
from django.http import HttpResponseRedirect, request
from api.views import delete_changing_folder
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import PostHistory, CollectionsHistory
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date


class Writers(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'writers/writers_queue.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['title'] = 'Admin' if int(self.request.GET.get('w', 0)) else 'Writer'
        context['accessed'] = int(self.request.GET.get('w', 0))
        return context

    def get_queryset(self):
        if self.request.user.has_perm('posts_collections.view_writers_admin_queue') and int(self.request.GET.get('w', 0)) or self.request.user.is_superuser:
            collections = self.model.objects.annotate(
                posts_count = Count('posts', filter=Q(
                    posts__changed = self.request.GET.get('w', 0),
                    posts__edited = False
                ))
            ).filter(for_changing=True) 
        elif self.request.user.is_superuser and not int(self.request.GET.get('w', 0)): 
            collections = self.model.objects.annotate(
                posts_count = Count('posts', filter=Q(
                    posts__changed = self.request.GET.get('w', 0)
                ))
            ).filter(for_changing=True)
        elif not self.request.user.is_superuser and int(self.request.GET.get('w', 0)):
            raise PermissionDenied()
        else:
            collections = self.model.objects.annotate(
                posts_count = Count('posts', filter=Q(
                    posts__changed = self.request.GET.get('w', 0)
                ))
            ).filter(members__id=self.request.user.id, for_changing=True)
        return_data = []
        for i in collections.prefetch_related("members").order_by('title'):
            if len(i.members.all()) != 0:
                return_data.append(i)
            else:
                i.for_changing = False
        return return_data


class Writers_posts(LoginRequiredMixin, ListView):
    model = Collection

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        obj = self.get_object()
        context['collection_id'] = self.kwargs.get('pk')
        context['collection_writer'] = obj.members.all()
        return context

    def get_template_names(self):
        access = int(self.request.GET.get('w', 0))
        if self.request.user.is_superuser or self.request.user.has_perm('posts_collections.view_writers_admin_queue'):
            template_name = 'writers/writer_admin.html' if access else 'writers/writer.html'
        elif not self.request.user.is_superuser and not access:
            template_name = 'writers/writer.html'
        elif (not self.request.user.is_superuser or not self.request.user.has_perm('posts_collections.view_writers_admin_queue'))  and access:
            raise PermissionDenied()
        return template_name

    def post(self, request, *args, **kwargs):
        if 'approve' in request.POST and (self.request.user.is_superuser or self.request.user.has_perm('posts_collections.view_writers_admin_queue') ):
            obj = self.get_object().posts.filter(changed=self.request.GET.get('w', False), edited=False)
            obj.update(edited=True, edited_data=date.today())
            delete_changing_folder()
            return HttpResponseRedirect('/writer/?w=1')

        if 'Autor_to_collection' in request.POST and (self.request.user.is_superuser or self.request.user.has_perm('posts_collections.view_writers_admin_queue') ):
            print(request.POST.get("Autor_to_collection"))
            obj = self.get_object()
            obj.members.remove(User.objects.get(username=request.POST.get("Autor_to_collection")))
            obj.save()
            return self.get(request, *args, **kwargs)
        return self.get(request, *args, **kwargs)

    def get_object(self):
        obj = Collection.objects.get(pk=self.kwargs.get('pk'))
        return obj

    def get_queryset(self):
        return self.get_object().posts.filter(changed=self.request.GET.get('w', False), edited=False).prefetch_related('collections', 'tags')


class Collections_history(LoginRequiredMixin, ListView):
    model = CollectionsHistory
    template_name = 'writers/history_queue.html'

    def get_queryset(self):
        collections = self.model.objects.annotate(
            posts_count = Count('collections_history', filter=Q(
                collections_history__post__edited = True
            ))
        )
        return collections


class History_posts(LoginRequiredMixin, ListView):
    model = PostHistory
    template_name = 'writers/posts_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        return context

    def get_object(self):
        obj = CollectionsHistory.objects.get(pk=self.kwargs.get('pk'))

        # order_by('-id')
        return obj

    def get_queryset(self):
        return self.get_object().collections_history.prefetch_related('writer', 'post', 'post__collections').filter(post__changed=True, post__edited=True)

