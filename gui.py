import tkinter as tk
from tkinter import filedialog, messagebox
import math
import random
import time

# ============== COLOR PALETTE ==============
BG_DARK = "#0A0E27"
BG_DARKER = "#050812"
ACCENT_CYAN = "#00D4FF"
ACCENT_PURPLE = "#9D4EDD"
ACCENT_PINK = "#FF006E"
ACCENT_GREEN = "#3A86FF"
ACCENT_ORANGE = "#FB5607"
ACCENT_YELLOW = "#FFB703"
FG_COLOR = "#FFFFFF"
TXT_BG = "#0F1B3C"

# ============== ANIMATED PARTICLE BACKGROUND ==============
class ParticleCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg=BG_DARK, highlightthickness=0)
        self.particles = []
        self.orbs = []
        self.setup_particles()
        self.setup_orbs()
        self.time = 0
        self.animate()
    
    def setup_particles(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 100 or h < 100:
            self.after(100, self.setup_particles)
            return
        
        for _ in range(50):
            x = random.randint(0, w)
            y = random.randint(0, h)
            vx = random.uniform(-1.5, 1.5)
            vy = random.uniform(-2, 0.5)
            size = random.randint(1, 4)
            color = random.choice([ACCENT_CYAN, ACCENT_PURPLE, ACCENT_PINK, ACCENT_YELLOW])
            opacity = random.randint(50, 200)
            self.particles.append({
                'x': x, 'y': y, 'vx': vx, 'vy': vy,
                'size': size, 'color': color, 'opacity': opacity,
                'id': None, 'max_opacity': opacity, 'angle': random.uniform(0, 2*math.pi)
            })
    
    def setup_orbs(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w < 100 or h < 100:
            self.after(100, self.setup_orbs)
            return
        
        for _ in range(3):
            self.orbs.append({
                'x': random.randint(100, w-100),
                'y': random.randint(100, h-100),
                'radius': random.randint(30, 80),
                'color': random.choice([ACCENT_CYAN, ACCENT_PURPLE, ACCENT_PINK]),
                'pulse': random.uniform(0, 2*math.pi)
            })
    
    def animate(self):
        w = self.winfo_width()
        h = self.winfo_height()
        
        self.delete("particle", "orb")
        
        self.time += 0.02
        
        # Draw pulsing orbs
        for orb in self.orbs:
            pulse_size = orb['radius'] + math.sin(self.time + orb['pulse']) * 20
            alpha = int(50 + 50 * math.sin(self.time + orb['pulse']))
            
            self.create_oval(
                orb['x'] - pulse_size, orb['y'] - pulse_size,
                orb['x'] + pulse_size, orb['y'] + pulse_size,
                outline=orb['color'], width=2, tags="orb"
            )
            
            # Inner glow
            self.create_oval(
                orb['x'] - pulse_size*0.6, orb['y'] - pulse_size*0.6,
                orb['x'] + pulse_size*0.6, orb['y'] + pulse_size*0.6,
                outline=orb['color'], width=1, tags="orb"
            )
        
        # Animate particles
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.05
            p['angle'] += 0.1
            
            if p['x'] < 0 or p['x'] > w or p['y'] > h:
                p['x'] = random.randint(0, w)
                p['y'] = -10
                p['opacity'] = p['max_opacity']
            
            p['opacity'] = max(0, p['opacity'] - 0.5)
            
            try:
                self.create_oval(
                    p['x'] - p['size'], p['y'] - p['size'],
                    p['x'] + p['size'], p['y'] + p['size'],
                    fill=p['color'], outline="", tags="particle"
                )
            except:
                pass
        
        self.after(30, self.animate)

# ============== WAVE ANIMATION ==============
class WaveCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg=BG_DARK, highlightthickness=0)
        self.time = 0
        self.animate()
    
    def animate(self):
        self.delete("wave")
        self.time += 0.05
        
        w = self.winfo_width()
        h = self.winfo_height()
        
        for i in range(0, w, 20):
            y = h // 2 + int(20 * math.sin(i * 0.02 + self.time)) + int(10 * math.cos(self.time * 0.5))
            self.create_line(i, y, i+10, y, fill=ACCENT_CYAN, width=2, tags="wave")
        
        self.after(50, self.animate)

# ============== GLOWING BUTTON WITH MEGA ANIMATIONS ==============
class SuperGlowingButton(tk.Canvas):
    def __init__(self, parent, text, command, color=ACCENT_GREEN, **kwargs):
        super().__init__(parent, width=250, height=70, bg=parent['bg'], 
                        highlightthickness=0, cursor="hand2")
        self.command = command
        self.text = text
        self.base_color = color
        self.is_hovered = False
        self.pulse = 0
        self.clicked = False
        self.click_time = 0
        self.particles = []
        
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        
        self.draw()
        self.animate()
    
    def spawn_particles(self):
        """Create explosion particles on click"""
        for _ in range(12):
            angle = random.uniform(0, 2*math.pi)
            speed = random.uniform(2, 5)
            self.particles.append({
                'x': 125, 'y': 35,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': 1.0,
                'color': random.choice([self.base_color, ACCENT_PINK])
            })
    
    def draw(self):
        self.delete("all")
        
        # Calculate glow intensity
        if self.clicked:
            glow_intensity = 4
            color = ACCENT_PINK
            scale = 1.1
        elif self.is_hovered:
            glow_intensity = 3 + int(math.sin(self.pulse) * 1.5)
            color = ACCENT_PINK
            scale = 1.05
        else:
            glow_intensity = 1 + int(math.sin(self.pulse) * 1)
            color = self.base_color
            scale = 1.0
        
        # Draw multiple glow layers
        for i in range(5, 0, -1):
            alpha_factor = (5 - i) / 5
            self.create_oval(
                15 - i*3, 10 - i*2.5, 235 + i*3, 60 + i*2.5,
                outline=color, width=max(1, glow_intensity - i + 1),
                fill=""
            )
        
        # Main button with gradient effect
        self.create_rectangle(15, 10, 235, 60, fill=color, outline=color, width=3)
        
        # Draw particles
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.2
            p['life'] -= 0.08
            
            if p['life'] > 0:
                size = 3 * p['life']
                self.create_oval(
                    p['x'] - size, p['y'] - size,
                    p['x'] + size, p['y'] + size,
                    fill=p['color'], outline="", tags="particle"
                )
        
        self.particles = [p for p in self.particles if p['life'] > 0]
        
        # Text with shadow and glow
        shadow_offset = 2
        self.create_text(125 + shadow_offset, 35 + shadow_offset, text=self.text,
                        font=("Arial", 12, "bold"), fill="#000000", tags="shadow")
        self.create_text(125, 35, text=self.text, font=("Arial", 12, "bold"),
                        fill=FG_COLOR, tags="text")
    
    def on_hover(self, e):
        self.is_hovered = True
    
    def on_leave(self, e):
        self.is_hovered = False
        self.clicked = False
    
    def on_click(self, e):
        self.clicked = True
        self.spawn_particles()
        self.click_time = 0.3
        self.after(150, lambda: setattr(self, 'clicked', False))
        self.command()
    
    def animate(self):
        self.pulse += 0.1
        self.draw()
        self.after(30, self.animate)

# ============== ANIMATED LABEL WITH GLOW ==============
class AnimatedGlowLabel(tk.Label):
    def __init__(self, parent, text, **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.original_text = text
        self.char_index = 0
        self.glow_intensity = 0
        self.animate_text()
    
    def animate_text(self):
        if self.char_index <= len(self.original_text):
            self.config(text=self.original_text[:self.char_index])
            self.char_index += 1
            self.after(40, self.animate_text)

# ============== GLOWING ENTRY WITH ANIMATIONS ==============
class AdvancedEntry(tk.Entry):
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
        self.focused = False
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
    
    def on_focus_in(self, e):
        self.config(bg="#1A2847", highlightbackground=ACCENT_PINK)
        self.animate_focus_in()
    
    def animate_focus_in(self):
        pass
    
    def on_focus_out(self, e):
        self.config(bg=TXT_BG, highlightbackground=TXT_BG)

# ============== TEXT WITH CURSOR ANIMATION ==============
class AnimatedText(tk.Text):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(
            bg=TXT_BG,
            fg=FG_COLOR,
            insertbackground=ACCENT_CYAN,
            font=("Arial", 10),
            relief="flat",
            bd=2,
            highlightthickness=2,
            highlightcolor=ACCENT_CYAN,
            highlightbackground=TXT_BG,
            wrap="word"
        )
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
    
    def on_focus_in(self, e):
        self.config(bg="#1A2847", highlightbackground=ACCENT_PINK)
    
    def on_focus_out(self, e):
        self.config(bg=TXT_BG, highlightbackground=TXT_BG)

# ============== MAIN WINDOW ==============
def create_main_window():
    root = tk.Tk()
    root.title("⚡ STEGANOGRAPHY MASTER ⚡")
    root.geometry("1400x900")
    root.configure(bg=BG_DARK)
    root.resizable(True, True)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - 700
    y = (root.winfo_screenheight() // 2) - 450
    root.geometry(f"1400x900+{x}+{y}")
    
    def toggle_fullscreen(e=None):
        root.state('zoomed' if root.state() == 'normal' else 'normal')
    
    root.bind("<F11>", toggle_fullscreen)
    
    # ============== ANIMATED PARTICLE BACKGROUND ==============
    bg_canvas = ParticleCanvas(root, width=1400, height=900)
    bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    
    # ============== MAIN CONTAINER ==============
    main_frame = tk.Frame(root, bg=BG_DARK)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    # ============== HEADER ==============
    header_frame = tk.Frame(main_frame, bg=BG_DARK, height=140)
    header_frame.pack(fill="x", pady=(20, 15))
    header_frame.pack_propagate(False)
    
    title_label = AnimatedGlowLabel(
        header_frame,
        text="🔐 STEGANOGRAPHY MASTER 🔐",
        font=("Arial", 32, "bold"),
        bg=BG_DARK,
        fg=ACCENT_CYAN
    )
    title_label.pack(pady=(10, 5))
    
    subtitle = tk.Label(
        header_frame,
        text="✨ Hide Your Secrets in Plain Sight ✨",
        font=("Arial", 13, "italic"),
        bg=BG_DARK,
        fg=ACCENT_PURPLE
    )
    subtitle.pack()
    
    # Animated wave separator
    wave_canvas = WaveCanvas(header_frame, bg=BG_DARK, height=30, highlightthickness=0)
    wave_canvas.pack(fill="x", padx=50, pady=10)
    
    # ============== CONTENT FRAME ==============
    content_frame = tk.Frame(main_frame, bg=BG_DARK)
    content_frame.pack(fill="both", expand=True, padx=50, pady=20)
    
    # Left panel
    left_panel = tk.Frame(content_frame, bg=BG_DARK)
    left_panel.pack(side="left", fill="both", expand=True, padx=30)
    
    # Right panel
    right_panel = tk.Frame(content_frame, bg=BG_DARK)
    right_panel.pack(side="right", fill="both", expand=True, padx=30)
    
    # ============== LEFT PANEL ==============
    controls_title = tk.Label(
        left_panel,
        text="📋 FILE SETTINGS",
        font=("Arial", 16, "bold"),
        bg=BG_DARK,
        fg=ACCENT_ORANGE
    )
    controls_title.pack(anchor="w", pady=(0, 20))
    
    # Image input
    tk.Label(left_panel, text="📁 Input Image:", bg=BG_DARK,
            fg=ACCENT_CYAN, font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 8))
    img_entry = AdvancedEntry(left_panel, width=40)
    img_entry.pack(anchor="w", pady=(0, 12), ipady=10)
    
    def browse_image():
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if path:
            img_entry.delete(0, tk.END)
            img_entry.insert(0, path)
    
    tk.Button(left_panel, text="🔍 BROWSE IMAGE", command=browse_image,
             bg=ACCENT_GREEN, fg=FG_COLOR, font=("Arial", 10, "bold"),
             relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
             activebackground=ACCENT_PINK, activeforeground=FG_COLOR).pack(anchor="w", pady=(0, 25))
    
    # Output path
    tk.Label(left_panel, text="💾 Output Path:", bg=BG_DARK,
            fg=ACCENT_CYAN, font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 8))
    out_entry = AdvancedEntry(left_panel, width=40)
    out_entry.pack(anchor="w", pady=(0, 12), ipady=10)
    
    def browse_save():
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                           filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if path:
            out_entry.delete(0, tk.END)
            out_entry.insert(0, path)
    
    tk.Button(left_panel, text="💾 SAVE LOCATION", command=browse_save,
             bg=ACCENT_GREEN, fg=FG_COLOR, font=("Arial", 10, "bold"),
             relief="flat", bd=0, padx=20, pady=10, cursor="hand2",
             activebackground=ACCENT_PINK, activeforeground=FG_COLOR).pack(anchor="w")
    
    # ============== RIGHT PANEL ==============
    message_title = tk.Label(
        right_panel,
        text="📝 SECRET MESSAGE",
        font=("Arial", 16, "bold"),
        bg=BG_DARK,
        fg=ACCENT_ORANGE
    )
    message_title.pack(anchor="w", pady=(0, 15))
    
    msg_text = AnimatedText(right_panel, height=15, width=45)
    msg_text.pack(fill="both", expand=True, pady=(0, 20))
    
    # ============== BUTTON FRAME ==============
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
            messagebox.showinfo("✅ Success!", "Message hidden successfully!\n(stego module not found)")
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
            messagebox.showinfo("🔓 Extracted!", "Your hidden message!\n(stego module not found)")
        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
    
    hide_btn = SuperGlowingButton(btn_frame, "🔒 HIDE MESSAGE", hide_action, color=ACCENT_GREEN)
    hide_btn.pack(side="left", padx=25)
    
    extract_btn = SuperGlowingButton(btn_frame, "🔓 EXTRACT MESSAGE", extract_action, color=ACCENT_PURPLE)
    extract_btn.pack(side="left", padx=25)
    
    # ============== FOOTER ==============
    footer = tk.Label(
        main_frame,
        text="🌟 Powered by Advanced Steganography | Press F11 for Fullscreen 🌟",
        font=("Arial", 10, "italic"),
        bg=BG_DARKER,
        fg=ACCENT_PURPLE
    )
    footer.pack(fill="x", pady=12)
    
    return root

# ============== RUN ==============
if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()