import factory
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.news.models import News, NewsImages


class NewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = News

    title = factory.Sequence(lambda n: f"News {n}")
    description = factory.Faker('text', max_nb_chars=500)
    is_active = True
    created = factory.LazyFunction(timezone.now)
    youtube = factory.Faker('url')
    image = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_news.jpg",
            content=b"fake image content",
            content_type="image/jpeg"
        )
    )


class NewsImagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NewsImages

    news = factory.SubFactory(NewsFactory)
    image = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_news_image.jpg",
            content=b"fake image content",
            content_type="image/jpeg"
        )
    )


