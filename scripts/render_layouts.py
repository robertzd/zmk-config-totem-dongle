#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
KEYMAP = REPO_ROOT / "config" / "totem.keymap"
INFO_JSON = REPO_ROOT / "config" / "info.json"
OUTPUT_DIR = REPO_ROOT / "docs" / "layouts"
PYTHON_BIN = Path("/usr/bin/python3")


EXACT_LABELS = {
    "OUT USB": "USB",
    "OUT BLE": "BLE",
    "BT CLR": "BT clr",
    "LEFT WIN": "Gui",
    "LEFT GUI": "Gui",
    "LEFT_ALT": "Alt",
    "LEFT ALT": "Alt",
    "LEFT CONTROL": "Ctrl",
    "LEFT_CTRL": "Ctrl",
    "RCTRL": "Ctrl",
    "RIGHT CONTROL": "Ctrl",
    "RIGHT_CTRL": "Ctrl",
    "LEFT SHIFT": "Shift",
    "LSHIFT": "Shift",
    "RIGHT SHIFT": "Shift",
    "RSHIFT": "Shift",
    "RIGHT ALT": "AltGr",
    "RALT": "AltGr",
    "RIGHT WIN": "Gui",
    "RIGHT GUI": "Gui",
    "LEFT ARROW": "Left",
    "RIGHT ARROW": "Right",
    "UP ARROW": "Up",
    "DOWN ARROW": "Down",
    "PAGE DOWN": "PgDn",
    "PG UP": "PgUp",
    "PRINTSCREEN": "PrtSc",
    "ESCAPE": "Esc",
    "ESC": "Esc",
    "DELETE": "Del",
    "INSERT": "Ins",
    "BACKSPACE": "Bsp",
    "BSPC": "Bsp",
    "PREVIOUS": "Prev",
    "VOLUME DOWN": "Vol-",
    "VOL UP": "Vol+",
    "NEXT": "Next",
    "STOP": "Stop",
    "PP": "Play",
    "MUTE": "Mute",
    "CAPS WORD": "CapsWord",
    "OS_Mac": "Mac mode",
    "Base": "Base",
    "Gaming_2": "Game 2",
}

HID_LABELS = {
    "KEYBOARD Q": "Q",
    "KEYBOARD W": "W",
    "KEYBOARD E": "E",
    "KEYBOARD R": "R",
    "KEYBOARD T": "T",
    "KEYBOARD Y": "Y",
    "KEYBOARD U": "U",
    "KEYBOARD I": "I",
    "KEYBOARD O": "O",
    "KEYBOARD P": "P",
    "KEYBOARD A": "A",
    "KEYBOARD S": "S",
    "KEYBOARD D": "D",
    "KEYBOARD F": "F",
    "KEYBOARD G": "G",
    "KEYBOARD H": "H",
    "KEYBOARD J": "J",
    "KEYBOARD K": "K",
    "KEYBOARD L": "L",
    "KEYBOARD Z": "Z",
    "KEYBOARD X": "X",
    "KEYBOARD C": "C",
    "KEYBOARD V": "V",
    "KEYBOARD B": "B",
    "KEYBOARD N": "N",
    "KEYBOARD M": "M",
    "KEYBOARD 0 AND RIGHT PARENTHESIS": "0",
    "KEYBOARD 1 AND EXCLAMATION": "1",
    "KEYBOARD 2 AND AT": "2",
    "KEYBOARD 3 AND HASH": "3",
    "KEYBOARD 4 AND DOLLAR": "4",
    "KEYBOARD 5 AND PERCENT": "5",
    "KEYBOARD 6 AND CARET": "6",
    "KEYBOARD 7 AND AMPERSAND": "7",
    "KEYBOARD 8 AND ASTERISK": "8",
    "KEYBOARD 9 AND LEFT PARENTHESIS": "9",
    "KEYBOARD LEFT BRACKET AND LEFT BRACE": "A_RING",
    "KEYBOARD SEMICOLON AND COLON": "O_SLASH",
    "KEYBOARD APOSTROPHE AND QUOTE": "AE",
    "KEYBOARD COMMA AND LESS THAN": ",",
    "KEYBOARD PERIOD AND GREATER THAN": ".",
    "KEYBOARD SLASH AND QUESTION MARK": "MINUS",
    "KEYBOARD NON US BACKSLASH AND PIPE": "LESS_THAN",
    "KEYBOARD BACKSLASH AND PIPE": "SINGLE_QUOTE",
    "KEYBOARD EQUAL AND PLUS": "BACKSLASH",
    "KEYBOARD RIGHT BRACKET AND RIGHT BRACE": "UMLAUT",
    "KEYBOARD GRAVE ACCENT AND TILDE": "PIPE",
}

