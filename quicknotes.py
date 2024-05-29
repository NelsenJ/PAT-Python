import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style

class QuickNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Notes App")
        self.root.geometry("470x400")
        
        self.style = Style(theme='darkly')
        
        # Frame utama
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
        self.main_frame.grid_columnconfigure(2, weight=0)
        
        # Bar input di paling atas
        self.note_entry = ttk.Entry(self.main_frame, width=40)
        self.note_entry.grid(row=0, column=0, padx=(5, 5), pady=5, sticky="ew")
        self.set_note_placeholder()
        
        # Tombol Tambah catatan
        self.add_button = ttk.Button(self.main_frame, text="Tambah", command=self.add_note)
        self.add_button.grid(row=0, column=1, padx=(5, 5), pady=5, sticky="ew")
        
        # Tombol Done
        self.done_button = ttk.Button(self.main_frame, text="Done", command=self.done_notes)
        self.done_button.grid(row=0, column=2, padx=(5, 5), pady=5, sticky="ew")
        
        # Listbox untuk daftar catatan
        self.notes_listbox = tk.Listbox(self.main_frame, width=60)
        self.notes_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
        self.notes_listbox.bind("<<ListboxSelect>>", self.load_selected_note)
        
        # Tombol Hapus
        self.delete_button = ttk.Button(self.main_frame, text="Hapus", command=self.delete_note)
        self.delete_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        # Tombol Simpan Perubahan
        self.save_button = ttk.Button(self.main_frame, text="Simpan Perubahan", command=self.save_note)
        self.save_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Tombol Edit
        self.edit_button = ttk.Button(self.main_frame, text="Edit", command=self.edit_note)
        self.edit_button.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
        
        # Bar pencarian
        self.search_entry = ttk.Entry(self.main_frame, width=40)
        self.search_entry.grid(row=3, column=0, columnspan=3, padx=(5, 5), pady=5, sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.search_notes)
        self.set_search_placeholder()

        # Inisialisasi daftar catatan
        self.notes = []
        self.current_edit_index = None
        self.load_notes()
    
    def set_search_placeholder(self):
        self.search_placeholder_color = "grey"
        self.default_fg_color = self.search_entry.cget("foreground")

        self.search_entry.insert(0, "Auto Search")
        self.search_entry.configure(foreground=self.search_placeholder_color)
        self.search_entry.bind("<FocusIn>", self.clear_search_placeholder)
        self.search_entry.bind("<FocusOut>", self.add_search_placeholder)
    
    def clear_search_placeholder(self, event):
        if self.search_entry.get() == "Auto Search":
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(foreground=self.default_fg_color)
    
    def add_search_placeholder(self, event):
        if self.search_entry.get() == "":
            self.search_entry.insert(0, "Auto Search")
            self.search_entry.configure(foreground=self.search_placeholder_color)
    
    def set_note_placeholder(self):
        self.note_placeholder_color = "grey"
        self.default_note_fg_color = self.note_entry.cget("foreground")

        self.note_entry.insert(0, "Isi catatan")
        self.note_entry.configure(foreground=self.note_placeholder_color)
        self.note_entry.bind("<FocusIn>", self.clear_note_placeholder)
        self.note_entry.bind("<FocusOut>", self.add_note_placeholder)
    
    def clear_note_placeholder(self, event):
        if self.note_entry.get() == "Isi catatan":
            self.note_entry.delete(0, tk.END)
            self.note_entry.configure(foreground=self.default_note_fg_color)
    
    def add_note_placeholder(self, event):
        if self.note_entry.get() == "":
            self.note_entry.insert(0, "Isi catatan")
            self.note_entry.configure(foreground=self.note_placeholder_color)
    
    def load_notes(self):
        self.notes_listbox.delete(0, tk.END)
        for note in self.notes:
            # Tambahkan spasi sebagai padding di awal dan akhir teks catatan
            padded_note = f"  {note['text']}  "
            self.notes_listbox.insert(tk.END, padded_note)
    
    def add_note(self):
        note_text = self.note_entry.get().strip()
        if note_text and note_text.lower() != "isi catatan":
            self.notes.append({"text": note_text, "category": ""})
            self.load_notes()
            self.note_entry.delete(0, tk.END)
            self.add_note_placeholder(None)
    
    def delete_note(self):
        selected_index = self.notes_listbox.curselection()
        if selected_index:
            del self.notes[selected_index[0]]
            self.load_notes()
            self.note_entry.delete(0, tk.END)
            self.add_note_placeholder(None)
    
    def save_note(self):
        if self.current_edit_index is not None:
            self.notes[self.current_edit_index]["text"] = self.note_entry.get().strip()
            self.load_notes()
            self.note_entry.delete(0, tk.END)
            self.current_edit_index = None
            self.add_note_placeholder(None)
    
    def load_selected_note(self, event):
        selected_index = self.notes_listbox.curselection()
        if selected_index:
            note_text = self.notes[selected_index[0]]["text"]
            self.note_entry.delete(0, tk.END)
            self.note_entry.insert(0, note_text)
            self.note_entry.configure(foreground=self.default_note_fg_color)
    
    def search_notes(self, event):
        search_text = self.search_entry.get().strip().lower()
        self.notes_listbox.delete(0, tk.END)
        for note in self.notes:
            if search_text in note["text"].lower():
                padded_note = f"  {note['text']}  "
                self.notes_listbox.insert(tk.END, padded_note)
    
    def edit_note(self):
        selected_index = self.notes_listbox.curselection()
        if selected_index:
            self.current_edit_index = selected_index[0]
            self.note_entry.delete(0, tk.END)
            self.note_entry.insert(0, self.notes[selected_index[0]]["text"])
            self.note_entry.configure(foreground=self.default_note_fg_color)
    
    def done_notes(self):
        notes_text = "\n".join(note["text"] for note in self.notes)
        full_text = f"List - list notes :\n{notes_text}"
        messagebox.showinfo("All Notes", full_text)
        self.root.destroy()

def main():
    root = tk.Tk()
    app = QuickNotesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
