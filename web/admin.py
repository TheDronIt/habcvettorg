from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ProductAdminForm(forms.ModelForm):
    Description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm


class BlogAdminForm(forms.ModelForm):
    About = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Blog
        fields = '__all__'

class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm


admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Shop)
admin.site.register(Basket)
admin.site.register(Order)
admin.site.register(Banner)
admin.site.register(Yookassa)