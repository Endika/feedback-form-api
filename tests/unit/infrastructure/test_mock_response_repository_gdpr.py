import pytest

from domain.entities.answer import Answer
from domain.entities.response import Response
from domain.value_objects.form_id import FormId
from domain.value_objects.question_id import QuestionId
from domain.value_objects.response_id import ResponseId
from infrastructure.persistence.mock_response_repository import MockResponseRepository


@pytest.mark.asyncio()
async def test_given_responses_with_user_id_when_get_by_user_id_then_returns_matching_responses():
    # Given: A repository with responses from different users
    repository = MockResponseRepository()
    user1_id = "user1"
    user2_id = "user2"

    response1 = Response(
        id=ResponseId("response-1"),
        form_id=FormId("form-1"),
        answers=[Answer(question_id=QuestionId("q-1"), value=5)],
        user_id=user1_id,
    )
    response2 = Response(
        id=ResponseId("response-2"),
        form_id=FormId("form-1"),
        answers=[Answer(question_id=QuestionId("q-1"), value=4)],
        user_id=user1_id,
    )
    response3 = Response(
        id=ResponseId("response-3"),
        form_id=FormId("form-2"),
        answers=[Answer(question_id=QuestionId("q-2"), value="Good")],
        user_id=user2_id,
    )

    await repository.create(response1)
    await repository.create(response2)
    await repository.create(response3)

    # When: Get responses by user_id
    user1_responses = await repository.get_by_user_id(user1_id)
    user2_responses = await repository.get_by_user_id(user2_id)

    # Then: Only matching responses are returned
    expected_user1_count = 2
    expected_user2_count = 1
    assert len(user1_responses) == expected_user1_count
    assert all(r.user_id == user1_id for r in user1_responses)
    assert len(user2_responses) == expected_user2_count
    assert all(r.user_id == user2_id for r in user2_responses)


@pytest.mark.asyncio()
async def test_given_responses_with_user_id_when_delete_by_user_id_then_deletes_matching_responses():
    # Given: A repository with responses from different users
    repository = MockResponseRepository()
    user1_id = "user1"
    user2_id = "user2"

    response1 = Response(
        id=ResponseId("response-1"),
        form_id=FormId("form-1"),
        answers=[Answer(question_id=QuestionId("q-1"), value=5)],
        user_id=user1_id,
    )
    response2 = Response(
        id=ResponseId("response-2"),
        form_id=FormId("form-1"),
        answers=[Answer(question_id=QuestionId("q-1"), value=4)],
        user_id=user1_id,
    )
    response3 = Response(
        id=ResponseId("response-3"),
        form_id=FormId("form-2"),
        answers=[Answer(question_id=QuestionId("q-2"), value="Good")],
        user_id=user2_id,
    )

    await repository.create(response1)
    await repository.create(response2)
    await repository.create(response3)

    # When: Delete responses by user_id
    deleted_count = await repository.delete_by_user_id(user1_id)

    # Then: Matching responses are deleted
    expected_deleted_count = 2
    assert deleted_count == expected_deleted_count

    # And: Other user's responses remain
    remaining = await repository.get_all()
    assert len(remaining) == 1
    assert remaining[0].user_id == user2_id


@pytest.mark.asyncio()
async def test_given_no_responses_for_user_when_delete_by_user_id_then_returns_zero():
    # Given: A repository without responses for a user
    repository = MockResponseRepository()

    # When: Delete responses by user_id
    deleted_count = await repository.delete_by_user_id("nonexistent-user")

    # Then: Zero is returned
    assert deleted_count == 0


@pytest.mark.asyncio()
async def test_given_responses_without_user_id_when_get_by_user_id_then_returns_empty_list():
    # Given: A repository with responses without user_id
    repository = MockResponseRepository()

    response = Response(
        id=ResponseId("response-1"),
        form_id=FormId("form-1"),
        answers=[Answer(question_id=QuestionId("q-1"), value=5)],
        user_id=None,
    )

    await repository.create(response)

    # When: Get responses by user_id
    result = await repository.get_by_user_id("user123")

    # Then: Empty list is returned
    assert result == []
