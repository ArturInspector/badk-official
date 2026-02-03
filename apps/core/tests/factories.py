import factory
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.core.models import (
    Cooperation,
    InternationalCooperation,
    InternationalCooperationImages,
    Document,
    DocumentFile,
    EduProcess,
    EduProcessFile,
)


class CooperationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cooperation

    title = factory.Sequence(lambda n: f"Cooperation {n}")
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_cooperation.pdf",
            content=b"fake pdf content",
            content_type="application/pdf"
        )
    )


class InternationalCooperationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InternationalCooperation

    title = factory.Sequence(lambda n: f"International Cooperation {n}")
    description = factory.Faker('text', max_nb_chars=500)
    image = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_international.jpg",
            content=b"fake image content",
            content_type="image/jpeg"
        )
    )
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_agreement.pdf",
            content=b"fake pdf content",
            content_type="application/pdf"
        )
    )


class InternationalCooperationImagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = InternationalCooperationImages

    international = factory.SubFactory(InternationalCooperationFactory)
    image = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_image.jpg",
            content=b"fake image content",
            content_type="image/jpeg"
        )
    )


class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    title = factory.Sequence(lambda n: f"Document {n}")
    is_active = True


class DocumentFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DocumentFile

    document = factory.SubFactory(DocumentFactory)
    title = factory.Sequence(lambda n: f"Document File {n}")
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_document.pdf",
            content=b"fake pdf content",
            content_type="application/pdf"
        )
    )


class EduProcessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EduProcess

    title = factory.Sequence(lambda n: f"Education Process {n}")
    is_active = True


class EduProcessFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EduProcessFile

    process = factory.SubFactory(EduProcessFactory)
    title = factory.Sequence(lambda n: f"Process File {n}")
    file = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_process_file.pdf",
            content=b"fake pdf content",
            content_type="application/pdf"
        )
    )

