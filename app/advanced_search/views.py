from django.views.generic import View, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from posts_collections.models import Collection
from django.http.response import JsonResponse
from django.views.generic.base import ContextMixin
from django.db.models import Q
from functools import reduce
import operator
from django.core.exceptions import PermissionDenied
from posts.models import Post
from .serializers import PostsSerializer
from django.core.paginator import Paginator, Page
from django.db.models.aggregates import Count
from .models import IgnoreList
from silk.profiling.profiler import silk_profile


class DSEPaginator(Paginator):
    def __init__(self, *args, **kwargs):
        super(DSEPaginator, self).__init__(*args, **kwargs)
        self._count = self.object_list.hits.total

    def page(self, number):
        # returned the sliced data already.
        number = self.validate_number(number)
        return Page(self.object_list, number, self)


class Search_main(View, ContextMixin):
    template_name = "search/main.html"

    def get(self, request, *args, **kwargs):
        if request.user.has_perm("posts.can_search"):
            pass
        else:
            raise PermissionDenied

        context = self.get_context_data(**kwargs)
        template = loader.get_template(self.template_name)
        if request.GET.get("search_text") is None:
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect("/search/")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context["collections_list"] = Collection.objects.all().order_by(
                "title"
                )
        return context


class Search(ListView):
    paginate_by = 4
    context_object_name = 'posts'
    data = None
    model = Post

    def __init__(self):
        self.query = None
        self.paginator = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collections_list"] = Collection.objects.all().order_by("title")
        context["query"] = self.query
        return context

    @silk_profile(name='Search Post')
    def post(self, request):
        page = int(request.POST.get('page', '1'))
        start = (page-1) * 300
        end = start + 300
        self.options = request.POST.getlist('options[]')

        if request.POST.get('lazy_load') == '1':
            x = [i for i in request.POST.getlist('query')[0].split(',')]
            self.query = [
                [x[0], x[1], x[2]],
                [x[3], x[4], x[5]],
                [x[6], x[7], x[8]],
                [x[9], x[10], x[11]],
                [x[12], [13], x[14]]
            ]
        else:
            self.query = [request.POST.getlist(f'querry{i}[]') for i in range(1, 6)]
        print(self.query)
        self.data = self.search(self.query)
        num_posts = self.data.count()

        if int(num_posts) > end:
            show_new = 1
        else:
            show_new = 0
        print(show_new)
        serialized = PostsSerializer(self.data[start:end], many=True)
        posts_html = loader.render_to_string('search/search_posts.html',
                                             {"projects": serialized.data},
                                             request=request)
        output_data = {'output_data': posts_html,
                       'show': show_new,
                       'query': self.query,
                       'search_count': num_posts}
        return JsonResponse(output_data)

    @silk_profile(name='Search')
    def search(self, query):
        raw = self._combine_queries(query)
        raw = raw.filter(accessed=True).order_by('-author').prefetch_related(
                'collections').annotate(collections_count=Count('collections'))
        if self.options[-1] == 'true':
            if self.options[0] == 'true' and self.options[1] == 'true':
                raw = raw.filter(collections_count__lte=1)
            elif self.options[0] == 'true' or self.options[1] == 'true':
                if self.options[0] == 'true':
                    raw = raw.filter(collections_count=0)
                else:
                    raw = raw.filter(collections_count=1)
            else:
                raw = raw.filter(collections_count__lte=1)
        else:
            if self.options[0] == 'true' and self.options[1] == 'true':
                pass
            elif self.options[0] == 'true' or self.options[1] == 'true':
                if self.options[0] == 'true':
                    raw = raw.filter(collections_count=0)
                else:
                    raw = raw.filter(collections_count=1)
            else:
                pass
        raw = raw.exclude(author__in=[i.title for i in IgnoreList.objects.all()])
        return raw

    def _combine_queries(self, query):
        raw = None
        ignore = []
        for row in range(len(query)):
            if row in ignore:
                continue
            if query[row][0] == "":
                continue
            if raw is None:
                filter_kwargs = self._get_filter_kwargs(query[row])
                list_of_Q = [Q(**{key: val}) for key, val in filter_kwargs.items()]
                if self._check_next_query_row(query, row):
                    filter_kwargs = self._get_filter_kwargs(query[row+1])
                    [list_of_Q.append(Q(**{key: val})) for key, val in filter_kwargs.items()]
                    ignore.append(row+1)
                    if self._check_next_query_row(query, row+1):
                        filter_kwargs = self._get_filter_kwargs(query[row+2])
                        [list_of_Q.append(Q(**{key: val})) for key, val in filter_kwargs.items()]
                        ignore.append(row+2)
                        if self._check_next_query_row(query, row+2):
                            filter_kwargs = self._get_filter_kwargs(query[row+3])
                            [list_of_Q.append(Q(**{key: val})) for key, val in filter_kwargs.items()]
                            ignore.append(row+3)
                            if self._check_next_query_row(query, row+3):
                                filter_kwargs = self._get_filter_kwargs(query[row+4])
                                [list_of_Q.append(Q(**{key: val})) for key, val in filter_kwargs.items()]
                                ignore.append(row+4)
                    raw = Post.objects.filter(reduce(operator.or_, list_of_Q))
                else:
                    raw = Post.objects.filter(reduce(operator.or_, list_of_Q))
            elif raw is not None:
                filter_kwargs = self._get_filter_kwargs(query[row])
                list_of_Q = [Q(**{key: val}) for key, val in filter_kwargs.items()]
                if self._check_next_query_row(query, row):
                    filter_kwargs = self._get_filter_kwargs(query[row+1])
                    [list_of_Q.append(Q(**{key: val})) for key, val in filter_kwargs.items()]
                    raw = raw.filter(reduce(operator.or_, list_of_Q))
                    ignore.append(row+1)
                else:
                    raw = raw.filter(reduce(operator.or_, list_of_Q))
        return raw

    def _get_filter_kwargs(self, row):
        coll_list = [
            'author',
            'date',
            'image_field',
            'text_comments',
            'mentions',
            'caption',
            'tags_list',
            'ai_caption',
            'ai_description',
        ]
        filter_kwargs = {}
        if row[1] == 'all':
            for coll in coll_list:
                self._create_query(filter_kwargs, coll, row[0])
        elif row[1] in coll_list:
            self._create_query(filter_kwargs, row[1], row[0])
        return filter_kwargs

    def _check_next_query_row(self, query, row):
        if len(query) > row+1:
            if query[row+1][0] != "":
                return True if query[row+1][2] == 'true' else False
            else:
                return False
        else:
            return False

    def _create_query(self, filter, field, x_data):
        if field == 'author':
            filter["author__icontains"] = x_data
        elif field == 'date':
            filter["date__icontains"] = x_data
        elif field == 'image_field':
            filter["image_field__icontains"] = x_data
        elif field == 'text_comments':
            filter["text_comments__icontains"] = x_data
        elif field == 'mentions':
            filter["mentions__icontains"] = x_data
        elif field == 'caption':
            filter["caption__icontains"] = x_data
        elif field == 'tags_list':
            filter["tags_list__icontains"] = x_data
        elif field == 'ai_caption':
            filter["ai_caption__icontains"] = x_data
        elif field == 'ai_description':
            filter["ai_description__icontains"] = x_data
