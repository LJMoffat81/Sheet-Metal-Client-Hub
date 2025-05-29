# Sheet Metal Client Hub

![Python](https://img.shields.io/badge/python-3.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python-based Tkinter GUI application for automating cost calculations for sheet metal parts, developed for the PDSWD7 PDA in Software Development Level 7 at Fife College, Semester 1, 2024/25, using a Waterfall SDLC.

---

## 🚀 Overview

The **Sheet Metal Client Hub** streamlines manual quoting processes for UK sheet metal fabricators. It automates cost calculations for single parts and assemblies, delivering precision and usability for end users in the fabrication industry.

**Key Features**:
- 🔒 **FR1: Login**: Authenticates users with username and password stored in `data/users.json` (e.g., `laurie:moffat123`).
- 📝 **FR2: Part Input**: Specifies material (steel/aluminum), thickness (1, 1.2, 1.5, 2, 2.5, 3 mm), lay-flat dimensions (50–3000 mm length, 50–1500 mm width), and quantity.
- 💸 **FR3–FR4: Cost Calculation and Display**: Calculates costs across 10 work centres (cutting, bending, welding, deburring, assembly, inspection, surface treatment, machining, forming, fastening) using `data/rates.json`, displaying in GBP.
- 💾 **FR5: Store Output**: Saves cost calculations to `data/output.txt`.
- 📈 **FR7: Generate Quote**: Creates quotes with customer details and profit margins, saved to `data/quotes.txt`.
- ⚙️ **FR6: Settings**: Admins adjust material and labour rates, saved to `data/rates.json`.

Hosted at [github.com/LJMoffat81/Sheet-Metal-Client-Hub](https://github.com/LJMoffat81/Sheet-Metal-Client-Hub).

---

## 📋 Setup Instructions

To run the **Sheet Metal Client Hub** locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LJMoffat81/Sheet-Metal-Client-Hub.git
   ```
2. **Ensure Python 3.9 is Installed**:
   - Verify with:
     ```bash
     python --version
     ```
3. **Navigate to the Project Directory**:
   ```bash
   cd Sheet-Metal-Client-Hub
   ```
4. **Install Dependencies**:
   - Install `mock` for unit tests:
     ```bash
     pip install -r requirements.txt
     ```
5. **Run the Application**:
   ```bash
   python src/main.py
   ```

### Testing

To verify the application’s functionality, automated test scripts are provided for GUI, cost, file I/O, and unit tests, with results logged in `test_logs/Test_Log.docx`.

1. **Run Automated GUI, Cost, and File I/O Tests**:
   - Executes `TC-GUI-02` to `TC-GUI-10`, `TC-COST-01` to `TC-COST-05`, `TC-FIO-002` to `TC-FIO-005`:
     ```bash
     python src/automate_test_log_ui.py
     ```
2. **Run Unit and Log-Based Tests**:
   - Executes `TC-UNIT-01` to `TC-UNIT-04`, `TC-GUI-01`, `TC-FIO-001`:
     ```bash
     python src/generate_test_log.py
     ```
3. **View Test Results**:
   - Open `test_logs/Test_Log.docx` for detailed test outcomes.
   - Logs: `test_logs/gui_test_log_ui.log`, `test_logs/test_log_generation.log`.
4. **Test Plan**:
   - See `docs/documents/#5_Sheet_Metal_Client_Hub_Test_Plan.pdf` for the testing strategy and `docs/documents/#7_Sheet_Metal_Client_Hub_Test_Log.pdf` for results.

<details>
<summary>🔍 Detailed Setup</summary>

- **Requirements**: Windows 10, 4GB RAM, 500MB disk space.
- **Environment**: Python 3.9 with Tkinter (standard library).
- **Dependencies**: `mock` for unit tests (`pip install mock`).
- **Troubleshooting**: Use `python3` if `python` fails; ensure Python is in PATH.
- **IDE**: PyScripter recommended, or any Python IDE.
- **Testing**: Run unit tests with:
  ```bash
  python -m unittest discover src/tests
  ```

</details>

---

## 🗂 Repository Structure

| Path | Description |
|------|-------------|
| `src/` | Source code |
| `src/main.py` | Application entry point |
| `src/gui.py` | GUI logic for login, part input, cost output, settings (FR1, FR2, FR4, FR6, FR7) |
| `src/calculator.py` | Cost calculation logic (FR3–FR4) |
| `src/file_handler.py` | File I/O for user data, rates, outputs, quotes (FR1, FR5, FR6, FR7) |
| `src/logic.py` | Business logic for part processing |
| `src/logging_config.py` | Logging configuration |
| `src/logger.py` | Logger setup |
| `src/utils.py` | Utility functions |
| `src/automate_test_log_ui.py` | Automated tests for GUI, cost, and file I/O (TC-GUI-02–10, TC-COST-01–05, TC-FIO-002–005) |
| `src/generate_test_log.py` | Automated unit and log-based tests (TC-UNIT-01–04, TC-GUI-01, TC-FIO-001) |
| `src/tests/` | Unit tests (`test_calculator.py`, `test_gui.py`, `test_logic.py`, `test_utils.py`) |
| `data/` | Data files |
| `data/users.json` | User credentials |
| `data/rates.json` | Cost rates (material, labour, 10 work centres) |
| `data/output.txt` | Cost calculation results |
| `data/quotes.txt` | Generated quotes |
| `data/parts_catalogue.txt` | Fastener catalogue |
| `data/test_cases.json` | Test case definitions |
| `data/key.key` | Encryption key |
| `data/log/` | Application logs (`calculator.log`, `file_handler.log`, etc.) |
| `docs/` | Documentation |
| `docs/documents/` | Project deliverables |
| `docs/documents/#1_Project_Proposal.pdf` | Project objectives |
| `docs/documents/#2_Project_Charter.pdf` | Scope and deliverables |
| `docs/documents/#3_Development_Plan.pdf` | SDLC timeline and tasks |
| `docs/documents/#4_Design_Document.pdf` | Wireframes, UML, Data Dictionary, pseudocode |
| `docs/documents/#5_Sheet_Metal_Client_Hub_Test_Plan.pdf` | Testing strategy |
| `docs/documents/#6_Sheet_Metal_Client_Hub_Test_Case_Document.pdf` | Test case definitions |
| `docs/documents/#7_Sheet_Metal_Client_Hub_Test_Log.pdf` | Test results |
| `docs/documents/Test_Cases.xlsx` | Test case spreadsheet |
| `docs/diagrams/` | UML and process diagrams (`#1_Gantt_Chart.png` to `#9_State_Diagram.png`) |
| `docs/wireframes/` | UI wireframes (`#1_Login_Screen.png` to `#4_Settings_Screen.png`) |
| `docs/images/` | Additional images (`laser_gear.png`, `laser_gear.ico`) |
| `docs/pseudocode.txt` | Pseudocode for FR1–FR7 implementation |
| `test_logs/` | Test result logs |
| `test_logs/Test_Log.docx` | Detailed test results for all test cases |
| `test_logs/gui_test_log_ui.log` | Log for automated GUI, cost, and file I/O tests |
| `test_logs/test_log_generation.log` | Log for unit and log-based tests |
| `test_logs/screenshots/` | Test screenshots (`1.png`, `Add Parts from Database.png`, etc.) |
| `.github/workflows/` | GitHub Actions workflows (`python-package-conda.yml`) |
| `.gitignore` | Excludes temporary files (e.g., `__pycache__/`, `*.pyc`) |
| `LICENSE` | MIT License |
| `requirements.txt` | Python dependencies |
| `verify_repo.sh` | Repository verification script |
| `README.md` | Project overview |

## 🔄 Recent Changes
- **29 May 2025**:
  - Added `src/automate_test_log_ui.py` to automate GUI (`TC-GUI-02` to `TC-GUI-10`), cost (`TC-COST-01` to `TC-COST-05`), and file I/O (`TC-FIO-002` to `TC-FIO-005`) tests, resolving `Part ID or Revision missing` errors (commit TBD).
  - Updated `src/generate_test_log.py` to pass unit and log-based tests (`TC-UNIT-01` to `TC-UNIT-04`, `TC-GUI-01`, `TC-FIO-001`), with results in `test_logs/Test_Log.docx`.
  - Updated `test_logs/Test_Log.docx` with passing results for automated tests and manual verification of cost and file I/O tests.
  - Added test logs (`test_logs/gui_test_log_ui.log`, `test_logs/test_log_generation.log`) and screenshots (`test_logs/screenshots/`).
  - Updated `README.md` to reflect accurate repository structure, testing instructions, and documentation paths.
- **19 May 2025**:
  - Updated `.py` files in `src/` and `src/tests/` with detailed `#` comments for FR1–FR7, improving clarity for submission (commit `3cb7e2e`).
  - Fixed `.gitignore` to ensure `data/rates_global.txt` syncs to GitHub (commit `01ea058`).
  - Moved wireframes to `docs/wireframes/` from `docs/diagrams/wireframes/` for better organization.
  - Removed erroneous `docs/pseudocode.txt.txt`.
  - Added `docs/pseudocode.txt` for FR1–FR7 pseudocode.
  - Updated `docs/documents/#4_Design_Document.pdf` to reference `docs/wireframes/`.

---

## 📚 Documentation

Key deliverables in the `docs/documents/` folder, prepared for submission via the Fife College portal by 31 May 2025, in creation order:

- **[#1 Project Proposal](docs/documents/#1_Project_Proposal.pdf)**: Defines objectives and scope.
- **[#2 Project Charter](docs/documents/#2_Project_Charter.pdf)**: Outlines scope and deliverables.
- **[#3 Development Plan](docs/documents/#3_Development_Plan.pdf)**: Details SDLC timeline and tasks.
- **[#4 Design Document](docs/documents/#4_Design_Document.pdf)**: Includes wireframes, UML diagrams, Data Dictionary, and pseudocode.
- **[#5 Sheet Metal Client Hub Test Plan](docs/documents/#5_Sheet_Metal_Client_Hub_Test_Plan.pdf)**: Testing strategy.
- **[#6 Sheet Metal Client Hub Test Case Document](docs/documents/#6_Sheet_Metal_Client_Hub_Test_Case_Document.pdf)**: Test case definitions.
- **[#7 Sheet Metal Client Hub Test Log](docs/documents/#7_Sheet_Metal_Client_Hub_Test_Log.pdf)**: Test results.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Fife College**: For the academic framework and resources.
- **Grok**: AI tool by xAI, used to refine documentation and code.
- **Visual Paradigm**: For creating diagrams.

---

*Developed by Laurie Moffat for PDSWD7, Fife College, 2024/25.*