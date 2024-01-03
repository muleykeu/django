from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    image = models.ImageField(blank=True, null=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()

    likes = models.ManyToManyField('auth.User', related_name='begeni_posts')

    def total_likes(self):
        return self.likes.count()

    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def yayinla(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Gönderiler'

    def get_absolute_url(self):
        return reverse('post_ayrinti', kwargs={'pk': self.pk})

class Yorum(models.Model):
    post = models.ForeignKey(Post, related_name='yorumlar', on_delete=models.CASCADE)
    isim = models.CharField(max_length=200)
    yorum = models.TextField()
    yorum_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.isim)

    class Meta:
        verbose_name_plural = 'Yorumlar'


class Mesaj(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    gonderen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    alici = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    mesaj = models.TextField(max_length=1000, blank=True, null=True)
    tarih = models.DateTimeField(auto_now_add=True)
    okundu = models.BooleanField(default=False)

    def mesaj_gonder(from_user, to_user, mesaj):
        gonderen_mesaj = Mesaj(user=from_user,
                               gonderen=from_user,
                               alici=to_user,
                               mesaj=mesaj,
                               okundu=True)
        gonderen_mesaj.save()

        alici_mesaj = Mesaj(user=to_user,
                            gonderen=from_user,
                            mesaj=mesaj,
                            alici=from_user)
        alici_mesaj.save()

        return gonderen_mesaj

    def mesaj_al(user):
        kullanicilar = []
        mesajlar = Mesaj.objects.filter(user=user).values('alici').annotate(last=Max('tarih')).order_by('-last')
        for mesaj in mesajlar:
            kullanicilar.append({
                'user': User.objects.get(pk=mesaj['alici']),
                'last': mesaj['last'],
                'okunmadi':Mesaj.objects.filter(user=user, alici__pk=mesaj['alici'], okundu=False).count()})
        return kullanicilar

    class Meta:
        verbose_name_plural = 'Mesajlar'
