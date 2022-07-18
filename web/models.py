from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import FileExtensionValidator

class Category(models.Model):
	class Meta:
		verbose_name = 'Категории'
		verbose_name_plural = 'Категории'

	Show_nav_list = [
		("Отображать", "Отображать"),
		("Не отображать", "Не отображать")
	]

	Name = models.CharField(verbose_name="Название", max_length=50)
	Image = models.ImageField(verbose_name="Изображение", upload_to='category/')
	Color = models.CharField(verbose_name="Цвет (html color code)  #", max_length=50)
	Show_nav = models.CharField(max_length=50, choices=Show_nav_list, default="Не отображать", verbose_name="Отображать в меню")

	def __str__(self):
		return str(self.Name)


class Tag(models.Model):
	class Meta:
		verbose_name = 'Ярлыки'
		verbose_name_plural = 'Ярлыки'
	
	Visible_status_list = [
		("Отображать", "Отображать"),
		("Не отображать", "Не отображать")
	]

	Name = models.CharField(verbose_name="Название", max_length=50)
	Color = models.CharField(verbose_name="Цвет (html color code)  #", max_length=50)
	Visible_status = models.CharField(max_length=50, choices=Visible_status_list, default="Не отображать", verbose_name="Блок на главной")

	def __str__(self):
			return str(self.Name)


class ProductImage(models.Model):
	class Meta:
		verbose_name = 'Изображения товаров'
		verbose_name_plural = 'Изображения товаров'
	Image = models.ImageField(upload_to='product/images/', blank=True)

	def __str__(self):
			return str(self.Image)


class Product(models.Model):
	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товар'

	Availability_list = [
		("Есть в наличии", "Есть в наличии"),
		("Нет в наличии", "Нет в наличии")
	]
	UsedCondition = [
		("Новое", "Новое"),
		("Б/У", "Б/У")
	]
	Recommendation_list = [
		("Отображать", "Отображать"),
		("Не отображать", "Не отображать")
	]

	Name = models.CharField(verbose_name="Название", max_length=50)
	Image = models.ImageField(verbose_name="Изображение", upload_to='product/')
	Images = models.ManyToManyField(ProductImage, verbose_name="Изображения товара", blank=True)
	Category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
	Tags = models.ManyToManyField(Tag, verbose_name="Ярлыки", blank=True)
	Recommendation = models.CharField(max_length=50, choices=Recommendation_list, default="Не отображать", verbose_name="Рекомендации")
	Short_description = models.TextField(blank=True, verbose_name="Краткое описание карточки")
	Description = models.TextField(blank=True, verbose_name="Описание товара")
	Video = models.FileField(upload_to='product/video/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])], verbose_name="Видеообзор")
	Price = models.IntegerField(verbose_name="Цена")

	def __str__(self):
		return str(self.Name)


class Blog(models.Model):
	class Meta:
		verbose_name = 'Блог'
		verbose_name_plural = 'Блог'

	Title = models.CharField(verbose_name="Название", max_length=50)
	Image = models.ImageField(verbose_name="Изображение", upload_to='category/')
	Color = models.CharField(verbose_name="Цвет (html color code)  #", max_length=50)
	About = models.TextField(blank=True, verbose_name="Описание")
	Date = models.DateField(verbose_name='Дата', blank=True)
	Text = models.TextField(blank=True, verbose_name="Текст")

	def __str__(self):
		return str(self.Title)


class Shop(models.Model):
	class Meta:
		verbose_name = 'Магазин'
		verbose_name_plural = 'Магазин'

	Address = models.CharField(verbose_name="Адрес", max_length=80)
	Schedule = models.CharField(verbose_name="График работы", max_length=80)
	Phone = models.CharField(verbose_name="Телефон", max_length=20)

	def __str__(self):
		return str(self.Address)



class Basket(models.Model):
	class Meta:
		verbose_name = 'Корзина (system)'
		verbose_name_plural = 'Корзина (system)'

	session_key = models.CharField(max_length=120)
	product_id = models.CharField(max_length=120)
	product_value = models.IntegerField()

	def __str__(self):
		return str(self.id)



class Banner(models.Model):
	class Meta:
		verbose_name = "Баннер"
		verbose_name_plural = "Баннер"

	Image = models.FileField(upload_to='banner/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['JPEG','JPG','GIF','PNG','APNG','SVG','BMP','ICO'])], verbose_name="Изображение")
	Link = models.CharField(verbose_name="Ссылка", max_length=50, blank=True)

	def __str__(self):
		return str(self.id)



class Order(models.Model):
	class Meta:
		verbose_name = "Заказы"
		verbose_name_plural = "Заказы"

	Delivery_type_list = [
		("Самовывоз", "Самовывоз"),
		("Доставка", "Доставка"),
		("Доставка вне города", "Доставка вне города")
	]


	Name_Sender = models.CharField(verbose_name="Имя отправителя", max_length=50)
	Phone_Sender = models.CharField(verbose_name="Телефон отправителя", max_length=50)
	Email_Sender = models.CharField(verbose_name="Email отправителя", max_length=50, blank=True)

	Products = models.TextField(verbose_name='Заказ')
	Delivery_type = models.CharField(max_length=50, choices=Delivery_type_list, verbose_name="Тип доставки")

	Name_Receiver = models.CharField(verbose_name="Имя получателя ", max_length=50)
	Phone_Receiver = models.CharField(verbose_name="Телефон получателя", max_length=50)
	Address = models.CharField(verbose_name="Адрес доставки", max_length=50)
	Date = models.DateField(verbose_name='Дата', blank=True, null=True, default=None)
	Time = models.TimeField(verbose_name='Время', blank=True, null=True, default=None)
	Comment = models.TextField(verbose_name='Комментарий')

	Price = models.IntegerField(verbose_name='Итоговая цена')

	def __str__(self):
		return str(self.id)+") "+str(self.Name_Sender)


class Thanks(models.Model):
	class Meta:
		verbose_name = "Отзывы"
		verbose_name_plural = "Отзывы"

	Image = models.FileField(upload_to='thanks/',null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['JPEG','JPG','GIF','PNG','APNG','SVG','BMP','ICO'])], verbose_name="Изображение")
	def __str__(self):
		return str(self.id)




class Yookassa(models.Model):
	Delivery_type_list = [
		("Самовывоз", "Самовывоз"),
		("Доставка", "Доставка"),
		("Доставка вне города", "Доставка вне города")
	]

	session_key = models.CharField(max_length=120)

	Name_Sender = models.CharField(verbose_name="ФИО", max_length=50)
	Phone_Sender = models.CharField(verbose_name="Телефон", max_length=50)
	Email_Sender = models.CharField(verbose_name="Email", max_length=50, blank=True)

	Delivery_type = models.CharField(max_length=50, choices=Delivery_type_list, verbose_name="Тип доставки")

	Name_Receiver = models.CharField(verbose_name="ФИО", max_length=50)
	Phone_Receiver = models.CharField(verbose_name="Телефон", max_length=50)
	Address = models.CharField(verbose_name="Адрес доставки", max_length=50)
	Date = models.DateField(verbose_name='Дата', blank=True, null=True, default=None)
	Time = models.TimeField(verbose_name='Время', blank=True, null=True, default=None)
	Comment = models.TextField(verbose_name='Комментарий')

	def __str__(self):
		return str(self.id) + ") "+ str(self.session_key)
	