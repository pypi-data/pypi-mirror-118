"""
Generator module where the real work happens
"""
from os import path, system
import inflect
from dr_scaffold.scaffold_templates import model_templates
from dr_scaffold.scaffold_templates import admin_templates
from dr_scaffold.scaffold_templates import view_templates
from dr_scaffold.scaffold_templates import serializer_templates
from dr_scaffold.scaffold_templates import url_templates
from dr_scaffold import file_api

def pluralize(string):
    """
    pluralizes a string word using a python library, needed for verbose model names and url paths
    """
    pluralizer = inflect.engine()
    return pluralizer.plural(string)

class Generator():
    """
    A wrapper for CLI command arguments and the REST api different files generation methods
    """

    def __init__(self, appdir, model_name, fields):
        """
        :param appdir: a string that has the app directory's path or just the appname itself
        :param model_name: model name we want to generate
        :param fields: a list of fields strings we want to generate along
        """
        self.appdir = appdir
        self.app_name = appdir.split("/")[1] if len(appdir.split('/'))>= 2 else appdir
        self.model_name = model_name
        self.fields = fields

    def run(self):
        """
        runs generate api and throws an exception if something went wrong
        """
        try:
            self.generate_api()
        except Exception as error:
            return print(f"🤔 Oops something is wrong: {error}")
        return print(f"🎉 Your RESTful {self.model_name} api resource is ready 🎉")

    def generate_api(self):
        """
        Generates a REST api files based on CLI command arguments
        """
        self.generate_app()
        self.generate_models()
        self.register_models_to_admin()
        self.generate_serializers()
        self.generate_views()
        self.generate_urls()

    @classmethod
    def add_setup_imports(cls, file_paths, matching_imports):
        """
        adds the bare minimum imports needed for each file
        """
        for i, file_path in enumerate(file_paths):
            file_api.set_file_content(file_path, matching_imports[i])

    def setup_files(self):
        """
        creates files if not exist, and adds appropriate imports
        """
        files = (f"{self.appdir}/serializers.py",
            f"{self.appdir}/urls.py",
            f"{self.appdir}/models.py",
            f"{self.appdir}/admin.py",
            f"{self.appdir}/views.py")
        files_matching_imports = (serializer_templates.SETUP,
            url_templates.SETUP,
            model_templates.SETUP,
            admin_templates.SETUP,
            view_templates.SETUP)
        file_api.create_files(files)
        file_api.wipe_files(files)
        self.add_setup_imports(files, files_matching_imports)

    def generate_app(self):
        """
        APP GENERATION
        1 - first we generate a django app through django's startapp command
        2 - we move the generated app directory to the apps directory if one is
         specified in our CLI command
        3 - we setup the files with the basic imports needed for each component
        4 - if application folder does already exist we return
        """
        if not path.exists('%s' % (self.appdir)):
            system(f'python manage.py startapp {self.app_name}')
            if self.appdir != self.app_name:
                system(f'mv {self.app_name} {self.appdir}')
            self.setup_files()

    def get_fields_string(self, fields):
        """
        get appropriate fields templates based on the field type and return them joined in a string
        """
        actual_fields = []
        relation_types = ('foreignkey', 'manytomany', 'onetoone')
        file = f"{self.appdir}/models.py"
        for field in fields:
            field_name = field.split(':')[0]
            field_type = field.split(':')[1].lower()
            field_dict = dict(name= field_name,
                related = field.split(':')[2] if (field_type in relation_types) else '')
            if field_type in relation_types:
                # tells developer if related model doesn't exist in file
                chunk = f'class {field_dict["related"]}(models.Model)'
                if not file_api.is_present_in_file(file, chunk):
                    print(f"⚠️ bare in mind that {field_dict['related']} model doesn't exist yet!")
            field_template = model_templates.FIELD_TYPES[field_type] % field_dict
            actual_fields.append(field_template)
        fields_string = ''.join(f for f in actual_fields)
        return fields_string

    def get_model_string(self):
        """
        returns a Model class string with fields and Meta class
        """
        fields_string = self.get_fields_string(self.fields)
        params = (self.model_name, fields_string, pluralize(self.model_name.lower()).capitalize())
        return model_templates.MODEL % params

    def generate_models(self):
        """
        MODELS GENERATION METHODS
        1 - get_fields_string : match fields from cli with their templates and return a
         string of them joined
        2 - get_model_string : yield the fields string in the Model template and returns
         a new Model string
        3 - generate_models: check if the model does already exists in the models.py
         file if not it append it
        """
        file = f"{self.appdir}/models.py"
        chunk = f'class {self.model_name}'
        if file_api.is_present_in_file(file, chunk):
            return
        model_string = self.get_model_string()
        file_api.append_file_content(file, model_string)

    def get_admin_parts(self):
        """
        returns admin Model register template and import
        """
        app_path = self.appdir.replace("/", ".")
        model_register_template = admin_templates.REGISTER % {'model': self.model_name}
        model_import_template = admin_templates.MODEL_IMPORT % {'app': app_path,
            'model': self.model_name}
        return (model_import_template, model_register_template)

    def register_models_to_admin(self):
        """
        MODELS REGISTRATION TO ADMIN
        1 - get_admin_parts : returns the register template and imports of the Model
         class
        2 - register_models_to_admin : check if the model already registered in admin.py
         if not it wraps the admin file content between the Model imports and register
         template
        """
        file = f"{self.appdir}/admin.py"
        chunk = f'@admin.register({self.model_name})'
        if file_api.is_present_in_file(file, chunk):
            return
        head, body = self.get_admin_parts()
        file_api.wrap_file_content(file, head, body)

    def get_viewset_parts(self):
        """
        returns viewsets templates and imports
        """
        app_path = self.appdir.replace("/", ".")
        viewset_template = view_templates.VIEWSET % {'model': self.model_name}
        model_import_template = view_templates.MODEL_IMPORT % {'app': app_path,
            'model': self.model_name}
        serializer_import_template= view_templates.SERIALIZER_IMPORT % {'app': app_path,
            'model': self.model_name}
        imports = model_import_template + serializer_import_template
        return (imports, viewset_template)

    def generate_views(self):
        """
        VIEWS GENERATION
        1 - get_viewset_parts : returns the viewset template and model + serializers
        imports of the Model class
        2 - generate_views : check if the viewset already exists in views.py if not
        it wraps the file content between the imports and the viewset template
        """
        file = f"{self.appdir}/views.py"
        chunk = f'class {self.model_name}ViewSet'
        if file_api.is_present_in_file(file, chunk):
            return
        head, body = self.get_viewset_parts()
        file_api.wrap_file_content(file, head, body)

    def get_serializer_parts(self):
        """
        returns serializer class template and model import
        """
        app_path = self.appdir.replace("/", ".")
        serializer_template = serializer_templates.SERIALIZER % {'model': self.model_name}
        imports = serializer_templates.MODEL_IMPORT % {'app': app_path, 'model': self.model_name}
        return(imports, serializer_template)

    def generate_serializers(self):
        """
        SERIALIZER GENERATION
        1 - get_serializer_parts : returns the serializer template and imports of the Model class
        2 - generate_serializers : check if the viewset already exists in serializers.py if not
        it wraps the file content between the imports and the serializer template
        """
        serializer_file = f"{self.appdir}/serializers.py"
        serializer_head = f'class {self.model_name}Serializer'
        if file_api.is_present_in_file(serializer_file, serializer_head):
            return
        head, body = self.get_serializer_parts()
        file_api.wrap_file_content(serializer_file, head, body)

    def get_url_parts(self):
        """
        returns the url template and imports of the Model class
        """
        app_path = self.appdir.replace("/", ".")
        plural_path = pluralize(self.model_name.lower())
        url_template = url_templates.URL % {'model': self.model_name, 'path': plural_path}
        imports = url_templates.MODEL_IMPORT % {'app': app_path, 'model': self.model_name}
        return(imports, url_template)

    def generate_urls(self):
        """
        URLS GENERATION
        1 - get_url_parts : returns the url template and model imports of the Model class
        2 - generate_urls : check if the url already exists in urls.py if not
        it wraps the file content between the imports and the url template, before wrapping
        it checks if the file has URL_PATTERS it take it off and append it to the url template
        """
        file = f"{self.appdir}/urls.py"
        chunk = f'{self.model_name}ViewSet)'
        if file_api.is_present_in_file(file, chunk):
            return
        head, body = self.get_url_parts()
        if file_api.is_present_in_file(file, url_templates.URL_PATTERNS):
            file_api.replace_file_chunk(file,url_templates.URL_PATTERNS, "")
        body = body + url_templates.URL_PATTERNS
        file_api.wrap_file_content(file, head, body)
