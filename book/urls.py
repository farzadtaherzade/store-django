from django.urls import path
from . import views

urlpatterns = [
    # Books
    path("", views.BookCreateListCreateView.as_view(), name="book-list-create"),
    path("<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),

    # Reviews (still logically tied to books)
    path("<int:book_id>/reviews/", views.ReviewList.as_view(), name="review-list"),
    path("<int:book_id>/reviews/create/",
         views.ReviewCreate.as_view(), name="review-create"),

    # Single review detail (update/delete/view)
    path("reviews/<int:pk>/", views.ReviewRetrieveUpdateDestroy.as_view(),
         name="review-detail"),
]
