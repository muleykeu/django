from django.contrib import admin
from .models import Post, Yorum, Mesaj

# Register your models here.
admin.site.register(Post)
admin.site.register(Yorum)
admin.site.register(Mesaj)