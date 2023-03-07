"""
Utilitary functions to the views module.
"""

from string import Template
from osemu.api.views.base_views import get_entry_api_cls, get_group_api_cls

default_group_docstr = {
    'get': """Get all `$name` objects.
        ---
        description: Get all `$name` objects.
        tags:
        - $name
        responses:
          200:
            description: Get all `$name` objects.
            content:
              application/json:
                schema:
                  type: array
                  items: $schema
        """,

    'post': """Post `$name` object.
        ---
        description: Create one or more `$name` objects.
        tags:
        - $name
        requestBody:
          required: True
          content:
            application/json:
              schema: 
                oneOf:
                  - $schema
                  - type: array
                    items: $schema
        security:
          - cookieAuth: []
        responses:
          200:
            description: Created new `$name` succesfully
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    new:
                      type: array
                      items: $schema
                      description: Newly created objects.
                    existent:
                      type: array
                      items: $schema
                      description: Objects that already existed.
          400:
            description: Invalid information provided.
          401:
            description: Not logged in.
        """
}

default_entry_docstr = {
    'get': """Get `$name` by ID
    ---
    description: Get a single `$name` by ID.
    tags:
        - $name
    parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Item found.
        content:
          application/json:
            schema: $schema
      404:
        description: Item not found.
    """,
    
    'patch': """Patch `$name` by ID
    ---
    description: Patch a single `$name` by ID.
    tags:
        - $name
    security:
          - cookieAuth: []
    requestBody:
      required: True
      content:
        application/json:
          schema: $schema
    parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Item modified succesfully.
        content:
          application/json:
            schema: $schema
      404:
        description: Item not found.
    """,

    'put': """Put `$name` by ID
    ---
    description: Put (update) a `$name` by ID.
    tags:
        - $name
    security:
          - cookieAuth: []
    requestBody:
      required: True
      content:
        application/json:
          schema: $schema
    parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Item updated succesfully.
        content:
          application/json:
            schema: $schema
      404:
        description: Item not found.
    """,

    'delete': """Put `$name` by ID
    ---
    description: Delete a `$name` by ID.
    tags:
        - $name
    security:
          - cookieAuth: []
    parameters:
      - in: path
        name: id
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Item deleted succesfully.
      404:
        description: Item not found.
    """
}



def apply_docstring(_cls, docs, template_args):
    """Adds docstrings to methods.

    Args:
        docs (dict): dictionary where the key is the method name and the value is the docstring.
        template_args (dict, optional): template parameters to substitute. Defaults to {}.

    Returns:
        class: the class with docstrings.
    """    

    for k, v in docs.items():
        s = Template(v).substitute(template_args)
        getattr(_cls, k).__doc__ = s

    return _cls


def register_views(bp, Schema, Model):

    group_cls = apply_docstring(get_group_api_cls(), default_group_docstr, {'name': Model.__name__, 'schema': Schema.__name__})
    entry_cls = apply_docstring(get_entry_api_cls(), default_entry_docstr, {'name': Model.__name__, 'schema': Schema.__name__})

    rname = Model.__name__.lower()

    group_view = group_cls.as_view(f'{rname}-group', Model, Schema)
    entry_view = entry_cls.as_view(f'{rname}-entry', Model, Schema)

    bp.add_url_rule('/', view_func=group_view)
    bp.add_url_rule('/<id>/', view_func=entry_view)
    return group_view, entry_view