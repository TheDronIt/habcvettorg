from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import datetime
import random
from .models import *

now = datetime.datetime.now()


def index__page(request):

	tags = {}
	Tags = Tag.objects.filter(Visible_status="Отображать")

	for tag in Tags:
		tags[tag] = Product.objects.filter(Tags__Name=tag)[:4]

	data = {
		'tags': tags,
		'Banners': Banner.objects.all(),
		'Nav_category': nav_category(),
	}
	return render(request, 'page/index.html', data)


def catalog__page(request):
	Categorys = Category.objects.all()
	data = {
		'Categorys': Categorys,
		'Nav_category': nav_category()
	}
	return render(request, 'page/catalog.html', data)


def product_catalog__page(request, id):
	Category_info = Category.objects.get(id=id)
	Products = Product.objects.all()
	data = {
		'Products': Products,
		'Category': Category_info,
		'Nav_category': nav_category()
	}
	return render(request, 'page/product_catalog.html', data)


def product__page(request, id):
	AboutProduct = Product.objects.get(id=id)

	if request.method == "POST":
		if request.POST['button']:
			if request.POST['button'] == "В корзину":
				if product_in_basket(request, id) == False:
					db = Basket(session_key = session_key(request), product_id=id, product_value=1)
					db.save()
					return redirect("/product/"+str(id))
				else:
					return redirect("/basket")	
			elif request.POST['button'] == "Добавлено":
				return redirect("/basket")

	data = {
		'Product': AboutProduct,
		'Popular': recommendations()[:4],
		'Nav_category': nav_category()
	}
	return render(request, 'page/product.html', data)


def blog_list__page(request):
	Blogs = Blog.objects.all()
	data = {
		'Blogs': Blogs,
		'Nav_category': nav_category()
	}
	return render(request, 'page/blog_list.html', data)


def blog__page(request, id):
	BlogInfo = Blog.objects.get(id=id)
	data = {
		'Blog': BlogInfo,
		'Nav_category': nav_category()
	}
	return render(request, 'page/blog.html', data)


def about__page(request):
	data = {
		'Nav_category': nav_category()
	}
	return render(request, 'page/about.html', data)


def contacts__page(request):
	Shops = Shop.objects.all()
	data = {
		'Shops': Shops,
		'Nav_category': nav_category()
	}
	return render(request, 'page/contacts.html', data)


def basket__page(request):
	user_product = Basket.objects.filter(session_key=session_key(request)).order_by('id')
	#about_product = Product.objects.get()
	product_list = []
	for product_el in user_product:
		product = Product.objects.get(id=int(product_el.product_id))
		product_list.append(
			dict(
				Id=product.id,
				Name=product.Name,
				Link="/product/"+str(product.id),
				Image=product.Image.url,
				Value=product_el.product_value,
				Price=product.Price,
				Full_price=product.Price * product_el.product_value,
			))


	if request.method == "POST":
		if request.POST['button']:
			button = request.POST['button']
			if button == "+" or button == "-" or button == "✖":
				
				product_id = request.POST['product_id']
				print(product_id)
				
				
				if button == "+":
					Basket.objects.filter(session_key=session_key(request)).filter(product_id=product_id).update(product_value = int(product_value(request))+1)
				
				elif button == "-":
					Basket.objects.filter(session_key=session_key(request)).filter(product_id=product_id).update(product_value = int(product_value(request))-1)
					if product_value(request) < 1:
						Basket.objects.filter(session_key=session_key(request)).filter(product_id=product_id).delete()
				
				elif button == "✖":
					Basket.objects.filter(session_key=session_key(request)).filter(product_id=product_id).delete()

				return HttpResponseRedirect("/basket")
	
	data = {
		'Product_list': product_list,
		'datetime': [now.strftime("%Y-%m-%d"), now.strftime("%H:%M")],
		'Nav_category': nav_category(),
		'BasketPrice': basket_price(request),
	}
	return render(request, 'page/basket.html', data)	


''
def search__page(request):
	query = ""
	query_result = ""

	if request.method:
		if request.method == "GET":
			if request.GET['q']:
				query = request.GET['q']
				query_result = Product.objects.filter(Name__icontains=query)
				print(query_result)
	data = {
		"Nav_category": nav_category(),
		"Query_result": query_result,
		"Query": query
	}
	return render(request, 'page/search.html', data)



def session_key(request):
	session_key = request.session.session_key
	if not session_key:
		request.session.cycle_key()
	return session_key;


def recommendations():
	recommendation = Product.objects.filter(Recommendation="Отображать").order_by("?")
	return recommendation


def product_in_basket(request, id):
	product = Basket.objects.filter(session_key=session_key(request)).filter(product_id=id)
	if len(product) >= 1:
		return True
	else:
		return False


def product_value(request):
	product_id = request.POST['product_id']
	product_value = Basket.objects.filter(session_key=session_key(request)).get(product_id=product_id).product_value
	return product_value


def nav_category():
	category = Category.objects.filter(Show_nav="Отображать").order_by("id")
	return category


def basket_price(request):
	basket = Basket.objects.filter(session_key=session_key(request))
	full_price = 0
	for product in basket:
		full_price = (Product.objects.get(id=product.product_id).Price * product.product_value) + full_price
	return full_price