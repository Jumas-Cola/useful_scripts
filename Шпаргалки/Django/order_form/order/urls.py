from django.urls import path
from . import views
from django.conf.urls import url, include
from django.views.generic import RedirectView
from .models import Order

from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    # path('', RedirectView.as_view(url=LessonPart.objects.all().first().url, permanent=True)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('', views.OrderCreate.as_view(), name='index'),
    url(r'^update/(?P<pk>[-\w]+)$', views.OrderUpdate.as_view(), name='order_update'),
    url(r'^delete/(?P<pk>[-\w]+)$', views.OrderDelete.as_view(), name='order_delete'),
    url(r'^orders/(?P<pk>[-\w]+)$', views.OrderDetailView.as_view(), name='order_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
