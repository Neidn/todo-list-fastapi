import factory
from factory.fuzzy import FuzzyChoice
from src.apps.todo.models.domain.todos import TodoItemBase
from src.apps.todo.models.schema.todos import TodoCreateRequest, TodoUpdateRequest


class TodoItemFactory(factory.Factory):
    """Creates fake TodoItem for testing"""

    class Meta:
        """Maps factory to data model"""

        model = TodoItemBase

    id = factory.Faker("uuid4")
    title = factory.Faker("sentence")
    content = factory.Faker("text")
    is_done = FuzzyChoice(choices=[True, False])
    created_at = "2021-01-01 00:00:00"
    updated_at = "2021-01-01 00:00:00"


class TodoCreateRequestFactory(factory.Factory):
    """Creates fake TodoCreateRequest for testing"""

    class Meta:
        """Maps factory to data model"""

        model = TodoCreateRequest

    title = factory.Faker("sentence")
    content = factory.Faker("text")
    is_done = FuzzyChoice(choices=[True, False])


class TodoUpdateRequestFactory(factory.Factory):
    """Creates fake TodoUpdateRequest for testing"""

    class Meta:
        """Maps factory to data model"""

        model = TodoUpdateRequest

    title = factory.Faker("sentence")
    content = factory.Faker("text")
    is_done = FuzzyChoice(choices=[True, False])
