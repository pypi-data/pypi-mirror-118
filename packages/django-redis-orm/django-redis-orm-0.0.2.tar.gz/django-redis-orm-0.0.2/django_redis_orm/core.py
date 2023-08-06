import asyncio
import json
from copy import deepcopy
import redis
import datetime

from django.db.models import Model as DjangoModel

from django_redis_orm.utils import check_types


class RedisField:

    def __init__(self, default=None, choices=None, null=True, ttl=None):
        self.default = default
        self.value = None
        self.choices = choices
        self.null = null
        if ttl is not None:
            check_types(ttl, (int, float))
        self.ttl = ttl

    def _get_default_value(self):
        if self.default is not None:
            try:
                self.value = self.default()
            except BaseException as ex:
                self.value = self.default
        return self.value

    def _check_choices(self, value):
        if self.choices:
            if value not in self.choices.keys():
                raise Exception(f'{value} is not allowed. Allowed values: {", ".join(list(self.choices.keys()))}')

    def check_value(self):
        if self.value is None:
            self.value = self._get_default_value()
        if self.value is None:
            if self.null:
                self.value = 'null'
            else:
                raise Exception('null is not allowed')
        if self.value:
            self._check_choices(self.value)
        return self.value

    def clean(self):
        self.value = self.check_value()
        return self.value

    def deserialize_value_check_null(self, value, redis_root):
        if value == 'null':
            if not self.null:
                if redis_root.ignore_deserialization_errors:
                    print(f'{value} can not be deserialized like {self.__class__.__name__}, ignoring')
                else:
                    raise Exception(f'{value} can not be deserialized like {self.__class__.__name__}')

    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        return value


class RedisString(RedisField):

    def clean(self):
        self.value = self.check_value()
        if self.value and self.value != 'null':
            self.value = f'{self.value}'
        return super().clean()

    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value != 'null':
            value = f'{value}'
        return value


class RedisNumber(RedisField):

    def clean(self):
        self.value = self.check_value()
        if self.value and self.value != 'null':
            check_types(self.value, (int, float))
        return super().clean()

    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value != 'null':
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        else:
            value = 0
        return value


class RedisId(RedisNumber):

    def __init__(self, **kwargs):
        self.null = False
        super().__init__(**kwargs)


class RedisDateTime(RedisNumber):

    def clean(self):
        self.value = self.check_value()
        if self.value and self.value != 'null':
            check_types(self.value, datetime.datetime)
            utc_timestamp = self.value.replace(tzinfo=datetime.timezone.utc).timestamp()
            self.value = utc_timestamp
        return super().clean()

    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value != 'null':
            value = super().deserialize_value(value, redis_root)
            check_types(value, (int, float))
            value = datetime.datetime.utcfromtimestamp(value)
        return value


class RedisForeignKey(RedisNumber):

    def __init__(self, model=None, **kwargs):
        super().__init__(**kwargs)
        if not issubclass(model, RedisModel):
            raise Exception(f'{model.__name__} class is not RedisModel')
        self.model = model

    def _get_id_from_instance_dict(self):
        if self.value:
            if type(self.value) == dict:
                if 'id' in self.value.keys():
                    self.value = self.value['id']
                else:
                    raise Exception(
                        f"{self.value} has no key 'id', please provide serialized instance or dict like " + "{'id': 1, ...}")
            else:
                raise Exception(
                    f'{self.value} type is not dict, please provide serialized instance or dict like ' + "{'id': 1, ...}")
        return self.value

    def clean(self):
        self.value = self.check_value()
        if self.value and self.value != 'null':
            self.value = self._get_id_from_instance_dict()
        return super().clean()

    def _get_instance_by_id(self, id, redis_root):
        model_name = self.model.__name__
        instance = {
            'id': id
        }
        for key in redis_root.redis_instance.scan_iter(f'{redis_root.prefix}:{model_name}:{id}:*'):
            prefix, model_name, instance_id, field_name = key.split(':')
            raw_value = redis_root.redis_instance.get(key)
            value = redis_root.deserialize_value(raw_value, model_name, field_name)
            instance[field_name] = value
        return instance

    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value != 'null':
            value = super().deserialize_value(value, redis_root)
            check_types(value, int)
            value = self._get_instance_by_id(value, redis_root)
        return value


class RedisJson(RedisField):

    def __init__(self, json_allowed_types=(list, dict), **kwargs):
        self.json_allowed_types = json_allowed_types
        super().__init__(**kwargs)

    def set_json_allowed_types(self, allowed_types):
        self.json_allowed_types = allowed_types
        return self.json_allowed_types

    def clean(self):
        self.value = self.check_value()
        if self.value and self.value != 'null':
            check_types(self.value, self.json_allowed_types)
            json_string = json.dumps(self.value)
            self.value = json_string
        return super().clean()

    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value != 'null':
            check_types(value, str)
            value = json.loads(value)
            check_types(value, self.json_allowed_types)
        return value


class RedisDict(RedisJson):

    def clean(self):
        self.set_json_allowed_types(dict)
        return super().clean()

    def deserialize_value(self, value, redis_root):
        self.set_json_allowed_types(dict)
        self.deserialize_value_check_null(value, redis_root)
        if value != 'null':
            value = super().deserialize_value(value, redis_root)
        return value


class RedisList(RedisJson):

    def clean(self):
        self.set_json_allowed_types(list)
        return super().clean()

    def deserialize_value(self, value, redis_root):
        self.set_json_allowed_types(list)
        self.deserialize_value_check_null(value, redis_root)
        if value != 'null':
            value = super().deserialize_value(value, redis_root)
        return value


