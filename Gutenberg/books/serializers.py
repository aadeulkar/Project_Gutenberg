from rest_framework import serializers
from .models import Book, Author, Bookshelf, Format, Language, Subject


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'death_year']


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['mime_type', 'url']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']


class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = ['name']


class BookSerializer(serializers.ModelSerializer):
    # Assuming these fields exist in the Book model and related models
    title = serializers.CharField()
    authors = AuthorSerializer(many=True, read_only=True)
    bookshelves = BookshelfSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    download_links = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'title', 'authors', 'languages', 'subjects', 'bookshelves',  'download_links'
        ]

    def get_download_links(self, obj):
        # Fetch formats related to the book
        formats = Format.objects.filter(book=obj)
        return FormatSerializer(formats, many=True).data
