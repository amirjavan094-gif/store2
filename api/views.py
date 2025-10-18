from .serializers import ProductSerializer
from store.models import Products
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        # تعیین کاربر به عنوان صاحب محصول
        serializer.save(user=self.request.user)

# from rest_framework import viewsets
# from .serializers import ProductSerializer
# from store.models import Products
# from .permissions import IsAdminOrReadOnly

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAdminOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


