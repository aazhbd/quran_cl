from django.db import models

from django.contrib.auth.models import User

class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, blank=False)
    iso_code = models.CharField(max_length=50, blank=False)
    direction = models.IntegerField(blank=False)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        pass


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    country = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=250, blank=True)
    alang = models.ForeignKey(Language, related_name='author_language', blank=True)
    translation_type = models.CharField(max_length=50, blank=True)
    date_published = models.DateTimeField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        pass


class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    english_name = models.CharField(max_length=1000, blank=False)
    arabic_name = models.CharField(max_length=1000, blank=False)
    transliteration = models.CharField(max_length=1000, blank=False)
    total_verses = models.IntegerField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.transliteration )

    class Meta:
        pass


class Verse(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(blank=False)

    vtext = models.CharField(max_length=10000, blank=False)

    chapter = models.ForeignKey(Chapter, related_name='chapter', null=True)
    author = models.ForeignKey(Author, related_name='author', null=True)
    vlang = models.ForeignKey(Language, related_name='verse_language', null=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.vlang) + " - " + str(self.number) + ":" + str(self.chapter)

    class Meta:
        pass


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='user')

    vnum = models.IntegerField(blank=False)
    cnum = models.IntegerField(blank=False)

    ctext = models.TextField('Comment', blank=False)
    comment_type = models.CharField(max_length=100, blank=False, choices=(('Translation', 'Translation'), ('Explanation', 'Explanation'), ('Question', 'Question'), ('Comments', 'Comments')), default='Question')
    date_published = models.DateTimeField(null=False, blank=False,auto_now_add=True)

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        pass
