# TOTEM Dongle ZMK Config

Personal ZMK config for the [TOTEM](https://github.com/GEIGEIGEIST/TOTEM) keyboard with a third dongle setup built around [Prospector](https://github.com/carrefinho/prospector). This repo contains the firmware config, local shield files, and personal keymap changes for my setup, including Norwegian key definitions, dual-OS layers, host switching, and a few dongle-specific tweaks.

Detailed hardware information belongs in the upstream TOTEM and Prospector repos.

## Based On / Related Projects

- [TOTEM](https://github.com/GEIGEIGEIST/TOTEM) - base keyboard hardware/project.
- [ZMK](https://github.com/zmkfirmware/zmk) - firmware and build system.
- [Prospector](https://github.com/carrefinho/prospector) - dongle/display hardware platform.
- [prospector-zmk-module](https://github.com/carrefinho/prospector-zmk-module) - ZMK module used for Prospector integration.

## What This Repo Builds

From [`build.yaml`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/build.yaml):

- `totem_left`
- `totem_right`
- `totem_dongle prospector_adapter`
- `settings_reset`

These are the left half, right half, dongle, and reset images for the setup.

## What Is Customized Here

- Local TOTEM shield files and a dongle target in [`boards/shields/totem`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/boards/shields/totem).
- Dongle-specific Prospector/display settings such as fixed brightness, display rotation, and split central battery proxying.
- Norwegian localized keys via [`config/keys_nb.h`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/config/keys_nb.h).
- Personal keymap and behaviors in [`config/totem.keymap`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/config/totem.keymap).
- Dual-OS Mac layers, host switching, ZMK Studio unlock, and gaming layers.
- Minor BLE/radio tuning in [`config/totem.conf`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/config/totem.conf).

## Upstream Refs

- [`zmkfirmware/zmk`](https://github.com/zmkfirmware/zmk): `main`
- [`carrefinho/prospector-zmk-module`](https://github.com/carrefinho/prospector-zmk-module): `feat/new-status-screens`
- Build workflow: `zmkfirmware/zmk/.github/workflows/build-user-config.yml@main`

These are tracked refs/branches from [`config/west.yml`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/config/west.yml) and [`.github/workflows/build.yml`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/.github/workflows/build.yml), not tagged release versions.

## Where To Edit

- [`config/totem.keymap`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/config/totem.keymap)
- [`config/totem.conf`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/config/totem.conf)
- [`config/west.yml`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/config/west.yml)
- [`boards/shields/totem`](/home/robert/.t3/worktrees/zmk-config-totem-dongle/t3code-6fa37bab/boards/shields/totem)
