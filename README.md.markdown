# Sheet Metal Client Hub

![Python](https://img.shields.io/badge/python-3.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A **Python-based Tkinter GUI application** for automating cost calculations for sheet metal parts, developed as part of the **PDSWD7 PDA in Software Development Level 7** at Fife College, Semester 1, 2024/25, using a Waterfall SDLC.

---

## 🚀 Overview

The **Sheet Metal Client Hub** streamlines manual quoting processes for UK sheet metal fabricators. It automates cost calculations for single parts and assemblies, delivering precision and usability for end users in the fabrication industry.

**Key Features**:
- 🔒 **Secure Login**: User authentication with username and password stored in `data/users.txt`.
- 📝 **Part Input**: Specifications including material thickness (1, 1.2, 1.5, 2, 2.5, 3 mm), lay-flat dimensions (50–3000 mm length, 50–1500 mm width), and bends (0–20).
- 💸 **Cost Output**: Calculates costs across 10 work centres: **cutting**, **bending**, **welding**, **deburring**, **assembly**, **inspection**, **surface treatment**, **machining**, **forming**, and **fastening**, with zero default rates.
- ⚙️ **Settings**: Adjusts material and labour rates, saved to `data/rates_global.txt`.
- 💾 **File Storage**: Saves user credentials, rates, and calculation results to text files.

The project is hosted at [github.com/LJMoffat81/Sheet-Metal-Client-Hub](https://github.com/LJMoffat81/Sheet-Metal-Client-Hub).

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
4. **Install Dependencies** (if any):
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Application**:
   ```bash
   python src/main.py
   ```

<details>
<summary>🔍 Detailed Setup (click to expand)</summary>

- **Requirements**: Windows 10, 4GB RAM, 500MB disk space.
- **Environment**: Python 3.9 with Tkinter (standard library).
- **Troubleshooting**: Use `python3` if `python` fails; ensure Python is in PATH.
- **IDE**: PyScripter recommended, or any Python IDE.

</details>

---

## 🗂 Repository Structure

| Path | Description |
|------|-------------|
| **`src/`** | Source code |
| `src/main.py` | Application entry point |
| `src/gui.py` | GUI logic for login, input, output, and settings |
| `src/calculator.py` | Cost calculation logic |
| `src/file_handler.py` | File I/O for user data and rates |
| `src/tests/` | Unit tests (`test_calculator.py`, `test_gui.py`) |
| **`data/`** | Data files |
| `data/users.txt` | Stores usernames and passwords |
| `data/rates_global.txt` | Global cost rates for work centres |
| `data/output.txt` | Stores calculation results |
| **`docs/`** | Documentation and diagrams |
| `docs/diagrams/` | Visual Paradigm PNGs (e.g., Gantt chart, UML, wireframes) |
| `docs/Sheet_Metal_Client_Hub_Project_Proposal.pdf` | Project objectives and justification |
| `docs/Sheet_Metal_Client_Hub_Project_Charter.pdf` | Scope, stakeholders, and deliverables |
| `docs/Sheet_Metal_Client_Hub_Development_Plan.pdf` | Waterfall SDLC timeline and tasks |
| `docs/Sheet_Metal_Client_Hub_Design_Document.pdf` | Wireframes, UML diagrams, Data Dictionary, pseudocode |
| `docs/Sheet_Metal_Client_Hub_Test_Plan.docx` | Testing strategy |
| `docs/Sheet_Metal_Client_Hub_Test_Logs.docx` | Test results |
| **`.gitignore`** | Excludes temporary and sensitive files |
| **`LICENSE`** | MIT License |
| **`requirements.txt`** | Python dependencies |
| **`README.md`** | Project overview |

---

## 📚 Documentation

Key deliverables, in the `docs/` folder, are prepared for submission via the Fife College portal by **20 May 2025** in creation order:

- **[Project Proposal](docs/Sheet_Metal_Client_Hub_Project_Proposal.pdf)**: Defines project objectives and scope.
- **[Project Charter](docs/Sheet_Metal_Client_Hub_Project_Charter.pdf)**: Outlines scope, stakeholders, and deliverables.
- **[Development Plan](docs/Sheet_Metal_Client_Hub_Development_Plan.pdf)**: Details Waterfall SDLC timeline and tasks.
- **[Design Document](docs/Sheet_Metal_Client_Hub_Design_Document.pdf)**: Includes wireframes, UML diagrams, Data Dictionary table, and pseudocode.
- **[Test Plan](docs/Sheet_Metal_Client_Hub_Test_Plan.docx)**: Outlines testing strategy.
- **[Test Logs](docs/Sheet_Metal_Client_Hub_Test_Logs.docx)**: Records test results.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Fife College**: For providing the academic framework and resources.
- **Grok**: AI tool by xAI, used to refine documentation and code under the author’s direction.
- **Visual Paradigm**: For creating diagrams.

---

*Developed by Laurie Moffat for PDSWD7, Fife College, 2024/25.*