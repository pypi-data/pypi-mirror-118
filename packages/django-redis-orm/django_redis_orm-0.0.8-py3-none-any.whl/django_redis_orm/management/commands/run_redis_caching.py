from django.core.management.base import BaseCommand
from django_redis_orm.core import *
from django.conf import settings

class Command(BaseCommand):
    help = 'Redis caching system'

    def handle(self, *args, **options):
        redis_roots = settings.get('REDIS_ROOTS', False)

        if redis_roots:
            if type(redis_roots) == dict:
                print('STARTING CACHING')
                while True:
                    for redis_root_name, redis_root in redis_roots:
                        redis_root.check_cache()
            else:
                raise Exception('REDIS_ROOTS must be dict')
        else:
            raise Exception('No REDIS_ROOTS found in settings.py')

