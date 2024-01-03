from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import KullaniciKaydiFormu, KullaniciGuncellemeFormu, ProfilGuncellemeFormu
from blog.models import Post
from blog.views import AramaSonuclari
# Create your views here.


def kaydol(request):
    if request.method == 'POST':
        form = KullaniciKaydiFormu(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesabınız oluşturuldu. Lütfen giriş yapın.')
            return redirect('giris')
    else:
        form = KullaniciKaydiFormu()
    return render(request, 'users/kaydol.html', {'form': form})



@login_required
def profil(request):
    current_user=request.user
    user_posts = Post.objects.filter(author=current_user).order_by('-created_date')
    return render(request, 'users/profil.html', {'userpost': user_posts})


@login_required
def profduzenle(request):
    if request.method == 'POST':
        k_form = KullaniciGuncellemeFormu(request.POST, instance=request.user)
        p_form = ProfilGuncellemeFormu(request.POST, request.FILES, instance=request.user.profil)
        if k_form.is_valid() and p_form.is_valid():
            k_form.save()
            p_form.save()
            messages.success(request, f'Profiliniz güncellendi.')
            return redirect('profil')
    else:
        k_form = KullaniciGuncellemeFormu(instance=request.user)
        p_form = ProfilGuncellemeFormu(instance=request.user.profil)
    context = {
        'k_form' : k_form,
        'p_form' : p_form
    }
    return render(request, 'users/profduzenle.html', context)
