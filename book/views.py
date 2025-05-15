from rest_framework import generics
from .serializers import BooksSerializers
from .models import Books
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.


class BookCreateListCreateView(generics.ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["author", "language"]
    ordering_fields = ["created", "price"]
    search_fields = ["name", "description"]

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializers
    permission_classes = [IsOwnerOrReadOnly]
