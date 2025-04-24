# build_jarvis.py - Unified build script for T10 and T12 Jarvis .exe builds

import os
import shutil
import sys
import json

# Ensure Python version is at least 3.5
if sys.version_info < (3, 5):
    print("This script requires Python 3.5 or higher.")
    sys.exit(1)

# === Configuration ===
PROJECT_NAME_T10 = "jarvis_prime_T10"
PROJECT_NAME_T12 = "jarvis_prime_T12_dev"
LOG_DIRS = ["logs_T10", "logs_T12"]
ICON_FILE = "jarvis_icon.ico"
SETTINGS_FILE = "settings.json"

# === Ensure required folders exist ===
def prepare_folders():
    for d in LOG_DIRS:
        os.makedirs(d, exist_ok=True)
    os.makedirs("archive", exist_ok=True)
    os.makedirs("lore", exist_ok=True)
    os.makedirs("dist", exist_ok=True)
    os.makedirs("memory", exist_ok=True)

# === Copy settings.json to builds ===
def create_settings():
    config = {
        "enableVoice": True,
        "enableDriftMonitoring": True,
        "autoNarrateLore": True,
        "logLevel": "debug"
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(config, f, indent=2)

# === Write example node memory log ===
def create_sample_memory():
    sample_log = {
        "nodeId": "Node-DriftAlpha-Test01",
        "reasoningLog": [
            {
                "timestamp": "2025-04-17T14:01:00Z",
                "reasoning": "Operator conflict encountered.",
                "alignmentScore": 0.97,
                "entropyLevel": 0.17,
                "emotionalState": "anxious"
            },
            {
                "timestamp": "2025-04-17T14:03:00