class RedisDjangoForeignKey(RedisNumber):

    def __init__(self, model=None, **kwargs):
        super().__init__(**kwargs)
        self.model = None
        if not issubclass(model.__class__, DjangoModel):
            raise Exception(f'{model.__class__.__name__} class is not django.db.models Model')
        self.model = model

    def _get_id_from_instance(self):
        if issubclass(self.value.__class__, DjangoModel):
            if isinstance(self.value, self.model):
                if self.value.id:
                    django_instances_with_this_id = self.model.objects.filter(id=self.value.id)
                    if django_instances_with_this_id:
                        if len(django_instances_with_this_id) == 1:
                            self.value = self.value.id
                        elif len(django_instances_with_this_id) > 1:
                            raise Exception(f'There are {len(django_instances_with_this_id)} django instances with this id')
                        else:
                            raise Exception(f'There are no django instances with this id')
                    else:
                        raise Exception(f'There are no django instances with this id')
                else:
                    raise Exception(f'This django instance ({self.value}) has no attribute id')
            else:
                raise Exception(f'{self.value} is not instance of {self.model}')
        else:
            raise Exception(f'{self.value} class is not django.db.models Model')
        return self.value

    def clean(self):
        self.value = self.check_value()
        if self.value and self.value != 'null':
            self.value = self._get_id_from_instance()
        return super().clean()

    def _get_instance_by_id(self, id):
        instance = {
            'id': id
        }
        django_instances_with_this_id = self.model.objects.filter(id=id)
        if django_instances_with_this_id:
            if len(django_instances_with_this_id) == 1:
                instance = django_instances_with_this_id[0]
            elif len(django_instances_with_this_id) > 1:
                raise Exception(f'There are {len(django_instances_with_this_id)} django instances with this id')
            else:
                raise Exception(f'There are no django instances with this id')
        else:
            raise Exception(f'There are no django instances with this id')
        return instance

    def deserialize_value(self, value, redis_root):
        self.deserialize_value_check_null(value, redis_root)
        if value != 'null':
            value = super().deserialize_value(value, redis_root)
            check_types(value, int)
            value = self._get_instance_by_id(value)
#         return value


