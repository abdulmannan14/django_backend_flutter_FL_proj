"""Amplified_Beauty_Australia_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from amplifiedbeautyaus.api import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls', namespace='rest_framework_social_oauth2')),

    path('api/', include([
        path('auth/', include([
            path('login/', LoginView.as_view()),
            path('apple/', AppleLoginView.as_view()),
            path('google/', GoogleLoginView.as_view()),
            path('register/', CustomerRegisterView.as_view()),
            path('profile/', GetCustomerProfileView.as_view()),
            path('reset/', include([
                path('request/', ResetPasswordRequestView.as_view()),
                path('confirm/', ResetPasswordConfirmView.as_view()),
            ])),
        ])),

        path('products/', include([
            path('search/<str:query>', SearchProducts.as_view()),
            path('popular/', GetPopularProductsView.as_view()),
            path('get/<pk>', GetProductDetail.as_view()),
            path('range/', include([
                path('', GetProductRanges.as_view()),
                path('<pk>', GetProductRangeDetails.as_view()),
            ])),
        ])),

        path('tips/', include([
            path('get/', GetAllTipsView.as_view()),
            path('bookmarked/', GetBookmarkedTipsView.as_view()),
            path('actions/', include([
                path('add/<pk>', AddBookmarkTipView.as_view()),
                path('remove/<pk>', RemoveBookmarkTipView.as_view()),
            ])),
        ])),

        path('alerts/', include([
            path('get/', GetUserAlerts.as_view()),
            path('actions/', include([
                path('delete/<pk>', DeleteUserAlert.as_view()),
                path('delete_all/', DeleteAllUserAlerts.as_view())
            ])),
        ])),

        path('wishlist/', include([
            path('get/', GetCustomerWishlist.as_view()),
            path('add/', AddProductToWishlist.as_view()),
            path('remove/', RemoveProductFromWishlist.as_view()),
        ])),

        path('addresses/', include([
            path('get/', GetCustomerAddresses.as_view()),
            path('set/', SetCustomerAddress.as_view()),
            path('create/', CreateCustomerAddress.as_view()),
            path('delete/', DeleteCustomerAddress.as_view()),
        ])),

        path('cart/', include([
            path('get/', GetUserCart.as_view()),
            path('add/', AddItemToCart.as_view()),
            path('remove/<pk>', RemoveItemFromCart.as_view()),
            path('quantity/', include([
                path('add/<pk>', AddQuantityFromCart.as_view()),
                path('remove/<pk>', RemoveQuantityFromCart.as_view()),
            ])),
        ])),

        path('order/', include([
            path('payment/', UpdatePaymentMethodView.as_view()),
            path('place/', PlaceOrderView.as_view()),
        ])),

        path('orders/', include([
            path('details/<pk>', GetOrderDetails.as_view()),
            path('active/', GetAllActiveOrders.as_view()),
            path('past/', GetAllPastOrders.as_view()),
        ])),
    ])),
]
