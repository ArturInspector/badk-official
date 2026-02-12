import pytest
from django.urls import reverse
from apps.specialty.tests.factories import SpecialtyFactory


@pytest.mark.django_db
class TestSpecialtyListView:
    def test_list_view_status_code(self, client):
        SpecialtyFactory.create_batch(5, is_active=True)
        url = reverse('specialties_list')
        response = client.get(url)
        assert response.status_code == 200

    def test_list_view_context(self, client):
        SpecialtyFactory.create_batch(5, is_active=True)
        SpecialtyFactory.create_batch(2, is_active=False)
        url = reverse('specialties_list')
        response = client.get(url)
        assert 'specialties' in response.context
        assert len(response.context['specialties']) == 7

    def test_list_view_queryset(self, client):
        SpecialtyFactory.create_batch(3, is_active=True)
        SpecialtyFactory.create_batch(2, is_active=False)
        url = reverse('specialties_list')
        response = client.get(url)
        assert len(response.context['specialties']) == 5


@pytest.mark.django_db
class TestSpecialtyDetailView:
    def test_detail_view_status_code(self, client):
        specialty = SpecialtyFactory()
        url = reverse('specialties_detail', kwargs={'pk': specialty.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_detail_view_context(self, client):
        specialty = SpecialtyFactory()
        url = reverse('specialties_detail', kwargs={'pk': specialty.pk})
        response = client.get(url)
        assert 'specialty' in response.context
        assert response.context['specialty'] == specialty

    def test_detail_view_404(self, client):
        url = reverse('specialties_detail', kwargs={'pk': 99999})
        response = client.get(url)
        assert response.status_code == 404


