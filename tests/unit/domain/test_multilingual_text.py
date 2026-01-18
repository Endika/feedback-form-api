import pytest

from domain.value_objects.multilingual_text import MultilingualText


def test_given_valid_translations_when_create_multilingual_text_then_succeeds():
    translations = {"en": "Hello", "es": "Hola"}
    multilingual_text = MultilingualText(translations)
    assert multilingual_text.translations == translations


def test_given_empty_translations_when_create_multilingual_text_then_raises_error():
    with pytest.raises(ValueError, match="must have at least one translation"):
        MultilingualText({})


def test_given_invalid_language_code_when_create_multilingual_text_then_raises_error():
    with pytest.raises(ValueError, match="Language code must be a non-empty string"):
        MultilingualText({"": "Hello"})


def test_given_invalid_text_when_create_multilingual_text_then_raises_error():
    with pytest.raises(ValueError, match="Translation text must be a non-empty string"):
        MultilingualText({"en": ""})


def test_given_language_code_when_get_text_then_returns_translation():
    translations = {"en": "Hello", "es": "Hola"}
    multilingual_text = MultilingualText(translations)
    assert multilingual_text.get_text("en") == "Hello"
    assert multilingual_text.get_text("es") == "Hola"


def test_given_missing_language_code_when_get_text_then_returns_default():
    translations = {"en": "Hello"}
    multilingual_text = MultilingualText(translations)
    assert multilingual_text.get_text("es", default="Default") == "Default"


def test_given_missing_language_code_when_get_text_without_default_then_returns_first_translation():
    translations = {"en": "Hello", "fr": "Bonjour"}
    multilingual_text = MultilingualText(translations)
    assert multilingual_text.get_text("es") == "Hello"
