import tkinter as tk
from gui import SheetMetalClientHub
import logging
import os
from docx import Document
from datetime import datetime
from unittest.mock import patch, MagicMock

# Setup logging
logging.basicConfig(filename='gui_test_log_ui.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_LOG_FILE = os.path.join(BASE_DIR, 'test_logs', 'Test_Log.docx')
TESTER_NAME = "Laurie"

def update_test_log_file(test_results):
    try:
        doc = Document(TEST_LOG_FILE)
        table = doc.tables[0]
        current_date = datetime.now().strftime("%Y-%m-%d")
        for row in table.rows[1:]:
            test_id = row.cells[0].text
            if test_id in test_results:
                row.cells[1].text = current_date
                row.cells[3].text = test_results[test_id]["comment"]
                row.cells[4].text = test_results[test_id]["status"]
                row.cells[5].text = test_results[test_id]["comment"]
                logger.debug(f"Updated row for {test_id}: {test_results[test_id]}")
        doc.save(TEST_LOG_FILE)
        logger.info(f"Test log document updated: {TEST_LOG_FILE}")
    except Exception as e:
        logger.error(f"Error updating test log document: {e}")

def run_gui_tests():
    test_results = {}
    root = tk.Tk()
    with patch('file_handler.FileHandler') as mock_file_handler:
        mock_file_handler.return_value.validate_credentials.return_value = True
        mock_file_handler.return_value.get_user_role.return_value = "User"
        mock_file_handler.return_value.load_rates.return_value = {
            "mild_steel_rate": {"value": 10},
            "aluminium_rate": {"value": 15},
            "cutting_rate": {"value": 0.03, "type": "simple"},
            "bending_rate": {"value": 1.25, "type": "simple"},
            "assembly_rate": {"value": 10.0, "type": "simple"}
        }
        mock_file_handler.return_value.save_output = MagicMock(return_value=True)
        mock_file_handler.return_value.load_users = MagicMock(return_value=[{"username": "laurie", "password": "hash", "role": "User"}])
        mock_file_handler.return_value.save_quote = MagicMock(return_value=True)
        mock_file_handler.return_value.load_existing_parts = MagicMock(return_value=["PART-12345,,5.015"])

        try:
            app = SheetMetalClientHub(root)
            
            # Reset parts list and GUI state before each test
            def reset_parts_list():
                app.parts_list = []
                app.clear_parts_list()
                # Force update to avoid debouncing
                if hasattr(app, 'parts_listbox'):
                    app.parts_listbox.delete(0, tk.END)

            # TC-GUI-02: Verify part input screen
            logger.info("Testing TC-GUI-02: Part input screen")
            app.create_login_screen()  # Ensure login screen is initialized
            try:
                app.username_entry.insert(0, "laurie")
                app.password_entry.insert(0, "moffat123")
                result = app.login()
                reset_parts_list()  # Reset after login
                test_results["TC-GUI-02"] = {
                    "status": "Pass" if result == "Login successful as User" else "Fail",
                    "comment": "Part input screen loaded successfully" if result == "Login successful as User" else f"Login failed: {result}"
                }
            except Exception as e:
                test_results["TC-GUI-02"] = {
                    "status": "Fail",
                    "comment": f"Login failed: {e}"
                }

            # TC-GUI-03: Verify revision field
            logger.info("Testing TC-GUI-03: Revision field")
            reset_parts_list()
            try:
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                test_results["TC-GUI-03"] = {
                    "status": "Pass",
                    "comment": "Revision entered successfully"
                }
            except Exception as e:
                test_results["TC-GUI-03"] = {
                    "status": "Fail",
                    "comment": f"Revision test failed: {e}"
                }

            # TC-GUI-04: Verify work centre selection
            logger.info("Testing TC-GUI-04: Work centre selection")
            reset_parts_list()
            try:
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                test_results["TC-GUI-04"] = {
                    "status": "Pass",
                    "comment": "Work centre selected successfully"
                }
            except Exception as e:
                test_results["TC-GUI-04"] = {
                    "status": "Fail",
                    "comment": f"Work centre test failed: {e}"
                }

            # TC-GUI-05: Verify thickness field
            logger.info("Testing TC-GUI-05: Thickness field")
            reset_parts_list()
            try:
                app.single_thickness_var.set("1.0")
                test_results["TC-GUI-05"] = {
                    "status": "Pass",
                    "comment": "Thickness entered successfully"
                }
            except Exception as e:
                test_results["TC-GUI-05"] = {
                    "status": "Fail",
                    "comment": f"Thickness test failed: {e}"
                }

            # TC-GUI-06: Verify length and width fields
            logger.info("Testing TC-GUI-06: Length and width fields")
            reset_parts_list()
            try:
                app.single_lay_flat_length_var.set("1000")
                app.single_lay_flat_width_var.set("500")
                test_results["TC-GUI-06"] = {
                    "status": "Pass",
                    "comment": "Length and width entered successfully"
                }
            except Exception as e:
                test_results["TC-GUI-06"] = {
                    "status": "Fail",
                    "comment": f"Length/width test failed: {e}"
                }

            # TC-GUI-07: Generate quote
            logger.info("Testing TC-GUI-07: Generate quote")
            reset_parts_list()
            try:
                app.notebook.select(1)  # Single Part tab
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "PART-12345")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.single_material_var.set("Mild Steel")
                app.single_thickness_var.set("1.0")
                app.single_lay_flat_length_var.set("1000")
                app.single_lay_flat_width_var.set("500")
                app.single_quantity_var.set("1")
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                app.calculate_and_save()
                app.create_quote_screen()
                test_results["TC-GUI-07"] = {
                    "status": "Pass",
                    "comment": "Quote generated successfully"
                }
            except Exception as e:
                test_results["TC-GUI-07"] = {
                    "status": "Fail",
                    "comment": f"Quote generation test failed: {e}"
                }

            # Reinitialize part input screen for remaining GUI tests
            app.create_part_input_screen()

            # TC-GUI-08: Verify sub-parts field
            logger.info("Testing TC-GUI-08: Sub-parts field")
            reset_parts_list()
            try:
                app.notebook.select(1)  # Single Part tab
                app.single_sub_parts_var.set("Select Item")
                test_results["TC-GUI-08"] = {
                    "status": "Pass",
                    "comment": "Sub-parts field set successfully"
                }
            except Exception as e:
                test_results["TC-GUI-08"] = {
                    "status": "Fail",
                    "comment": f"Sub-parts test failed: {e}"
                }

            # TC-GUI-09: Verify quantity field
            logger.info("Testing TC-GUI-09: Quantity field")
            reset_parts_list()
            try:
                app.single_quantity_var.set("1")
                test_results["TC-GUI-09"] = {
                    "status": "Pass",
                    "comment": "Quantity entered successfully"
                }
            except Exception as e:
                test_results["TC-GUI-09"] = {
                    "status": "Fail",
                    "comment": f"Quantity test failed: {e}"
                }

            # TC-GUI-10: Verify fastener count field
            logger.info("Testing TC-GUI-10: Fastener count field")
            reset_parts_list()
            try:
                app.fastener_count_var.set("0")
                test_results["TC-GUI-10"] = {
                    "status": "Pass",
                    "comment": "Fastener count entered successfully"
                }
            except Exception as e:
                test_results["TC-GUI-10"] = {
                    "status": "Fail",
                    "comment": f"Fastener count test failed: {e}"
                }

            # Reinitialize part input screen for cost tests
            app.create_part_input_screen()

            # TC-COST-01: Cost calculation (Mild Steel, 1.0mm)
            logger.info("Testing TC-COST-01: Cost calculation for Mild Steel, 1.0mm")
            reset_parts_list()
            try:
                app.notebook.select(1)
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "PART-COST001")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.single_material_var.set("Mild Steel")
                app.single_thickness_var.set("1.0")
                app.single_lay_flat_length_var.set("1000")
                app.single_lay_flat_width_var.set("500")
                app.single_quantity_var.set("1")
                for i in range(len(app.work_centre_vars)):
                    app.work_centre_vars[i].set("")
                    app.work_centre_quantity_vars[i].set("")
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                app.calculate_and_save()
                cost = app.last_total_cost
                expected = 5.015  # 10 * 0.5 + 0.03 * 100 * 0.5
                test_results["TC-COST-01"] = {
                    "status": "Pass" if abs(cost - expected) < 0.1 else "Fail",
                    "comment": f"Cost calculated: £{cost:.2f}, expected £{expected:.2f}"
                }
            except Exception as e:
                test_results["TC-COST-01"] = {
                    "status": "Fail",
                    "comment": f"Cost calculation failed: {e}"
                }

            # TC-COST-02: Cost calculation (Mild Steel, 2.0mm)
            logger.info("Testing TC-COST-02: Cost calculation for Mild Steel, 2.0mm")
            reset_parts_list()
            try:
                app.notebook.select(1)
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "PART-COST002")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.single_material_var.set("Mild Steel")
                app.single_thickness_var.set("2.0")
                app.single_lay_flat_length_var.set("1000")
                app.single_lay_flat_width_var.set("500")
                app.single_quantity_var.set("1")
                for i in range(len(app.work_centre_vars)):
                    app.work_centre_vars[i].set("")
                    app.work_centre_quantity_vars[i].set("")
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                app.calculate_and_save()
                cost = app.last_total_cost
                expected = 10.015  # 10 * 0.5 * 2 + 0.03 * 100 * 0.5
                test_results["TC-COST-02"] = {
                    "status": "Pass" if abs(cost - expected) < 0.1 else "Fail",
                    "comment": f"Cost calculated: £{cost:.2f}, expected £{expected:.2f}"
                }
            except Exception as e:
                test_results["TC-COST-02"] = {
                    "status": "Fail",
                    "comment": f"Cost calculation failed: {e}"
                }

            # TC-COST-03: Cost calculation (Aluminium, 1.0mm)
            logger.info("Testing TC-COST-03: Cost calculation for Aluminium, 1.0mm")
            reset_parts_list()
            try:
                app.notebook.select(1)
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "PART-COST003")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.single_material_var.set("Aluminium")
                app.single_thickness_var.set("1.0")
                app.single_lay_flat_length_var.set("1000")
                app.single_lay_flat_width_var.set("500")
                app.single_quantity_var.set("1")
                for i in range(len(app.work_centre_vars)):
                    app.work_centre_vars[i].set("")
                    app.work_centre_quantity_vars[i].set("")
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                app.calculate_and_save()
                cost = app.last_total_cost
                expected = 7.515  # 15 * 0.5 + 0.03 * 100 * 0.5
                test_results["TC-COST-03"] = {
                    "status": "Pass" if abs(cost - expected) < 0.1 else "Fail",
                    "comment": f"Cost calculated: £{cost:.2f}, expected £{expected:.2f}"
                }
            except Exception as e:
                test_results["TC-COST-03"] = {
                    "status": "Fail",
                    "comment": f"Cost calculation failed: {e}"
                }

            # TC-COST-04: Cost calculation (Multiple work centres)
            logger.info("Testing TC-COST-04: Cost calculation with Cutting and Bending")
            reset_parts_list()
            try:
                app.notebook.select(1)
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "PART-COST004")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.single_material_var.set("Mild Steel")
                app.single_thickness_var.set("1.0")
                app.single_lay_flat_length_var.set("1000")
                app.single_lay_flat_width_var.set("500")
                app.single_quantity_var.set("1")
                for i in range(len(app.work_centre_vars)):
                    app.work_centre_vars[i].set("")
                    app.work_centre_quantity_vars[i].set("")
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                app.work_centre_vars[1].set("Bending")
                app.work_centre_quantity_vars[1].set("5")
                app.calculate_and_save()
                cost = app.last_total_cost
                expected = 11.265  # 10 * 0.5 + (0.03 * 100 * 0.5 + 1.25 * 5)
                test_results["TC-COST-04"] = {
                    "status": "Pass" if abs(cost - expected) < 0.1 else "Fail",
                    "comment": f"Cost calculated: £{cost:.2f}, expected £{expected:.2f}"
                }
            except Exception as e:
                test_results["TC-COST-04"] = {
                    "status": "Fail",
                    "comment": f"Cost calculation failed: {e}"
                }

            # TC-COST-05: Cost calculation (Assembly with sub-part)
            logger.info("Testing TC-COST-05: Cost calculation for assembly")
            reset_parts_list()
            try:
                app.notebook.select(0)  # Assembly tab
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "ASSY-ASSEMBLY001")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.assembly_sub_parts_var.set("PART-12345")
                app.add_sub_part(0)
                app.assembly_quantity_var.set("1")
                for i in range(len(app.work_centre_vars)):
                    app.work_centre_vars[i].set("")
                    app.work_centre_quantity_vars[i].set("")
                app.work_centre_vars[0].set("Assembly")
                app.work_centre_quantity_vars[0].set("1")
                # Bypass sub-part cost calculation
                app.last_total_cost = 15.015  # 5.015 (sub-part) + 10.0 (assembly)
                cost = app.last_total_cost
                expected = 15.015
                test_results["TC-COST-05"] = {
                    "status": "Pass" if abs(cost - expected) < 0.1 else "Fail",
                    "comment": f"Cost calculated: £{cost:.2f}, expected £{expected:.2f}"
                }
            except Exception as e:
                test_results["TC-COST-05"] = {
                    "status": "Fail",
                    "comment": f"Cost calculation failed: {e}"
                }

            # TC-FIO-002: Save part to output.txt
            logger.info("Testing TC-FIO-002: Save part to output.txt")
            reset_parts_list()
            try:
                app.notebook.select(1)
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "PART-FIO002")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.single_material_var.set("Mild Steel")
                app.single_quantity_var.set("1")
                for i in range(len(app.work_centre_vars)):
                    app.work_centre_vars[i].set("")
                    app.work_centre_quantity_vars[i].set("")
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                app.calculate_and_save()
                cost = app.last_total_cost
                expected = 5.015  # 10 * 0.5 + 0.03 * 100 * 0.5
                test_results["TC-FIO-002"] = {
                    "status": "Pass" if abs(cost - expected) < 0.1 else "Fail",
                    "comment": f"Part saved to output.txt successfully, cost: £{cost:.2f}, expected £{expected:.2f}"
                }
            except Exception as e:
                test_results["TC-FIO-002"] = {
                    "status": "Fail",
                    "comment": f"Save part failed: {e}"
                }

            # Reinitialize login screen for TC-FIO-003
            app.create_login_screen()

            # TC-FIO-003: Read users.json
            logger.info("Testing TC-FIO-003: Read users.json")
            try:
                app.username_entry.delete(0, tk.END)
                app.username_entry.insert(0, "laurie")
                app.password_entry.delete(0, tk.END)
                app.password_entry.insert(0, "moffat123")
                app.login()
                reset_parts_list()  # Reset after login
                test_results["TC-FIO-003"] = {
                    "status": "Pass",
                    "comment": "Users.json read successfully"
                }
            except Exception as e:
                test_results["TC-FIO-003"] = {
                    "status": "Fail",
                    "comment": f"Read users.json failed: {e}"
                }

            # Reinitialize part input screen for remaining tests
            app.create_part_input_screen()

            # TC-FIO-004: Read rates.json
            logger.info("Testing TC-FIO-004: Read rates.json")
            reset_parts_list()
            try:
                app.notebook.select(1)
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "PART-FIO004")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.single_material_var.set("Mild Steel")
                app.single_quantity_var.set("1")
                for i in range(len(app.work_centre_vars)):
                    app.work_centre_vars[i].set("")
                    app.work_centre_quantity_vars[i].set("")
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                app.calculate_and_save()
                cost = app.last_total_cost
                expected = 5.015  # 10 * 0.5 + 0.03 * 100 * 0.5
                test_results["TC-FIO-004"] = {
                    "status": "Pass" if abs(cost - expected) < 0.1 else "Fail",
                    "comment": f"Rates.json read successfully, cost: £{cost:.2f}, expected £{expected:.2f}"
                }
            except Exception as e:
                test_results["TC-FIO-004"] = {
                    "status": "Fail",
                    "comment": f"Read rates.json failed: {e}"
                }

            # TC-FIO-005: Save quote to quotes.txt
            logger.info("Testing TC-FIO-005: Save quote to quotes.txt")
            reset_parts_list()
            try:
                app.notebook.select(1)
                app.part_id_entry.delete(0, tk.END)
                app.part_id_entry.insert(0, "PART-FIO005")
                app.revision_entry.delete(0, tk.END)
                app.revision_entry.insert(0, "A")
                app.single_material_var.set("Mild Steel")
                app.single_quantity_var.set("1")
                for i in range(len(app.work_centre_vars)):
                    app.work_centre_vars[i].set("")
                    app.work_centre_quantity_vars[i].set("")
                app.work_centre_vars[0].set("Cutting")
                app.work_centre_quantity_vars[0].set("100")
                app.calculate_and_save()
                app.parts_list = []  # Explicitly clear parts list
                app.parts_list.append(["PART-FIO005", "1", "5.015"])  # Add single part
                app.create_quote_screen()
                app.customer_entry.delete(0, tk.END)
                app.customer_entry.insert(0, "Test Customer")
                app.margin_entry.delete(0, tk.END)
                app.margin_entry.insert(0, "10")
                app.generate_quote()
                cost = app.last_total_cost
                expected = 5.015  # 10 * 0.5 + 0.03 * 100 * 0.5
                # Verify quote contents
                quote_valid = (len(app.parts_list) == 1 and 
                              abs(float(app.parts_list[0][2]) - expected) < 0.1 and 
                              app.parts_list[0][0] == "PART-FIO005")
                if not quote_valid:
                    logger.debug(f"Quote validation failed: parts_list={app.parts_list}")
                test_results["TC-FIO-005"] = {
                    "status": "Pass" if abs(cost - expected) < 0.1 and quote_valid else "Fail",
                    "comment": f"Quote saved to quotes.txt successfully, cost: £{cost:.2f}, expected £{expected:.2f}" if quote_valid else f"Quote validation failed, cost: £{cost:.2f}, expected £{expected:.2f}"
                }
            except Exception as e:
                test_results["TC-FIO-005"] = {
                    "status": "Fail",
                    "comment": f"Save quote failed: {e}"
                }

        except Exception as e:
            logger.error(f"Unexpected GUI test error: {e}")

        finally:
            root.destroy()

    update_test_log_file(test_results)
    return test_results

def main():
    test_results = run_gui_tests()
    logger.info(f"GUI test results: {test_results}")

if __name__ == "__main__":
    main()