"""Context builder module for assembling the 5-layer WidgetWare SDR context package."""

import copy
from pathlib import Path
from typing import Any
import yaml

from widgetware_sdr.instructions import get_system_instructions


def _find_config_dir(custom_path: str | Path | None = None) -> Path:
    """Find the configuration directory containing products.yaml, icp.yaml, policies.yaml."""
    if custom_path is not None:
        cfg_path = Path(custom_path)
        if cfg_path.exists() and cfg_path.is_dir():
            return cfg_path
        raise FileNotFoundError(f"Configuration directory not found at: {cfg_path}")

    # Search common locations relative to current working dir or package
    cwd_config = Path.cwd() / "config"
    if cwd_config.exists() and cwd_config.is_dir():
        return cwd_config

    pkg_config = Path(__file__).resolve().parents[2] / "config"
    if pkg_config.exists() and pkg_config.is_dir():
        return pkg_config

    raise FileNotFoundError("Configuration directory 'config' could not be found.")


def load_yaml_config(file_path: Path) -> dict[str, Any]:
    """Load a YAML configuration file safely."""
    if not file_path.exists():
        raise FileNotFoundError(f"Required configuration file missing: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Configuration file {file_path.name} must contain a YAML dictionary.")
    return data


def build_context(
    account: dict[str, Any],
    objective: str,
    evidence: list[dict[str, Any]],
    state: dict[str, Any] | None = None,
    config_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Build the 5-layer WidgetWare SDR context package.

    Args:
        account: Target account data dictionary (untrusted task context).
        objective: Research objective string.
        evidence: List of evidence dictionaries preserving provenance.
        state: Optional workflow execution state dictionary.
        config_dir: Optional path to config directory.

    Returns:
        Dict containing system_instructions, business_context, task_context,
        retrieved_evidence, and state.
    """
    cfg_dir = _find_config_dir(config_dir)

    products_file = cfg_dir / "products.yaml"
    icp_file = cfg_dir / "icp.yaml"
    policies_file = cfg_dir / "policies.yaml"

    products = load_yaml_config(products_file)
    icp = load_yaml_config(icp_file)
    policies = load_yaml_config(policies_file)

    instructions = get_system_instructions()

    assembled_context = {
        "system_instructions": instructions,
        "business_context": {
            "products": products,
            "icp": icp,
            "policies": policies,
        },
        "task_context": {
            "account": copy.deepcopy(account),
            "objective": objective,
        },
        "retrieved_evidence": copy.deepcopy(evidence),
        "state": copy.deepcopy(state) if state is not None else {},
    }

    return assembled_context
