"""
Gateway Arch Generator GUI

Graphical interface for generating Gateway Arch schematics with
customizable options and preview.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import json
from pathlib import Path
from arch_generator import ArchGenerator


# Settings file location (in user's config directory or app directory)
def get_settings_path() -> Path:
    """Get the path to the settings file."""
    # Try XDG config directory first (Linux)
    xdg_config = os.environ.get('XDG_CONFIG_HOME')
    if xdg_config:
        config_dir = Path(xdg_config) / 'theresthearch'
    else:
        # Fallback to home directory
        config_dir = Path.home() / '.config' / 'theresthearch'
    
    # Create directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'settings.json'


DEFAULT_SETTINGS = {
    'scale': 0.33,
    'girth_scale': 0.33,
    'leg_thickness_scale': 1.0,
    'lock_scales': True,
    'hollow': True,
    'thickness': 1,
    'primary_block': 'minecraft:iron_block',
    'primary_block_display': 'Iron Block',
    'corner_block': '',
    'corner_block_display': 'Same as Primary',
    'output_file': 'gateway_arch.litematic',
}


class ArchGeneratorGUI:
    """GUI application for Gateway Arch generator."""
    
    # Common Minecraft blocks for selection
    BLOCK_OPTIONS = [
        ("Quartz Block", "minecraft:quartz_block"),
        ("Smooth Quartz", "minecraft:smooth_quartz"),
        ("White Concrete", "minecraft:white_concrete"),
        ("Light Gray Concrete", "minecraft:light_gray_concrete"),
        ("Gray Concrete", "minecraft:gray_concrete"),
        ("Stone Bricks", "minecraft:stone_bricks"),
        ("Polished Andesite", "minecraft:polished_andesite"),
        ("Polished Diorite", "minecraft:polished_diorite"),
        ("Prismarine", "minecraft:prismarine"),
        ("Iron Block", "minecraft:iron_block"),
        ("Diamond Block", "minecraft:diamond_block"),
        ("Gold Block", "minecraft:gold_block"),
        ("Obsidian", "minecraft:obsidian"),
        ("Blackstone", "minecraft:blackstone"),
        ("Deepslate Tiles", "minecraft:deepslate_tiles"),
    ]
    
    CORNER_OPTIONS = [
        ("Same as Primary", None),
        ("Quartz Pillar", "minecraft:quartz_pillar"),
        ("Purpur Pillar", "minecraft:purpur_pillar"),
        ("Stone Brick Stairs", "minecraft:stone_brick_stairs"),
        ("Polished Andesite Stairs", "minecraft:polished_andesite_stairs"),
        ("Dark Oak Log", "minecraft:dark_oak_log"),
        ("Oak Log", "minecraft:oak_log"),
        ("Stripped Oak Log", "minecraft:stripped_oak_log"),
        ("Bone Block", "minecraft:bone_block"),
    ]
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Gateway Arch Generator")
        self.root.geometry("1000x1430")
        self.root.resizable(True, True)
        
        # Load saved settings
        self.settings = self.load_settings()
        
        # Variables (initialized from saved settings)
        self.scale_var = tk.DoubleVar(value=self.settings['scale'])
        self.girth_scale_var = tk.DoubleVar(value=self.settings['girth_scale'])
        self.leg_thickness_scale_var = tk.DoubleVar(value=self.settings['leg_thickness_scale'])
        self.lock_scales_var = tk.BooleanVar(value=self.settings['lock_scales'])
        self.hollow_var = tk.BooleanVar(value=self.settings['hollow'])
        self.thickness_var = tk.IntVar(value=self.settings['thickness'])
        self.primary_block_var = tk.StringVar(value=self.settings['primary_block'])
        self.primary_block_display = tk.StringVar(value=self.settings['primary_block_display'])
        self.corner_block_var = tk.StringVar(value=self.settings['corner_block'])
        self.corner_block_display = tk.StringVar(value=self.settings['corner_block_display'])
        self.output_file_var = tk.StringVar(value=self.settings['output_file'])
        
        # Preview variables
        self.preview_blocks = {}
        self.preview_dimensions = {}
        
        # Debouncing for sliders
        self.update_timer = None
        
        # Settings save timer (debounced)
        self.settings_save_timer = None
        
        # Create UI
        self.create_widgets()
        self.update_preview()
        
        # Save settings on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def load_settings(self) -> dict:
        """Load settings from disk, returning defaults if not found."""
        settings_path = get_settings_path()
        try:
            if settings_path.exists():
                with open(settings_path, 'r') as f:
                    saved = json.load(f)
                # Merge with defaults to handle missing keys from older versions
                return {**DEFAULT_SETTINGS, **saved}
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Warning: Could not load settings: {e}")
        return DEFAULT_SETTINGS.copy()
    
    def save_settings(self):
        """Save current settings to disk."""
        settings = {
            'scale': self.scale_var.get(),
            'girth_scale': self.girth_scale_var.get(),
            'leg_thickness_scale': self.leg_thickness_scale_var.get(),
            'lock_scales': self.lock_scales_var.get(),
            'hollow': self.hollow_var.get(),
            'thickness': self.thickness_var.get(),
            'primary_block': self.primary_block_var.get(),
            'primary_block_display': self.primary_block_display.get(),
            'corner_block': self.corner_block_var.get(),
            'corner_block_display': self.corner_block_display.get(),
            'output_file': self.output_file_var.get(),
        }
        
        settings_path = get_settings_path()
        try:
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=2)
        except (IOError, OSError) as e:
            print(f"Warning: Could not save settings: {e}")
    
    def schedule_settings_save(self):
        """Schedule a settings save with debouncing (avoid saving on every slider tick)."""
        if self.settings_save_timer:
            self.root.after_cancel(self.settings_save_timer)
        self.settings_save_timer = self.root.after(1000, self.save_settings)
    
    def on_close(self):
        """Handle window close - save settings before exit."""
        self.save_settings()
        self.root.destroy()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title = ttk.Label(
            main_frame,
            text="Gateway Arch Schematic Generator",
            font=("Arial", 16, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Description
        desc = ttk.Label(
            main_frame,
            text="Generate a Minecraft schematic of the Gateway Arch using the mathematical catenary equation.",
            wraplength=950,
            justify=tk.CENTER
        )
        desc.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        row = 2
        
        # Scale Options
        scale_frame = ttk.LabelFrame(main_frame, text="Scale Options", padding="10")
        scale_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Lock scales checkbox
        lock_check = ttk.Checkbutton(
            scale_frame,
            text="🔒 Lock height and width together (authentic proportions)",
            variable=self.lock_scales_var,
            command=self.on_lock_changed
        )
        lock_check.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Height scale
        ttk.Label(scale_frame, text="Height Scale:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.scale_slider = ttk.Scale(
            scale_frame,
            from_=0.1,
            to=2.0,
            orient=tk.HORIZONTAL,
            variable=self.scale_var,
            command=lambda _: self.on_height_scale_changed()
        )
        self.scale_slider.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.scale_label = ttk.Label(scale_frame, text="0.50 (315 blocks tall)")
        self.scale_label.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Girth scale
        ttk.Label(scale_frame, text="Width Scale:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.girth_slider = ttk.Scale(
            scale_frame,
            from_=0.1,
            to=2.0,
            orient=tk.HORIZONTAL,
            variable=self.girth_scale_var,
            command=lambda _: self.on_width_scale_changed()
        )
        self.girth_slider.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.girth_label = ttk.Label(scale_frame, text="0.50 (315 blocks wide)")
        self.girth_label.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        
        # Leg thickness scale (chunkiness)
        ttk.Label(scale_frame, text="Leg Thickness:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.leg_thickness_slider = ttk.Scale(
            scale_frame,
            from_=0.5,
            to=5.0,
            orient=tk.HORIZONTAL,
            variable=self.leg_thickness_scale_var,
            command=lambda _: self.on_leg_thickness_changed()
        )
        self.leg_thickness_slider.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.leg_thickness_label = ttk.Label(scale_frame, text="1.00× (proportional)")
        self.leg_thickness_label.grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
        
        scale_frame.columnconfigure(1, weight=1)
        
        ttk.Label(
            scale_frame,
            text="Height and width can be scaled independently. 1.0 = Full size (630 blocks)",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 2))
        
        ttk.Label(
            scale_frame,
            text="Leg Thickness makes the triangular cross-section chunkier. Increase for smaller scales.",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        # Structure Options
        struct_frame = ttk.LabelFrame(main_frame, text="Structure Options", padding="10")
        struct_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        hollow_check = ttk.Checkbutton(
            struct_frame,
            text="Hollow Interior",
            variable=self.hollow_var,
            command=self.on_hollow_changed
        )
        hollow_check.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        ttk.Label(struct_frame, text="Wall Thickness:").grid(row=1, column=0, sticky=tk.W, pady=5)
        thickness_spin = ttk.Spinbox(
            struct_frame,
            from_=1,
            to=10,
            textvariable=self.thickness_var,
            width=10,
            command=self.on_thickness_changed
        )
        thickness_spin.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(struct_frame, text="blocks").grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # Block Options
        block_frame = ttk.LabelFrame(main_frame, text="Block Types", padding="10")
        block_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(block_frame, text="Primary Block:").grid(row=0, column=0, sticky=tk.W, pady=5)
        # Build primary block values - show names, store block IDs
        primary_display_values = [name for name, _ in self.BLOCK_OPTIONS]
        self.primary_combo = ttk.Combobox(
            block_frame,
            textvariable=self.primary_block_display,
            values=primary_display_values,
            state="readonly",
            width=30
        )
        self.primary_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.primary_combo.bind('<<ComboboxSelected>>', self.on_primary_selected)
        
        ttk.Label(block_frame, text="Corner/Edge Block:").grid(row=1, column=0, sticky=tk.W, pady=5)
        # Build corner block values - show names, store block IDs
        corner_display_values = [name for name, _ in self.CORNER_OPTIONS]
        self.corner_combo = ttk.Combobox(
            block_frame,
            textvariable=self.corner_block_display,
            values=corner_display_values,
            state="readonly",
            width=30
        )
        self.corner_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.corner_combo.bind('<<ComboboxSelected>>', self.on_corner_selected)
        
        block_frame.columnconfigure(1, weight=1)
        
        ttk.Label(
            block_frame,
            text="Select 'Same as Primary' to use the same block for corners",
            font=("Arial", 8),
            foreground="gray"
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Preview Frame
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Dimensions preview
        dims_frame = ttk.Frame(preview_frame)
        dims_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(dims_frame, text="Overall Dimensions:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.overall_label = ttk.Label(dims_frame, text="---")
        self.overall_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=2)
        
        ttk.Label(dims_frame, text="Base Dimensions:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.base_label = ttk.Label(dims_frame, text="---")
        self.base_label.grid(row=1, column=1, sticky=tk.W, padx=10, pady=2)
        
        ttk.Label(dims_frame, text="Peak Dimensions:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.peak_label = ttk.Label(dims_frame, text="---")
        self.peak_label.grid(row=2, column=1, sticky=tk.W, padx=10, pady=2)
        
        # Block counts preview
        ttk.Separator(preview_frame, orient=tk.HORIZONTAL).grid(
            row=1, column=0, sticky=(tk.W, tk.E), pady=10
        )
        
        ttk.Label(preview_frame, text="Estimated Blocks:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        
        self.blocks_text = tk.Text(preview_frame, height=10, width=60, state=tk.DISABLED)
        self.blocks_text.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        blocks_scrollbar = ttk.Scrollbar(preview_frame, orient=tk.VERTICAL, command=self.blocks_text.yview)
        blocks_scrollbar.grid(row=3, column=1, sticky=(tk.N, tk.S))
        self.blocks_text['yscrollcommand'] = blocks_scrollbar.set
        
        # Output Options
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(output_frame, textvariable=self.output_file_var, width=40)
        output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        browse_btn = ttk.Button(output_frame, text="Browse...", command=self.browse_output)
        browse_btn.grid(row=0, column=2, padx=5, pady=5)
        
        output_frame.columnconfigure(1, weight=1)
        
        # Progress bar
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=400
        )
        self.progress_label = ttk.Label(self.progress_frame, text="")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
        
        self.generate_btn = ttk.Button(
            button_frame,
            text="Generate Schematic",
            command=self.generate_schematic,
            width=20
        )
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Update Preview",
            command=self.update_preview,
            width=20
        ).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def schedule_preview_update(self):
        """Schedule a preview update with debouncing."""
        # Cancel any pending update
        if self.update_timer:
            self.root.after_cancel(self.update_timer)
        
        # Schedule new update after 300ms of no slider movement
        self.update_timer = self.root.after(300, self.update_preview)
    
    def on_hollow_changed(self):
        """Handle hollow checkbox change."""
        self.update_preview()
        self.schedule_settings_save()
    
    def on_thickness_changed(self):
        """Handle thickness spinbox change."""
        self.update_preview()
        self.schedule_settings_save()
    
    def on_lock_changed(self):
        """Handle lock checkbox change."""
        if self.lock_scales_var.get():
            # When locking, sync girth to height
            self.girth_scale_var.set(self.scale_var.get())
            self.schedule_preview_update()
        self.schedule_settings_save()
    
    def on_height_scale_changed(self):
        """Handle height scale slider change."""
        if self.lock_scales_var.get():
            # If locked, sync width to height
            self.girth_scale_var.set(self.scale_var.get())
        self.schedule_preview_update()
        self.schedule_settings_save()
    
    def on_width_scale_changed(self):
        """Handle width scale slider change."""
        if self.lock_scales_var.get():
            # If locked, sync height to width
            self.scale_var.set(self.girth_scale_var.get())
        self.schedule_preview_update()
        self.schedule_settings_save()
    
    def on_leg_thickness_changed(self):
        """Handle leg thickness scale slider change."""
        self.schedule_preview_update()
        self.schedule_settings_save()
    
    def on_primary_selected(self, event=None):
        """Handle primary block selection."""
        display_name = self.primary_block_display.get()
        # Find the corresponding block ID
        for name, block_id in self.BLOCK_OPTIONS:
            if name == display_name:
                self.primary_block_var.set(block_id)
                break
        self.update_preview()
        self.schedule_settings_save()
    
    def on_corner_selected(self, event=None):
        """Handle corner block selection."""
        display_name = self.corner_block_display.get()
        # Find the corresponding block ID
        for name, block_id in self.CORNER_OPTIONS:
            if name == display_name:
                self.corner_block_var.set(block_id if block_id else "")
                break
        self.update_preview()
        self.schedule_settings_save()
    
    def browse_output(self):
        """Open file dialog to select output location."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".litematic",
            filetypes=[("Litematica files", "*.litematic"), ("All files", "*.*")],
            initialfile=self.output_file_var.get()
        )
        if filename:
            self.output_file_var.set(filename)
            self.schedule_settings_save()
    
    def update_preview(self):
        """Update the preview information."""
        try:
            scale = self.scale_var.get()
            girth_scale = self.girth_scale_var.get()
            leg_thickness_scale = self.leg_thickness_scale_var.get()
            hollow = self.hollow_var.get()
            thickness = self.thickness_var.get()
            primary = self.primary_block_var.get()
            corner = self.corner_block_var.get() or None
            
            # Update scale labels
            height = int(630 * scale)
            width = int(630 * girth_scale)
            self.scale_label.config(text=f"{scale:.2f} ({height} blocks tall)")
            self.girth_label.config(text=f"{girth_scale:.2f} ({width} blocks wide)")
            
            # Update leg thickness label with computed base width
            base_leg_blocks = int(54 * girth_scale * leg_thickness_scale)
            if leg_thickness_scale == 1.0:
                self.leg_thickness_label.config(text=f"{leg_thickness_scale:.2f}× (proportional, {base_leg_blocks} blocks)")
            else:
                self.leg_thickness_label.config(text=f"{leg_thickness_scale:.2f}× ({base_leg_blocks} blocks at base)")
            
            # Create generator
            generator = ArchGenerator(
                scale=scale,
                girth_scale=girth_scale,
                hollow=hollow,
                thickness=thickness,
                primary_block=primary,
                corner_block=corner,
                leg_thickness_scale=leg_thickness_scale
            )
            
            # Get dimensions
            dims = generator.calculate_dimensions()
            
            overall = dims['overall']
            self.overall_label.config(
                text=f"{overall[0]}W × {overall[1]}H × {overall[2]}D blocks"
            )
            
            base = dims['base']
            self.base_label.config(
                text=f"{base[0]}W × {base[1]}H × {base[2]}D blocks"
            )
            
            peak = dims['peak']
            self.peak_label.config(
                text=f"{peak[0]}W × {peak[1]}H × {peak[2]}D blocks"
            )
            
            # Estimate blocks (in background to avoid freezing UI)
            self.blocks_text.config(state=tk.NORMAL)
            self.blocks_text.delete(1.0, tk.END)
            self.blocks_text.insert(tk.END, "Calculating...\n")
            self.blocks_text.config(state=tk.DISABLED)
            
            # Run estimation in thread
            def estimate():
                blocks = generator.estimate_blocks()
                self.update_blocks_display(blocks)
            
            threading.Thread(target=estimate, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update preview: {e}")
    
    def update_blocks_display(self, blocks):
        """Update the blocks display with counts."""
        self.blocks_text.config(state=tk.NORMAL)
        self.blocks_text.delete(1.0, tk.END)
        
        total = sum(blocks.values())
        total_stacks = total / 64
        total_shulkers = total / (27 * 64)
        
        self.blocks_text.insert(tk.END, f"Total Blocks: {total:,}\n")
        self.blocks_text.insert(tk.END, f"Total Stacks: {total_stacks:,.1f}\n")
        self.blocks_text.insert(tk.END, f"Total Shulker Boxes: {total_shulkers:,.2f}\n\n")
        
        for block_type, count in sorted(blocks.items()):
            block_name = block_type.replace("minecraft:", "").replace("_", " ").title()
            stacks = count / 64
            shulkers = count / (27 * 64)
            
            self.blocks_text.insert(tk.END, f"{block_name}:\n")
            self.blocks_text.insert(tk.END, f"  {count:,} blocks\n")
            self.blocks_text.insert(tk.END, f"  {stacks:,.1f} stacks\n")
            self.blocks_text.insert(tk.END, f"  {shulkers:,.2f} shulker boxes\n")
        
        self.blocks_text.config(state=tk.DISABLED)
    
    def generate_schematic(self):
        """Generate the schematic."""
        try:
            # Validate output file
            output_file = self.output_file_var.get()
            if not output_file:
                messagebox.showerror("Error", "Please specify an output file")
                return
            
            # Get parameters
            scale = self.scale_var.get()
            girth_scale = self.girth_scale_var.get()
            leg_thickness_scale = self.leg_thickness_scale_var.get()
            hollow = self.hollow_var.get()
            thickness = self.thickness_var.get()
            primary = self.primary_block_var.get()
            corner = self.corner_block_var.get() or None
            
            # Disable generate button
            self.generate_btn.config(state=tk.DISABLED)
            
            # Show progress bar
            self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
            self.progress_label.grid(row=1, column=0, pady=5)
            self.progress_bar['value'] = 0
            self.progress_label.config(text="Starting...")
            
            # Generate in thread
            def generate():
                try:
                    generator = ArchGenerator(
                        scale=scale,
                        girth_scale=girth_scale,
                        hollow=hollow,
                        thickness=thickness,
                        primary_block=primary,
                        corner_block=corner,
                        leg_thickness_scale=leg_thickness_scale
                    )
                    
                    def progress(current, total, message):
                        percent = (current / total) * 100
                        self.root.after(0, lambda p=percent, m=message: self.update_progress(p, m))
                    
                    schematic = generator.generate(progress_callback=progress)
                    schematic.save(output_file)
                    
                    self.root.after(0, lambda f=output_file: self.generation_complete(f))
                    
                except Exception as e:
                    error_msg = str(e)
                    self.root.after(0, lambda err=error_msg: self.generation_error(err))
            
            threading.Thread(target=generate, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start generation: {e}")
            self.generate_btn.config(state=tk.NORMAL)
    
    def update_progress(self, percent, message):
        """Update progress bar."""
        self.progress_bar['value'] = percent
        self.progress_label.config(text=f"{message} ({percent:.1f}%)")
        self.root.update_idletasks()
    
    def generation_complete(self, filename):
        """Handle successful generation."""
        self.progress_bar.grid_remove()
        self.progress_label.grid_remove()
        self.generate_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo(
            "Success",
            f"Schematic generated successfully!\n\nSaved to: {filename}"
        )
    
    def generation_error(self, error_msg):
        """Handle generation error."""
        self.progress_bar.grid_remove()
        self.progress_label.grid_remove()
        self.generate_btn.config(state=tk.NORMAL)
        
        messagebox.showerror("Error", f"Failed to generate schematic:\n\n{error_msg}")


def main():
    """Run the GUI application."""
    root = tk.Tk()
    app = ArchGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

