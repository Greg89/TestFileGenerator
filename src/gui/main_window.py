"""
Main GUI window for the Test Data Generator application.
Follows Single Responsibility Principle by handling only GUI concerns.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional
import os
from pathlib import Path

from ..models.data_config import FileConfig, ColumnConfig, DataType, GenerationRequest
from ..services.data_generation_service import DataGenerationService


class MainWindow:
    """Main application window."""

    def __init__(self):
        self.root = tk.Tk()
        self.service = DataGenerationService()
        self.column_widgets = []
        self.setup_window()
        self.create_widgets()
        self.setup_layout()

    def setup_window(self):
        """Configure main window properties."""
        self.root.title("Test Data Generator")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Set minimum window size
        self.root.minsize(900, 700)

        # Configure style
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        self.root.configure(bg='#f0f0f0')

    def create_widgets(self):
        """Create all GUI widgets."""
        self.create_header()
        self.create_format_section()
        self.create_dimensions_section()
        self.create_columns_section()
        self.create_output_section()
        self.create_actions_section()
        self.create_status_section()

    def create_header(self):
        """Create application header."""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill='x', padx=20, pady=10)

        title_label = ttk.Label(
            header_frame,
            text="Test Data Generator",
            font=('Arial', 24, 'bold')
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame,
            text="Generate test files in various formats with realistic random data",
            font=('Arial', 12)
        )
        subtitle_label.pack(pady=5)

    def create_format_section(self):
        """Create file format selection section."""
        format_frame = ttk.LabelFrame(self.root, text="File Format", padding=10)
        format_frame.pack(fill='x', padx=20, pady=5)

        self.format_var = tk.StringVar(value="csv")
        formats = self.service.get_available_file_formats()

        for i, fmt in enumerate(formats):
            radio = ttk.Radiobutton(
                format_frame,
                text=fmt.upper(),
                variable=self.format_var,
                value=fmt,
                command=self.on_format_change
            )
            radio.grid(row=0, column=i, padx=10, pady=5)

    def create_dimensions_section(self):
        """Create dimensions configuration section."""
        dim_frame = ttk.LabelFrame(self.root, text="Dimensions", padding=10)
        dim_frame.pack(fill='x', padx=20, pady=5)

        # Rows
        ttk.Label(dim_frame, text="Number of Rows:").grid(row=0, column=0, sticky='w', padx=5)
        self.rows_var = tk.StringVar(value="100")
        rows_entry = ttk.Entry(dim_frame, textvariable=self.rows_var, width=10)
        rows_entry.grid(row=0, column=1, padx=5, pady=5)

        # Columns
        ttk.Label(dim_frame, text="Number of Columns:").grid(row=0, column=2, sticky='w', padx=5)
        self.columns_var = tk.StringVar(value="5")
        columns_entry = ttk.Entry(dim_frame, textvariable=self.columns_var, width=10)
        columns_entry.grid(row=0, column=3, padx=5, pady=5)

        # Bind column change
        columns_entry.bind('<KeyRelease>', self.on_columns_change)

    def create_columns_section(self):
        """Create column configuration section."""
        self.columns_frame = ttk.LabelFrame(self.root, text="Column Configuration", padding=10)
        self.columns_frame.pack(fill='both', expand=True, padx=20, pady=5)

        # Create scrollable frame for columns
        canvas = tk.Canvas(self.columns_frame)
        scrollbar = ttk.Scrollbar(self.columns_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add mouse wheel support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_column_widgets()

    def create_column_widgets(self):
        """Create widgets for column configuration with smart preservation of existing data."""
        try:
            num_columns = int(self.columns_var.get())
        except ValueError:
            num_columns = 5

        current_columns = len(self.column_widgets)
        
        # Create header if this is the first time
        if current_columns == 0:
            headers = ["Column Name", "Data Type", "Min Value", "Max Value", "Text Length"]
            for i, header in enumerate(headers):
                label = ttk.Label(self.scrollable_frame, text=header, font=('Arial', 10, 'bold'))
                label.grid(row=0, column=i, padx=5, pady=5, sticky='w')

        data_types = self.service.get_available_data_types()

        if num_columns > current_columns:
            # Add new rows for additional columns
            for col_idx in range(current_columns, num_columns):
                self.create_column_row(col_idx, data_types)
        elif num_columns < current_columns:
            # Remove excess rows from the end
            for col_idx in range(num_columns, current_columns):
                if col_idx < len(self.column_widgets):
                    row_widgets = self.column_widgets[col_idx]
                    for widget in row_widgets:
                        widget.destroy()
            # Keep only the first num_columns rows
            self.column_widgets = self.column_widgets[:num_columns]
        # If num_columns == current_columns, do nothing (preserve all data)

    def create_column_row(self, col_idx: int, data_types: List[str]):
        """Create a single column configuration row."""
        row_widgets = []

        # Column name
        name_var = tk.StringVar(value=f"Column_{col_idx + 1}")
        name_entry = ttk.Entry(self.scrollable_frame, textvariable=name_var, width=15)
        name_entry.grid(row=col_idx + 1, column=0, padx=5, pady=2, sticky='w')
        row_widgets.append(name_entry)

        # Data type
        type_var = tk.StringVar(value=data_types[0])
        type_combo = ttk.Combobox(self.scrollable_frame, textvariable=type_var, values=data_types, width=15)
        type_combo.grid(row=col_idx + 1, column=1, padx=5, pady=2, sticky='w')
        row_widgets.append(type_combo)

        # Min value
        min_var = tk.StringVar()
        min_entry = ttk.Entry(self.scrollable_frame, textvariable=min_var, width=10)
        min_entry.grid(row=col_idx + 1, column=2, padx=5, pady=2, sticky='w')
        row_widgets.append(min_entry)

        # Max value
        max_var = tk.StringVar()
        max_entry = ttk.Entry(self.scrollable_frame, textvariable=max_var, width=10)
        max_entry.grid(row=col_idx + 1, column=3, padx=5, pady=2, sticky='w')
        row_widgets.append(max_entry)

        # Text length
        length_var = tk.StringVar()
        length_entry = ttk.Entry(self.scrollable_frame, textvariable=length_var, width=10)
        length_entry.grid(row=col_idx + 1, column=4, padx=5, pady=2, sticky='w')
        row_widgets.append(length_entry)

        self.column_widgets.append(row_widgets)

    def create_output_section(self):
        """Create output configuration section."""
        output_frame = ttk.LabelFrame(self.root, text="Output Configuration", padding=10)
        output_frame.pack(fill='x', padx=20, pady=5)

        # Output directory
        ttk.Label(output_frame, text="Output Directory:").grid(row=0, column=0, sticky='w', padx=5)
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        output_dir_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var, width=50)
        output_dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_dir)
        browse_btn.grid(row=0, column=2, padx=5, pady=5)

        # Filename
        ttk.Label(output_frame, text="Filename:").grid(row=1, column=0, sticky='w', padx=5)
        self.filename_var = tk.StringVar(value="test_data")
        filename_entry = ttk.Entry(output_frame, textvariable=self.filename_var, width=50)
        filename_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        # Configure grid weights
        output_frame.columnconfigure(1, weight=1)

    def create_actions_section(self):
        """Create action buttons section."""
        actions_frame = ttk.Frame(self.root)
        actions_frame.pack(fill='x', padx=20, pady=10)

        # Generate button
        self.generate_btn = ttk.Button(
            actions_frame,
            text="Generate Test Data",
            command=self.generate_data,
            style='Accent.TButton'
        )
        self.generate_btn.pack(side='left', padx=5)

        # Clear button
        clear_btn = ttk.Button(
            actions_frame,
            text="Clear Configuration",
            command=self.clear_configuration
        )
        clear_btn.pack(side='left', padx=5)

        # Exit button
        exit_btn = ttk.Button(
            actions_frame,
            text="Exit",
            command=self.root.quit
        )
        exit_btn.pack(side='right', padx=5)

    def create_status_section(self):
        """Create status display section."""
        self.status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        self.status_frame.pack(fill='x', padx=20, pady=5)

        self.status_var = tk.StringVar(value="Ready to generate test data")
        status_label = ttk.Label(self.status_frame, textvariable=self.status_var)
        status_label.pack()

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.status_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill='x', pady=5)

    def setup_layout(self):
        """Configure widget layout and bindings."""
        # Configure main window grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)  # Columns section should expand

    def on_format_change(self):
        """Handle file format change."""
        # Update filename extension
        current_filename = self.filename_var.get()
        if '.' in current_filename:
            current_filename = current_filename.rsplit('.', 1)[0]

        new_extension = self.format_var.get()
        self.filename_var.set(f"{current_filename}.{new_extension}")

    def on_columns_change(self, event=None):
        """Handle number of columns change."""
        self.create_column_widgets()

    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)

    def get_column_configs(self) -> List[ColumnConfig]:
        """Extract column configurations from GUI."""
        configs = []

        for row_widgets in self.column_widgets:
            try:
                name = row_widgets[0].get()
                data_type = DataType(row_widgets[1].get())

                # Parse numeric values
                min_val = None
                max_val = None
                text_length = None

                min_str = row_widgets[2].get().strip()
                if min_str:
                    min_val = float(min_str)

                max_str = row_widgets[3].get().strip()
                if max_str:
                    max_val = float(max_str)

                length_str = row_widgets[4].get().strip()
                if length_str:
                    text_length = int(length_str)

                config = ColumnConfig(
                    name=name,
                    data_type=data_type,
                    min_value=min_val,
                    max_value=max_val,
                    text_length=text_length
                )
                configs.append(config)

            except Exception as e:
                raise ValueError(f"Invalid column configuration: {str(e)}")

        return configs

    def generate_data(self):
        """Generate test data based on current configuration."""
        try:
            # Update status
            self.status_var.set("Validating configuration...")
            self.progress_var.set(10)
            self.root.update()

            # Get configuration from GUI
            num_rows = int(self.rows_var.get())
            num_columns = int(self.columns_var.get())
            file_format = self.format_var.get()
            output_dir = self.output_dir_var.get()
            filename = self.filename_var.get()

            # Ensure filename has correct extension
            if not filename.endswith(f".{file_format}"):
                filename = f"{filename}.{file_format}"

            output_path = os.path.join(output_dir, filename)

            # Get column configurations
            columns = self.get_column_configs()

            # Create file configuration
            file_config = FileConfig(
                file_format=file_format,
                num_rows=num_rows,
                num_columns=num_columns,
                columns=columns,
                output_path=output_path
            )

            # Validate configuration
            self.progress_var.set(20)
            self.root.update()

            errors = self.service.validate_configuration(file_config)
            if errors:
                error_msg = "\n".join(errors)
                messagebox.showerror("Configuration Error", f"Please fix the following errors:\n\n{error_msg}")
                return

            # Create generation request
            request = GenerationRequest(
                config=file_config,
                seed=None,  # Random seed for variety
                batch_size=1000
            )

            # Generate data
            self.status_var.set("Generating test data...")
            self.progress_var.set(40)
            self.root.update()

            output_file = self.service.generate_test_data(request)

            # Update progress and status
            self.progress_var.set(100)
            self.status_var.set(f"Successfully generated: {output_file}")

            messagebox.showinfo(
                "Success",
                f"Test data generated successfully!\n\nFile: {output_file}\nRows: {num_rows}\nColumns: {num_columns}"
            )

        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            self.progress_var.set(0)
            messagebox.showerror("Generation Error", f"Failed to generate test data:\n\n{str(e)}")

    def clear_configuration(self):
        """Clear all configuration fields."""
        self.rows_var.set("100")
        self.columns_var.set("5")
        self.filename_var.set("test_data")
        self.create_column_widgets()
        self.status_var.set("Configuration cleared")
        self.progress_var.set(0)

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()
