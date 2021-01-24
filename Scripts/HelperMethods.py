from datetime import date
from pandas import DataFrame

from apps.frontend.models.Location import Location


def date_time_converter(o):
    if isinstance(o, date):
        return o.__str__()


def get_model_with_kwargs_else_false(model, **kwargs):
    """
    :param model: Class of a django model
    :param kwargs:
    :return: model_instance or False if model_instance DNE
    """
    try:
        model_instance = model.objects.get(**kwargs)
        return model_instance
    except model.DoesNotExist:
        return False


def update_model_instance_from_post(model_instance, kwargs):
    for key, value in kwargs.items():
        setattr(model_instance, key, value)
    model_instance.save()


def get_model_df_with_kwargs_else_false(model, *args, **kwargs):
    try:
        df = DataFrame.from_records(model.objects.filter(**kwargs).values(*args))
        return df
    except model.DoesNotExist:
        return False


def get_key_from_state(state_code):
    from numpy import array, where
    state_array = array(list(Location.STATE_CHOICES))
    return where(state_array == state_code)[0][0]
