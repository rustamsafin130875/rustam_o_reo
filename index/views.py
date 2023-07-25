from django.shortcuts import render, redirect
from . import forms
from .models import *
from .handlers import bot

# Create your views here.
def home_page(request):
    search_bar = forms.SearchForm()
    #Собираем названия всех продуктов
    product_info = Product.objects.all()
    #Собираем названия всех категорий
    category_info = Category.objects.all()

    # Передаем данные на фронт
    context = {
        'form': search_bar,
        'product': product_info,
        'category': category_info
    }

    return render(request, 'index.html', context)


def product_page(request, pk):
    product_info = Product.objects.get(id=pk)

    # if request.method == "POST":
    #     Cart.objects.create(user_id=request.user.id,
    #                         user_product=product_info,
    #                         user_product_amount=request.POST.get('amount_products'))

    if request.method == 'POST':
        user_id = request.user.id  # предполагается, что пользователь авторизован
        #user_product_id = request.POST.get('user_product')
        user_product_id = product_info.id
        user_product_amount = request.POST.get('amount_products')

        cart = Cart(user_id=user_id, user_product_id=user_product_id, user_product_amount=user_product_amount)
        cart.save()

        return redirect('/')  # Перенаправление на другую страницу после успешного добавления в корзину

    #Передаем данные на фронт
    context = {'product': product_info}
    return render(request, 'about_product.html', context)

def category_page(request, pk):
    category_info = Category.objects.get(id=pk)
    product_info = Product.objects.filter(product_category=category_info)

    #Передаем данные на фронт
    context = {'products': product_info}

    return render(request, 'about_category.html', context)

def search_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        try:
            exact_product = Product.objects.get(product_name__icontains=get_product)
            return redirect(f'product/{exact_product.id}')
        except:
            return redirect('/')

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = forms.RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def get_user_cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)

    if request.method == 'POST':
        main_text = 'Новый заказ!\n\n\n'

        for i in user_cart:
            main_text += f'Товар: {i.user_product}\n\nКоличество: {i.user_product_amount} \n\nЦена: {i.user_product.product_price} '

        bot.send_message(5172674378, main_text)
        user_cart.delete()
        return redirect('/')
    return render(request, 'user_cart.html', {'cart': user_cart})


def add_to_cart(request):
    if request.method == 'POST':
        user_id = request.user.id  # предполагается, что пользователь авторизован
        #user_product_id = request.POST.get('user_product')
        user_product_id = request.product.product_name
        user_product_amount = request.POST.get('amount_products')

        cart = Cart(user_id=user_id, user_product_id=user_product_id, user_product_amount=user_product_amount)
        cart.save()

        return redirect('/')  # Перенаправление на другую страницу после успешного добавления в корзину

    return render(request, 'about_product.html')

def del_from_cart(request, pk):
    cart = Cart.objects.filter(user_id=request.user.id, user_product=pk)
    cart.delete()
    return redirect('/')

def about_page(request):
    return render(request, 'about.html')
def contact_page(request):
    return render(request, 'contacts.html')

def category_pages(request):
    search_bar = forms.SearchForm()
    # Собираем названия всех продуктов
    product_info = Product.objects.all()
    # Собираем названия всех категорий
    category_info = Category.objects.all()

    # Передаем данные на фронт
    context = {
        'form': search_bar,
        'product': product_info,
        'category': category_info
    }

    return render(request, 'category.html', context)