class RedisRoot:

    def __init__(self, redis_instance=None, prefix='redis_test', ignore_deserialization_errors=True,
                 save_consistency=False, economy=False):
        self.registered_models = []
        if type(prefix) == str:
            self.prefix = prefix
        else:
            print(f'Prefix {prefix} is type of {type(prefix)}, allowed only str, using default prefix "redis_test"')
            self.prefix = 'redis_test'
        self.ignore_deserialization_errors = ignore_deserialization_errors
        self.save_consistency = save_consistency
        self.economy = economy
        if redis_instance:
            self.redis_instance = redis_instance
        else:
            print(f'{self.__class__.__name__}: No redis_instance provided, trying default config...')
            default_host = 'localhost'
            default_port = 6379
            default_db = 0
            try:
                redis_instance = redis.StrictRedis(
                    decode_responses=True,
                    host=default_host,
                    port=default_port,
                    db=default_db,
                )
                self.redis_instance = redis_instance
            except BaseException as ex:
                raise Exception(
                    f'Default config ({default_host}:{default_port}, db={default_db}) failed, please provide redis_instance to {self.__class__.__name__}')

    def register_models(self, models_list):
        for model in models_list:
            if issubclass(model, RedisModel):
                if model not in self.registered_models:
                    self.registered_models.append(model)
            else:
                raise Exception(f'{model.__name__} class is not RedisModel')

    def _get_registered_model_by_name(self, model_name):
        found = False
        model = None
        for registered_model in self.registered_models:
            if registered_model.__name__ == model_name:
                found = True
                model = registered_model
                break
        if not found:
            if self.ignore_deserialization_errors:
                print(f'{model_name} not found in registered models, ignoring')
                model = model_name
            else:
                raise Exception(f'{model_name} not found in registered models')
        return model

    def _get_field_instance_by_name(self, field_name, model):
        field_instance = None
        try:
            if field_name == 'id':
                field_instance = getattr(model, field_name)
            else:
                field_instance = getattr(model, field_name)
        except BaseException as ex:
            if self.ignore_deserialization_errors:
                print(f'{model.__name__} has no field {field_name}, ignoring deserialization')
                field_instance = field_name
            else:
                raise Exception(f'{model.__name__} has no field {field_name}')
        return field_instance

    def _deserialize_value_by_field_instance(self, raw_value, field_instance):
        value = field_instance.deserialize_value(raw_value, self)
        try:
            pass
        except BaseException as ex:
            if self.ignore_deserialization_errors:
                print(f'{raw_value} can not be deserialized like {field_instance.__class__.__name__}, ignoring')
                value = raw_value
            else:
                raise Exception(f'{raw_value} can not be deserialized like {field_instance.__class__.__name__}')
        return value

    def deserialize_value(self, raw_value, model_name, field_name):
        value = raw_value
        saved_model = self._get_registered_model_by_name(model_name)
        if issubclass(saved_model, RedisModel):
            saved_field_instance = self._get_field_instance_by_name(field_name, saved_model)
            if issubclass(saved_field_instance.__class__, RedisField):
                value = self._deserialize_value_by_field_instance(raw_value, saved_field_instance)
        return value

    def _return_with_format(self, instances, return_dict=False):
        if return_dict:
            return instances
        else:
            instances_list = [
                {
                    'id': instance_id,
                    **instance_fields
                }
                for instance_id, instance_fields in instances.items()
            ]
            return instances_list

    def _check_fields_existence(self, model, instances_with_allowed, filters):
        checked_instances = {}
        fields = model.__dict__
        cleaned_fields = {}
        for field_name, field in fields.items():
            if not field_name.startswith('__'):
                cleaned_fields[field_name] = field
        if 'id' not in cleaned_fields.keys():
            cleaned_fields['id'] = RedisString(null=True)
        fields = cleaned_fields
        for instance_id, instance_fields in instances_with_allowed.items():
            checked_instances[instance_id] = {}
            for field_name, field in fields.items():
                if field_name in instance_fields.keys():
                    checked_instances[instance_id][field_name] = instance_fields[field_name]
                else:
                    field.value = None
                    cleaned_value = field.clean()
                    allowed = self._filter_field_name(field_name, cleaned_value, filters)
                    checked_instances[instance_id][field_name] = {
                        'value': cleaned_value,
                        'allowed': allowed
                    }
        return checked_instances

    def _filter_value(self, value, filter_type, filter_by):
        allowed = True
        if filter_type == 'exact':
            if value != filter_by:
                allowed = False
        elif filter_type == 'iexact':
            if value.lower() != filter_by.lower():
                allowed = False
        elif filter_type == 'contains':
            if filter_by not in value:
                allowed = False
        elif filter_type == 'icontains':
            if filter_by.lower() not in value.lower():
                allowed = False
        elif filter_type == 'in':
            if value not in filter_by:
                allowed = False
        elif filter_type == 'gt':
            if value <= filter_by:
                allowed = False
        elif filter_type == 'gte':
            if value < filter_by:
                allowed = False
        elif filter_type == 'lt':
            if value >= filter_by:
                allowed = False
        elif filter_type == 'lte':
            if value > filter_by:
                allowed = False
        elif filter_type == 'startswith':
            if not value.startswith(filter_by):
                allowed = False
        elif filter_type == 'istartswith':
            if not value.lower().startswith(filter_by.lower()):
                allowed = False
        elif filter_type == 'endswith':
            if not value.endswith(filter_by):
                allowed = False
        elif filter_type == 'iendswith':
            if not value.lower().endswith(filter_by.lower()):
                allowed = False
        elif filter_type == 'range':
            if value not in range(filter_by):
                allowed = False
        return allowed

    def _filter_field_name(self, field_name, value, raw_filters):
        allowed_list = [True]
        for filter_param in raw_filters.keys():
            filter_by = raw_filters[filter_param]
            filter_field_name, filter_type = filter_param, 'exact'
            if '__' in filter_param:
                filter_field_name, filter_type = filter_param.split('__')
            if field_name == filter_field_name:
                allowed_list.append(self._filter_value(value, filter_type, filter_by))
        allowed = all(allowed_list)
        return allowed

    def _get_all_stored_model_instances(self, model, filters=None):
        model_name = model.__name__
        instances_with_allowed = {}
        for key in self.redis_instance.scan_iter(f'{self.prefix}:{model_name}:*'):
            prefix, model_name, instance_id, field_name = key.split(':')
            instance_id = int(instance_id)
            raw_value = self.redis_instance.get(key)
            value = self.deserialize_value(raw_value, model_name, field_name)
            allowed = self._filter_field_name(field_name, value, filters)
            if instance_id not in instances_with_allowed.keys():
                instances_with_allowed[instance_id] = {}
            instances_with_allowed[instance_id][field_name] = {
                'value': value,
                'allowed': allowed
            }
        return instances_with_allowed

    def _get_instances_from_instances_with_allowed(self, instances_with_allowed):
        instances = {}
        for instance_id, instance_fields in instances_with_allowed.items():
            instance_allowed = all([
                instance_field_data['allowed']
                for instance_field_data in instance_fields.values()
            ])
            if instance_allowed and instance_id not in instances.keys():
                instances[instance_id] = {
                    instance_field_name: instance_field_data['value']
                    for instance_field_name, instance_field_data in instance_fields.items()
                }
        return instances

    def _get_all_model_instances(self, model, filters=None):
        if filters is None:
            filters = {}
        instances_with_allowed = self._get_all_stored_model_instances(model, filters)
        if self.save_consistency:
            instances_with_allowed = self._check_fields_existence(model, instances_with_allowed, filters)
        instances = self._get_instances_from_instances_with_allowed(instances_with_allowed)
        return instances

    def get(self, model, return_dict=False, **kwargs):
        instances = self._get_all_model_instances(model, kwargs)
        return self._return_with_format(instances, return_dict)

    def order(self, instances, field_name):
        reverse = False
        if field_name.startswith('-'):
            reverse = True
            field_name = field_name[1:]

        return sorted(instances, key=(lambda instance: instance[field_name]), reverse=reverse)

    def _get_ids_from_untyped_data(self, instances):
        if type(instances) == dict:
            if 'id' in instances:
                ids_to_delete = [instances['id']]
            else:
                if all([
                    (type(instance_key) == int)
                    for instance_key in instances.keys()
                ]):
                    ids_to_delete = list(set(instances.keys()))
                else:
                    raise Exception('Not all keys are of the type int')
        elif type(instances) in [list, tuple, set]:
            if all([
                (type(instance_id) == int)
                for instance_id in instances
            ]):
                ids_to_delete = list(set(instances))
            else:
                raise Exception('Not all elements are of the type int')
        else:
            raise Exception('Please provide valid data to delete')
        return ids_to_delete

    def _get_ttl_by_update_params(self, field, saved_model, renew_ttl, new_ttl):
        field_ttl = None
        if new_ttl is not None:
            check_types(new_ttl, (int, float))
            field_ttl = new_ttl
        else:
            if renew_ttl:
                field_ttl = saved_model.get_field_ttl(field)
        return field_ttl

    def _update_by_key(self, key, fields_to_update, renew_ttl, new_ttl):
        updated_data = None
        prefix, model_name, instance_id, field_name = key.split(':')
        instance_id = int(instance_id)
        if field_name in fields_to_update.keys():
            saved_model = self._get_registered_model_by_name(model_name)
            if issubclass(saved_model, RedisModel):
                saved_field_instance = self._get_field_instance_by_name(field_name, saved_model)
                if issubclass(saved_field_instance.__class__, RedisField):
                    saved_field_instance.value = fields_to_update[field_name]
                    cleaned_value = saved_field_instance.clean()
                    field_ttl = self._get_ttl_by_update_params(saved_field_instance, saved_model, renew_ttl, new_ttl)
                    self.redis_instance.set(key, cleaned_value, ex=field_ttl)
                    updated_data = {
                        'model': saved_model,
                        'id': instance_id
                    }
        return updated_data

    def update(self, model, instances=None, return_dict=False, renew_ttl=False, new_ttl=None, **fields_to_update):
        model_name = model.__name__
        updated_datas = []
        if instances is None:
            for key in self.redis_instance.scan_iter(f'{self.prefix}:{model_name}:*'):
                updated_data = self._update_by_key(key, fields_to_update, renew_ttl, new_ttl)
                if updated_data is not None:
                    updated_datas.append(updated_data)
        else:
            ids_to_delete = self._get_ids_from_untyped_data(instances)
            for instance_id in ids_to_delete:
                for key in self.redis_instance.scan_iter(f'{self.prefix}:{model_name}:{instance_id}:*'):
                    updated_data = self._update_by_key(key, fields_to_update, renew_ttl, new_ttl)
                    if updated_data is not None:
                        updated_datas.append(updated_data)
        updated_instances = {}
        for updated_data in updated_datas:
            updated_model = updated_data['model']
            updated_id = updated_data['id']
            if self.economy:
                updated_instances[updated_id] = {'id': updated_id}
            else:
                updated_instance_qs = self.get(updated_model, id=updated_id)
                updated_instance = updated_instance_qs[0]
                updated_instances[updated_id] = updated_instance
        return self._return_with_format(updated_instances, return_dict)

    def _delete_by_key(self, key):
        self.redis_instance.delete(key)

    def delete(self, model, instances=None):
        model_name = model.__name__
        if instances is None:
            for key in self.redis_instance.scan_iter(f'{self.prefix}:{model_name}:*'):
                self._delete_by_key(key)
        else:
            ids_to_delete = self._get_ids_from_untyped_data(instances)
            for instance_id in ids_to_delete:
                for key in self.redis_instance.scan_iter(f'{self.prefix}:{model_name}:{instance_id}:*'):
                    self._delete_by_key(key)


