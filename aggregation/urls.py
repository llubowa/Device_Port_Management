from django.urls import path
from . import views


urlpatterns = [
	path('aggregation/',views.aggregation, name="aggregation-hubs"),
    path('aggsearch/',views.aggsearch,name="aggregation-search"),
    path('aggedit/',views.aggedit,name="aggregation-edit"),
    path('aggfree/',views.aggfree,name="aggregation-free"),
]