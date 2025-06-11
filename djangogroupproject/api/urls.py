from rest_framework.routers import DefaultRouter
from .viewsets import CampaignViewSet, OrganizationViewSet, DonationViewSet, TagViewSet

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'donations', DonationViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = router.urls