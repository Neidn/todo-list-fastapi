import factory
from factory.fuzzy import FuzzyChoice

from src.apps.auth.model.domain.user import User
from src.apps.auth.model.schema.user import UserCreateRequest


class UserFactory(factory.Factory):
    """Creates fake User for testing"""

    class Meta:
        """Maps factory to data model"""

        model = User

    id = factory.Faker("uuid4")
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    full_name = factory.Faker("name")
    hashed_password = factory.Faker("password")
    disabled = FuzzyChoice(choices=[True, False])
    created_at = "2021-01-01 00:00:00"
    updated_at = "2021-01-01 00:00:00"


class UserCreateRequestFactory(factory.Factory):
    """Creates fake UserCreateRequest for testing"""

    class Meta:
        """Maps factory to data model"""

        model = UserCreateRequest

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    full_name = factory.Faker("name")
    plain_password = factory.Faker("password")
    repeat_plain_password = factory.Faker("password")
