import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import os


def setup_sentry():
    """Setup Sentry for error tracking."""
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
        environment=os.environ.get('ENVIRONMENT', 'production'),
    )
