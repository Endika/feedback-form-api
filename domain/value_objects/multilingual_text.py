from dataclasses import dataclass


@dataclass(frozen=True)
class MultilingualText:
    translations: dict[str, str]

    def __post_init__(self) -> None:
        if not self.translations:
            msg = "MultilingualText must have at least one translation"
            raise ValueError(msg)
        for lang_code, text in self.translations.items():
            if not lang_code or not isinstance(lang_code, str):
                msg = "Language code must be a non-empty string"
                raise ValueError(msg)
            if not text or not isinstance(text, str):
                msg = "Translation text must be a non-empty string"
                raise ValueError(msg)

    def get_text(self, language_code: str, default: str | None = None) -> str:
        return self.translations.get(
            language_code, default or next(iter(self.translations.values()))
        )

    def get_available_languages(self) -> list[str]:
        return list(self.translations.keys())

    def __str__(self) -> str:
        return next(iter(self.translations.values())) if self.translations else ""
