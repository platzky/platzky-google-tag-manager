"""Platzky Google Tag Manager plugin — injects GTM tracking code into pages."""

from typing import cast

from platzky.engine import Engine
from platzky.plugin.plugin import PluginBase, PluginBaseConfig
from pydantic import field_validator


class GoogleTagManagerConfig(PluginBaseConfig):
    """Configuration model for the Google Tag Manager plugin."""

    ID: str

    @field_validator("ID")
    @classmethod
    def id_must_not_be_empty(cls, v: str) -> str:
        """Validate that the GTM ID is not empty."""
        if not v.strip():
            raise ValueError("GTM ID must not be empty")
        return v


class GoogleTagManagerPlugin(PluginBase[GoogleTagManagerConfig]):
    """Platzky plugin that injects Google Tag Manager tracking code."""

    @classmethod
    def get_config_model(cls) -> type[GoogleTagManagerConfig]:
        """Return the config model class for this plugin."""
        return GoogleTagManagerConfig

    def process(self, app: Engine) -> Engine:
        """Inject GTM tracking scripts into the app's dynamic head and body."""
        config = cast(GoogleTagManagerConfig, self.config)
        gtm_id = config.ID

        head_code = (
            "<!-- Google Tag Manager -->\n"
            "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
            "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
            "})(window,document,'script','dataLayer','" + gtm_id + "');</script>\n"
            "<!-- End Google Tag Manager -->\n"
        body = (
            '<!-- Google Tag Manager (noscript) -->\n'
            '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id='
             gtm_id
             '" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
            '<!-- End Google Tag Manager (noscript) -->\n'
        )
        app.add_dynamic_body(body)

        return app
