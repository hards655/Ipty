# Android 15 — Galaxy S23 layout test

This project boots a standard Android API 35 x86_64 virtual device in GitHub Actions, with a Galaxy S23-inspired 1080×2340 display. It is for application compatibility and UI tests, not Samsung firmware.

The requested SM-S911B / dm1q identification and firmware are reference values only. The running image reports its actual ABI, build fingerprint and security state. Android Emulator does not provide Samsung One UI, physical Snapdragon/Adreno hardware, Knox or Samsung hardware-backed attestation. Editing properties alone cannot add these capabilities.

## Run

Open Actions → Android 15 emulator → Run workflow, or push changes to the repository. The workflow boots the emulator, checks API 35, and exports real system properties and a screenshot as a temporary artifact. GitHub-hosted runners stop the emulator at the end; this is not a persistent interactive phone.

The AVD uses SDK-provided system images; no Samsung proprietary image is bundled. RAM is set to 4096 MB and CPU to 4 virtual cores for CI. The screen profile is in `config.ini`.