HID_VARIANTS = {
    ("A_RING", None): "Å",
    ("O_SLASH", None): "Ø",
    ("AE", None): "Æ",
    ("UMLAUT", None): "¨",
    ("PIPE", None): "|",
    ("SINGLE_QUOTE", None): "'",
    ("SINGLE_QUOTE", "LS"): "*",
    ("BACKSLASH", None): "\\",
    ("BACKSLASH", "LS"): "`",
    ("BACKSLASH", "RA"): "´",
    ("MINUS", None): "-",
    ("MINUS", "LS"): "?",
    ("LESS_THAN", None): "<",
    ("LESS_THAN", "LS"): ">",
    ("PIPE", "LS"): "§",
    ("PIPE", "RA"): "~",
    ("UMLAUT", "LS"): "^",
    ("UMLAUT", "RA"): "~",
    ("7", "LS"): "/",
    ("7", "RA"): "{",
    ("8", "LS"): "(",
    ("8", "RA"): "[",
    ("9", "LS"): ")",
    ("9", "RA"): "]",
    ("0", "LS"): "=",
    ("0", "RA"): "}",
    ("1", "LS"): "!",
    ("2", "LS"): "\"",
    ("2", "RA"): "@",
    ("3", "LS"): "#",
    ("4", "LS"): "¤",
    ("4", "RA"): "$",
    ("5", "LS"): "%",
    ("5", "RA"): "€",
    ("6", "LS"): "&",
    (",", "LS"): ";",
    (".", "LS"): ":",
}

MOD_LABELS = {
    "LEFT_WIN": "Gui",
    "LEFT_GUI": "Gui",
    "RIGHT_WIN": "Gui",
    "RIGHT_GUI": "Gui",
    "LEFT_CONTROL": "Ctrl",
    "LEFT_CTRL": "Ctrl",
    "RIGHT_CONTROL": "Ctrl",
    "RIGHT_CTRL": "Ctrl",
    "LCTRL": "Ctrl",
    "RCTRL": "Ctrl",
    "LEFT_SHIFT": "Shift",
    "RIGHT_SHIFT": "Shift",
    "LSHIFT": "Shift",
    "RSHFT": "Shift",
    "LEFT_ALT": "Alt",
    "LALT": "Alt",
    "RIGHT_ALT": "AltGr",
    "RALT": "AltGr",
}


def run_keymap_drawer(*args: str) -> None:
    env = os.environ.copy()
    tools_dir = REPO_ROOT / ".tools"
    if tools_dir.exists():
        python_path = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(tools_dir) if not python_path else f"{tools_dir}:{python_path}"
    subprocess.run([str(PYTHON_BIN), "-m", "keymap_drawer", *args], check=True, env=env, cwd=REPO_ROOT)


