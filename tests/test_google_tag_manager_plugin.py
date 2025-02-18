from platzky_google_tag_manager.entrypoint import process
from unittest.mock import Mock


def test_renders_head_code_with_gtm_id():
    app = Mock()
    plugin_config = {"ID": "GTM-XXXX"}

    result = process(app, plugin_config)

    app.add_dynamic_head.assert_called_once_with(
        """<!-- Google Tag Manager -->
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-XXXX');</script>
        <!-- End Google Tag Manager -->\n    """
    )
    assert result == app


def test_renders_body_code_with_gtm_id():
    app = Mock()
    plugin_config = {"ID": "GTM-XXXX"}

    result = process(app, plugin_config)

    app.add_dynamic_body.assert_called_once_with(
        """<!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXX
        "
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->
    """
    )
    assert result == app


def test_handles_empty_gtm_id():
    app = Mock()
    plugin_config = {"ID": ""}

    result = process(app, plugin_config)

    app.add_dynamic_head.assert_called_once_with(
        """<!-- Google Tag Manager -->
        <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
        new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','');</script>
        <!-- End Google Tag Manager -->
    """
    )
    app.add_dynamic_body.assert_called_once_with(
        """<!-- Google Tag Manager (noscript) -->
        <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=
        "
        height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
        <!-- End Google Tag Manager (noscript) -->
    """
    )
    assert result == app
