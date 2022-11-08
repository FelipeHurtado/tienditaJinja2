"""
An example how to generate angularjs code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""
from os import mkdir , rmdir
from os.path import exists, dirname, join
import jinja2
from entity_test import get_entity_mm
import shutil




def main(debug=False):

    this_folder = dirname(__file__)

    entity_mm = get_entity_mm(debug)

    # Build tiendita model from tiendita.ent file
    tiendita_model = entity_mm.model_from_file(join(this_folder, 'test.ent'))

    def is_entity(n):
        """
        Test to prove if some type is an entity
        """
        if n.type in tiendita_model.entities:
            return True
        else:
            return False

    def javatype(s):
        """
        Maps type names from PrimitiveType to Java.
        """
        return {
                'integer': 'int',
                'string': 'String'
        }.get(s.name, s.name)

    # Create output folder
    srcgen_folder = join(this_folder, 'tienditaMicroServices')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)
    else:
        shutil.rmtree(srcgen_folder)
        mkdir(srcgen_folder)

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filter for mapping Entity type names to Java type names.

    #jinja_env.tests['entity'] = is_entity

    #jinja_env.filters['javatype'] = javatype

    # Load template
    template_app = jinja_env.get_template('/Templates/app.template')
    template_docker = jinja_env.get_template('/Templates/docker.template')
    template_req = jinja_env.get_template('/Templates/requirements.template')
    template_docker_compose = jinja_env.get_template('/Templates/docker-compose.template')
    template_nginx = jinja_env.get_template('/Templates/nginx.template')
    template_readme = jinja_env.get_template('/Templates/readme.template')

    for entity in tiendita_model.entities:
        #crear carpeta dinamicamente para cada microservicio
        var_folder = join(this_folder,"tienditaMicroServices", entity.name.lower())
        if not exists(var_folder):
            mkdir(var_folder)
        # For each entity generate java file
        with open(join(var_folder,
                       "app.py"), 'w') as f:
            f.write(template_app.render(entity=entity))
        with open(join(var_folder,
                       "Dockerfile"), 'w') as f:
            f.write(template_docker.render(entity=entity))
        with open(join(var_folder,
                       "requirements.txt"), 'w') as f:
            f.write(template_req.render(entity=entity))

    var_folder = join(this_folder,"tienditaMicroServices")
    with open(join(var_folder,
                       "docker-compose.yml"), 'w') as f:
            f.write(template_docker_compose.render(tiendita_model=tiendita_model))
    with open(join(var_folder,
                       "nginx.conf"), 'w') as f:
            f.write(template_nginx.render(tiendita_model=tiendita_model))
    with open(join(var_folder,
                       "README.md"), 'w') as f:
            f.write(template_readme.render(tiendita_model=tiendita_model))
  
if __name__ == "__main__":
    main()
