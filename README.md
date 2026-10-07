# Fantasy Cricket Team Game

A fantasy cricket team management application built using Python, PySide6, Qt Designer, and SQLite.

## Project Overview

This application allows users to create and manage a fantasy cricket team within a 1,000-point budget.

Users can:

- Create a new fantasy cricket team
- Select players by category
- Add and remove players
- Build a team of up to 11 players
- Manage a 1,000-point player budget
- Save teams to an SQLite database
- Open previously saved teams
- Evaluate the team's fantasy score
- Calculate fantasy points based on player match performance

## Technologies Used

- Python
- PySide6
- Qt Designer
- SQLite

## Project Files

| File | Description |
|---|---|
| `main.py` | Main application and GUI logic |
| `setup_database.py` | Creates the SQLite database and tables |
| `insert_data.py` | Inserts player and match data |
| `fantasy_cricket.ui` | GUI designed using Qt Designer |

## How to Run

### 1. Install PySide6

```bash
pip install PySide6
