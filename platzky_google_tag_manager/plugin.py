"""Platzky Google Tag Manager plugin — injects GTM tracking code into pages."""

import re
from typing import Any

from platzky.plugin.html_injector import HtmlInjectorPluginBase
from platzky.plugin.plugin import ConfigPluginError
from pydantic import BaseModel, ValidationError, field_validator

GTM_ID_PATTERN = re.compile(r"^(GTM|G|AW|DC)-[A-Z0-9]+$")


class _Config(BaseModel):
    """Internal config model for the Google Tag Manager plugin."""

    ID: str

    @field_validator("ID")
    @classmethod
    def id_must_be_valid_gtm_format(cls, v: str) -> str:
        """Validate that the ID matches a known Google tag format."""
        if not GTM_ID_PATTERN.match(v):
            raise ValueError(
                f"Invalid GTM ID '{v}'."
                " Expected format: GTM-XXXXXX, G-XXXXXXX, AW-XXXXXXX, or DC-XXXXXXX"
            )
        return v


class GoogleTagManagerPlugin(HtmlInjectorPluginBase):
    """Platzky plugin that injects Google Tag Manager tracking code."""

    accepted_page_sections = frozenset({"head", "body"})

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        try:
            validated = _Config.model_validate(config)
        except ValidationError as e:
            raise ConfigPluginError(str(e)) from e
        self._gtm_id = validated.ID

    def get_head_html(self) -> str:
        """Return the GTM script tag for injection into ``<head>``."""
        gtm_id = self._gtm_id
        return (
            "<!-- Google Tag Manager -->\n"
            "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
            "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            "})(window,document,'script','dataLayer','" + gtm_id + "');</script>\n"
            "<!-- End Google Tag Manager -->\n"
        )

    def get_body_html(self) -> str:
        """Return the GTM noscript iframe for injection at the start of ``<body>``."""
        gtm_id = self._gtm_id
        return (
            "<!-- Google Tag Manager (noscript) -->\n"
            '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id='
            + gtm_id
            + '" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
            "<!-- End Google Tag Manager (noscript) -->\n"
        )
