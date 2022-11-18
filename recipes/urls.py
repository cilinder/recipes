from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:recipe_id>/', views.detail, name='detail'),
    path('new_recipe', views.new_recipe, name='new_recipe'),
    path('new_recipe/save', views.save_recipe, name='save_recipe'),
    path('delete/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
    path('edit/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
    path('update_recipe/<int:recipe_id>/', views.update_recipe, name='update_recipe'),
    path('upload_image', views.image_request, name='image_request'),

    path('api', views.api_root),
    path('api/recipe_list', views.RecipeList.as_view(), name='recipe-list'),
    path('api/recipe/<int:pk>', views.RecipeDetail.as_view(), name='recipe-detail'),
    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)