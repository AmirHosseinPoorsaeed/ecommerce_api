from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views


router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

products_router = NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comments')

urlpatterns = router.urls + products_router.urls
