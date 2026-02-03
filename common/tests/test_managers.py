import pytest
from django.utils import timezone
from django.db import models
from common.managers import ActiveManager
from apps.core.tests.factories import DocumentFactory, EduProcessFactory
from apps.core.models import Document


@pytest.mark.django_db
class TestActiveManager:
    def test_filter_active_only(self):
        active_doc = DocumentFactory(is_active=True)
        inactive_doc = DocumentFactory(is_active=False)

        active_queryset = Document.active.all()
        assert active_doc in active_queryset
        assert inactive_doc not in active_queryset

    def test_order_by_created_desc(self):
        from apps.core.models import EduProcess
        process1 = EduProcessFactory(is_active=True)
        process2 = EduProcessFactory(is_active=True)
        process3 = EduProcessFactory(is_active=True)

        active_queryset = EduProcess.active.all()
        assert len(active_queryset) == 3
        queryset_list = list(active_queryset)
        assert queryset_list[0].created >= queryset_list[1].created
        assert queryset_list[1].created >= queryset_list[2].created

    def test_only_active_in_queryset(self):
        DocumentFactory.create_batch(3, is_active=True)
        DocumentFactory.create_batch(2, is_active=False)

        active_queryset = Document.active.all()
        assert active_queryset.count() == 3
        for item in active_queryset:
            assert item.is_active is True

