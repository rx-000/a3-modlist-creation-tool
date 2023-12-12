# Arma 3 Modlist Creation Tool

This web application, built using Flask (Python), simplifies the process of creating personalized Arma 3 modlists for users. By integrating a server's modlist and enabling users to select additional whitelisted mods, it generates a modlist for download.

## How It Works

1. **Server Modlist Integration:** The tool uses the server's modlist as its base.
2. **User Whitelist Selection:** Users can easily select additional whitelisted mods they wish to include.
3. **Compilation and Download:** The tool consolidates the selected mods and the server's modlist into a single modlist file, ready for download and import.

## How to Use

1. Add the following files to the main directory:
- `mandatory.html`: Base mods (e.g. server modlist)
- `whitelist.html`: Whitelisted mods (e.g. client-side mods)

2. Run via `app.py`; configure port as needed
