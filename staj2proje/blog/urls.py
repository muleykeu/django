from django.urls import path
from . import views
from .views import PostListView, PostDetailView, YeniPost, YorumYap, AramaSonuclari, GelenKutusu, Direkt, Gonder, \
    KullaniciAra, YeniKonusma

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_ayrinti'),
    path('yenipost/', YeniPost, name='post_olustur'),
    path('begeni/<int:pk>', views.LikeView, name='post_begen'),
    path('anasayfa/', PostListView.as_view(), name='anasayfa'),
    path('post/<int:pk>/yorum/', YorumYap.as_view(), name='yorum_yap'),
    path('arama_sonuclari/', AramaSonuclari, name='arama_sonuclari'),
    path('gelen_kutusu/', GelenKutusu, name='gelen_kutusu'),
    path('direkt/<str:username>', Direkt, name='direkt'),
    path('gonder/', Gonder, name='gonder'),
    path('kullanici_ara/', KullaniciAra, name='kullanici_ara'),
    path('yeni_konusma/<str:username>', YeniKonusma, name='yeni_konusma'),
]