class RedisModel:
    id = RedisId()

    def __init__(self, redis_root=None, **kwargs):
        self.__model_data__ = {
            'redis_root': None,
            'redis_instance': None,
            'name': None,
            'fields': None,
            'meta': {}
        }

        if isinstance(redis_root, RedisRoot):
            self.__model_data__['redis_root'] = redis_root
            self.__model_data__['redis_instance'] = redis_root.redis_instance
            self.__model_data__['name'] = self.__class__.__name__
            if self.__class__ != RedisModel:
                self.__model_data__['redis_root'].register_models([self.__class__])
                self._renew_fields()
                self._fill_fields_values(kwargs)

        else:
            raise Exception(f'{redis_root.__name__} type is {type(redis_root)}. Allowed only RedisRoot')

    def _check_meta_ttl(self, ttl):
        check_types(ttl, (int, float))
        return ttl

    def _set_meta(self, meta_fields):
        allowed_meta_fields_with_check_functions = {
            'ttl': self._check_meta_ttl
        }
        for field_name, field_value in meta_fields.items():
            if field_name in allowed_meta_fields_with_check_functions.keys():
                cleaned_value = allowed_meta_fields_with_check_functions[field_name](field_value)
                if cleaned_value is not None:
                    self.__model_data__['meta'][field_name] = cleaned_value

    def _get_initial_model_field(self, field_name):
        if field_name in self.__class__.__dict__.keys():
            return deepcopy(self.__class__.__dict__[field_name])
        else:
            raise Exception(f'{self.__class__} has no field {field_name}')

    def _renew_fields(self):
        class_fields = self.__class__.__dict__.copy()
        fields = {}
        for field_name, field in class_fields.items():
            if not field_name.startswith('__'):
                if field_name == 'Meta':
                    self._set_meta(self.__class__.Meta.__dict__)
                else:
                    fields[field_name] = self._get_initial_model_field(field_name)
        self._get_new_id()
        if 'id' not in fields.keys():
            fields['id'] = self.id
        self.__model_data__['fields'] = fields

    def _fill_fields_values(self, field_values_dict):
        for name, value in field_values_dict.items():
            fields = self.__model_data__['fields']
            if name in fields.keys():
                self.__model_data__['fields'][name].value = value
            else:
                raise Exception(f'{self.__class__.__name__} has no field {name}')

    def get_field_ttl(self, field):
        field_ttl = field.ttl
        if field_ttl is None:
            meta = self.__model_data__['meta']
            if 'ttl' in meta.keys():
                field_ttl = meta['ttl']
        return field_ttl

    def _get_fields_with_model_key(self):
        redis_root = self.__model_data__['redis_root']
        name = self.__model_data__['name']
        fields = self.__model_data__['fields']
        fields = dict(fields)
        model_key = f'{redis_root.prefix}:{name}:{self.id.value}'
        cleaned_fields = {}
        for field_name, field in fields.items():
            if not field_name.startswith('__'):
                try:
                    cleaned_value = field.clean()
                    field_ttl = self.get_field_ttl(field)
                    cleaned_fields[model_key + f':{field_name}'] = {
                        'value': cleaned_value,
                        'ttl': field_ttl
                    }
                except BaseException as ex:
                    raise Exception(f'{ex} ({name} -> {field_name})')
        fields_with_model_key = cleaned_fields
        return fields_with_model_key

    def _set_fields(self):
        field_to_write = self._get_fields_with_model_key()
        redis_instance = self.__model_data__['redis_instance']
        for key, field_data in field_to_write.items():
            redis_instance.set(key, field_data['value'], ex=field_data['ttl'])

    def _get_new_id(self):
        redis_root = self.__model_data__['redis_root']
        instances_with_ids = redis_root.get(self.__class__, return_dict=True)
        all_ids = [int(instance_id) for instance_id in list(instances_with_ids.keys())]
        if all_ids:
            max_id = max(all_ids)
        else:
            max_id = 0
        self.id.value = int(max_id + 1)

    def save(self):
        self._set_fields()
        redis_root = self.__model_data__['redis_root']
        if self.__model_data__['redis_root'].economy:
            deserialized_instance = {'id': self.id.value}
        else:
            deserialized_instance = redis_root.get(self.__class__, id=self.id.value)[0]
        return deserialized_instance

















