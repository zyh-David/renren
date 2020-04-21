from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from article import views

urlpatterns = [
    path('image/', views.ImageAPIView.as_view()),
    path('collection/', views.CollecionAPIView.as_view()),
    re_path("^collection/(?P<pk>\d+)/$", views.CollecionDetailAPIView.as_view()),
    path('special/list/', views.SpecialListAPIView.as_view()),
    re_path("^(?P<pk>\d+)/$", views.ArticleInfoAPIView.as_view())

]

router = SimpleRouter()
router.register("", views.ArticleAPIView)
urlpatterns += router.urls