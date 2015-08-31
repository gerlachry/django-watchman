import sys
from testing.elasticsearch import ElasticSearchServer

#setup Elastic testing server dependent on elasticsearch being on current PATH
es = ElasticSearchServer()
es.start()

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
                "HOST": "http://" + es._bind_host,
                "PORT": str(es._bind_port),
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




def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    #stop Elastic testing server
    es.stop()

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
