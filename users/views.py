import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from users.models import User, Location


class UserView(ListView):
	models = User
	queryset = User.objects.all()

	def get(self, request, *args, **kwargs):
		super().get(request, *args, **kwargs)
		self.object_list = self.object_list.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True)))
		paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
		number_page = request.GET.get('page')
		page_data = paginator.get_page(number_page)
		res_users = []
		for value in page_data:
			res_users.append({
				"id": value.id,
				"username": value.username,
				"first_name": value.first_name,
				"last_name": value.last_name,
				"role": value.role,
				"age": value.age,
				"locations": list(map(str, value.locations.all())),
				"total_ads": value.total_ads,
			})
		res = {
			"items": res_users,
			"total": page_data.paginator.count,
			"num_pages": settings.TOTAL_ON_PAGE,
		}
		return JsonResponse(res, safe=False)


class UserDetailView(DetailView):
	model = User

	def get(self, request, *args, **kwargs):
		try:
			user = self.get_object()
		except Http404:
			return JsonResponse({'error': 'Not Found'}, status=404)
		return JsonResponse({
			"id": user.id,
			"username": user.username,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"role": user.role,
			"age": user.age,
			"locations": list(map(str, user.locations.all())),
		})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
	model = User
	fields = ["username", "password", "first_name", "last_name", "role", "age", "locations"]

	def post(self, request, *args, **kwargs):
		data_db = json.loads(request.body)
		user = User.objects.create(
			username=data_db["username"],
			password=data_db["password"],
			first_name=data_db["first_name"],
			last_name=data_db["last_name"],
			role=data_db["role"],
			age=data_db["age"],
		)
		for value in data_db["locations"]:
			location, _ = Location.objects.get_or_create(name=value)
			user.locations.add(location)
		return JsonResponse({
			"id": user.id,
			"username": user.username,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"role": user.role,
			"age": user.age,
			"locations": list(map(str, user.locations.all())),
		})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
	model = User
	fields = ["username", "password", "first_name", "last_name", "role", "age", "locations"]

	def patch(self, request, *args, **kwargs):
		super().post(request, *args, **kwargs)
		data_db = json.loads(request.body)
		self.object.username = data_db["username"]
		self.object.password = data_db["password"]
		self.object.first_name = data_db["first_name"]
		self.object.last_name = data_db["last_name"]
		self.object.age = data_db["age"]
		for value in data_db["locations"]:
			location, _ = Location.objects.get_or_create(name=value)
			self.object.locations.add(location)
		self.object.save()
		return JsonResponse({
			"id": self.object.id,
			"username": self.object.username,
			"first_name": self.object.first_name,
			"last_name": self.object.last_name,
			"role": self.object.role,
			"age": self.object.age,
			"locations": list(map(str, self.object.locations.all())),
		})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
	model = User
	success_url = "/"

	def delete(self, request, *args, **kwargs):
		super().delete(request, *args, **kwargs)
		return JsonResponse({"status": "ok"}, status=200)
