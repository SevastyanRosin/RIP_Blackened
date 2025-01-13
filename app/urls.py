from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/units/', search_units),  # GET
    path('api/units/<int:unit_id>/', get_unit_by_id),  # GET
    path('api/units/<int:unit_id>/update/', update_unit),  # PUT
    path('api/units/<int:unit_id>/update_image/', update_unit_image),  # POST
    path('api/units/<int:unit_id>/delete/', delete_unit),  # DELETE
    path('api/units/create/', create_unit),  # POST
    path('api/units/<int:unit_id>/add_to_decree/', add_unit_to_decree),  # POST

    # Набор методов для заявок
    path('api/decrees/', search_decrees),  # GET
    path('api/decrees/<int:decree_id>/', get_decree_by_id),  # GET
    path('api/decrees/<int:decree_id>/update/', update_decree),  # PUT
    path('api/decrees/<int:decree_id>/update_status_user/', update_status_user),  # PUT
    path('api/decrees/<int:decree_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/decrees/<int:decree_id>/delete/', delete_decree),  # DELETE

    # Набор методов для м-м
    path('api/decrees/<int:decree_id>/units/<int:unit_id>/', get_unit_decree),  # GET
    path('api/decrees/<int:decree_id>/update_unit/<int:unit_id>/', update_unit_in_decree),  # PUT
    path('api/decrees/<int:decree_id>/delete_unit/<int:unit_id>/', delete_unit_from_decree),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/users/register/", register),  # POST
    path("api/users/login/", login),  # POST
    path("api/users/logout/", logout),  # POST
    path("api/users/<int:user_id>/update/", update_user)  # PUT
]
