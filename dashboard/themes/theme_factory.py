from .themes import (
    darkly_theme,
    flatly_theme,
    pulse_theme,
    sandstone_theme,
    slate_theme,
    solar_theme,
    spacelab_theme,
)


class ThemeFactory:
    @classmethod
    def create(self, theme_name: str):
        if theme_name == flatly_theme.name:
            return flatly_theme
        elif theme_name == darkly_theme.name:
            return darkly_theme
        elif theme_name == slate_theme.name:
            return slate_theme
        elif theme_name == sandstone_theme.name:
            return sandstone_theme
        elif theme_name == pulse_theme.name:
            return pulse_theme
        elif theme_name == solar_theme.name:
            return solar_theme
        elif theme_name == spacelab_theme.name:
            return spacelab_theme
        else:
            raise ValueError(f"UI theme {theme_name=} doesn't exist.")