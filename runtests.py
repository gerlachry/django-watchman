import sys
import elasticsearch

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="watchman.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "watchman",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        ELASTICS={
            "default": {
                "HOST": "http://192.168.99.100",
                "PORT": "32769",
            },
            "backup": {
                "HOST": "http://192.168.99.100",
                "PORT": "32769",
                "proxies": {
                    "http": None,
                    "https": None
                }
            }
        }
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")

#setup Elastic testing server
try:
    #es = ElasticSearchServer(settings.ELASTICS['default']['HOST'] + ':' + settings.ELASTICS['default']['PORT'])
    #es.start()
    es = elasticsearch.Elasticsearch(hosts=settings.ELASTICS['default']['HOST'] + ':' + settings.ELASTICS['default']['PORT'])
except RuntimeError:
    raise RuntimeError("Elastic client not able to connect to %s on port %s" % (settings.ELASTICS['default']['HOST'], settings.ELASTICS['default']['PORT']))
    sys.exit(1)


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
