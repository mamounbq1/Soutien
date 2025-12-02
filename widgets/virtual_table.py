"""
Virtual Scrolling Table with Canvas
High-performance table widget that only renders visible rows
"""

import customtkinter as ctk
from tkinter import Canvas, Event
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.theme import ModernTheme


class VirtualScrollTable(ctk.CTkFrame):
    """
    High-performance virtual scrolling table using Canvas
    Only renders visible rows for optimal performance
    """
    
    def __init__(self, parent, headers, column_widths=None, row_height=45, visible_rows=12, rows_per_page=10, enable_pagination=True):
        super().__init__(parent, fg_color="transparent")
        
        self.headers = headers
        self.column_widths = column_widths or [150] * len(headers)
        self.row_height = row_height
        self.visible_rows = visible_rows
        self.rows_per_page = rows_per_page
        self.enable_pagination = enable_pagination
        
        # Data storage
        self.data = []  # All rows data
        self.filtered_data = []  # Data for current page
        self.row_callbacks = {}  # Callbacks for row actions
        
        # Pagination state
        self.current_page = 1
        self.total_pages = 1
        
        # Selection state
        self.selected_row = None
        self.hovered_row = None
        
        # Scroll position
        self.scroll_position = 0
        self.max_scroll = 0
        
        # Professional Colors (Improved)
        self.bg_color = "#FAFBFC"  # Light grey background
        self.header_bg = "#1E88E5"  # Professional blue
        self.header_fg = "#FFFFFF"
        self.row_bg = "#FFFFFF"  # Pure white
        self.row_alt_bg = "#F5F7FA"  # Very light grey
        self.row_hover_bg = "#E3F2FD"  # Light blue hover
        self.row_selected_bg = "#BBDEFB"  # Selected blue
        self.border_color = "#E1E4E8"  # Soft border
        self.text_color = "#24292E"  # Dark grey text
        self.action_icon_color = "#1E88E5"  # Blue action icon
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the table UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        if self.enable_pagination:
            self.grid_rowconfigure(2, weight=0)  # Pagination row
        
        # Header canvas
        header_width = sum(self.column_widths)  # Fixed width based on columns
        self.header_canvas = Canvas(
            self,
            height=self.row_height,
            width=header_width,  # Fixed width (no expansion)
            bg=self.header_bg,
            highlightthickness=0
        )
        self.header_canvas.grid(row=0, column=0, sticky="w")
        
        # Main canvas for rows
        canvas_height = self.row_height * self.visible_rows
        canvas_width = sum(self.column_widths)  # Fixed width based on columns
        self.canvas = Canvas(
            self,
            bg=self.bg_color,
            highlightthickness=1,
            highlightbackground=self.border_color,
            height=canvas_height,
            width=canvas_width,  # Fixed width (no expansion)
            cursor=""  # Remove cursor
        )
        self.canvas.grid(row=1, column=0, sticky="ns")
        
        # Scrollbar (only if pagination is disabled)
        if not self.enable_pagination:
            self.scrollbar = ctk.CTkScrollbar(
                self,
                command=self._on_scroll
            )
            self.scrollbar.grid(row=1, column=1, sticky="ns")
        else:
            self.scrollbar = None  # No scrollbar with pagination
        
        # Bind events
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)  # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_mousewheel)  # Linux scroll down
        self.canvas.bind("<Motion>", self._on_mouse_move)
        self.canvas.bind("<Button-1>", self._on_mouse_click)
        self.canvas.bind("<Leave>", self._on_mouse_leave)
        
        # Draw headers
        self._draw_headers()
        
        # Pagination controls (if enabled)
        if self.enable_pagination:
            self._create_pagination_controls()
    
    def _draw_headers(self):
        """Draw table headers"""
        self.header_canvas.delete("all")
        
        x = 0
        for i, (header, width) in enumerate(zip(self.headers, self.column_widths)):
            # Header background
            self.header_canvas.create_rectangle(
                x, 0, x + width, self.row_height,
                fill=self.header_bg,
                outline=self.border_color
            )
            
            # Header text
            self.header_canvas.create_text(
                x + width // 2, self.row_height // 2,
                text=header,
                fill=self.header_fg,
                font=("Segoe UI", 11, "bold"),
                anchor="center"
            )
            
            x += width
    
    def _on_canvas_configure(self, event):
        """Handle canvas resize"""
        self._update_scrollbar()
        self._redraw_visible_rows()
    
    def _on_scroll(self, *args):
        """Handle scrollbar movement"""
        if args[0] == "moveto":
            fraction = float(args[1])
            self.scroll_position = int(fraction * self.max_scroll)
        elif args[0] == "scroll":
            delta = int(args[1])
            self.scroll_position = max(0, min(
                self.scroll_position + delta * 3,
                self.max_scroll
            ))
        
        self._redraw_visible_rows()
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        if event.num == 4 or event.delta > 0:
            # Scroll up
            delta = -3
        elif event.num == 5 or event.delta < 0:
            # Scroll down
            delta = 3
        else:
            return
        
        self.scroll_position = max(0, min(
            self.scroll_position + delta,
            self.max_scroll
        ))
        
        self._update_scrollbar()
        self._redraw_visible_rows()
    
    def _on_mouse_move(self, event):
        """Handle mouse movement for hover effect"""
        row_index = (event.y // self.row_height) + self.scroll_position
        
        data_to_check = self.filtered_data if self.enable_pagination else self.data
        if 0 <= row_index < len(data_to_check):
            if self.hovered_row != row_index:
                self.hovered_row = row_index
                self._redraw_visible_rows()
        else:
            if self.hovered_row is not None:
                self.hovered_row = None
                self._redraw_visible_rows()
    
    def _on_mouse_leave(self, event):
        """Handle mouse leaving canvas"""
        if self.hovered_row is not None:
            self.hovered_row = None
            self._redraw_visible_rows()
    
    def _on_mouse_click(self, event):
        """Handle mouse click on row"""
        row_index = (event.y // self.row_height) + self.scroll_position
        
        data_to_check = self.filtered_data if self.enable_pagination else self.data
        if 0 <= row_index < len(data_to_check):
            # Check if clicked on action buttons area (last column)
            x_pos = event.x
            action_col_start = sum(self.column_widths[:-1])
            
            if x_pos >= action_col_start:
                # Clicked on actions column
                self._show_actions_menu(event, row_index)
            else:
                # Select row
                self.selected_row = row_index
                self._redraw_visible_rows()
    
    def _show_actions_menu(self, event, row_index):
        """Show context menu for actions"""
        menu = ctk.CTkToplevel(self)
        menu.withdraw()
        menu.overrideredirect(True)
        
        # Position menu at mouse
        x = event.x_root
        y = event.y_root
        
        # Create menu frame
        menu_frame = ctk.CTkFrame(
            menu,
            fg_color=("#FFFFFF", "#2B2B2B"),
            corner_radius=8
        )
        menu_frame.pack(padx=2, pady=2)
        
        # Edit button
        if "edit" in self.row_callbacks:
            edit_btn = ctk.CTkButton(
                menu_frame,
                text="✏️ Modifier",
                width=120,
                height=32,
                corner_radius=6,
                fg_color=ModernTheme.WARNING,
                hover_color="#E65100",
                command=lambda: self._execute_action(menu, "edit", row_index)
            )
            edit_btn.pack(padx=8, pady=(8, 4))
        
        # Delete button
        if "delete" in self.row_callbacks:
            delete_btn = ctk.CTkButton(
                menu_frame,
                text="🗑️ Supprimer",
                width=120,
                height=32,
                corner_radius=6,
                fg_color=ModernTheme.DANGER,
                hover_color=ModernTheme.BTN_DANGER_HOVER,
                command=lambda: self._execute_action(menu, "delete", row_index)
            )
            delete_btn.pack(padx=8, pady=(4, 8))
        
        # Show menu
        menu.deiconify()
        menu.geometry(f"+{x}+{y}")
        
        # Auto close on focus out
        menu.bind("<FocusOut>", lambda e: menu.destroy())
        menu.focus_set()
    
    def _execute_action(self, menu, action, row_index):
        """Execute action callback and close menu"""
        menu.destroy()
        if action in self.row_callbacks:
            callback = self.row_callbacks[action]
            # Get actual row data (accounting for pagination)
            if self.enable_pagination:
                # Map visible row index to actual data index
                actual_index = (self.current_page - 1) * self.rows_per_page + row_index
                row_data = self.data[actual_index]
            else:
                row_data = self.data[row_index]
            callback(row_data)
    
    def _update_scrollbar(self):
        """Update scrollbar position and size"""
        if self.scrollbar is None:  # No scrollbar with pagination
            return
        
        data_to_use = self.filtered_data if self.enable_pagination else self.data
        total_rows = len(data_to_use)
        if total_rows <= self.visible_rows:
            self.scrollbar.set(0, 1)
            self.max_scroll = 0
        else:
            self.max_scroll = max(0, total_rows - self.visible_rows)
            visible_fraction = self.visible_rows / total_rows
            scroll_fraction = self.scroll_position / total_rows
            
            self.scrollbar.set(
                scroll_fraction,
                scroll_fraction + visible_fraction
            )
    
    def _redraw_visible_rows(self):
        """Redraw only visible rows (Virtual Scrolling)"""
        self.canvas.delete("all")
        
        canvas_height = self.canvas.winfo_height()
        if canvas_height <= 1:
            canvas_height = self.row_height * self.visible_rows
        
        # Calculate visible row range
        data_to_use = self.filtered_data if self.enable_pagination else self.data
        start_row = self.scroll_position
        end_row = min(start_row + self.visible_rows + 1, len(data_to_use))
        
        # Draw visible rows
        for i in range(start_row, end_row):
            y_offset = (i - start_row) * self.row_height
            self._draw_row(i, y_offset)
    
    def _draw_row(self, row_index, y_offset):
        """Draw a single row"""
        data_to_use = self.filtered_data if self.enable_pagination else self.data
        row_data = data_to_use[row_index]
        
        # Determine background color
        if row_index == self.selected_row:
            bg_color = self.row_selected_bg
        elif row_index == self.hovered_row:
            bg_color = self.row_hover_bg
        elif row_index % 2 == 0:
            bg_color = self.row_bg
        else:
            bg_color = self.row_alt_bg
        
        # Draw row background
        total_width = sum(self.column_widths)
        self.canvas.create_rectangle(
            0, y_offset,
            total_width, y_offset + self.row_height,
            fill=bg_color,
            outline=self.border_color,
            tags=f"row_{row_index}"
        )
        
        # Draw cells
        x = 0
        for col_index, (cell_data, width) in enumerate(zip(row_data, self.column_widths)):
            # Draw cell border
            self.canvas.create_line(
                x, y_offset,
                x, y_offset + self.row_height,
                fill=self.border_color
            )
            
            # Draw cell text
            if col_index < len(row_data) - 1:  # Not actions column
                text = str(cell_data) if cell_data else "-"
                # Use grey color for empty data (dash)
                text_color = "#ADB5BD" if text == "-" else self.text_color
                self.canvas.create_text(
                    x + 10, y_offset + self.row_height // 2,
                    text=text,
                    fill=text_color,
                    font=("Segoe UI", 10),
                    anchor="w",
                    tags=f"row_{row_index}"
                )
            else:
                # Actions column - show icon (improved)
                self.canvas.create_text(
                    x + width // 2, y_offset + self.row_height // 2,
                    text="⋮",
                    fill=self.action_icon_color,
                    font=("Segoe UI", 18, "bold"),
                    anchor="center",
                    tags=f"row_{row_index}"
                )
                # Add subtle circle background for action icon
                circle_radius = 12
                cx = x + width // 2
                cy = y_offset + self.row_height // 2
                if row_index == self.hovered_row:
                    self.canvas.create_oval(
                        cx - circle_radius, cy - circle_radius,
                        cx + circle_radius, cy + circle_radius,
                        fill="#E3F2FD",
                        outline="",
                        tags=f"row_{row_index}"
                    )
                    # Redraw icon on top
                    self.canvas.create_text(
                        cx, cy,
                        text="⋮",
                        fill=self.action_icon_color,
                        font=("Segoe UI", 18, "bold"),
                        anchor="center",
                        tags=f"row_{row_index}"
                    )
            
            x += width
    
    def set_data(self, data):
        """Set table data (list of lists)"""
        self.data = data
        self.scroll_position = 0
        self.selected_row = None
        self.hovered_row = None
        
        if self.enable_pagination:
            self._update_pagination()
        else:
            self.filtered_data = self.data
            self._update_scrollbar()
            self._redraw_visible_rows()
    
    def clear(self):
        """Clear all data"""
        self.data = []
        self.filtered_data = []
        self.scroll_position = 0
        self.selected_row = None
        self.hovered_row = None
        self.current_page = 1
        self.canvas.delete("all")
        if self.enable_pagination:
            self._update_pagination()
        else:
            self._update_scrollbar()
    
    def add_row(self, row_data):
        """Add a single row"""
        self.data.append(row_data)
        if self.enable_pagination:
            self._update_pagination()
        else:
            self._update_scrollbar()
            self._redraw_visible_rows()
    
    def set_row_callback(self, action, callback):
        """Set callback for row actions (edit, delete, etc.)"""
        self.row_callbacks[action] = callback
    
    def get_selected_row_index(self):
        """Get currently selected row index"""
        return self.selected_row
    
    def get_selected_row_data(self):
        """Get currently selected row data"""
        if self.selected_row is not None and 0 <= self.selected_row < len(self.data):
            return self.data[self.selected_row]
        return None
    
    def _create_pagination_controls(self):
        """Create pagination controls at bottom of table"""
        pagination_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0,
            height=50
        )
        pagination_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))
        pagination_frame.grid_columnconfigure(1, weight=1)
        
        # Left side - Info
        info_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="w", padx=15)
        
        self.page_info_label = ctk.CTkLabel(
            info_frame,
            text="Page 1 sur 1 (0 élèves)",
            font=("Segoe UI", 11),
            text_color="#6C757D"
        )
        self.page_info_label.pack(side="left")
        
        # Right side - Navigation buttons
        nav_frame = ctk.CTkFrame(pagination_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=1, sticky="e", padx=15)
        
        # First page button
        self.first_page_btn = ctk.CTkButton(
            nav_frame,
            text="⏮",
            width=35,
            height=32,
            corner_radius=6,
            fg_color="#E9ECEF",
            text_color="#495057",
            hover_color="#DEE2E6",
            command=self._go_to_first_page,
            font=("Segoe UI", 14)
        )
        self.first_page_btn.pack(side="left", padx=2)
        
        # Previous page button
        self.prev_page_btn = ctk.CTkButton(
            nav_frame,
            text="◀",
            width=35,
            height=32,
            corner_radius=6,
            fg_color="#E9ECEF",
            text_color="#495057",
            hover_color="#DEE2E6",
            command=self._go_to_prev_page,
            font=("Segoe UI", 12)
        )
        self.prev_page_btn.pack(side="left", padx=2)
        
        # Current page display
        self.current_page_label = ctk.CTkLabel(
            nav_frame,
            text="1",
            font=("Segoe UI", 12, "bold"),
            text_color="#1E88E5",
            width=40,
            height=32,
            corner_radius=6,
            fg_color="#E3F2FD"
        )
        self.current_page_label.pack(side="left", padx=5)
        
        # Next page button
        self.next_page_btn = ctk.CTkButton(
            nav_frame,
            text="▶",
            width=35,
            height=32,
            corner_radius=6,
            fg_color="#E9ECEF",
            text_color="#495057",
            hover_color="#DEE2E6",
            command=self._go_to_next_page,
            font=("Segoe UI", 12)
        )
        self.next_page_btn.pack(side="left", padx=2)
        
        # Last page button
        self.last_page_btn = ctk.CTkButton(
            nav_frame,
            text="⏭",
            width=35,
            height=32,
            corner_radius=6,
            fg_color="#E9ECEF",
            text_color="#495057",
            hover_color="#DEE2E6",
            command=self._go_to_last_page,
            font=("Segoe UI", 14)
        )
        self.last_page_btn.pack(side="left", padx=2)
    
    def _update_pagination(self):
        """Update pagination state and display"""
        total_items = len(self.data)
        self.total_pages = max(1, (total_items + self.rows_per_page - 1) // self.rows_per_page)
        
        # Ensure current page is valid
        self.current_page = max(1, min(self.current_page, self.total_pages))
        
        # Calculate start and end indices for current page
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, total_items)
        
        # Set filtered data for current page
        self.filtered_data = self.data[start_idx:end_idx]
        
        # Update UI
        self._update_pagination_ui()
        self._update_scrollbar()
        self._redraw_visible_rows()
    
    def _update_pagination_ui(self):
        """Update pagination UI elements"""
        if not self.enable_pagination:
            return
        
        total_items = len(self.data)
        start_idx = (self.current_page - 1) * self.rows_per_page + 1
        end_idx = min(start_idx + len(self.filtered_data) - 1, total_items)
        
        # Update info label
        info_text = f"Page {self.current_page} sur {self.total_pages} ({total_items} élèves)"
        if total_items > 0:
            info_text += f" - Affichage de {start_idx} à {end_idx}"
        self.page_info_label.configure(text=info_text)
        
        # Update current page display
        self.current_page_label.configure(text=str(self.current_page))
        
        # Enable/disable navigation buttons
        if self.current_page <= 1:
            self.first_page_btn.configure(state="disabled", fg_color="#F8F9FA", text_color="#ADB5BD")
            self.prev_page_btn.configure(state="disabled", fg_color="#F8F9FA", text_color="#ADB5BD")
        else:
            self.first_page_btn.configure(state="normal", fg_color="#E9ECEF", text_color="#495057")
            self.prev_page_btn.configure(state="normal", fg_color="#E9ECEF", text_color="#495057")
        
        if self.current_page >= self.total_pages:
            self.next_page_btn.configure(state="disabled", fg_color="#F8F9FA", text_color="#ADB5BD")
            self.last_page_btn.configure(state="disabled", fg_color="#F8F9FA", text_color="#ADB5BD")
        else:
            self.next_page_btn.configure(state="normal", fg_color="#E9ECEF", text_color="#495057")
            self.last_page_btn.configure(state="normal", fg_color="#E9ECEF", text_color="#495057")
    
    def _go_to_first_page(self):
        """Navigate to first page"""
        if self.current_page != 1:
            self.current_page = 1
            self._update_pagination()
    
    def _go_to_prev_page(self):
        """Navigate to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_pagination()
    
    def _go_to_next_page(self):
        """Navigate to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._update_pagination()
    
    def _go_to_last_page(self):
        """Navigate to last page"""
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self._update_pagination()
