# Sheet Metal Client Hub

**A Python-based Tkinter GUI application** for automating cost calculations for sheet metal parts, developed as part of the **PDSWD7 PDA in Software Development Level 7* at Fife College, Semester 1, 2024/25, using a Waterfall SDLC.

---

## 🚀 Overview

The **Sheet Metal Client Hub** streamlines manual quoting processes for UK sheet metal fabricators. Key features include:

- **Secure Login**: User authentication with username and password.
- **Part Input**: Supports part specifications, including material thickness (1, 1.2, 1.5, 2, 2.5, 3 mm), lay-flat dimensions (50-3000 mm length, 50-1500 mm width), and bends (0-20).
- **Cost Output**: Calculates costs across 10 real-world work centres (cutting, bending, welding, deburring, assembly, inspection, surface treatment, machining, forming, fastening).
- **Settings**: Adjusts cost rates for flexibility.
- **File Storage**: Saves user credentials, rates, and output results.

The project is hosted at [github.com/LJMoffat81/Sheet-Metal-Client-Hub](https://github.com/LJMoffat81/Sheet-Metal-Client-Hub).

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
  - `Project_Proposal_Sheet_Metal_Client_Hub_Rev1.pdf`
  - `Sheet_Metal_Client_Hub_Development_Plan.docx`
  - `Sheet_Metal_Client_Hub_Project_Charter.pdf`
  - `Sheet_Metal_Client_Hub_Design_Document.docx`
  - `Sheet_Metal_Client_Hub_Test_Plan.docx`
  - `Sheet_Metal_Client_Hub_Test_Logs.docx`
- **`.gitignore`**: Excludes temporary and sensitive files
- **`LICENSE`**: MIT License
- **`requirements.txt`**: Python dependencies
- **`README.md`**: Project overview

---

## 📚 Documentation

Key project documents are located in the `docs/` folder:

- **[Project Proposal](docs/Project_Proposal_Sheet_Metal_Client_Hub_Rev1.pdf)**: Outlines project objectives and justification.
- **[Development Plan](docs/Sheet_Metal_Client_Hub_Development_Plan.docx)**: Details the Waterfall SDLC timeline and tasks.
- **[Project Charter](docs/Sheet_Metal_Client_Hub_Project_Charter.pdf)**: Defines scope, stakeholders, and deliverables.
- **[Design Document](docs/Sheet_Metal_Client_Hub_Design_Document.docx)**: Includes wireframes, UML diagrams, and data dictionary.
- **[Test Plan](docs/Sheet_Metal_Client_Hub_Test_Plan.docx)**: Outlines testing strategy.
- **[Test Logs](docs/Sheet_Metal_Client_Hub_Test_Logs.docx)**: Records test results.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.

---

*This README was refined with assistance from Grok, an AI tool developed by xAI, under the author’s direction.*
