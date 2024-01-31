from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views


router = DefaultRouter()

router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('carts', views.CartViewSet, basename='cart')

products_router = NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('comments', views.CommentViewSet, basename='product-comments')

carts_router = NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_router.urls
