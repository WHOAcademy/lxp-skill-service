import logging

from django.http import HttpResponse, HttpResponseServerError

logger = logging.getLogger("healthz")

# Liveness and Readiness probes for k8s/OCP
# https://www.ianlewis.org/en/kubernetes-health-checks-django
class HealthCheckMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        health_check_root_path = "/healthcheck"
        if request.method == "GET":
            if request.path == health_check_root_path + "/readiness":
                return self.readiness(request)
            elif request.path == health_check_root_path + "/liveness":
                return self.liveness(request)
        return self.get_response(request)

    def liveness(self, request):
        """
        Returns that the server is alive.
        """
        return HttpResponse("OK")

    def readiness(self, request):
        # Connect to each database and do a generic standard SQL query
        # that doesn't write any data and doesn't depend on any tables
        # being present.
        try:
            from django.db import connections
            for name in connections:
                cursor = connections[name].cursor()
                cursor.execute("SELECT 1;")
                row = cursor.fetchone()
                if row is None:
                    return HttpResponseServerError("db: invalid response")
        except Exception as e:
            logger.exception(e)
            return HttpResponseServerError("db: cannot connect to database.")

        # TODO: Enable once we introduce the cache
        #
        # # Call get_stats() to connect to each memcached instance and get it's stats.
        # # This can effectively check if each is online.
        # try:
        #     from django.core.cache import caches
        #     from django.core.cache import caches
        #     from django_redis.cache import RedisCache
        #     for cache in caches.all():
        #         if isinstance(cache, RedisCache):
        #             stats = cache._cache.get_stats()
        #             if len(stats) != len(cache._servers):
        #                 return HttpResponseServerError("cache: cannot connect to cache.")
        # except Exception as e:
        #     logger.exception(e)
        #     return HttpResponseServerError("cache: cannot connect to cache.")

        return HttpResponse("OK")
