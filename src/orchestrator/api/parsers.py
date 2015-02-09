import jsonschema
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
 
from . import schemas
from django import forms
 
 
class JSONSchemaParser(JSONParser):
 
    def parse(self, stream, media_type=None, parser_context=None):
        data = super(JSONSchemaParser, self).parse(stream, media_type,
                                                   parser_context)
        try:
            jsonschema.validate(
                data,
                schemas.json[parser_context['view'].schema_name])
        except (ValueError, jsonschema.exceptions.ValidationError) as error:
            import ipdb
            ipdb.set_trace()
            raise ParseError(detail=error.message)
        else:
            return data
