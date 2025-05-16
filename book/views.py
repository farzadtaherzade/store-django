from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import BooksSerializers, ReviewSerializers
from .models import Books, Review
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
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


class ReviewCreate(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)


class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["created_at", "updated_at", "rating"]
    search_fields = ["comment"]
    ordering = ["-created_at"]

    def get_queryset(self):
        book_id = self.kwargs.get("book_id")
        return self.queryset.filter(book_id=book_id)


class ReviewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsOwnerOrReadOnly]
