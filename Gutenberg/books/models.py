from django.db import models


class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'books_author'


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField()
    media_type = models.CharField(max_length=16)
    title = models.TextField(blank=True, null=True)

    # Relationships
    authors = models.ManyToManyField(Author, through='BookAuthor', related_name='books')
    bookshelves = models.ManyToManyField('Bookshelf', through='BookBookshelf', related_name='books')
    languages = models.ManyToManyField('Language', through='BookLanguage', related_name='books')
    subjects = models.ManyToManyField('Subject', through='BookSubject', related_name='books')

    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'books_book'


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_book_authors'


class Bookshelf(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'books_bookshelf'


class BookBookshelf(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_book_bookshelves'


class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'books_language'


class BookLanguage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_book_languages'


class Subject(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'books_subject'


class BookSubject(models.Model):
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_book_subjects'


class Format(models.Model):
    id = models.IntegerField(primary_key=True)
    mime_type = models.CharField(max_length=32)
    url = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'books_format'
