# FocusTokens

FocusTokens is a token-based attention and check-in system. Users receive daily tokens and spend them to send "pings" (normal or urgent). Tokens reset daily and all actions are recorded for history.

## Description
FocusTokens is a command-line application written in Python that manages user focus tokens.
Users can send pings to each other, view token balances, and manage daily token usage.
The application uses a layered architecture with controllers, models, and a persistent SQLite database.

## Features
- User creation and selection
- Daily token balance with automatic refresh
- Send normal and urgent pings with token costs
- View and delete ping history
- Change system settings (token limits and costs)
- Persistent storage using SQLite

## Project Structure
- `src/core` - business logic (tokens, pings)
- `src/data` - SQLite + repositories
- `src/cli` - CLI interface
- `src/web` - Flask web UI (later)
- `diagrams` - UML/DFD exports
- `tests` - unit/integration tests

## How to Run
1. Ensure Python 3.10+ is installed
2. Navigate to the project root directory
3. Run the application:

```bash
python -m src.cli.main