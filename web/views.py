from sre_constants import SUCCESS
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import datetime
import random
from django.core.mail import send_mail
from .models import *
import uuid
from django.views.decorators.csrf import csrf_exempt
from yookassa import Configuration, Payment
import json
import traceback


Configuration.account_id = 860268
Configuration.secret_key = 'test_SgoBIO7txIDy-CU-jHhgyo5CTmZqjeijgqM_81xAyQU'

now = datetime.datetime.now()


def index__page(request):


	tags = {}
	Tags = Tag.objects.filter(Visible_status="Отображать")

	for tag in Tags:
		tags[tag] = Product.objects.filter(Tags__Name=tag)[:4]

	if contactus_form(request) == True:
		success_form = True
	else:
		success_form = False


	data = {
		'tags': tags,
		'Banners': Banner.objects.all(),
		'Nav_category': nav_category(),
		'ThanksList': Thanks.objects.all().order_by("?")[:6],
		'Success_form': success_form
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
	Products = Product.objects.filter(Category__id=id)
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
					db = Basket(session_key=session_key(request),
								product_id=id, product_value=1)
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
	user_product = Basket.objects.filter(
		session_key=session_key(request)).order_by('id')
	# about_product = Product.objects.get()
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

				if button == "+":
					Basket.objects.filter(session_key=session_key(request)).filter(
						product_id=product_id).update(product_value=int(product_value(request))+1)

				elif button == "-":
					Basket.objects.filter(session_key=session_key(request)).filter(
						product_id=product_id).update(product_value=int(product_value(request))-1)
					if product_value(request) < 1:
						Basket.objects.filter(session_key=session_key(
							request)).filter(product_id=product_id).delete()

				elif button == "✖":
					Basket.objects.filter(session_key=session_key(
						request)).filter(product_id=product_id).delete()
				return HttpResponseRedirect("/basket")

			if button == "Оформить":

				Name_Sender = ""
				Phone_Sender = ""
				Email_Sender = ""
				Delivery_type = ""
				Name_Receiver = ""
				Phone_Receiver = ""
				Address = ""
				Date = None
				Time = None
				Comment = ""

				delivery_price = 0

				if request.POST['Sender_Name']:
					Name_Sender = request.POST['Sender_Name']

				if request.POST['Sender_Phone']:
					Phone_Sender = request.POST['Sender_Phone']

				if request.POST['Sender_Email']:
					Email_Sender = request.POST['Sender_Email']

				if request.POST['Delivery']:
					if request.POST['Delivery'] == "1":
						Delivery_type = "Самовывоз"
					elif request.POST['Delivery'] == "2":
						Delivery_type = "Доставка"
						delivery_price = 280
					elif request.POST['Delivery'] == "3":
						Delivery_type = "Доставка вне города"
						delivery_price = 380

				if request.POST['Delivery'] == "2" or request.POST['Delivery'] == "3":
					if request.POST['Geter_Name']:
						Name_Receiver = request.POST['Geter_Name']

					if request.POST['Geter_Phone']:
						Phone_Receiver = request.POST['Geter_Phone']

					if request.POST['Geter_Address']:
						Address = request.POST['Geter_Address']

					if request.POST['Geter_Delivery_date']:
						Date = request.POST['Geter_Delivery_date']

					if request.POST['Geter_Delivery_time']:
						Time = request.POST['Geter_Delivery_time']

					if request.POST['Geter_Comment']:
						Comment = request.POST['Geter_Comment']

				db = Yookassa(session_key=str(session_key(request)), Name_Sender=Name_Sender, Phone_Sender=Phone_Sender, Email_Sender=Email_Sender,
							  Delivery_type=Delivery_type, Name_Receiver=Name_Receiver, Phone_Receiver=Phone_Receiver, Address=Address, Date=Date, Time=Time, Comment=Comment)
				db.save()

				payment = Payment.create({
					"amount": {
						"value": int(basket_price(request))+int(delivery_price),
						"currency": "RUB"
					},
					"confirmation": {
						"type": "redirect",
						"return_url": "https://HabCvetTorg.ru"
					},
					"capture": True,
					"description": str(session_key(request))
				}, uuid.uuid4())
				return HttpResponseRedirect(payment.confirmation.confirmation_url)

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
	data = {
		"Nav_category": nav_category(),
		"Query_result": query_result,
		"Query": query
	}
	return render(request, 'page/search.html', data)


@csrf_exempt
def Yookassa_payment(request):
	try:
		yookassa_json = json.loads(request.body)
		payment_id = yookassa_json['object']['id']

		if yookassa_json['event'] == "payment.waiting_for_capture":
			Payment.capture(payment_id)

		if yookassa_json['event'] == "payment.succeeded":

			session_key = yookassa_json['object']['description']

			Products = Basket.objects.filter(session_key=session_key)

			if int(len(Products)) > 0:
				Product_list = []
				db_Order = ""
				number = 1

				Customer = Yookassa.objects.filter(
					session_key=session_key).order_by('-id')[:1]

				for product in Products:
					AboutProduct = Product.objects.get(
						id=int(product.product_id))

					Product_list.append(
						dict(
							name=AboutProduct.Name,
							product_value=product.product_value,
							price_one=AboutProduct.Price,
							price_full=AboutProduct.Price * product.product_value,
						)
					)

				full_price = 0

				for product in Products:
					full_price = (Product.objects.get(
						id=product.product_id).Price * product.product_value) + full_price

				for product in Product_list:
					db_Order = str(db_Order) + str(number) + ") " + str(product['name']) + " | Кол-во: " + str(
						product['product_value']) + " | За один: " + str(product['price_one']) + " | Цена: " + str(product['price_full']) + "\n"
					number += 1

				# Добавить к фулл прайсу стоимость за доставку

				for Customer in Customer:

					if Customer.Delivery_type == "Доставка":
						full_price += 280
					elif Customer.Delivery_type == "Доставка вне города":
						full_price += 380

					db = Order(Name_Sender=str(Customer.Name_Sender), Phone_Sender=str(Customer.Phone_Sender), Email_Sender=str(Customer.Email_Sender), Products=str(db_Order), Delivery_type=str(Customer.Delivery_type), Name_Receiver=str(
						Customer.Name_Receiver), Phone_Receiver=str(Customer.Phone_Receiver), Address=str(Customer.Address), Date=Customer.Date, Time=Customer.Time, Comment=str(Customer.Comment), Price=str(full_price))
					db.save()
				Basket.objects.filter(session_key=session_key).delete()

	except Exception as err:
		print(err)
		traceback.print_exc()

	return render(request, 'page/yookassapayment.html')


def session_key(request):
	session_key = request.session.session_key
	if not session_key:
		request.session.cycle_key()
	return session_key


def recommendations():
	recommendation = Product.objects.filter(
		Recommendation="Отображать").order_by("?")
	return recommendation


def product_in_basket(request, id):
	product = Basket.objects.filter(
		session_key=session_key(request)).filter(product_id=id)
	if len(product) >= 1:
		return True
	else:
		return False


def product_value(request):
	product_id = request.POST['product_id']
	product_value = Basket.objects.filter(session_key=session_key(
		request)).get(product_id=product_id).product_value
	return product_value


def nav_category():
	category = Category.objects.filter(Show_nav="Отображать").order_by("id")
	return category


def basket_price(request):
	basket = Basket.objects.filter(session_key=session_key(request))
	full_price = 0
	for product in basket:
		full_price = (Product.objects.get(
			id=product.product_id).Price * product.product_value) + full_price
	return full_price


def contactus_form(request):
	Success_form = False
	if request.method == "POST" and request.POST['button']:
		button = request.POST['button']
		if button == "Отправить":
			Name = ""
			Phone = ""
			Email = ""
			Message = ""

			if request.POST['Name']:
				Name = request.POST['Name']
			if request.POST['Phone']:
				Phone = request.POST['Phone']
			if request.POST['Email']:
				Email = request.POST['Email']
			if request.POST['Message']:
				Message = request.POST['Message']

			db = ContactUS(Name=Name, Phone=Phone, Email=Email, Message=Message)
			db.save()
			
			mail_to_admin = send_mail(
							'ХабЦветТорг | Новое сообщение',
							'Имя: '+str(Name)+'\nТелефон: '+str(Phone)+'\nПочта: '+str(Email)+'\nСообщение: '+str(Message),
							'dronbrother@yandex.ru', #mail_from
							['andreykae28@gmail.com'], #mail_to
							fail_silently=False,
						)

			Success_form = True

			return Success_form
