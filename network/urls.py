from rest_framework.routers import DefaultRouter
from network.apps import NetworkConfig
from network.views import NetworkLinkViewSet, ProductViewSet


app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r"networks", NetworkLinkViewSet, basename='networks')
router.register(r"products", ProductViewSet, basename='products')

urlpatterns = []

urlpatterns += router.urls
