# Python Log Cleanup & Analysis Tool

A Python-based log management tool that analyzes log files and safely removes logs older than a configurable age.

## Features

- Discovers `.log` files automatically
- Analyzes INFO, WARNING, and ERROR entries
- Calculates file age using modification time
- Configurable cleanup age
- Safe `--dry-run` mode
- `--clean` mode for actual deletion
- Handles invalid command-line input
- Handles missing log directories
- Handles empty log directories
- Provides a cleanup and analysis summary

## Usage

Run in dry-run mode:

```bash
python log_cleanup.py