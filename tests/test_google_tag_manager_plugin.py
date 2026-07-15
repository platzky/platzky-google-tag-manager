import pytest
from platzky.plugin.plugin import ConfigPluginError

from platzky_google_tag_manager.plugin import GoogleTagManagerPlugin


def test_get_head_html_contains_gtm_id():
    """Test that GTM head script contains the correct tracking ID."""
    plugin = GoogleTagManagerPlugin({"ID": "GTM-XXXX"})

    head = plugin.get_head_html()

    assert "GTM-XXXX" in head
    assert "googletagmanager.com/gtm.js" in head


def test_get_body_html_contains_gtm_id():
    """Test that GTM noscript body code contains the correct tracking ID."""
    plugin = GoogleTagManagerPlugin({"ID": "GTM-XXXX"})

    body = plugin.get_body_html()

    assert "GTM-XXXX" in body
    assert "googletagmanager.com/ns.html" in body


def test_accepted_page_sections():
    """Test that the plugin declares both head and body as accepted sections."""
    plugin = GoogleTagManagerPlugin({"ID": "GTM-XXXX"})

    assert plugin.accepted_page_sections == frozenset({"head", "body"})


@pytest.mark.parametrize(
    "invalid_id",
    [
        "",
        "invalid",
        "');alert(1);//",
        "GTM-",
        "gtm-ABC123",
        "XYZ-123456",
    ],
)
def test_rejects_invalid_gtm_id(invalid_id: str):
    """Test that plugin raises validation error for invalid GTM IDs."""
    with pytest.raises(ConfigPluginError, match="Invalid GTM ID"):
        GoogleTagManagerPlugin({"ID": invalid_id})


@pytest.mark.parametrize(
    "valid_id",
    [
        "GTM-ABC123",
        "G-ABC123DEF",
        "AW-123456789",
        "DC-ABCDEF",
    ],
)
def test_accepts_valid_gtm_id(valid_id: str):
    """Test that plugin accepts valid Google tag ID formats."""
    plugin = GoogleTagManagerPlugin({"ID": valid_id})

    assert valid_id in plugin.get_head_html()
    assert valid_id in plugin.get_body_html()


def test_get_head_html_without_consent_default_omits_consent_script():
    """Test that no consent script is emitted when CONSENT_DEFAULT is unset."""
    plugin = GoogleTagManagerPlugin({"ID": "GTM-XXXX"})

    head = plugin.get_head_html()

    assert "consent" not in head.lower()


def test_get_head_html_with_consent_default_precedes_gtm_script():
    """Test that the consent default script is emitted before the GTM script."""
    plugin = GoogleTagManagerPlugin(
        {
            "ID": "GTM-XXXX",
            "CONSENT_DEFAULT": {
                "ad_storage": "denied",
                "analytics_storage": "denied",
            },
        }
    )

    head = plugin.get_head_html()

    assert "gtag('consent', 'default'," in head
    assert '"ad_storage": "denied"' in head
    assert '"analytics_storage": "denied"' in head
    assert head.index("gtag('consent', 'default',") < head.index("Google Tag Manager -->")


@pytest.mark.parametrize(
    "invalid_consent_default",
    [
        {"ad_storage": "maybe"},
        {"not_a_real_consent_type": "granted"},
    ],
)
def test_rejects_invalid_consent_default(invalid_consent_default: dict[str, str]):
    """Test that plugin raises validation error for malformed consent defaults."""
    with pytest.raises(ConfigPluginError):
        GoogleTagManagerPlugin({"ID": "GTM-XXXX", "CONSENT_DEFAULT": invalid_consent_default})
