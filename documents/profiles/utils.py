from docxtpl import DocxTemplate
from django.conf import settings
from pathlib import Path


def generate_word(path, params):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    doc = DocxTemplate(settings.MEDIA_ROOT / 'tmp.docx')
    doc.render(params)
    doc.save(path)
