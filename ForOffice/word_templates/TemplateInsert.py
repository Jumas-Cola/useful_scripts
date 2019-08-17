from os import path
from docxtpl import DocxTemplate


class TemplateInsert:
    def __init__(self, template_path, source, out_path=None, name=None, name_field=None):
        self.template_path = template_path
        self.source = source
        self.name_field = name_field
        self.name = name
        self.out_path = out_path

    def render(self):
        for n, context in enumerate(self.source):
            template = DocxTemplate(self.template_path)
            name = '{}_{}'.format(self.name if (
                self.name is not None) else 'new_document', n)
            if (self.name_field is not None) and (self.name_field in context):
                name = '{}'.format(context[self.name_field])
            name = path.join(self.out_path if (self.out_path is not None)
                             else path.split(self.template_path)[0], name)
            template.render(context)
            if path.exists(name + '.docx'):
                name = '{}_{}'.format(name, n)
            template.save(name + '.docx')
