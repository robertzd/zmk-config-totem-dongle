# TOTEM Dongle ZMK Config

Personal ZMK config for a TOTEM split keyboard with a 3-device setup: left half, right half, and a Prospector-based dongle. Built for Seeeduino XIAO BLE controllers, with Norwegian key definitions, Mac-mode overlays, Bluetooth host switching, gaming layers, and dongle-specific display and battery behavior.

Hardware build details, PCB files, and assembly instructions live in the upstream TOTEM and Prospector projects. This README focuses on the firmware configuration in this repo.

## Built On

- [TOTEM](https://github.com/GEIGEIGEIST/TOTEM)
- [ZMK](https://github.com/zmkfirmware/zmk)
- [Prospector](https://github.com/carrefinho/prospector)
- [prospector-zmk-module](https://github.com/carrefinho/prospector-zmk-module): ZMK module used for Prospector integration
- [keymap-drawer](https://github.com/caksoylar/keymap-drawer): layout rendering tool used by `scripts/render_layouts.py`
- [miryoku](https://github.com/manna-harbour/miryoku) as layout inspiration

Tracked refs:

- [`zmkfirmware/zmk`](https://github.com/zmkfirmware/zmk): `main`
- [`carrefinho/prospector-zmk-module`](https://github.com/carrefinho/prospector-zmk-module): `feat/new-status-screens`
- Build workflow: `zmkfirmware/zmk/.github/workflows/build-user-config.yml@main`

These are the tracked refs from [`config/west.yml`](config/west.yml) and [`.github/workflows/build.yml`](.github/workflows/build.yml), not tagged releases.

## Key Features

- Norwegian-localized keymap in [`config/totem.keymap`](config/totem.keymap) via [`config/keys_nb.h`](config/keys_nb.h)
- Main layers: `Base`, `Nav`, `Num`, `Sym`, `Meta`, `Media`
- Home row mods on the base and Mac overlay layers
- Mac mode through conditional layers
- Bluetooth slot switching, Bluetooth clear, and output select on `Meta`
- Two gaming layers
- Dongle tweaks: fixed brightness, 180-degree display rotation, split battery proxying
- Global radio/BLE tuning in [`config/totem.conf`](config/totem.conf)

## Layer Controls

The leftmost thumb key is `Esc` when tapped and activates `Meta` when held:

- Hold `Meta` and press `Q` to select Bluetooth output.
- Hold `Meta` and press `A` to select USB output.
- Hold `Meta` and press `W`, `E`, `R`, or `T` to select Bluetooth profile 0, 1, 2, or 3.
- Hold `Meta` and press `P` to toggle Mac mode.
- Hold `Meta` and press `G` to enter `Gaming`.
- Hold `Meta` and press `B` to enter `Gaming_2`.
- Press the rightmost thumb key in either gaming layer to return to `Base`.
- Hold `Meta` and press `P` again to leave Mac mode.

## Layout Reference

Rendered layout references live in [`docs/layouts`](docs/layouts). They are generated from [`config/totem.keymap`](config/totem.keymap) by [`scripts/render_layouts.py`](scripts/render_layouts.py), which uses [keymap-drawer](https://github.com/caksoylar/keymap-drawer) to parse the keymap, normalize this repo's Norwegian and custom legends, and write the SVG/PNG outputs. The helper script was originally created with GPT/Codex assistance and is now maintained in-repo.

Main layers:
- [`docs/layouts/totem-layouts-main.png`](docs/layouts/totem-layouts-main.png)
- [`docs/layouts/totem-layouts-main.svg`](docs/layouts/totem-layouts-main.svg)

Full layout:
- [`docs/layouts/totem-layouts.png`](docs/layouts/totem-layouts.png)
- [`docs/layouts/totem-layouts.svg`](docs/layouts/totem-layouts.svg)
- [`docs/layouts/totem-layouts.yaml`](docs/layouts/totem-layouts.yaml)

![TOTEM main layout reference](docs/layouts/totem-layouts-main.png)

To regenerate:

```sh
python3 -m pip install --target .tools keymap-drawer PyYAML
python3 scripts/render_layouts.py
```

PNG output requires `rsvg-convert` in `PATH`.

## Build Targets

- `totem_left`: left keyboard half
- `totem_right`: right keyboard half
- `totem_dongle prospector_adapter`: Prospector dongle target
- `settings_reset`: reset target for clearing saved ZMK settings

Targets are defined in [`build.yaml`](build.yaml) and built in GitHub Actions via [`.github/workflows/build.yml`](.github/workflows/build.yml), which uses the upstream ZMK user-config workflow.

## Where To Edit

- [`config/totem.keymap`](config/totem.keymap): active keymap
- [`config/totem.conf`](config/totem.conf): global config
- [`config/boards/shields/totem`](config/boards/shields/totem): local shield and dongle overrides
- [`config/west.yml`](config/west.yml): upstream dependencies
- [`docs/layouts`](docs/layouts): generated layout references
- [`scripts/render_layouts.py`](scripts/render_layouts.py): layout rendering

There is also a shield-local [`config/boards/shields/totem/totem.keymap`](config/boards/shields/totem/totem.keymap), but the active user keymap for this repo is [`config/totem.keymap`](config/totem.keymap).
