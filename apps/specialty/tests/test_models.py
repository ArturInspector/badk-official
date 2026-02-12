import pytest
from django.urls import reverse
from apps.specialty.tests.factories import SpecialtyFactory
from apps.specialty.models import Specialty
from common import constants as cons


@pytest.mark.django_db
@pytest.mark.models
class TestSpecialty:
    def test_creation(self):
        specialty = SpecialtyFactory()
        assert specialty.pk is not None
        assert specialty.title is not None
        assert specialty.slug is not None

    def test_slug_generation(self):
        specialty = SpecialtyFactory(title="Test Specialty Title")
        assert specialty.slug is not None
        assert len(specialty.slug) > 0

    def test_form_verbose(self):
        specialty = SpecialtyFactory(form_of_training=cons.FULL_TIME)
        assert specialty.form_verbose() is not None
        assert len(specialty.form_verbose()) > 0

    def test_basis_verbose(self):
        specialty = SpecialtyFactory(basis_learning=cons.CONTRACT)
        assert specialty.basis_verbose() is not None
        assert len(specialty.basis_verbose()) > 0

    def test_active_manager(self):
        active_specialty = SpecialtyFactory(is_active=True)
        inactive_specialty = SpecialtyFactory(is_active=False)

        active_queryset = Specialty.active.all()
        assert active_specialty in active_queryset
        assert inactive_specialty not in active_queryset

    def test_get_absolute_url(self):
        specialty = SpecialtyFactory()
        url = specialty.get_absolute_url()
        assert url is not None
        assert str(specialty.pk) in url

    def test_str_method(self):
        specialty = SpecialtyFactory(title="Test Specialty")
        assert str(specialty) == "Test Specialty"

    def test_choices_form_of_training(self):
        specialty_full = SpecialtyFactory(form_of_training=cons.FULL_TIME)
        specialty_part = SpecialtyFactory(form_of_training=cons.PART_TIME)
        specialty_full_part = SpecialtyFactory(form_of_training=cons.FULL_AND_PART)

        assert specialty_full.form_of_training == cons.FULL_TIME
        assert specialty_part.form_of_training == cons.PART_TIME
        assert specialty_full_part.form_of_training == cons.FULL_AND_PART

    def test_choices_basis_learning(self):
        specialty_contract = SpecialtyFactory(basis_learning=cons.CONTRACT)
        specialty_budget = SpecialtyFactory(basis_learning=cons.CONTRACT_BUDGET)

        assert specialty_contract.basis_learning == cons.CONTRACT
        assert specialty_budget.basis_learning == cons.CONTRACT_BUDGET


