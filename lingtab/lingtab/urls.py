from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.views import LoginView
from core.views import DeleteTransactionView, NewTransaction, TransactionListView

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", include('core.urls')),
    path("api-auth/", include('rest_framework.urls')),
    path("api", include(router.urls)),
    path("new-transaction/", NewTransaction.as_view(), name='new-transaction'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('transaction/<int:pk>/delete/', DeleteTransactionView.as_view(), name='delete-transaction'),
    path('api/transactions/', TransactionListView.as_view(), name='api-transactions'),
]