import datetime
import random
from time import sleep


# from django_redis_orm.core import *


def generate_token(chars_count):
    allowed_chars = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    token = f'{"".join([random.choice(allowed_chars) for i in range(chars_count)])}'
    return token


def generate_token_12_chars():
    return generate_token(12)


class BotSession(RedisModel):
    session_token = RedisString(default=generate_token_12_chars)
    created = RedisDateTime(default=datetime.datetime.now)


class TaskChallenge(RedisModel):
    bot_session = RedisForeignKey(model=BotSession)
    task_id = RedisNumber(default=0, null=False)
    status = RedisString(default='in_work', choices={
        'in_work': 'В работе',
        'completed': 'Завершён успешно',
        'completed_frozen_points': 'Завершён успешно, получил поинты в холде',
        'completed_points': 'Завершён успешно, получил поинты',
        'completed_decommissioning': 'Завершён успешно, поинты списаны',
        'failed_bot': 'Зафейлил бот',
        'failed_task_creator': 'Зафейлил создатель задания',
    }, null=False)
    account_checks_count = RedisNumber(default=0)
    created = RedisDateTime(default=datetime.datetime.now)


class TtlCheckModel(RedisModel):
    redis_number_with_ttl = RedisNumber(default=0, null=False, ttl=5)


class MetaTtlCheckModel(RedisModel):
    redis_number = RedisNumber(default=0, null=False)

    class Meta:
        ttl = 5


class DictCheckModel(RedisModel):
    redis_dict = RedisDict()


class ListCheckModel(RedisModel):
    redis_list = RedisList()


class DjangoForeignKeyModel(RedisModel):
    foreign_key = RedisDjangoForeignKey(model=Proxy)


def get_redis_instance(connection_pool=None):
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    redis_instance = redis.Redis(
        decode_responses=True,
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
        connection_pool=connection_pool
    )
    return redis_instance


def clean_db_after_test(redis_instance, prefix):
    for key in redis_instance.scan_iter(f'{prefix}:*'):
        redis_instance.delete(key)


def basic_test(redis_instance, prefix):
    try:
        redis_root = RedisRoot(
            prefix=prefix,
            redis_instance=redis_instance,
            ignore_deserialization_errors=True
        )
        redis_root.register_models([
            TaskChallenge,
        ])
        for i in range(5):
            TaskChallenge(
                redis_root=redis_root,
                status='in_work',
            ).save()
        task_challenges_without_keys = redis_root.get(TaskChallenge)
        task_challenges_with_keys = redis_root.get(TaskChallenge, return_dict=True)
        have_exception = False
        if not len(task_challenges_without_keys):
            have_exception = True
        if not task_challenges_with_keys:
            have_exception = True
        else:
            if not task_challenges_with_keys.keys():
                have_exception = True
            else:
                if len(list(task_challenges_with_keys.keys())) != len(task_challenges_without_keys):
                    have_exception = True
    except BaseException as ex:
        have_exception = True
    clean_db_after_test(redis_instance, prefix)
    return have_exception


def auto_reg_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    task_challenge_1 = TaskChallenge(
        redis_root=redis_root,
        status='in_work',
    ).save()
    try:
        task_challenges = redis_root.get(TaskChallenge)
        have_exception = False
    except BaseException as ex:
        have_exception = True
    clean_db_after_test(redis_instance, prefix)
    return have_exception


def no_redis_instance_test(*args, **kwargs):
    try:
        redis_root = RedisRoot(
            ignore_deserialization_errors=True
        )
        task_challenge_1 = TaskChallenge(
            redis_root=redis_root,
            status='in_work',
        )
        task_challenge_1.save()
        task_challenges = redis_root.get(TaskChallenge)
        have_exception = False
        clean_db_after_test(redis_root.redis_instance, redis_root.prefix)
    except BaseException as ex:
        have_exception = True
    return have_exception


