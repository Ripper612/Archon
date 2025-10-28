@echo off
REM bd-docker.bat - Convenience batch script to run beads (bd) commands in Docker
REM Usage: .\bd-docker.bat <command> [args...]

docker run --rm -v "%cd%:/workspace" -v "%USERPROFILE%\.beads:/home/beads/.beads" -w /workspace beads %*
