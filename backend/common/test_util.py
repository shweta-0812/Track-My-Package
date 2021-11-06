# type: ignore
import pytest
from mockito import unstub


@pytest.mark.unit
class BaseUnitTestCase:
    @classmethod
    def teardown_class(cls):
        unstub()

    def teardown_method(func):
        unstub()


@pytest.mark.integration
class BaseIntegrationTestCase:
    @classmethod
    def teardown_class(cls):
        unstub()

    def teardown_method(func):
        unstub()


@pytest.mark.integration
@pytest.mark.asyncio
class BaseAsyncIntegrationTestCase:
    @classmethod
    def teardown_class(cls):
        unstub()

    def teardown_method(func):
        unstub()


@pytest.mark.api
@pytest.mark.asyncio
class BaseAPITestCase:
    @classmethod
    def teardown_class(cls):
        unstub()

    def teardown_method(func):
        unstub()


@pytest.fixture
def main_app():
    from main import app

    return app
