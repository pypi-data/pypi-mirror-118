from django.apps import AppConfig
from django.conf import settings

from health.service import checker


class HealthConfig(AppConfig):
    name = 'health'

    def ready(self):
        if getattr(settings, 'HEALTH_CHECKER_ENABLED', True):
            # By default, there are 3 enabled checkers: DISK, DATABASE, CACHE
            # To disable any, just use 'health.checkers.base.DisabledHealthChecker'
            checkers = {
                'DISK': 'health.checkers.disk.DiskHealthChecker',
                'DATABASES': 'health.checkers.database.DatabaseHealthChecker',
                'CACHES': 'health.checkers.cache.CacheHealthChecker'
            }

            current_checkers = getattr(settings, 'HEALTH_CHECKERS', {})
            checkers.update(current_checkers)

            for key, checker_pkg in checkers:
                checker.register(key, checker_pkg)
