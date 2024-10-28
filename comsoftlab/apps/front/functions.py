from django.utils.datastructures import MultiValueDictKeyError


def get_variable(variable_name, source_request):
    try:
        variable = source_request.GET[variable_name]
        return variable
    except MultiValueDictKeyError:
        return None
    except Exception as e:
        return None
