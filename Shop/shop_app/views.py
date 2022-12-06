
from math import ceil
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from .models import Comments, OrderUpdate, Product, Contact, Order
from django.contrib.auth.models import User
from .PayTm import Checksum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from shop_app.templatetags import extras

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'


def home(request):
    products_list = []
    products_category = list(
        map(lambda lm: lm[0], Product.objects.values_list('product_category').distinct()))

    for category in products_category:
        products = Product.objects.filter(product_category=category)
        no_of_slide = len(products)//3 + \
            ceil(len(products)/3 - len(products)//3)
        products_list.append([products, no_of_slide, range(1, no_of_slide)])

    product_dict = {'products_list': products_list}
    # product_dict = {
    #     'products': products,
    #     'no_of_slide': no_of_slide,
    #     'range': range(1, no_of_slide),
    # }

    return render(request, 'home.html', product_dict)


def searchMatch(product, search_string):
    if search_string.lower() in product.product_name.lower() or \
            search_string.lower() in product.product_description.lower() or \
            search_string.lower() in product.product_category:
        return True
    else:
        return False


def search(request):
    search_string = request.GET.get('search', '')
    products = Product.objects.all()
    products_list = []

    products_category = list(
        map(lambda lm: lm[0], Product.objects.values_list('product_category').distinct()))
    search_products = [product.product_id for product in products if searchMatch(
        product, search_string)]
    for category in products_category:
        products = Product.objects.filter(
            product_category=category, product_id__in=search_products)
        no_of_slide = len(products)//3 + \
            ceil(len(products)/3 - len(products)//3)
        if products:
            products_list.append(
                [products, no_of_slide, range(1, no_of_slide)])

    if products_list:
        product_dict = {'products_list': products_list}
    else:
        product_dict = {'products_empty': products_list}

    # product_dict = {
    #     'products': products,
    #     'no_of_slide': no_of_slide,
    #     'range': range(1, no_of_slide),
    # }

    return render(request, 'home.html', product_dict)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def submit(request):
    message = {'message': ""}
    if request.method == "POST":
        if request.POST.get('page_name') == "contactus":
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            desc = request.POST.get('desc', '')

            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            message = {
                'message': "Thanks for contacting us. We wil get back to you soon!"}

            return render(request, 'submit.html', message)

        elif request.POST.get('page_name') == "checkout":
            import pdb;pdb.set_trace()
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            address = request.POST.get(
                'address', '') + ' ' + request.POST.get('address_line', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip = request.POST.get('zip', '')
            item_details = request.POST.get('item_details', '')
            item_ids = request.POST.get('item_ids', '').split(',')[:-1]
            total_price = request.POST.get('total_price', '')
            user = request.user
            order = Order(name=name, email=email, phone=phone, address=address,
                          city=city, state=state, zip=zip, item_details=item_details, order_price=total_price, user=user)
            order.save()
            order.product.set(item_ids)

            update = OrderUpdate(
                order=order, update_desc="Order placed Sucessfully")
            update.save()
            # message = {
            #     'message': f"Thanks for ordering with us. Your order id is {order.order_id}. Use it to track your order using our order tracker.",
            #     'clearcart': True,
            # }
            data_dict = {
                "MID": "WorldP64425807474247",
                "ORDER_ID": str(order.order_id),
                "CUST_ID": email,
                "TXN_AMOUNT": str(total_price),
                "CHANNEL_ID": "WEB",
                "INDUSTRY_TYPE_ID": "Retail",
                "WEBSITE": "WEBSTAGING",
                "CHANNEL_ID": "WEB",
                "CALLBACK_URL": "http://127.0.0.1:8080/payment_status/",
            }
            data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
                data_dict, MERCHANT_KEY)
            return render(request, 'submit.html', {'data_dict': data_dict})

    # return render(request, 'submit.html', message)


def product_view(request, product_id):
    product = Product.objects.get(product_id=product_id)
    comments = Comments.objects.filter(product=product, parent=None)
    replys = Comments.objects.filter(product=product).exclude(parent=None)
    replyDict = {}
    for reply in replys:
        if reply.parent.comment_id not in replyDict.keys():
            replyDict[reply.parent.comment_id] = [reply]
        else:
            replyDict[reply.parent.comment_id].append(reply)

    product_dict = {'product': product, 'comments': comments, 'replyDict': replyDict}
    return render(request, 'product_view.html', product_dict)


def post_comment(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        comment = request.POST.get('comment')
        parent_comment = request.POST.get('parent_comment')
        product = Product.objects.get(product_id=product_id)

        if parent_comment == "":
            new_comment = Comments(
                comment=comment, product=product, user=request.user)
        else:
            parent = Comments.objects.get(comment_id=parent_comment)
            new_comment = Comments(
                comment=comment, product=product, user=request.user, parent=parent)
        new_comment.save()

    return redirect(f'/product/{product_id}')


def checkout(request):
    return render(request, 'checkout.html')


def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('order', '')
        email = request.POST.get('email', '')
        order = Order.objects.filter(order_id=order_id, email=email)
        if order:
            update_details = []
            response = []
            updates = OrderUpdate.objects.filter(order=order_id)
            for update in updates:
                update_details.append({
                    'desc': update.update_desc,
                    'time': update.update_time,
                })
                response = json.dumps(
                    [update_details, order[0].item_details], default=str)
            return HttpResponse(response)
        else:
            return HttpResponse('{}')

    return render(request, 'tracker.html')


@csrf_exempt
def payment_status(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            message = f"Thanks for ordering with us. Your order id is {response_dict['ORDERID']}. Use it to track your order using our order tracker."
            clearcart = True
        else:
            message = f"Order was not successful because {response_dict['RESPMSG']}"
            clearcart = False

    return render(request, 'payment_status.html', {'response': response_dict, 'message': message, 'clearcart': clearcart})


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        new_user = User.objects.create_user(
            username=username, password=password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()

        return redirect('Home')
    else:
        return HttpResponse("404 - Not found")


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("Home")
        else:
            return redirect("Home")
    else:
        return HttpResponse("404 - Not found")


def user_logout(request):
    logout(request)
    return redirect('Home')
