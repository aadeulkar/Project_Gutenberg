from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from .models import Book
from .serializers import BookSerializer
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework.response import Response


class BookPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all().order_by('-download_count').prefetch_related(
        'authors', 'bookshelves', 'languages', 'subjects',
    )
    serializer_class = BookSerializer

    pagination_class = BookPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        filters = self.request.query_params

        try:
            # Filter by Gutenberg ID
            gutenberg_ids = filters.getlist('gutenberg_id')
            if gutenberg_ids:
                gutenberg_ids = [gutenberg_id.strip() for gutenberg_id in ','.join(gutenberg_ids).split(',')]
                if not all(gutenberg_id.isdigit() for gutenberg_id in gutenberg_ids):
                    raise ValidationError({"gutenberg_id": "All Gutenberg IDs must be integers."})
                queryset = queryset.filter(gutenberg_id__in=gutenberg_ids)

            # Filter by Language
            raw_languages = filters.get('language', '') + ',' + ','.join(filters.getlist('languages'))
            languages = [lang.strip().lower() for lang in raw_languages.split(',') if lang.strip()]
            print("Parsed languages:", languages)

            if languages:
                # Validate that all values are strings
                if not all(isinstance(lang, str) for lang in languages):
                    raise ValidationError({"language": "Languages must be valid language codes."})

                # Apply the filter
                queryset = queryset.filter(languages__code__in=languages)

            # Filter by Mime-Type
            mime_types = filters.getlist('mime_type')
            if mime_types:
                queryset = queryset.filter(format__mime_type__in=[mime_type.lower() for mime_type in mime_types])

            # Filter by Topic (Subject or Bookshelf)
            topics = filters.getlist('topic')
            if topics:
                topic_query = Q()
                for topic in topics:
                    topic_query |= Q(subjects__name__icontains=topic) | Q(bookshelves__name__icontains=topic)
                queryset = queryset.filter(topic_query)

            # Filter by Author
            authors = filters.getlist('author')
            if authors:
                author_query = Q()
                for author in authors:
                    if author.isdigit():
                        raise ValidationError({"author": "Author filter must be a string, not a numeric ID."})
                    author_query |= Q(authors__name__icontains=author)
                queryset = queryset.filter(author_query)

            # Filter by Title
            titles = filters.getlist('title')
            if titles:
                title_query = Q()
                for title in titles:
                    title_query |= Q(title__icontains=title)
                queryset = queryset.filter(title_query)

            return queryset.distinct()

        except ValidationError as e:
            raise ValidationError({"error": e.detail})
        except Exception as e:
            raise ValidationError({"error": str(e)})
