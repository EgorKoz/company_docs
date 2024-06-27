from docxtpl import DocxTemplate
from datetime import datetime


def generate_word(path, params):
    doc = DocxTemplate(
        r"C:\Users\ekozlov\PycharmProjects\company_docs\documents\tmp.docx")
    doc.render(params)
    date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    doc.save(
        rf"C:\Users\ekozlov\PycharmProjects\company_docs\documents\mediafiles\tmp_{date}.docx")

    return rf"C:\Users\ekozlov\PycharmProjects\company_docs\documents\mediafiles\tmp_{date}.docx"