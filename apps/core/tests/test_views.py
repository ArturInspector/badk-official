import pytest
from django.urls import reverse
from apps.core.tests.factories import (
    DocumentFactory,
    DocumentFileFactory,
    CooperationFactory,
    InternationalCooperationFactory,
    InternationalCooperationImagesFactory,
    EduProcessFactory,
    EduProcessFileFactory,
)


@pytest.mark.django_db
class TestIndexView:
    def test_index_view_status_code(self, client):
        url = reverse('index')
        response = client.get(url)
        assert response.status_code == 200

    def test_index_view_context(self, client):
        url = reverse('index')
        response = client.get(url)
        assert 'specialties' in response.context
        assert 'news' in response.context
        assert 'lives' in response.context
        assert 'employees' in response.context
        assert 'students' in response.context
        assert 'internationals' in response.context


@pytest.mark.django_db
class TestHistoryView:
    def test_history_view_status_code(self, client):
        url = reverse('history')
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestPasswordCollegeView:
    def test_password_college_view_status_code(self, client):
        url = reverse('password_college')
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestDocumentListView:
    def test_list_view_status_code(self, client):
        DocumentFactory.create_batch(3, is_active=True)
        url = reverse('documents_list')
        response = client.get(url)
        assert response.status_code == 200

    def test_list_view_context(self, client):
        DocumentFactory.create_batch(3, is_active=True)
        url = reverse('documents_list')
        response = client.get(url)
        assert 'documents' in response.context
        assert len(response.context['documents']) == 3

    def test_list_view_inactive_documents(self, client):
        DocumentFactory.create_batch(2, is_active=True)
        DocumentFactory.create_batch(2, is_active=False)
        url = reverse('documents_list')
        response = client.get(url)
        assert len(response.context['documents']) == 4


@pytest.mark.django_db
class TestDocumentDetailView:
    def test_detail_view_status_code(self, client):
        document = DocumentFactory()
        url = reverse('documents_detail', kwargs={'pk': document.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_detail_view_context(self, client):
        document = DocumentFactory()
        DocumentFileFactory.create_batch(3, document=document)
        url = reverse('documents_detail', kwargs={'pk': document.pk})
        response = client.get(url)
        assert 'document' in response.context
        assert response.context['document'] == document
        assert response.context['document'].files.count() == 3

    def test_detail_view_404(self, client):
        url = reverse('documents_detail', kwargs={'pk': 99999})
        response = client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestCooperationView:
    def test_cooperation_view_status_code(self, client):
        CooperationFactory.create_batch(3)
        url = reverse('cooperation')
        response = client.get(url)
        assert response.status_code == 200

    def test_cooperation_view_context(self, client):
        CooperationFactory.create_batch(3)
        url = reverse('cooperation')
        response = client.get(url)
        assert 'cooperation' in response.context
        assert len(response.context['cooperation']) == 3


@pytest.mark.django_db
class TestInternationalCooperationListView:
    def test_list_view_status_code(self, client):
        InternationalCooperationFactory.create_batch(3)
        url = reverse('internationals')
        response = client.get(url)
        assert response.status_code == 200

    def test_list_view_context(self, client):
        InternationalCooperationFactory.create_batch(3)
        url = reverse('internationals')
        response = client.get(url)
        assert 'internationals' in response.context
        assert len(response.context['internationals']) == 3


@pytest.mark.django_db
class TestInternationalCooperationDetailView:
    def test_detail_view_status_code(self, client):
        international = InternationalCooperationFactory()
        url = reverse('international_detail', kwargs={'slug': international.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_detail_view_context(self, client):
        international = InternationalCooperationFactory()
        InternationalCooperationImagesFactory.create_batch(3, international=international)
        url = reverse('international_detail', kwargs={'slug': international.slug})
        response = client.get(url)
        assert 'international' in response.context
        assert response.context['international'] == international
        assert response.context['international'].images.count() == 3

    def test_detail_view_404(self, client):
        url = reverse('international_detail', kwargs={'slug': 'non-existent-slug'})
        response = client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestEduProcessDetailView:
    def test_detail_view_status_code(self, client):
        process = EduProcessFactory()
        url = reverse('edu_process_detail', kwargs={'pk': process.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_detail_view_context(self, client):
        process = EduProcessFactory()
        EduProcessFileFactory.create_batch(3, process=process)
        url = reverse('edu_process_detail', kwargs={'pk': process.pk})
        response = client.get(url)
        assert 'process' in response.context
        assert response.context['process'] == process
        assert response.context['process'].files.count() == 3

    def test_detail_view_404(self, client):
        url = reverse('edu_process_detail', kwargs={'pk': 99999})
        response = client.get(url)
        assert response.status_code == 404


