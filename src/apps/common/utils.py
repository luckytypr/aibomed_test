from rest_framework import serializers


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer, ), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    serializer_class = create_serializer_class(name='', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def update_model_object(*, model, refresh_updated_at: bool = True, **data):

    if refresh_updated_at:
        for field_name, field_value in data.items():
            if hasattr(model, field_name):
                setattr(model, field_name, field_value)
        model.save()
    else:
        update_fields = []
        for field_name, field_value in data.items():
            if hasattr(model, field_name):
                setattr(model, field_name, field_value)
                update_fields.append(field_name)
        model.save(update_fields=update_fields)
    return model