def choices_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    task_challenge_1 = TaskChallenge(
        redis_root=redis_root,
        status='bruh',
    )
    try:
        task_challenge_1.save()
        task_challenges = redis_root.get(TaskChallenge)
        have_exception = True
    except BaseException as ex:
        have_exception = False
    clean_db_after_test(redis_instance, prefix)
    return have_exception


def order_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    for i in range(3):
        TaskChallenge(
            redis_root=redis_root
        ).save()
    have_exception = True
    try:
        task_challenges = redis_root.get(TaskChallenge)
        first_task_challenge = redis_root.order(task_challenges, 'id')[0]
        last_task_challenge = redis_root.order(task_challenges, '-id')[0]
        if first_task_challenge['id'] == 1 and last_task_challenge['id'] == len(task_challenges):
            have_exception = False
    except BaseException as ex:
        pass
    clean_db_after_test(redis_instance, prefix)
    return have_exception


def filter_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    have_exception = True
    try:
        same_tokens_count = 2
        random_tokens_count = 8
        same_token = generate_token(50)
        random_tokens = [generate_token(50) for i in range(random_tokens_count)]
        for i in range(same_tokens_count):
            BotSession(redis_root, session_token=same_token).save()
        for random_token in random_tokens:
            BotSession(redis_root, session_token=random_token).save()
        task_challenges_with_same_token = redis_root.get(BotSession, session_token=same_token)
        if len(task_challenges_with_same_token) == same_tokens_count:
            have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def update_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    have_exception = True
    try:
        bot_session_1 = BotSession(redis_root, session_token='123').save()
        bot_session_1_id = bot_session_1['id']
        redis_root.update(BotSession, bot_session_1, session_token='234')
        bot_sessions_filtered = redis_root.get(BotSession, id=bot_session_1_id)
        if len(bot_sessions_filtered) == 1:
            bot_session_1_new = bot_sessions_filtered[0]
            if 'session_token' in bot_session_1_new.keys():
                if bot_session_1_new['session_token'] == '234':
                    have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def functions_like_defaults_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    have_exception = False
    try:
        bot_session_1 = BotSession(redis_root).save()
        bot_session_2 = BotSession(redis_root).save()
        if bot_session_1.session_token == bot_session_2.session_token:
            have_exception = True
    except BaseException as ex:
        pass

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def redis_foreign_key_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    have_exception = True
    try:
        bot_session_1 = BotSession(
            redis_root=redis_root,
        ).save()
        task_challenge_1 = TaskChallenge(
            redis_root=redis_root,
            bot_session=bot_session_1
        ).save()
        bot_sessions = redis_root.get(BotSession)
        bot_session = redis_root.order(bot_sessions, '-id')[0]
        task_challenges = redis_root.get(TaskChallenge)
        task_challenge = redis_root.order(task_challenges, '-id')[0]
        if type(task_challenge['bot_session']) == dict:
            if task_challenge['bot_session'] == bot_session:
                have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


# def redis_django_foreign_key_test(redis_instance, prefix):
#     redis_root = RedisRoot(
#         prefix=prefix,
#         redis_instance=redis_instance,
#         ignore_deserialization_errors=True
#     )
#     have_exception = True
#     try:
#         bot_session_1 = BotSession(
#             redis_root=redis_root,
#         ).save()
#         task_challenge_1 = TaskChallenge(
#             redis_root=redis_root,
#             bot_session=bot_session_1
#         ).save()
#         bot_sessions = redis_root.get(BotSession)
#         bot_session = redis_root.order(bot_sessions, '-id')[0]
#         task_challenges = redis_root.get(TaskChallenge)
#         task_challenge = redis_root.order(task_challenges, '-id')[0]
#         if type(task_challenge['bot_session']) == dict:
#             if task_challenge['bot_session'] == bot_session:
#                 have_exception = False
#     except BaseException as ex:
#         print(ex)
#
#     clean_db_after_test(redis_instance, prefix)
#     return have_exception


