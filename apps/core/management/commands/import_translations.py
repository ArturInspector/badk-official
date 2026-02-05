import json
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Import modeltranslation fields from JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "--input",
            default="translations_export_db.json",
            help="Input JSON file path",
        )

    def handle(self, *args, **options):
        input_path = Path(options["input"])
        if not input_path.exists():
            raise FileNotFoundError(f"{input_path} not found")

        with input_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        default_language = settings.LANGUAGE_CODE.split("-")[0]
        languages = payload.get("languages", [])

        updated = 0
        skipped = 0

        for record in payload.get("records", []):
            model_label = record.get("model")
            obj_id = record.get("id")
            field = record.get("field")
            translations = record.get("translations", {})

            if not model_label or obj_id is None or not field:
                skipped += 1
                continue

            try:
                model = apps.get_model(model_label)
            except LookupError:
                skipped += 1
                continue

            update_fields = {}
            for lang in languages:
                value = translations.get(lang)
                if value is None or value == "":
                    continue
                update_fields[f"{field}_{lang}"] = value
                if lang == default_language:
                    update_fields[field] = value

            if not update_fields:
                skipped += 1
                continue

            model.objects.filter(pk=obj_id).update(**update_fields)
            updated += 1

        self.stdout.write(
            self.style.SUCCESS(f"Updated: {updated}, Skipped: {skipped}")
        )
