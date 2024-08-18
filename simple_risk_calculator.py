import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RiskCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OWASP Risk Calculator")

        # Initialize variables for the comboboxes
        self.variables = {}
        self.value_map = {
            "0 - Minimal": 0,
            "1 - Low": 1,
            "2 - Moderate": 2,
            "3 - High": 3,
            "4 - Critical": 4
        }

        # Set up the layout
        self.setup_ui()

    def setup_ui(self):
        # Threat Agent Factors
        ttk.Label(self.root, text="Threat Agent Factors").grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        self.create_factor_section("Skill Level", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High", "4 - Critical"], row=1, col=0, var_name="skill_level")
        self.create_factor_section("Motive", ["0 - Minimal", "1 - Low", "2 - Moderate"], row=2, col=0, var_name="motive")
        self.create_factor_section("Opportunity", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High"], row=3, col=0, var_name="opportunity")
        self.create_factor_section("Size", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High", "4 - Critical"], row=4, col=0, var_name="size")

        # Vulnerability Factors
        ttk.Label(self.root, text="Vulnerability Factors").grid(row=0, column=2, columnspan=2, padx=10, pady=5)
        self.create_factor_section("Ease of Discovery", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High"], row=1, col=2, var_name="ease_of_discovery")
        self.create_factor_section("Ease of Exploit", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High"], row=2, col=2, var_name="ease_of_exploit")
        self.create_factor_section("Awareness", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High"], row=3, col=2, var_name="awareness")
        self.create_factor_section("Intrusion Detection", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High"], row=4, col=2, var_name="intrusion_detection")

        # Impact Factors
        ttk.Label(self.root, text="Technical Impact Factors").grid(row=0, column=4, columnspan=2, padx=10, pady=5)
        self.create_factor_section("Loss Of Confidentiality", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High", "4 - Critical"], row=1, col=4, var_name="loss_of_confidentiality")
        self.create_factor_section("Loss Of Integrity", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High", "4 - Critical"], row=2, col=4, var_name="loss_of_integrity")
        self.create_factor_section("Loss Of Availability", ["0 - Minimal", "1 - Low", "2 - Moderate", "3 - High", "4 - Critical"], row=3, col=4, var_name="loss_of_availability")
        self.create_factor_section("Loss of Accountability", ["0 - Minimal", "1 - Low", "2 - Moderate"], row=4, col=4, var_name="loss_of_accountability")

        # Calculate Button
        ttk.Button(self.root, text="Calculate Risk", command=self.calculate_risk).grid(row=5, column=0, columnspan=6, pady=10)

    def create_factor_section(self, label, options, row, col, var_name):
        ttk.Label(self.root, text=label).grid(row=row, column=col, padx=10, pady=5, sticky="W")
        var = tk.StringVar()
        combo = ttk.Combobox(self.root, textvariable=var, values=options, state="readonly")
        combo.grid(row=row, column=col + 1, padx=10, pady=5)
        self.variables[var_name] = var

    def calculate_risk(self):
        try:
            # Fetch the selected values and convert to numeric
            scores = {key: self.value_map[value.get()] for key, value in self.variables.items()}

            # Example calculation
            total_risk = sum(scores.values())
            avg_risk = total_risk / len(scores)

            # Determine colors for the bars based on risk levels
            colors = ['red' if total_risk > 12 else 'orange' if total_risk > 8 else 'yellow' if total_risk > 4 else 'green', 
                      'red' if avg_risk > 3 else 'orange' if avg_risk > 2 else 'yellow' if avg_risk > 1 else 'green']

            # Plot the result
            self.plot_risk(total_risk, avg_risk, colors)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def plot_risk(self, total_risk, avg_risk, colors):
        # Create a new window for plotting
        plot_window = tk.Toplevel(self.root)
        plot_window.title("Risk Score Visualization")

        # Create a figure and plot
        fig, ax = plt.subplots()
        ax.bar(["Total Risk", "Average Risk"], [total_risk, avg_risk], color=colors)
        ax.set_ylabel("Risk Score")
        ax.set_title("Risk Score Analysis")

        # Display plot in Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Create the main window
root = tk.Tk()
app = RiskCalculatorApp(root)
root.mainloop()
