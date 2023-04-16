from django.urls import path
from . import views

urlpatterns = [
    path('delete_post/', views.delete_post, name="delete_post"),
    path('approve_post/', views.approve_post, name="approve_post"),
    path('add_new_tag/', views.add_new_tag, name="add_new_tag"),
    path('delete_tag/', views.delete_tag, name="delete_tag"),
    path('delete_post_form_collection/', views.delete_post_form_collection,
         name="delete_post_form_collection"),
    path('add_to_collection/', views.add_to_collection,
         name="add_to_collection"),
    path('change_post_data/', views.change_post_data, name='change_post_data'),
    path('massive_post_data_update/', views.massive_post_data_update,
         name='massive_post_data_update'),
    path('approve/', views.approve, name='approve'),
    path('approve_writer/', views.approve_writer, name='approve_writer'),
    path('send_to_revision/', views.send_to_revision, name='send_to_revision'),
    path('collections_massive_add_tag/', views.collections_massive_add_tag,
         name='collections_massive_add_tag'),
    path('approve_massive_add_tag/', views.approve_massive_add_tag,
         name='approve_massive_add_tag'),
    path('massive_save_for_writers/', views.massive_save_for_writers,
         name='massive_save_for_writers'),
    path('bulk_approve/', views.bulk_approve, name='bulk_approve'),
    path('bulk_delete/', views.bulk_delete, name='bulk_delete'),
    path('bulk_collection_add/', views.bulk_collection_add,
         name='bulk_collection_add'),
]