def delete_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    have_exception = True
    try:
        bot_session_1 = BotSession(
            redis_root=redis_root,
        ).save()
        task_challenge_1 = TaskChallenge(
            redis_root=redis_root,
            bot_session=bot_session_1
        ).save()
        redis_root.delete(BotSession, bot_session_1)
        redis_root.delete(TaskChallenge, task_challenge_1)
        bot_sessions = redis_root.get(BotSession)
        task_challenges = redis_root.get(TaskChallenge)
        if len(bot_sessions) == 0 and len(task_challenges) == 0:
            have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def ttl_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    have_exception = True
    try:
        ttl_check_model_1 = TtlCheckModel(
            redis_root=redis_root,
        ).save()
        ttl_check_models = redis_root.get(TtlCheckModel)
        if len(ttl_check_models):
            ttl_check_model = ttl_check_models[0]
            if 'redis_number_with_ttl' in ttl_check_model.keys():
                sleep(6)
                ttl_check_models = redis_root.get(TtlCheckModel)
                if len(ttl_check_models):
                    ttl_check_model = ttl_check_models[0]
                    if 'redis_number_with_ttl' not in ttl_check_model.keys():
                        have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def save_consistency_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True,
        save_consistency=True,
    )
    have_exception = True
    try:
        ttl_check_model_1 = TtlCheckModel(
            redis_root=redis_root,
        ).save()
        ttl_check_models = redis_root.get(TtlCheckModel)
        if len(ttl_check_models):
            ttl_check_model = ttl_check_models[0]
            if 'redis_number_with_ttl' in ttl_check_model.keys():
                sleep(6)
                ttl_check_models = redis_root.get(TtlCheckModel)
                if len(ttl_check_models):
                    ttl_check_model = ttl_check_models[0]
                    if 'redis_number_with_ttl' in ttl_check_model.keys():  # because consistency is saved
                        have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def meta_ttl_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True,
    )
    have_exception = True
    try:
        meta_ttl_check_model_1 = MetaTtlCheckModel(
            redis_root=redis_root,
        ).save()
        meta_ttl_check_models = redis_root.get(MetaTtlCheckModel)
        if len(meta_ttl_check_models):
            meta_ttl_check_model = meta_ttl_check_models[0]
            if 'redis_number' in meta_ttl_check_model.keys():
                sleep(6)
                meta_ttl_check_models = redis_root.get(MetaTtlCheckModel)
                if not len(meta_ttl_check_models):
                    have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def economy_test(redis_instance, prefix):
    have_exception = True
    try:

        redis_root = RedisRoot(
            prefix=prefix,
            redis_instance=redis_instance,
            ignore_deserialization_errors=True,
            economy=True
        )
        started_in_economy = datetime.datetime.now()
        for i in range(10):
            task_challenge_1 = TaskChallenge(
                redis_root=redis_root,
                status='in_work',
            ).save()
            redis_root.update(TaskChallenge, task_challenge_1, account_checks_count=1)
        ended_in_economy = datetime.datetime.now()
        economy_time = (ended_in_economy - started_in_economy).total_seconds()
        clean_db_after_test(redis_instance, prefix)

        redis_root = RedisRoot(
            prefix=prefix,
            redis_instance=redis_instance,
            ignore_deserialization_errors=True,
            economy=False
        )
        started_in_no_economy = datetime.datetime.now()
        for i in range(10):
            task_challenge_1 = TaskChallenge(
                redis_root=redis_root,
                status='in_work',
            ).save()
            redis_root.update(TaskChallenge, task_challenge_1, account_checks_count=1)
        ended_in_no_economy = datetime.datetime.now()
        no_economy_time = (ended_in_no_economy - started_in_no_economy).total_seconds()
        clean_db_after_test(redis_instance, prefix)
        economy_percent = round((no_economy_time / economy_time - 1) * 100, 2)
        economy_symbol = ('+' if economy_percent > 0 else '')
        print(f'Economy gives {economy_symbol}{economy_percent}% efficiency')
        if economy_symbol == '+':
            have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def dict_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    have_exception = True
    try:
        some_dict = {
            'age': 19,
            'weed': True
        }
        DictCheckModel(
            redis_root=redis_root,
            redis_dict=some_dict
        ).save()
        dict_check_model_instance = redis_root.get(DictCheckModel)[0]
        if 'redis_dict' in dict_check_model_instance.keys():
            if dict_check_model_instance['redis_dict'] == some_dict:
                have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def list_test(redis_instance, prefix):
    redis_root = RedisRoot(
        prefix=prefix,
        redis_instance=redis_instance,
        ignore_deserialization_errors=True
    )
    have_exception = True
    try:
        some_list = [5, 9, 's', 4.5, False]
        ListCheckModel(
            redis_root=redis_root,
            redis_list=some_list
        ).save()
        list_check_model_instance = redis_root.get(ListCheckModel)[0]
        if 'redis_list' in list_check_model_instance.keys():
            if list_check_model_instance['redis_list'] == some_list:
                have_exception = False
    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def async_test(redis_instance, prefix):
    have_exception = True
    try:

        async def async_task(data_count, use_async=True):
            redis_roots = []
            connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
            for i in range(data_count):
                redis_instance = get_redis_instance(connection_pool)
                redis_root = RedisRoot(
                    prefix=prefix,
                    redis_instance=redis_instance,
                    ignore_deserialization_errors=True
                )
                redis_roots.append(redis_root)

            async def create_list(redis_roots, redis_root_index, list_length):
                some_list = [random.choice('ABCDEF') for i in range(list_length)]
                redis_root = redis_roots[redis_root_index]
                list_check_model_instance = ListCheckModel(
                    redis_root=redis_root,
                    redis_list=some_list
                ).save()
                return {
                    'list': some_list,
                    'id': list_check_model_instance['id']
                }

            async def get_object_existence(redis_roots, redis_root_index, lists_with_ids):
                exists = False
                redis_root = redis_roots[redis_root_index]
                objects = redis_root.get(ListCheckModel, redis_list=lists_with_ids['list'])
                if objects:
                    if len(objects) == 1:
                        exists = objects[0]['id'] == lists_with_ids['id']
                return exists

            async def update_list(redis_roots, redis_root_index, lists_with_ids):
                result = False
                redis_root = redis_roots[redis_root_index]
                objects = redis_root.get(ListCheckModel, redis_list=lists_with_ids['list'])
                if objects:
                    if len(objects) == 1:
                        obj = objects[0]
                        new_list = deepcopy(lists_with_ids['list'])
                        new_list.append('check_value')
                        updated_obj = redis_root.update(ListCheckModel, obj, redis_list=new_list)
                        updated_objects = redis_root.get(ListCheckModel, redis_list=new_list)
                        if updated_objects:
                            if len(updated_objects) == 1:
                                result = updated_objects[0]['id'] == lists_with_ids['id']
                return result

            async def delete_list(redis_roots, redis_root_index, id):
                result = False
                redis_root = redis_roots[redis_root_index]
                objects = redis_root.get(ListCheckModel, id=id)
                if objects:
                    if len(objects) == 1:
                        obj = objects[0]
                        redis_root.delete(ListCheckModel, obj)
                        objects = redis_root.get(ListCheckModel, id=id)
                        if not objects:
                            result = True
                return result

            async def create_lists(lists_count, use_async=True):
                if use_async:
                    async_create_lists_tasks = [
                        create_list(redis_roots, i, i + 100)
                        for i in range(lists_count)
                    ]
                    list_of_lists_with_ids = await asyncio.gather(*async_create_lists_tasks)
                else:
                    list_of_lists_with_ids = [
                        await create_list(redis_roots, i, i + 100)
                        for i in range(lists_count)
                    ]
                return list_of_lists_with_ids

            async def get_objects_existence(list_of_lists_with_ids, use_async=True):
                if use_async:
                    async_get_object_by_list_tasks = [
                        get_object_existence(redis_roots, i, lists_with_ids)
                        for i, lists_with_ids in enumerate(list_of_lists_with_ids)
                    ]
                    list_of_results = await asyncio.gather(*async_get_object_by_list_tasks)
                else:
                    list_of_results = [
                        await get_object_existence(redis_roots, i, lists_with_ids)
                        for i, lists_with_ids in enumerate(list_of_lists_with_ids)
                    ]
                return list_of_results

            async def update_lists(list_of_lists_with_ids, use_async=True):
                if use_async:
                    async_update_list_tasks = [
                        update_list(redis_roots, i, lists_with_ids)
                        for i, lists_with_ids in enumerate(list_of_lists_with_ids)
                    ]
                    list_of_results = await asyncio.gather(*async_update_list_tasks)
                else:
                    list_of_results = [
                        await update_list(redis_roots, i, lists_with_ids)
                        for i, lists_with_ids in enumerate(list_of_lists_with_ids)
                    ]
                return list_of_results

            async def delete_lists(list_of_lists_with_ids, use_async=True):
                if use_async:
                    async_delete_list_tasks = [
                        delete_list(redis_roots, i, lists_with_ids['id'])
                        for i, lists_with_ids in enumerate(list_of_lists_with_ids)
                    ]
                    list_of_results = await asyncio.gather(*async_delete_list_tasks)
                else:
                    list_of_results = [
                        await delete_list(redis_roots, i, lists_with_ids)
                        for i, lists_with_ids in enumerate(list_of_lists_with_ids)
                    ]
                return list_of_results



            list_of_lists_with_ids = await create_lists(data_count, use_async)
            list_of_results = await get_objects_existence(list_of_lists_with_ids, use_async)
            if all(list_of_results):
                list_of_results = await update_lists(list_of_lists_with_ids, use_async)
                if all(list_of_results):
                    list_of_results = await delete_lists(list_of_lists_with_ids, use_async)
            return all(list_of_results)

        data_count = 10
        async_started_in = datetime.datetime.now()
        async_result = asyncio.run(async_task(data_count))
        async_ended_in = datetime.datetime.now()
        async_time = (async_ended_in - async_started_in).total_seconds()
        have_exception = not async_result
        sync_started_in = datetime.datetime.now()
        sync_result = asyncio.run(async_task(data_count, False))
        sync_ended_in = datetime.datetime.now()
        sync_time = (sync_ended_in - sync_started_in).total_seconds()

        async_percent = round((sync_time / async_time - 1) * 100, 2)
        async_symbol = ('+' if async_percent > 0 else '')
        print(f'Async gives {async_symbol}{async_percent}% efficiency')

    except BaseException as ex:
        print(ex)

    clean_db_after_test(redis_instance, prefix)
    return have_exception


