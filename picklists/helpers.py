from django.template import Context, TemplateSyntaxError, Engine

from letter_templates.context_variables import get_context_variables


class InvalidVarException(Exception):
    """
    InvalidVarException is triggered by the django template engine when it cannot
    find a context variable. This exception should be handled in places where the
    template may use an invalid variable (user entered variables)
    """

    def __mod__(self, missing):
        raise InvalidVarException("Invalid template variable {{ %s }}" % missing)

    def __contains__(self, search):
        if search == "%s":
            return True
        return False


def template_engine_factory():
    # Put the variable name in if missing variables. Else trigger an InvalidVarException.
    string_if_invalid = InvalidVarException()
    return Engine(
        string_if_invalid=string_if_invalid
    )


def picklist_paragraph_errors(request):
    template_engine = template_engine_factory()
    try:
        template = template_engine.from_string(request.POST["text"])
        context = Context(get_context_variables())
        template.render(context)
        # Template is valid! :)
    except (TemplateSyntaxError, InvalidVarException) as err:
        # Template is invalid! :(
        return {"text": err.args}
    return None
