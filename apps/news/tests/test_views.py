import pytest
from django.urls import reverse
from apps.news.tests.factories import NewsFactory, NewsImagesFactory


@pytest.mark.django_db
class TestNewsListView:
    def test_list_view_status_code(self, client):
        NewsFactory.create_batch(5, is_active=True)
        url = reverse('news_list')
        response = client.get(url)
        assert response.status_code == 200

    def test_list_view_context(self, client):
        NewsFactory.create_batch(5, is_active=True)
        NewsFactory.create_batch(2, is_active=False)
        url = reverse('news_list')
        response = client.get(url)
        assert 'news' in response.context
        assert len(response.context['news']) == 5
        assert 'title' in response.context
        assert 'sub_title' in response.context

    def test_list_view_only_active(self, client):
        NewsFactory.create_batch(3, is_active=True)
        NewsFactory.create_batch(2, is_active=False)
        url = reverse('news_list')
        response = client.get(url)
        assert len(response.context['news']) == 3
        for news_item in response.context['news']:
            assert news_item.is_active is True


@pytest.mark.django_db
class TestNewsDetailView:
    def test_detail_view_status_code(self, client):
        news = NewsFactory(is_active=True)
        url = reverse('news_detail', kwargs={'slug': news.slug})
        response = client.get(url)
        assert response.status_code == 200

    def test_detail_view_context(self, client):
        news = NewsFactory(is_active=True)
        NewsImagesFactory.create_batch(3, news=news)
        url = reverse('news_detail', kwargs={'slug': news.slug})
        response = client.get(url)
        assert 'item' in response.context
        assert response.context['item'] == news
        assert response.context['item'].images.count() == 3
        assert 'title' in response.context

    def test_detail_view_404_inactive(self, client):
        news = NewsFactory(is_active=False)
        url = reverse('news_detail', kwargs={'slug': news.slug})
        response = client.get(url)
        assert response.status_code == 404

    def test_detail_view_404_nonexistent(self, client):
        url = reverse('news_detail', kwargs={'slug': 'non-existent-slug'})
        response = client.get(url)
        assert response.status_code == 404


