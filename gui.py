import tkinter as tk
from tkinter import filedialog, messagebox
import math
import random
import time

# ============== ADVANCED STYLING CONSTANTS ==============
BG_DARK = "#0A0E27"
BG_DARKER = "#050812"
ACCENT_CYAN = "#00D4FF"
ACCENT_PURPLE = "#9D4EDD"
ACCENT_PINK = "#FF006E"
ACCENT_GREEN = "#3A86FF"
ACCENT_ORANGE = "#FB5607"
FG_COLOR = "#FFFFFF"
TXT_BG = "#0F1B3C"

# ============== ANIMATED PARTICLE BACKGROUND ==============
class ParticleCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg=BG_DARK, highlightthickness=0)
        self.particles = []
        self.setup_particles()
        self.animate()
    
    def setup_particles(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 100 or h < 100:
            self.after(100, self.setup_particles)
            return
        
        for _ in range(40):
            x = random.randint(0, w)
            y = random.randint(0, h)
            vx = random.uniform(-1, 1)
            vy = random.uniform(-2, 0.5)
            size = random.randint(1, 3)
            color = random.choice([ACCENT_CYAN, ACCENT_PURPLE, ACCENT_PINK])
            opacity = random.randint(50, 200)
            self.particles.append({
                'x': x, 'y': y, 'vx': vx, 'vy': vy,
                'size': size, 'color': color, 'opacity': opacity,
                'id': None, 'max_opacity': opacity
            })
    
    def animate(self):
        w = self.winfo_width()
        h = self.winfo_height()
        
        self.delete("particle")
        
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.1  # gravity
            
            if p['x'] < 0 or p['x'] > w or p['y'] > h:
                p['x'] = random.randint(0, w)
                p['y'] = -10
                p['opacity'] = p['max_opacity']
            
            # Fade effect
            p['opacity'] = max(0, p['opacity'] - 0.3)
            
            try:
                self.create_oval(
                    p['x'] - p['size'], p['y'] - p['size'],
                    p['x'] + p['size'], p['y'] + p['size'],
                    fill=p['color'], outline="", tags="particle"
                )
            except:
                pass
        
        self.after(30, self.animate)

# ============== GLOWING BUTTON WITH ANIMATION ==============
class GlowingButton(tk.Canvas):
    def __init__(self, parent, text, command, color=ACCENT_GREEN, **kwargs):
        super().__init__(parent, width=220, height=55, bg=parent['bg'], 
                        highlightthickness=0, cursor="hand2")
        self.command = command
        self.text = text
        self.base_color = color
        self.is_hovered = False
        self.pulse = 0
        self.clicked = False
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        
        self.draw()
        self.animate_glow()
    
    def draw(self):
        self.delete("all")
        
        if self.clicked:
            color = ACCENT_PINK
            glow_width = 4
        elif self.is_hovered:
            color = ACCENT_PINK
            glow_width = 3
        else:
            color = self.base_color
            glow_width = 1 + int(math.sin(self.pulse) * 2)
        
        # Multiple glow rings
        for i in range(3, 0, -1):
            alpha = int(100 / i)
            self.create_oval(
                10 - i*2, 8 - i*2, 210 + i*2, 52 + i*2,
                outline=color, width=max(1, glow_width - i),
                fill=""
            )
        
        # Main button
        self.create_rectangle(10, 8, 210, 52, fill=color, outline=color, width=2)
        
        # Text with shadow
        self.create_text(110, 31, text=self.text, font=("Arial", 11, "bold"),
                        fill="#000000", tags="shadow")
        self.create_text(109, 30, text=self.text, font=("Arial", 11, "bold"),
                        fill=FG_COLOR, tags="text")
    
    def on_hover(self, e):
        self.is_hovered = True
    
    def on_leave(self, e):
        self.is_hovered = False
        self.clicked = False
    
    def on_click(self, e):
        self.clicked = True
        self.after(200, lambda: setattr(self, 'clicked', False))
        self.command()
    
    def animate_glow(self):
        self.pulse += 0.1
        self.draw()
        self.after(30, self.animate_glow)

# ============== ANIMATED LABEL ==============
class AnimatedLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.original_text = text
        self.char_index = 0
        self.animate_text()
    
    def animate_text(self):
        if self.char_index <= len(self.original_text):
            self.config(text=self.original_text[:self.char_index])
            self.char_index += 1
            self.after(30, self.animate_text)

# ============== GLOWING ENTRY ==============
class GlowingEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            bg=TXT_BG,
            fg=FG_COLOR,
            insertbackground=ACCENT_CYAN,
            font=("Arial", 11),
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightcolor=ACCENT_CYAN,
            highlightbackground=TXT_BG
        )
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
    
    def on_focus_in(self, e):
        self.config(bg="#1A2847", highlightbackground=ACCENT_CYAN)
    
    def on_focus_out(self, e):
        self.config(bg=TXT_BG, highlightbackground=TXT_BG)

