from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.conf import settings

import json

from ads.models import Category, Ad
from users.models import User


def root_view(request):
    return JsonResponse({"status": "ok"})


class AdView(ListView):
    model = Ad
    queryset = Ad.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        categories = request.GET.getlist("cat", [])
        if categories:
            self.object_list = self.object_list.filter(category_id__in=categories)

        if request.GET.get("text", None):
            self.object_list = self.object_list.filter(name__icontains=request.GET.get("text"))

        if request.GET.get("location", None):
            self.object_list = self.object_list.filter(author__locations__name__icontains=request.GET.get("location"))

        if request.GET.get("price_from", None):
            self.object_list = self.object_list.filter(price__gte=request.GET.get("price_from"))

        if request.GET.get("price_to", None):
            self.object_list = self.object_list.filter(price__lte=request.GET.get("price_to"))


        self.object_list = self.object_list.select_related('author').order_by('-price')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        number_page = request.GET.get('page')
        page_data = paginator.get_page(number_page)
        res_ads = []
        for value in page_data:
            res_ads.append({
                "id": value.id,
                "name": value.name,
                "author_id": value.author_id,
                "author": value.author.first_name,
                "price": value.price,
                "description": value.description,
                "is_published": value.is_published,
                "category_id": value.category_id,
                "image": value.image.url if value.image else None,
            })
        res = {
            "items": res_ads,
            "total": page_data.paginator.count,
            "num_pages": settings.TOTAL_ON_PAGE,
        }
        return JsonResponse(res, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Http404:
            return JsonResponse({'error': 'Not Found'}, status=404)
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published", "category"]

    def post(self, request, *args, **kwargs):
        data_db = json.loads(request.body)
        author = get_object_or_404(User, data_db["author_id"])
        category = get_object_or_404(Category, data_db["category_id"])
        ad = Ad.objects.create(
            name=data_db["name"],
            author=author,
            price=data_db["price"],
            description=data_db["description"],
            is_published=data_db["is_published"],
            category=category,
        )
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "is_published", "description", "image"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data_db = json.loads(request.body)
        self.object.name = data_db["name"]
        self.object.price = data_db["price"]
        self.object.description = data_db["description"]
        self.object.author = get_object_or_404(User, id=data_db["author_id"])
        self.object.category = get_object_or_404(Category, id=data_db["category_id"])
        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadImageView(UpdateView):
    model = Ad
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image", None)
        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })


class CategoryView(ListView):
    models = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by("name")
        res = []
        for value in self.object_list:
            res.append({
                "id": value.id,
                "name": value.name,
            })
        return JsonResponse(res, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Http404:
            return JsonResponse({'id': 'Not Found'}, status=404)
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        data_db = json.loads(request.body)
        category = Category.objects.create(
            name=data_db["name"],
        )
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data_db = json.loads(request.body)
        self.object.name = data_db["name"]
        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)
