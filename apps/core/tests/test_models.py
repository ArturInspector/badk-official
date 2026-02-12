import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from apps.core.tests.factories import (
    CooperationFactory,
    InternationalCooperationFactory,
    InternationalCooperationImagesFactory,
    DocumentFactory,
    DocumentFileFactory,
    EduProcessFactory,
    EduProcessFileFactory,
)


@pytest.mark.django_db
@pytest.mark.models
class TestCooperation:
    def test_creation(self):
        cooperation = CooperationFactory()
        assert cooperation.pk is not None
        assert cooperation.title is not None
        assert cooperation.file is not None

    def test_str_method(self):
        cooperation = CooperationFactory(title="Test Cooperation")
        assert str(cooperation) == "Test Cooperation"


@pytest.mark.django_db
@pytest.mark.models
class TestInternationalCooperation:
    def test_creation(self):
        international = InternationalCooperationFactory()
        assert international.pk is not None
        assert international.title is not None
        assert international.slug is not None

    def test_slug_generation(self):
        international = InternationalCooperationFactory(title="Test International")
        assert international.slug is not None
        assert len(international.slug) > 0

    def test_get_absolute_url(self):
        international = InternationalCooperationFactory()
        url = international.get_absolute_url()
        assert url is not None
        assert international.slug in url

    def test_str_method(self):
        international = InternationalCooperationFactory(title="Test")
        assert str(international) == "Test"


@pytest.mark.django_db
@pytest.mark.models
class TestInternationalCooperationImages:
    def test_creation(self):
        image = InternationalCooperationImagesFactory()
        assert image.pk is not None
        assert image.international is not None
        assert image.image is not None

    def test_relationship(self):
        international = InternationalCooperationFactory()
        image = InternationalCooperationImagesFactory(international=international)
        assert image.international == international
        assert image in international.images.all()

    def test_str_method(self):
        international = InternationalCooperationFactory(title="Test")
        image = InternationalCooperationImagesFactory(international=international)
        assert str(image) == str(international.title)


@pytest.mark.django_db
@pytest.mark.models
class TestDocument:
    def test_creation(self):
        document = DocumentFactory()
        assert document.pk is not None
        assert document.title is not None
        assert document.is_active is True

    def test_is_active_default(self):
        document = DocumentFactory(is_active=False)
        assert document.is_active is False

    def test_str_method(self):
        document = DocumentFactory(title="Test Document")
        assert str(document) == "Test Document"


@pytest.mark.django_db
@pytest.mark.models
class TestDocumentFile:
    def test_creation(self):
        file = DocumentFileFactory()
        assert file.pk is not None
        assert file.document is not None
        assert file.title is not None
        assert file.file is not None

    def test_relationship(self):
        document = DocumentFactory()
        file = DocumentFileFactory(document=document)
        assert file.document == document
        assert file in document.files.all()

    def test_str_method(self):
        document = DocumentFactory(title="Test Doc")
        file = DocumentFileFactory(document=document, title="Test File")
        assert "Test Doc" in str(file)
        assert "Test File" in str(file)


@pytest.mark.django_db
@pytest.mark.models
class TestEduProcess:
    def test_creation(self):
        process = EduProcessFactory()
        assert process.pk is not None
        assert process.title is not None
        assert process.is_active is True

    def test_active_manager(self):
        active_process = EduProcessFactory(is_active=True)
        inactive_process = EduProcessFactory(is_active=False)

        active_queryset = EduProcess.active.all()
        assert active_process in active_queryset
        assert inactive_process not in active_queryset

    def test_str_method(self):
        process = EduProcessFactory(title="Test Process")
        assert str(process) == "Test Process"


@pytest.mark.django_db
@pytest.mark.models
class TestEduProcessFile:
    def test_creation(self):
        file = EduProcessFileFactory()
        assert file.pk is not None
        assert file.process is not None
        assert file.title is not None
        assert file.file is not None

    def test_relationship(self):
        process = EduProcessFactory()
        file = EduProcessFileFactory(process=process)
        assert file.process == process
        assert file in process.files.all()

    def test_str_method(self):
        process = EduProcessFactory(title="Test Process")
        file = EduProcessFileFactory(process=process, title="Test File")
        assert "Test Process" in str(file)
        assert "Test File" in str(file)


