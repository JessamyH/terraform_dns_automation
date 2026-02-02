
import unittest
from unittest.mock import patch
import main
import json
import builtins

class TestLambdaHandler(unittest.TestCase):
    def setUp(self):
        self.valid_add = {
            "Records": [
                {"body": json.dumps({
                    "request_id": "uuid-1",
                    "action": "add",
                    "client": "ikea",
                    "env": "production",
                    "subdomain": "ikea.production.jessamy-dns-test.com",
                    "record_type": "CNAME",
                    "ttl": 300,
                    "target": "prod-ikea-alb-123.elb.amazonaws.com"
                })}
            ]
        }
        self.valid_update = {
            "Records": [
                {"body": json.dumps({
                    "request_id": "uuid-2",
                    "action": "update",
                    "client": "ikea",
                    "env": "production",
                    "subdomain": "ikea.production.jessamy-dns-test.com",
                    "record_type": "CNAME",
                    "ttl": 300,
                    "target": "prod-ikea-alb-456.elb.amazonaws.com"
                })}
            ]
        }
        self.valid_delete = {
            "Records": [
                {"body": json.dumps({
                    "request_id": "uuid-3",
                    "action": "delete",
                    "client": "ikea",
                    "env": "production",
                    "subdomain": "ikea.production.jessamy-dns-test.com",
                    "record_type": "CNAME",
                    "ttl": 300,
                    "target": "prod-ikea-alb-456.elb.amazonaws.com"
                })}
            ]
        }
        self.invalid_event = {
            "Records": [
                {"body": json.dumps({
                    "client": "ikea",
                    "env": "production",
                    "record_type": "WRONG",
                    "ttl": -1,
                    "target": ""
                })}
            ]
        }
        self.no_subdomain = {
            "Records": [
                {"body": json.dumps({
                    "request_id": "uuid-4",
                    "action": "add",
                    "client": "ikea",
                    "env": "production",
                    "record_type": "A",
                    "ttl": 300,
                    "target": "1.2.3.4"
                })}
            ]
        }

    @patch("main.upsert_record")
    def test_valid_add(self, mock_upsert):
        mock_upsert.return_value = ("route53-ok", None)
        with patch.object(builtins, "print") as mock_print:
            main.handler(self.valid_add, None)
            output = "\n".join(str(a[0][0]) for a in mock_print.call_args_list)
        self.assertIn('"status": "success"', output)

    @patch("main.upsert_record")
    def test_valid_update(self, mock_upsert):
        mock_upsert.return_value = ("route53-ok", None)
        with patch.object(builtins, "print") as mock_print:
            main.handler(self.valid_update, None)
            output = "\n".join(str(a[0][0]) for a in mock_print.call_args_list)
        self.assertIn('"status": "success"', output)

    @patch("main.upsert_record")
    def test_valid_delete(self, mock_upsert):
        mock_upsert.return_value = ("route53-ok", None)
        with patch.object(builtins, "print") as mock_print:
            main.handler(self.valid_delete, None)
            output = "\n".join(str(a[0][0]) for a in mock_print.call_args_list)
        self.assertIn('"status": "success"', output)

    @patch("main.upsert_record")
    def test_invalid_event(self, mock_upsert):
        mock_upsert.return_value = ("route53-ok", None)
        with self.assertLogs(level='ERROR') as log:
            main.handler(self.invalid_event, None)
        self.assertIn('"status": "failure"', "\n".join(log.output) + "\n")

    @patch("main.upsert_record")
    def test_no_subdomain(self, mock_upsert):
        mock_upsert.return_value = ("route53-ok", None)
        with self.assertLogs(level='ERROR') as log:
            main.handler(self.no_subdomain, None)
        self.assertIn('Missing required field: subdomain', "\n".join(log.output) + "\n")

if __name__ == "__main__":
    unittest.main()
