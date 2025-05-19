# Sheet Metal Client Hub

![Python](https://img.shields.io/badge/python-3.9-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A Python-based Tkinter GUI application for automating cost calculations for sheet metal parts, developed for the PDSWD7 PDA in Software Development Level 7 at Fife College, Semester 1, 2024/25, using a Waterfall SDLC.

---

## 🚀 Overview

The **Sheet Metal Client Hub** streamlines manual quoting processes for UK sheet metal fabricators. It automates cost calculations for single parts and assemblies, delivering precision and usability for end users in the fabrication industry.

**Key Features**:
- 🔒 **FR1: Login**: Authenticates users with username and password stored in \`data/users.txt\` (e.g., \`laurie:moffat123\`).
- 📝 **FR2: Part Input**: Specifies material (steel/aluminum), thickness (1, 1.2, 1.5, 2, 2.5, 3 mm), lay-flat dimensions (50–3000 mm length, 50–1500 mm width), and quantity.
- 💸 **FR3–FR4: Cost Calculation and Display**: Calculates costs across 10 work centres (cutting, bending, welding, deburring, assembly, inspection, surface treatment, machining, forming, fastening) using \`data/rates_global.txt\`, displaying in GBP.
- 💾 **FR5: Store Output**: Saves cost calculations to \`data/output.txt\`.
- 📈 **FR7: Generate Quote**: Creates quotes with customer details and profit margins, saved to \`data/quotes.txt\`.
- ⚙️ **FR6: Settings**: Admins adjust material and labour rates, saved to \`data/rates_global.txt\`.

Hosted at [github.com/LJMoffat81/Sheet-Metal-Client-Hub](https://github.com/LJMoffat81/Sheet-Metal-Client-Hub).

---

## 📋 Setup Instructions

To run the **Sheet Metal Client Hub** locally:

1. **Clone the Repository**:
   \`\`\`bash
   git clone https://github.com/LJMoffat81/Sheet-Metal-Client-Hub.git
   \`\`\`
2. **Ensure Python 3.9 is Installed**:
   - Verify with:
     \`\`\`bash
     python --version
     \`\`\`
3. **Navigate to the Project Directory**:
   \`\`\`bash
   cd Sheet-Metal-Client-Hub
   \`\`\`
4. **Install Dependencies**:
   - Install \`mock\` for unit tests:
     \`\`\`bash
     pip install -r requirements.txt
     \`\`\`
5. **Run the Application**:
   \`\`\`bash
   python src/main.py
   \`\`\`

<details>
<summary>🔍 Detailed Setup</summary>

- **Requirements**: Windows 10, 4GB RAM, 500MB disk space.
- **Environment**: Python 3.9 with Tkinter (standard library).
- **Dependencies**: \`mock\` for unit tests (\`pip install mock\`).
- **Troubleshooting**: Use \`python3\` if \`python\` fails; ensure Python is in PATH.
- **IDE**: PyScripter recommended, or any Python IDE.
- **Testing**: Run unit tests with:
  \`\`\`bash
  python -m unittest discover src/tests
  \`\`\`

</details>

---

## 🗂 Repository Structure

| Path | Description |
|------|-------------|
| \`src/\` | Source code |
| \`src/main.py\` | Application entry point |
| \`src/gui.py\` | GUI logic for login, part input, cost output, settings (FR1, FR2, FR4, FR6, FR7) |
| \`src/calculator.py\` | Cost calculation logic (FR3–FR4) |
| \`src/file_handler.py\` | File I/O for user data, rates, outputs, quotes (FR1, FR5, FR6, FR7) |
| \`src/tests/\` | Unit tests (\`test_calculator.py\`, \`test_gui.py\`) |
| \`data/\` | Data files |
| \`data/users.txt\` | Usernames and passwords |
| \`data/rates_global.txt\` | Global cost rates (material, labour, 10 work centres) |
| \`data/output.txt\` | Cost calculation results |
| \`data/quotes.txt\` | Generated quotes |
| \`docs/\` | Documentation and diagrams |
| \`docs/pseudocode.txt\` | Pseudocode for FR1–FR7 implementation |
| \`docs/diagrams/\` | Visual Paradigm PNGs (e.g., Gantt chart, UML) |
| \`docs/wireframes/\` | UI wireframes (\`#1_Login_Screen.png\` to \`#4_Settings_Screen.png\`) |
| \`docs/#1_Project_Proposal.pdf\` | Project objectives |
| \`docs/#2_Project_Charter.pdf\` | Scope and deliverables |
| \`docs/#3_Development_Plan.pdf\` | SDLC timeline and tasks |
| \`docs/#4_Design_Document.pdf\` | Wireframes, UML, Data Dictionary, pseudocode |
| \`docs/#5_Test_Plan.docx\` | Testing strategy |
| \`docs/#6_Test_Logs.docx\` | Test results |
| \`.gitignore\` | Excludes temporary files (e.g., \`__pycache__/\`) |
| \`LICENSE\` | MIT License |
| \`requirements.txt\` | Python dependencies |
| \`verify_repo.sh\` | Repository verification script |
| \`README.md\` | Project overview |

## 🔄 Recent Changes
- **19 May 2025**:
  - Updated \`.py\` files in \`src/\` and \`src/tests/\` with detailed \`#\` comments for FR1–FR7, improving clarity for submission (commit \`3cb7e2e\`).
  - Fixed \`.gitignore\` to ensure \`data/rates_global.txt\` syncs to GitHub (commit \`01ea058\`).
  - Moved wireframes to \`docs/wireframes/\` from \`docs/diagrams/wireframes/\` for better organization.
  - Removed erroneous \`docs/pseudocode.txt.txt\`.
  - Added \`docs/pseudocode.txt\` for FR1–FR7 pseudocode.
  - Updated \`#4_Design_Document.pdf\` to reference \`docs/wireframes/\`.

---

## 📚 Documentation

Key deliverables in the \`docs/\` folder, prepared for submission via the Fife College portal by 20 May 2025, in creation order:

- **[#1 Project Proposal](docs/#1_Project_Proposal.pdf)**: Defines objectives and scope.
- **[#2 Project Charter](docs/#2_Project_Charter.pdf)**: Outlines scope and deliverables.
- **[#3 Development Plan](docs/#3_Development_Plan.pdf)**: Details SDLC timeline and tasks.
- **[#4 Design Document](docs/#4_Design_Document.pdf)**: Includes wireframes, UML diagrams, Data Dictionary, and pseudocode.
- **[#5 Test Plan](docs/#5_Test_Plan.docx)**: Outlines testing strategy.
- **[#6 Test Logs](docs/#6_Test_Logs.docx)**: Records test results.

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
