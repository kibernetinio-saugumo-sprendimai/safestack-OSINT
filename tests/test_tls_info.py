import ssl
import unittest
from unittest.mock import MagicMock, patch

from modules.tls_info.module import TLSInfoModule


class TLSInfoProtocolTest(unittest.TestCase):
    def test_probe_requires_tls_12_and_preserves_tls_13_and_sni(self):
        context = MagicMock()
        connection = MagicMock()
        raw_socket = MagicMock()
        connection.__enter__.return_value = raw_socket
        tls_connection = MagicMock()
        tls_socket = MagicMock()
        tls_connection.__enter__.return_value = tls_socket
        context.wrap_socket.return_value = tls_connection
        tls_socket.getpeercert.side_effect = [b"certificate", {}]
        tls_socket.version.return_value = "TLSv1.3"
        tls_socket.cipher.return_value = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)

        with patch(
            "modules.tls_info.module.ssl.create_default_context",
            return_value=context,
        ):
            with patch(
                "modules.tls_info.module.socket.create_connection",
                return_value=connection,
            ):
                result = TLSInfoModule()._probe_tls("example.com", 443)

        self.assertEqual(context.minimum_version, ssl.TLSVersion.TLSv1_2)
        context.wrap_socket.assert_called_once_with(
            raw_socket, server_hostname="example.com"
        )
        self.assertEqual(result["tls"]["protocol"], "TLSv1.3")


if __name__ == "__main__":
    unittest.main()
