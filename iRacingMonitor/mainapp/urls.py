
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login, name='index'),
    path('login', views.login, name='login'),
    path('members', views.members, name='members'),
    path('members/add', views.add_member, name='add_member'),
    path('members/edit', views.edit_member, name='edit_member'),
    path('members/delete/<int:id>', views.delete_member, name='delete_member'),
    path('stats', views.stats, name='stats'),
    path('stats/export', views.export_stats, name='export_stats'),
    path('meta', views.meta, name='meta'),
    path('meta/change', views.change_meta, name='change_meta'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



