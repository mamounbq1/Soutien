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
    
    def __init__(self, parent, headers, column_widths=None, row_height=45, visible_rows=12):
        super().__init__(parent, fg_color="transparent")
        
        self.headers = headers
        self.column_widths = column_widths or [150] * len(headers)
        self.row_height = row_height
        self.visible_rows = visible_rows
        
        # Data storage
        self.data = []  # All rows data
        self.row_callbacks = {}  # Callbacks for row actions
        
        # Selection state
        self.selected_row = None
        self.hovered_row = None
        
        # Scroll position
        self.scroll_position = 0
        self.max_scroll = 0
        
        # Colors
        self.bg_color = ModernTheme.BG_CARD_LIGHT
        self.header_bg = ModernTheme.PRIMARY
        self.header_fg = "#FFFFFF"
        self.row_bg = "#FFFFFF"
        self.row_alt_bg = "#F8F9FA"
        self.row_hover_bg = "#E3F2FD"
        self.row_selected_bg = "#BBDEFB"
        self.border_color = ModernTheme.BORDER_LIGHT
        self.text_color = ModernTheme.TEXT_PRIMARY_LIGHT
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the table UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header canvas
        self.header_canvas = Canvas(
            self,
            height=self.row_height,
            bg=self.header_bg,
            highlightthickness=0
        )
        self.header_canvas.grid(row=0, column=0, sticky="ew")
        
        # Main canvas for rows
        self.canvas = Canvas(
            self,
            bg=self.bg_color,
            highlightthickness=1,
            highlightbackground=self.border_color
        )
        self.canvas.grid(row=1, column=0, sticky="nsew")
        
        # Scrollbar
        self.scrollbar = ctk.CTkScrollbar(
            self,
            command=self._on_scroll
        )
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        
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
        
        if 0 <= row_index < len(self.data):
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
        
        if 0 <= row_index < len(self.data):
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
            row_data = self.data[row_index]
            callback(row_data)
    
    def _update_scrollbar(self):
        """Update scrollbar position and size"""
        total_rows = len(self.data)
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
        start_row = self.scroll_position
        end_row = min(start_row + self.visible_rows + 1, len(self.data))
        
        # Draw visible rows
        for i in range(start_row, end_row):
            y_offset = (i - start_row) * self.row_height
            self._draw_row(i, y_offset)
    
    def _draw_row(self, row_index, y_offset):
        """Draw a single row"""
        row_data = self.data[row_index]
        
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
                self.canvas.create_text(
                    x + 10, y_offset + self.row_height // 2,
                    text=text,
                    fill=self.text_color,
                    font=("Segoe UI", 10),
                    anchor="w",
                    tags=f"row_{row_index}"
                )
            else:
                # Actions column - show icon
                self.canvas.create_text(
                    x + width // 2, y_offset + self.row_height // 2,
                    text="⋮",
                    fill=ModernTheme.PRIMARY,
                    font=("Segoe UI", 16, "bold"),
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
        self._update_scrollbar()
        self._redraw_visible_rows()
    
    def clear(self):
        """Clear all data"""
        self.data = []
        self.scroll_position = 0
        self.selected_row = None
        self.hovered_row = None
        self.canvas.delete("all")
        self._update_scrollbar()
    
    def add_row(self, row_data):
        """Add a single row"""
        self.data.append(row_data)
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
