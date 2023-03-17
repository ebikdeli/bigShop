from django.urls import path

from . import views


app_name = 'vitrin'

urlpatterns = [
    path('', views.index, name='index'),
    path('pr', views.pr_data, name='pr-data'),
    path('add-product-cart', views.add_product_cart, name='add-to-cart'),
    path('delete-product-cart', views.delete_product_cart, name='delete-product-cart'),
    path('change-product-quantity-cart', views.change_product_quantity_cart, name='change-product-quantity-cart'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('send-html', views.send_html, name='send-html'),
    path('password-change', views.change_password, name='password-change'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('edit-profile-image', views.edit_profile_image, name='edit-profile-image'),
]
