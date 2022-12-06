from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Product(models.Model):

    product_id = models.AutoField(verbose_name='ID', primary_key=True)
    product_name = models.CharField('Product Name', max_length=50)
    product_description = models.CharField(
        'Product Description', max_length=500)
    product_date = models.DateTimeField('Product Date')
    price = models.IntegerField('Price')
    product_image = models.ImageField(
        'Image', default='', upload_to='shop_app/images')
    product_category = models.CharField('Product Category', choices=(
        ('product', 'Product'), ('material', 'Material')), max_length=25, default='product')

    def __str__(self):
        return self.product_name


class Contact(models.Model):

    contact_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Name', max_length=50)
    email = models.CharField('Email', max_length=50)
    phone = models.CharField('Phone', max_length=50)
    desc = models.CharField('Description', max_length=500)

    def __str__(self):
        return self.name


class Order(models.Model):

    order_id = models.AutoField('ID', primary_key=True)
    name = models.CharField('Name', max_length=50)
    email = models.CharField('Email', max_length=50)
    phone = models.CharField('Phone', max_length=50)
    city = models.CharField('City', max_length=50)
    state = models.CharField('State', max_length=50)
    zip = models.CharField('Zip', max_length=10)
    address = models.CharField('Address', max_length=500)
    order_price = models.IntegerField('Order Price', default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    item_details = models.CharField(
        'Item Details', max_length=5000, default="")
    product = models.ManyToManyField(Product)

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):

    order_update_id = models.AutoField('Id', primary_key=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name='Order')
    update_desc = models.CharField(
        'Update Description', max_length=5000, default="")
    update_time = models.DateField('Update Time', auto_now_add=True)

    def __str__(self):
        return self.update_desc[:20] + '...'


class Comments(models.Model):

    comment_id = models.AutoField('Id', primary_key=True)
    comment = models.TextField('Comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,blank=True)
    comment_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.comment[0:20]} by {self.user.first_name}"
