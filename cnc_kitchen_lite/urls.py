from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from posts.views import (
    index,
    search,
    post_list,
    post_detail,
    post_create,
    post_update,
    post_delete,
    IndexView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from marketing.views import email_list_signup

admin.site.site_header = 'CNC Kitchen v5.o'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index),

    # path('cnc_kitchen_lite/', post_list, name='post-list'),
    path('cnc_kitchen_lite/', PostListView.as_view(), name='post-list'),
    path('search/', search, name='search'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    # path('create/', post_create, name='post-create'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    # path('post/<id>/', post_detail, name='post-detail'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<id>/update/', post_update, name='post-update'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),

    path("recipes/", include(("recipe.urls", "recipe"), namespace='recipes'), ),  # UI Kits Html files
    path("modules/", include(("module.urls", "module"), namespace='modules')),  # UI Kits Html files
    path("tasks/", include("tasks.urls")),  # UI Kits Html files
    path("ingredients/", include(("ingredients.urls", "ingredients"), namespace='ingredients')),  # UI Kits Html files

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]