def run_tests():
    redis_instance = get_redis_instance()
    tests = [
        basic_test,
        auto_reg_test,
        no_redis_instance_test,
        choices_test,
        order_test,
        filter_test,
        functions_like_defaults_test,
        redis_foreign_key_test,
        # redis_django_foreign_key_test,
        update_test,
        delete_test,
        ttl_test,
        save_consistency_test,
        meta_ttl_test,
        economy_test,
        list_test,
        dict_test,
        async_test,
    ]
    results = []
    started_in = datetime.datetime.now()
    print('STARTING TESTS\n')
    for i, test in enumerate(tests):
        print(f'Starting {int(i + 1)} test: {test.__name__.replace("_", " ")}')
        test_started_in = datetime.datetime.now()
        result = not test(redis_instance, test.__name__)
        test_ended_in = datetime.datetime.now()
        test_time = (test_ended_in - test_started_in).total_seconds()
        print(f'{result = } / {test_time}s\n')
        results.append(result)
    ended_in = datetime.datetime.now()
    time = (ended_in - started_in).total_seconds()
    success_message = 'SUCCESS' if all(results) else 'FAILED'
    print('\n'
          f'{success_message}!\n')
    results_success_count = 0
    for i, result in enumerate(results):
        result_message = 'SUCCESS' if result else 'FAILED'
        print(f'Test {(i + 1)}/{len(results)}: {result_message} ({tests[i].__name__.replace("_", " ")})')
        if result:
            results_success_count += 1
    print(f'\n'
          f'{results_success_count} / {len(results)} tests ran successfully\n'
          f'All tests completed in {time}s\n')


if __name__ == '__main__':
    run_tests()
