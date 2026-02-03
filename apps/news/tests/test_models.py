import pytest
from django.urls import reverse
from apps.news.tests.factories import NewsFactory, NewsImagesFactory


@pytest.mark.django_db
@pytest.mark.models
class TestNews:
    def test_creation(self):
        news = NewsFactory()
        assert news.pk is not None
        assert news.title is not None
        assert news.slug is not None

    def test_slug_generation(self):
        news = NewsFactory(title="Test News Title")
        assert news.slug is not None
        assert len(news.slug) > 0

    def test_active_manager(self):
        active_news = NewsFactory(is_active=True)
        inactive_news = NewsFactory(is_active=False)

        active_queryset = news.active.all()
        assert active_news in active_queryset
        assert inactive_news not in active_queryset

    def test_get_absolute_url(self):
        news = NewsFactory()
        url = news.get_absolute_url()
        assert url is not None
        assert news.slug in url

    def test_str_method(self):
        news = NewsFactory(title="Test News")
        assert str(news) == "Test News"


@pytest.mark.django_db
@pytest.mark.models
class TestNewsImages:
    def test_creation(self):
        image = NewsImagesFactory()
        assert image.pk is not None
        assert image.news is not None
        assert image.image is not None

    def test_relationship(self):
        news = NewsFactory()
        image = NewsImagesFactory(news=news)
        assert image.news == news
        assert image in news.images.all()

    def test_str_method(self):
        news = NewsFactory(title="Test News")
        image = NewsImagesFactory(news=news)
        assert str(image) == news.title

