from unittest.mock import Mock

import pytest
from platzky.plugin.plugin import ConfigPluginError

from platzky_google_tag_manager.plugin import GoogleTagManagerPlugin


def test_renders_head_code_with_gtm_id():
    """Test that GTM head script is injected with the correct ID."""
    app = Mock()
    plugin = GoogleTagManagerPlugin({"ID": "GTM-XXXX"})

    result = plugin.process(app)

    app.add_dynamic_head.assert_called_once()
    head_call = app.add_dynamic_head.call_args[0][0]
    assert "GTM-XXXX" in head_call
    assert "googletagmanager.com/gtm.js" in head_call
    assert result == app


def test_renders_body_code_with_gtm_id():
    """Test that GTM noscript body code is injected with the correct ID."""
    app = Mock()
    plugin = GoogleTagManagerPlugin({"ID": "GTM-XXXX"})

    result = plugin.process(app)

    app.add_dynamic_body.assert_called_once()
    body_call = app.add_dynamic_body.call_args[0][0]
    assert "GTM-XXXX" in body_call
    assert "googletagmanager.com/ns.html" in body_call
    assert result == app


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
    app = Mock()
    plugin = GoogleTagManagerPlugin({"ID": valid_id})

    result = plugin.process(app)

    assert result == app
