from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.diagnoseView.as_view(), name='diagnose'),
    path('alzheimer/', views.AlzheimerView.as_view(), name='alzheimer'),
    path('alzheimer_result/', views.AlzheimerResultView.as_view(), name='alzheimer_result')
]
