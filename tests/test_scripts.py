import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import build_erp_url
import erp_config


class ErpConfigTests(unittest.TestCase):
    def test_default_config_path_is_user_config_file(self):
        self.assertEqual(
            erp_config.CONFIG_PATH,
            Path(os.path.expanduser("~/.config/erp-env.json")),
        )

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


class DirectTaskTrackerCallRegressionTests(unittest.TestCase):
    def _read_repository_text_files(self):
        root = Path(__file__).resolve().parents[1]
        text_suffixes = {".md", ".py", ".yaml", ".yml", ".json", ".example"}

        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in text_suffixes:
                continue
            if any(part in {".git", "__pycache__"} for part in path.parts):
                continue
            yield root, path, path.read_text(encoding="utf-8")

    def test_repository_does_not_call_external_tasktracker_scripts_directly(self):
        forbidden = [
            "python " + "api.py",
            "TASKTRACKER" + "_DIR",
            "skills/" + "tasktracker-api",
            "skills\\" + "tasktracker-api",
            "patch_task_command" + "_change_weight_task_id",
        ]

        offenders = []
        for root, path, content in self._read_repository_text_files():
            for token in forbidden:
                if token in content:
                    offenders.append(f"{path.relative_to(root)}: {token}")

        self.assertEqual(offenders, [])

    def test_erp_dependency_contract_points_to_visary_cloud_api_skills(self):
        root = Path(__file__).resolve().parents[1]
        required_files = [
            "SKILL.md",
            "README.md",
            "references/skill-map.md",
            "skills/epic-task-weight-estimator/SKILL.md",
        ]
        missing = []

        for relative_path in required_files:
            path = root / relative_path
            content = path.read_text(encoding="utf-8")
            if "visary-cloud-api-skills" not in content:
                missing.append(relative_path)

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
