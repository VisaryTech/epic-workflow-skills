import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import build_epic_status_report
import build_erp_url
import erp_config


class ErpConfigTests(unittest.TestCase):
    def test_load_known_keys_uses_lifecycle_statuses(self):
        lifecycle = {
            "status_env_map": {
                "draft": "ERP_LABEL_DRAFT",
                "qa-ready": "ERP_LABEL_QA_READY",
            },
            "plan_epic_label_env": "ERP_LABEL_EPIC_PLAN",
        }

        with mock.patch.object(erp_config, "load_lifecycle", return_value=lifecycle):
            keys = erp_config.load_known_keys()

        self.assertEqual(
            keys,
            [
                "ERP_BASE_URL",
                "ERP_PROJECT_ID",
                "ERP_LABEL_EPIC_PLAN",
                "ERP_LABEL_DRAFT",
                "ERP_LABEL_QA_READY",
            ],
        )

    def test_read_local_config_fails_on_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "erp-env.json"
            config_path.write_text("{invalid json", encoding="utf-8")

            with self.assertRaises(erp_config.ConfigError) as exc_info:
                erp_config.read_local_config(config_path)

        self.assertEqual(exc_info.exception.reason, "invalid_config")


class BuildErpUrlTests(unittest.TestCase):
    def test_resolve_base_url_requires_configured_value(self):
        with mock.patch.object(build_erp_url, "resolve_env_map", return_value=({}, ["ERP_BASE_URL"])):
            with self.assertRaises(erp_config.ConfigError) as exc_info:
                build_erp_url._resolve_base_url()

        self.assertEqual(exc_info.exception.reason, "missing_config")

    def test_extract_ids_from_epic_url(self):
        project_id, epic_id = build_erp_url._extract_ids_from_epic_url(
            "https://erp.local/tasktracker/projects/456/epics/123"
        )

        self.assertEqual(project_id, "456")
        self.assertEqual(epic_id, "123")

    def test_build_epic_url_requires_project_and_entity_id(self):
        payload, code = build_erp_url._build_epic_url(
            base_url="https://erp.local",
            entity_id="123",
            project_id=None,
        )

        self.assertEqual(code, 1)
        self.assertEqual(payload["reason"], "missing_required_parts")
        self.assertEqual(payload["missing"], ["project_id"])


class BuildEpicStatusReportTests(unittest.TestCase):
    def test_fetch_epics_paginates_beyond_first_page(self):
        pages = [
            {"value": [{"ID": str(index), "Title": f"Epic {index}", "Labels": []} for index in range(100)]},
            {"value": [{"ID": str(index), "Title": f"Epic {index}", "Labels": []} for index in range(100, 200)]},
            {"value": [{"ID": "200", "Title": "Epic 200", "Labels": []}]},
        ]

        def fake_run_json(cmd, cwd=None, reason=None):
            skip_arg = next(item for item in cmd if item.startswith("$skip="))
            skip = int(skip_arg.split("=", 1)[1])
            return pages[skip // 100]

        with mock.patch.object(build_epic_status_report, "run_json", side_effect=fake_run_json):
            epics = build_epic_status_report.fetch_epics("123", "Labels/any(...)")

        self.assertEqual(len(epics), 201)
        self.assertEqual(epics[0]["ID"], "0")
        self.assertEqual(epics[-1]["ID"], "200")

    def test_fetch_epics_fails_on_duplicate_page_items(self):
        pages = [
            {"value": [{"ID": str(index), "Title": f"Epic {index}", "Labels": []} for index in range(100)]},
            {"value": [{"ID": "99", "Title": "Epic 99 duplicate", "Labels": []}]},
        ]

        def fake_run_json(cmd, cwd=None, reason=None):
            skip_arg = next(item for item in cmd if item.startswith("$skip="))
            skip = int(skip_arg.split("=", 1)[1])
            return pages[skip // 100]

        with mock.patch.object(build_epic_status_report, "run_json", side_effect=fake_run_json):
            with redirect_stdout(StringIO()):
                with self.assertRaises(SystemExit):
                    build_epic_status_report.fetch_epics("123", "Labels/any(...)")


if __name__ == "__main__":
    unittest.main()
