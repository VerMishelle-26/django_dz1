from rest_framework.routers import DefaultRouter
from .views import WorkplaceViewSet

router = DefaultRouter()
router.register("workplaces", WorkplaceViewSet)

urlpatterns = router.urls