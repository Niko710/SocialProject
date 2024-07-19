from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST

from images.forms import ImageCreateForm
from images.models import Image


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image: Image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Images has been created succesfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'image': image})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    try:
        image = Image.objects.get(id=image_id)
        if action == 'like':
            image.users_like.add(request.user)
        else:
            image.users_like.remove(request.user)
        return JsonResponse({'status': 'ok'})
    except Image.DoesNotExist:
        return JsonResponse({'status': 'error'})


def image_list(request):
    images = Image.objects.all()
    images_only = request.GET.get('images_only')
    page = request.GET.get('page')
    paginator = Paginator(images, 4)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request, 'images/image/list_images.html', {'images': images})
    return render(request, 'images/image/list.html', {'images': images})
