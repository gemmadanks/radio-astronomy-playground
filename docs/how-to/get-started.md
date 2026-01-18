# How to get started with Radio Astronomy Playground

This guide shows you how to install `starbox`, the core python library of Radio Astronomy Playground, and its dependencies and run the get started notebook, which will demonstrate how to run an experiment in radio astronomy data processing.

## Pre-requisites
1. git
2. uv

## Steps
1. Clone this repository:
   ```bash
    git clone git@github.com:gemmadanks/radio-astronomy-playground.git
   ```
2. Install starbox and its dependencies using uv:
   ```bash
   uv sync
   ```
3. Run the `get-started.py` notebook to conduct your first experiment:
   ```bash
   uv run marimo run notebooks/get-started.py
   ```