# ============== MAIN WINDOW SETUP ==============
def create_main_window():
    root = tk.Tk()
    root.title("⚡ STEGANOGRAPHY MASTER ⚡")
    root.geometry("1100x800")
    root.configure(bg=BG_DARK)
    root.resizable(True, True)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 600
    y = (root.winfo_screenheight() // 2) - 400
    root.geometry(f"1200x800+{x}+{y}")
    
    # Make fullscreen toggle possible
    def toggle_fullscreen(e=None):
        root.state('zoomed' if root.state() == 'normal' else 'normal')
    
    root.bind("<F11>", toggle_fullscreen)
    
    # ============== ANIMATED BACKGROUND ==============
    bg_canvas = ParticleCanvas(root, width=1200, height=800)
    bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    
    # ============== MAIN CONTAINER ==============
    main_frame = tk.Frame(root, bg=BG_DARK)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # ============== HEADER WITH ANIMATION ==============
    header_frame = tk.Frame(main_frame, bg=BG_DARK, height=120)
    header_frame.pack(fill="x", pady=(20, 10))
    header_frame.pack_propagate(False)
    
    title_label = AnimatedLabel(
        header_frame,
        text="🔐 STEGANOGRAPHY MASTER 🔐",
        font=("Arial", 28, "bold"),
        bg=BG_DARK,
        fg=ACCENT_CYAN
    )
    title_label.pack(pady=(10, 5))
    
    subtitle = tk.Label(
        header_frame,
        text="✨ Hide Your Secrets in Plain Sight ✨",
        font=("Arial", 12, "italic"),
        bg=BG_DARK,
        fg=ACCENT_PURPLE
    )
    subtitle.pack()
    
    # Animated line separator
    line_canvas = tk.Canvas(
        header_frame,
        bg=BG_DARK,
        height=3,
        highlightthickness=0
    )
    line_canvas.pack(fill="x", padx=50, pady=10)
    
    line_canvas.create_line(0, 1, 1200, 1, fill=ACCENT_CYAN, width=2)
    line_canvas.create_line(0, 2, 1200, 2, fill=ACCENT_PURPLE, width=1)
    
    # ============== CONTENT FRAME ==============
    content_frame = tk.Frame(main_frame, bg=BG_DARK)
    content_frame.pack(fill="both", expand=True, padx=40, pady=20)
    
    # Left panel
    left_panel = tk.Frame(content_frame, bg=BG_DARK)
    left_panel.pack(side="left", fill="both", expand=True, padx=20)
    
    # Right panel
    right_panel = tk.Frame(content_frame, bg=BG_DARK)
    right_panel.pack(side="right", fill="both", expand=True, padx=20)
    
    # ============== LEFT PANEL - CONTROLS ==============
    controls_title = tk.Label(
        left_panel,
        text="📋 FILE SETTINGS",
        font=("Arial", 14, "bold"),
        bg=BG_DARK,
        fg=ACCENT_ORANGE
    )
    controls_title.pack(anchor="w", pady=(0, 15))
    
    # Image input
    tk.Label(left_panel, text="📁 Input Image:", bg=BG_DARK, 
            fg=ACCENT_CYAN, font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
    img_entry = GlowingEntry(left_panel, width=40)
    img_entry.pack(anchor="w", pady=(0, 10), ipady=8)
    
    def browse_image():
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if path:
            img_entry.delete(0, tk.END)
            img_entry.insert(0, path)
    
    tk.Button(left_panel, text="🔍 Browse Image", command=browse_image,
             bg=ACCENT_GREEN, fg=FG_COLOR, font=("Arial", 9, "bold"),
             relief="flat", bd=0, padx=15, pady=8).pack(anchor="w", pady=(0, 20))
    
    # Output path
    tk.Label(left_panel, text="💾 Output Path:", bg=BG_DARK,
            fg=ACCENT_CYAN, font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 5))
    out_entry = GlowingEntry(left_panel, width=40)
    out_entry.pack(anchor="w", pady=(0, 10), ipady=8)
    
    def browse_save():
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                           filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if path:
            out_entry.delete(0, tk.END)
            out_entry.insert(0, path)
    
    tk.Button(left_panel, text="💾 Save Location", command=browse_save,
             bg=ACCENT_GREEN, fg=FG_COLOR, font=("Arial", 9, "bold"),
             relief="flat", bd=0, padx=15, pady=8).pack(anchor="w")
    
    # ============== RIGHT PANEL - MESSAGE ==============
    message_title = tk.Label(
        right_panel,
        text="📝 SECRET MESSAGE",
        font=("Arial", 14, "bold"),
        bg=BG_DARK,
        fg=ACCENT_ORANGE
    )
    message_title.pack(anchor="w", pady=(0, 15))
    
    msg_text = tk.Text(
        right_panel,
        height=12,
        width=45,
        bg=TXT_BG,
        fg=FG_COLOR,
        insertbackground=ACCENT_CYAN,
        font=("Arial", 10),
        relief="flat",
        bd=2,
        highlightthickness=1,
        highlightcolor=ACCENT_CYAN,
        highlightbackground=TXT_BG,
        wrap="word"
    )
    msg_text.pack(fill="both", expand=True, pady=(0, 20))
    
    # ============== BUTTONS FRAME ==============
    btn_frame = tk.Frame(main_frame, bg=BG_DARK)
    btn_frame.pack(pady=20)
    
    def hide_action():
        img_path = img_entry.get()
        out_path = out_entry.get()
        msg = msg_text.get("1.0", tk.END).strip()
        
        if not img_path or not out_path or not msg:
            messagebox.showerror("⚠️ Error", "Please fill all fields!")
            return
        
        try:
            from stego import hide_message
            result = hide_message(img_path, out_path, msg)
            messagebox.showinfo("✅ Success", result)
        except ImportError:
            messagebox.showinfo("✅ Simulated", "Message hidden successfully!\n(stego module not found)")
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
    
    def extract_action():
        img_path = img_entry.get()
        
        if not img_path:
            messagebox.showerror("⚠️ Error", "Please select an image!")
            return
        
        try:
            from stego import extract_message
            result = extract_message(img_path)
            messagebox.showinfo("🔓 Extracted Message", result)
        except ImportError:
            messagebox.showinfo("🔓 Simulated", "Extracted: Your hidden message!\n(stego module not found)")
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
    
    hide_btn = GlowingButton(btn_frame, "🔒 HIDE MESSAGE", hide_action, color=ACCENT_GREEN)
    hide_btn.pack(side="left", padx=20)
    
    extract_btn = GlowingButton(btn_frame, "🔓 EXTRACT MESSAGE", extract_action, color=ACCENT_PURPLE)
    extract_btn.pack(side="left", padx=20)
    
    # ============== FOOTER ==============
    footer = tk.Label(
        main_frame,
        text="🌟 Powered by Advanced Steganography | Press F11 for Fullscreen 🌟",
        font=("Arial", 9, "italic"),
        bg=BG_DARKER,
        fg=ACCENT_PURPLE
    )
    footer.pack(fill="x", pady=10)
    
    return root

# ============== RUN APPLICATION ==============
if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()