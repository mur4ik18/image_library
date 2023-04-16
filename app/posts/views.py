from django.shortcuts import get_object_or_404, render

from posts_collections.models import Collection
from .models import *
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


class Posts_page(DetailView):
    template_name = 'posts/page.html'
    model = Post

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['comments'] = self.get_object().text_comments.split("', '")
        collections = Collection.objects.all().order_by('title')
        context['collcount'] = len(collections)
        context['collections'] = collections
        return context
        

    def get_object(self):
        return get_object_or_404(
            self.model, 
            pk=self.kwargs.get('pk')
            )

    def post(self,request, *args, **kwargs):
        if 'image_field_text' in request.POST:
            if request.POST.get("image_field_text") != '' or request.POST.get("image_field_text") != ' ' or request.POST.get("image_field_text") != None:
                post = get_object_or_404(Post, pk=request.POST.get("post_page_image_field"))
                post.image_field = request.POST.get("image_field_text")
                post.save()
                return self.get(request, *args, **kwargs)
        
        if 'page_alt_name' in request.POST:
            if request.POST.get("page_alt_name") != '' and request.POST.get("page_alt_name") != ' ' and request.POST.get("page_alt_name") != None:
                post = get_object_or_404(Post, pk=request.POST.get("post_page_alt_name"))
                post.alt_name = request.POST.get("page_alt_name")
                post.save()
                return self.get(request, *args, **kwargs)

        if 'page_file_name' in request.POST:
            if request.POST.get("page_file_name") != '' and request.POST.get("page_file_name") != ' ' and request.POST.get("page_file_name") != None:
                post = get_object_or_404(Post, pk=request.POST.get("post_page_file_name"))
                post.file_name = request.POST.get("page_file_name")
                post.save()
                return self.get(request, *args, **kwargs)

        if 'delete_that_post' in request.POST:
            post = get_object_or_404(Post, pk=request.POST.get("delete_that_post")).delete()
            return HttpResponseRedirect('/')

        if 'create_collection_name' in request.POST:
            title = request.POST.get('create_collection_name')
            print(title)
            Collection.objects.get_or_create(title=str(title))
            return self.get(request,*args, **kwargs)

        if 'sellect_to_save_in_collection' in request.POST:
            collid = request.POST.get('sellect_to_save_in_collection')
            obj = self.get_object()
            collection = Collection.objects.get(title=collid)
            obj.collections.add(collection.id)
            return self.get(request,*args, **kwargs)