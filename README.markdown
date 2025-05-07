# Sheet Metal Client Hub

**A Python-based Tkinter GUI application** for automating cost calculations for sheet metal parts, developed as part of the **PDSWD7 PDA in Software Development Level 7** at Fife College, Semester 1, 2024/25, using a Waterfall SDLC.

---

## 🚀 Overview

The **Sheet Metal Client Hub** streamlines manual quoting processes for UK sheet metal fabricators, designed for assessor Jacqueline Bijster and hypothetical end users (fabricators). Key features include:

- **Secure Login**: User authentication with username and password.
- **Part Input**: Supports part specifications, including material thickness (1, 1.2, 1.5, 2, 2.5, 3 mm), lay-flat dimensions (50–3000 mm length, 50–1500 mm width), and bends (0–20).
- **Cost Output**: Calculates costs across 10 work centres: cutting, bending, welding, deburring, assembly, inspection, surface treatment, machining, forming, and fastening.
- **Settings**: Adjusts cost rates for flexibility.
- **File Storage**: Saves user credentials, rates, and output results.

The project is hosted at [github.com/LJMoffat81/Sheet-Metal-Client-Hub](https://github.com/LJMoffat81/Sheet-Metal-Client-Hub). Diagrams are work in progress and will be embedded in the Design Document by 20 May 2025.

---

## 📋 Setup Instructions

To run the **Sheet Metal Client Hub** locally, follow these steps:

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
4. **Run the Application**:
   ```bash
   python src/main.py
   ```

---

## 🗂 Repository Structure

The repository is organized as follows:

- **`src/`**: Source code
  - `main.py`: Application entry point
  - `gui.py`: GUI logic for login, input, output, and settings screens
  - `calculator.py`: Cost calculation logic
  - `file_handler.py`: File I/O for user data and rates
  - `tests/`: Unit tests
    - `test_calculator.py`
    - `test_gui.py`
- **`data/`**: Data files
  - `users.txt`: Stores usernames and passwords
  - `rates_global.txt`: Global cost rates for work centres
  - `output.txt`: Stores calculation results
- **`docs/`**: Documentation and diagrams
  - `diagrams/`: Visual Paradigm PNGs (e.g., Gantt chart, wireframes, UML diagrams)
  - `Sheet_Metal_Client_Hub_Project_Proposal.pdf`
  - `Sheet_Metal_Client_Hub_Development_Plan.pdf`
  - `Sheet_Metal_Client_Hub_Project_Charter.pdf`
  - `Sheet_Metal_Client_Hub_Design_Document.pdf`: Includes Data Dictionary table and pseudocode
  - `Sheet_Metal_Client_Hub_Test_Plan.docx`
  - `Sheet_Metal_Client_Hub_Test_Logs.docx`
- **`.gitignore`**: Excludes temporary and sensitive files
- **`LICENSE`**: MIT License
- **`requirements.txt`**: Python dependencies
- **`README.md`**: Project overview
- **`verify_repo.sh`**: Script for repository verification (untracked)

---

## 📚 Documentation

Key project documents are located in the `docs/` folder, due for submission via the Fife College portal by 20 May 2025:

- **[Project Proposal](docs/Sheet_Metal_Client_Hub_Project_Proposal.pdf)**: Outlines project objectives and justification.
- **[Development Plan](docs/Sheet_Metal_Client_Hub_Development_Plan.pdf)**: Details the Waterfall SDLC timeline and tasks.
- **[Project Charter](docs/Sheet_Metal_Client_Hub_Project_Charter.pdf)**: Defines scope, stakeholders, and deliverables.
- **[Design Document](docs/Sheet_Metal_Client_Hub_Design_Document.pdf)**: Includes wireframes, UML diagrams, Data Dictionary table, and pseudocode.
- **[Test Plan](docs/Sheet_Metal_Client_Hub_Test_Plan.docx)**: Outlines testing strategy.
- **[Test Logs](docs/Sheet_Metal_Client_Hub_Test_Logs.docx)**: Records test results.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

---

*This README was refined with assistance from Grok, an AI tool developed by xAI, under the author’s direction.*