from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'ai_music'

urlpatterns = [
    path('', views.home, name='home'),
    path('music/', views.music, name='music'),
    path('alarm/', views.alarm, name='alarm'),
    # path('generate/', views.generate_music, name='generate'),
    # path('combine/', views.combine_midi, name='combine'),
    # path('gpt/', views.call_gpt, name='gpt'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

