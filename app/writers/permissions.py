from django.http import Http404
from posts_collections.models import Collection

class WriterPermissionsMixin:
    def has_permissions(self):
        return self.request.user.id in self.get_object().members.all()
    
    def dispatcher(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404
        return super().dispatch(request, *args, **kwargs)