def clean_text(text: str) -> str:
    if text in EXACT_LABELS:
        return EXACT_LABELS[text]

    if text.startswith("Ctl+") or text.startswith("Gui+"):
        prefix, rest = text.split("+", 1)
        return f"{prefix}+{clean_text(rest)}"

    match = re.fullmatch(r"&hm\s+([A-Z_]+)\s+(.+)", text)
    if match:
        hold, tap = match.groups()
        return yaml.safe_dump(
            {"t": clean_text(tap), "h": MOD_LABELS.get(hold, hold)},
            sort_keys=False,
            default_flow_style=True,
        ).strip()

    variant_match = re.search(r"\b(LS|RA)\s*\(", text)
    variant = variant_match.group(1) if variant_match else None

    normalized = re.sub(r"[_()]+", " ", text)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if "MINUS AND UNDERSCORE" in normalized:
        return "?" if variant == "LS" else "-"
    hid_names = re.findall(r"KEYBOARD ([A-Z0-9 ]+)", normalized)
    if hid_names:
        key_name = hid_names[-1].strip()
        key = HID_LABELS.get(f"KEYBOARD {key_name}")
        if key is None:
            for hid_name, mapped in sorted(HID_LABELS.items(), key=lambda item: len(item[0]), reverse=True):
                if hid_name in normalized:
                    key = mapped
                    break
        if key is None:
            return text
        return HID_VARIANTS.get((key, variant), key)

    return EXACT_LABELS.get(text, text)


def normalize_binding(binding):
    if isinstance(binding, str):
        hm_match = re.fullmatch(r"&hm\s+([A-Z_]+)\s+(.+)", binding)
        if hm_match:
            hold, tap = hm_match.groups()
            return {"t": clean_text(tap), "h": MOD_LABELS.get(hold, hold)}
        return clean_text(binding)

    if isinstance(binding, dict):
        normalized = {}
        for key, value in binding.items():
            if isinstance(value, str):
                normalized[key] = clean_text(value)
            else:
                normalized[key] = value
        return normalized

    return binding


def normalize_yaml(data: dict) -> dict:
    for layer_name, bindings in data["layers"].items():
        data["layers"][layer_name] = [normalize_binding(binding) for binding in bindings]

    for combo in data.get("combos", []):
        if combo.get("k") == "&caps_word":
            combo["k"] = "CapsWord"

    return data


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def render_svg(yaml_path: Path, output_path: Path, *, layers: list[str] | None = None, footer: str = "") -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as config_file:
        yaml.safe_dump(
            {
                "draw_config": {
                    "dark_mode": True,
                    "n_columns": 2,
                    "footer_text": footer,
                    "separate_combo_diagrams": True,
                    "combo_diagrams_scale": 2,
                    "shrink_wide_legends": 6,
                }
            },
            config_file,
            sort_keys=False,
            allow_unicode=True,
        )
        config_path = Path(config_file.name)

    try:
        args = ["-c", str(config_path), "draw", str(yaml_path), "-j", str(INFO_JSON), "-o", str(output_path)]
        if layers:
            args.extend(["-s", *layers])
        run_keymap_drawer(*args)
    finally:
        config_path.unlink(missing_ok=True)


def render_png(svg_path: Path, png_path: Path) -> None:
    converter = shutil.which("rsvg-convert")
    if not converter:
        return
    subprocess.run(
        [converter, "-b", "#111111", "-o", str(png_path), str(svg_path)],
        check=True,
        cwd=REPO_ROOT,
    )


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    parsed_yaml = OUTPUT_DIR / "totem-layouts.yaml"
    run_keymap_drawer("parse", "-z", str(KEYMAP), "-o", str(parsed_yaml))

    data = yaml.safe_load(parsed_yaml.read_text(encoding="utf-8"))
    normalized = normalize_yaml(data)
    write_yaml(parsed_yaml, normalized)

    full_svg = OUTPUT_DIR / "totem-layouts.svg"
    render_svg(
        parsed_yaml,
        full_svg,
        footer="Generated from config/totem.keymap",
    )
    main_svg = OUTPUT_DIR / "totem-layouts-main.svg"
    render_svg(
        parsed_yaml,
        main_svg,
        layers=["Base", "Nav", "Num", "Sym", "Meta", "Media"],
        footer="Main layers",
    )
    render_png(full_svg, OUTPUT_DIR / "totem-layouts.png")
    render_png(main_svg, OUTPUT_DIR / "totem-layouts-main.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
