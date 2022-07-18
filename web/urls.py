from django.urls import include, path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index__page, name='home'),
    path('catalog', views.catalog__page),
    path('catalog/<int:id>', views.product_catalog__page),
    path('product/<int:id>', views.product__page),
    path('blog', views.blog_list__page),
    path('blog/<int:id>', views.blog__page),
    path('about/', views.about__page),
    path('contacts/', views.contacts__page),
    path('basket/', views.basket__page),
    path('search/', views.search__page),
    path('yookassa/payment', views.Yookassa_payment),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('sitemap.xml', TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml"))
    ]