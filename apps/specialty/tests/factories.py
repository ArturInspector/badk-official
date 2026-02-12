import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.specialty.models import Specialty
from common import constants as cons


class SpecialtyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Specialty

    title = factory.Sequence(lambda n: f"Specialty {n}")
    description = factory.Faker('text', max_nb_chars=500)
    contract = factory.Sequence(lambda n: f"{n * 10000} som")
    form_of_training = cons.FULL_TIME
    basis_learning = cons.CONTRACT
    is_active = True
    image = factory.LazyAttribute(
        lambda _: SimpleUploadedFile(
            name="test_specialty.jpg",
            content=b"fake image content",
            content_type="image/jpeg"
        )
    )


