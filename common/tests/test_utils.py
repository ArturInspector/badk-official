import pytest
from common.utils import (
    get_english_translit,
    format_phone_number,
    get_generate_link_whatsapp,
)


class TestGetEnglishTranslit:
    def test_translit_russian_text(self):
        result = get_english_translit("Привет мир")
        assert result is not None
        assert len(result) > 0
        assert isinstance(result, str)

    def test_translit_with_special_letters(self):
        result = get_english_translit("ң ү ө")
        assert 'н' in result or 'y' in result or 'о' in result

    def test_slug_generation(self):
        result = get_english_translit("Test Text", slug=True)
        assert '-' in result or result.isalnum()

    def test_without_slug(self):
        result = get_english_translit("Test Text", slug=False)
        assert isinstance(result, str)

    def test_empty_string(self):
        result = get_english_translit("")
        assert isinstance(result, str)

    def test_special_characters(self):
        result = get_english_translit("Test!@#$%^&*()")
        assert isinstance(result, str)


class TestFormatPhoneNumber:
    def test_valid_phone_format(self):
        phone = "+996555123456"
        result = format_phone_number(phone)
        assert result.startswith("+")
        assert "(" in result
        assert ")" in result
        assert "-" in result

    def test_invalid_phone_length(self):
        phone = "12345"
        result = format_phone_number(phone)
        assert "Неправильный формат" in result

    def test_phone_with_spaces(self):
        phone = "+996 555 123 456"
        result = format_phone_number(phone)
        assert isinstance(result, str)

    def test_phone_with_dashes(self):
        phone = "+996-555-123-456"
        result = format_phone_number(phone)
        assert isinstance(result, str)

    def test_phone_without_plus(self):
        phone = "996555123456"
        result = format_phone_number(phone)
        assert isinstance(result, str)


class TestGetGenerateLinkWhatsapp:
    def test_generate_link_with_phone(self):
        phone = "+996555123456"
        message = "Hello"
        result = get_generate_link_whatsapp(phone, message)
        assert "whatsapp.com" in result
        assert phone in result
        assert "send" in result

    def test_generate_link_with_message(self):
        phone = "+996555123456"
        message = "Test message"
        result = get_generate_link_whatsapp(phone, message)
        assert message in result or "Test" in result

    def test_generate_link_encoding(self):
        phone = "+996555123456"
        message = "Hello World"
        result = get_generate_link_whatsapp(phone, message)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_generate_link_special_characters(self):
        phone = "+996555123456"
        message = "Hello! @#$%"
        result = get_generate_link_whatsapp(phone, message)
        assert isinstance(result, str)

    def test_generate_link_empty_message(self):
        phone = "+996555123456"
        message = ""
        result = get_generate_link_whatsapp(phone, message)
        assert "whatsapp.com" in result
        assert phone in result

