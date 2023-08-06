from rest_framework import routers
from .views import (
    AggregateListViewSet, IPAddressListViewSet, ListsRootView, PrefixListViewSet, PrometheusDeviceSD,
    PrometheusVirtualMachineSD, ServiceListviewSet, TagsListViewSet
)

router = routers.DefaultRouter()
router.APIRootView = ListsRootView

router.register("prefixes", PrefixListViewSet)
router.register("ip-addresses", IPAddressListViewSet)
router.register("aggregates", AggregateListViewSet)
router.register("services", ServiceListviewSet)
router.register("tags", TagsListViewSet)
router.register("prometheus-devices", PrometheusDeviceSD)
router.register("prometheus-vms", PrometheusVirtualMachineSD)
urlpatterns = router.urls
