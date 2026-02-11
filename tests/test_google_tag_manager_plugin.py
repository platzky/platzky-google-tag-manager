from unittest.mock import Mock

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


def test_handles_empty_gtm_id():
    """Test that plugin handles an empty GTM ID gracefully."""
    app = Mock()
    plugin = GoogleTagManagerPlugin({"ID": ""})

    result = plugin.process(app)

    app.add_dynamic_head.assert_called_once()
    app.add_dynamic_body.assert_called_once()
    assert result == app
