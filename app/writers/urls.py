from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Writers.as_view(), name='writers_q'),
    path('posts/<int:pk>/', views.Writers_posts.as_view(), name='writers_posts'),
    path('posts_history/', views.Collections_history.as_view(), name="posts_history"),
    path('posts_history/<int:pk>/', views.History_posts.as_view(), name="posts_history_collections"),
    # path('writer/<int:collection_id>', views.writer, name='writer'),
    # path('writer_update_post/', views.writer_update, name='writer_update_post'),
    # path('post_add_tag_writer/', views.post_add_tag_writer, name='post_add_tag_writer'),
    # path('post_remove_tag_writer/', views.post_remove_tag_writer, name='post_remove_tag_writer'),
    # path('adminpost_add_tag_writer/', views.adminpost_add_tag_writer, name='adminpost_add_tag_writer'),
    # path('adminpost_remove_tag_writer/', views.adminpost_remove_tag_writer, name='adminpost_remove_tag_writer'),
    # path('massive_write_update/', views.massive_write_update, name='massive_write_update'),
    # path('complete_writing_post/', views.compelete_writing, name="compelete_writing"),

    # path('writers_queue/', views.writers_queue, name='writers_queue'),

    # path('administrator_of_writers/', views.admin_writers, name='admin_writers'),
    # path('admin_update_post/', views.admin_update_post, name='admin_update_post'),
    # path('approve_writing_post/',views.approve_writing_post, name='approve_writing_post'),
    # path('send_in_for_revision/', views.send_in_for_revision, name='send_in_for_revision')
]