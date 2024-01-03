from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View

from .models import Post, Yorum, Mesaj
from django.views.generic import ListView, DetailView, CreateView
from .forms import YeniPostForm, YorumForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest


# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def anasayfa(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/anasayfa.html', context)


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    begenildi = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        begenildi = False
    else:
        post.likes.add(request.user)
        begenildi = True

    return HttpResponseRedirect(reverse('post_ayrinti', args=[str(pk)]))


class PostListView(ListView):
    model = Post
    template_name = 'blog/anasayfa.html'
    context_object_name = 'posts'
    ordering = ['-created_date']


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)

        ttllks = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = ttllks.total_likes()

        begenildi = False
        if ttllks.likes.filter(id=self.request.user.id).exists():
            begenildi = True

        context['total_likes'] = total_likes
        context['begenildi'] = begenildi
        return context


@login_required
def YeniPost(request):
    user = request.user.id

    if request.method == 'POST':
        form = YeniPostForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            text = form.cleaned_data.get('text')
            created_date = form.cleaned_data.get('created_date')
            title = form.cleaned_data.get('title')

            p, created = Post.objects.get_or_create(image=image, text=text, author_id=user, published_date=created_date, title= title)
            p.save()
            return redirect('anasayfa')

    else:
        form = YeniPostForm()
    contex = {
        'form': form,
    }
    return render(request, 'blog/post_form.html', contex)


class YorumYap(CreateView):
    model = Yorum
    form_class = YorumForm
    template_name = 'blog/post_yorum.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('anasayfa')


def AramaSonuclari(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        sonuclar = User.objects.filter(username=searched)
        return render(request, 'blog/arama_sonuclari.html', {'searched': searched, 'sonuclar': sonuclar})
    else:
        return render(request, 'blog/arama_sonuclari.html')


@login_required
def GelenKutusu(request):
    user = request.user
    mesajlar = Mesaj.mesaj_al(user=user)
    aktif_dm = None
    dmler = None

    if mesajlar:
        mesaj = mesajlar[0]
        aktif_dm = mesaj['user'].username
        dmler = Mesaj.objects.filter(user=user, alici=mesaj['user'])
        dmler.update(okundu=True)

        for mesaj in mesajlar:
            if mesaj['user'].username == aktif_dm:
                mesaj['okunmadi'] = 0

    contexts = {'dmler': dmler, 'mesajlar': mesajlar, 'aktif_dm': aktif_dm,}

    template = loader.get_template('blog/dm/dm.html')
    return HttpResponse(template.render(contexts, request))
    #return render(request, 'blog/dm/dm.html', {'dmler': dmler, 'mesajlar': mesajlar, 'aktif_dm': aktif_dm})


@login_required
def Direkt(request, username):
    user = request.user
    mesajlar = Mesaj.mesaj_al(user=user)
    aktif_dm = username
    dmler = Mesaj.objects.filter(user=user, alici__username=username)
    dmler.update(okundu=True)

    for mesaj in mesajlar:
        if mesaj['user'].username == username:
            mesaj['okunmadi'] = 0


    contextss = {
        'dmler': dmler,
        'mesajlar': mesajlar,
        'aktif_dm': aktif_dm,
    }

    template = loader.get_template('blog/dm/dm.html')
    return HttpResponse(template.render(contextss, request))


@login_required
def Gonder(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    mesaj = request.POST.get('mesaj')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Mesaj.mesaj_gonder(from_user, to_user, mesaj)
        return redirect('gelen_kutusu')
    else:
        HttpResponseBadRequest()


@login_required
def KullaniciAra(request):
    query = request.GET.get('q')
    context = {}

    if query:
        users = User.objects.filter(Q(username__icontains=query))

        sayfalayici = Paginator(users, 6)
        sayfa_num = request.GET.get('page')
        kullanici_sy = sayfalayici.get_page(sayfa_num)

        context = {'users': kullanici_sy}

    template = loader.get_template('blog/dm/kullanici_ara.html')
    return HttpResponse(template.render(context, request))



@login_required
def YeniKonusma(request, username):
    from_user = request.user
    mesaj = ''

    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('kullanici_ara')
    if from_user != to_user:
        Mesaj.mesaj_gonder(from_user, to_user, mesaj)
    return redirect('gelen_kutusu')

