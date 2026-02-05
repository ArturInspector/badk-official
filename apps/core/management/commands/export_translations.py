import json
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from modeltranslation.translator import translator


class Command(BaseCommand):
    help = "Export modeltranslation fields to JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default="translations_export_db.json",
            help="Output JSON file path",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"])
        languages = [lang_code for lang_code, _ in settings.LANGUAGES]

        records = []
        stats = {}

        for model in translator.get_registered_models():
            options = translator.get_options_for_model(model)
            fields = list(options.fields)
            label = model._meta.label

            model_stats = {"records": 0, "fields": {}}

            for obj in model.objects.all():
                for field in fields:
                    source_value = getattr(obj, field, None)
                    if source_value is None or source_value == "":
                        continue

                    translations = {}
                    for lang in languages:
                        translations[lang] = getattr(obj, f"{field}_{lang}", "") or ""

                    records.append(
                        {
                            "model": label,
                            "id": obj.pk,
                            "field": field,
                            "source": source_value,
                            "translations": translations,
                        }
                    )

                    model_stats["records"] += 1
                    model_stats["fields"][field] = model_stats["fields"].get(field, 0) + 1

            if model_stats["records"]:
                stats[label] = model_stats

        payload = {"languages": languages, "records": records, "stats": stats}
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Exported to {output_path}"))
