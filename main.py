import ast
import operator as op
import customtkinter as ctk

OPS={ast.Add:op.add,ast.Sub:op.sub,ast.Mult:op.mul,ast.Div:op.truediv,ast.Mod:op.mod,ast.USub:op.neg,ast.UAdd:op.pos}

def safe_eval(expr):
    expr=expr.replace("×","*").replace("÷","/").replace("−","-")
    def walk(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
        if isinstance(n,ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](walk(n.operand))
        if isinstance(n,ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](walk(n.left),walk(n.right))
        raise ValueError("Invalid expression")
    return walk(ast.parse(expr,mode="eval").body)

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NovaCalc"); self.geometry("460x720"); self.minsize(360,600)
        self.expr=""; self.history=[]; self.dark=True
        self.grid_columnconfigure(0,weight=1); self.grid_rowconfigure(2,weight=1)
        self.header(); self.display(); self.keys(); self.bind("<Key>",self.key)
        self.theme()
    def header(self):
        f=ctk.CTkFrame(self,fg_color="transparent"); f.grid(row=0,column=0,sticky="ew",padx=18,pady=12)
        f.grid_columnconfigure(0,weight=1)
        self.title_lbl=ctk.CTkLabel(f,text="NOVA CALCULATOR",font=ctk.CTkFont(size=22,weight="bold")); self.title_lbl.grid(row=0,column=0,sticky="w")
        ctk.CTkButton(f,text="☼",width=45,command=self.toggle).grid(row=0,column=1,padx=4)
        ctk.CTkButton(f,text="⌑",width=45,command=self.show_history).grid(row=0,column=2,padx=4)
    def display(self):
        self.panel=ctk.CTkFrame(self,corner_radius=22,border_width=1); self.panel.grid(row=1,column=0,sticky="nsew",padx=18,pady=(0,14))
        self.panel.grid_columnconfigure(0,weight=1)
        self.expression=ctk.CTkLabel(self.panel,text="",anchor="e",font=ctk.CTkFont(size=16)); self.expression.grid(row=0,column=0,sticky="ew",padx=20,pady=(18,0))
        self.result=ctk.CTkLabel(self.panel,text="0",anchor="e",font=ctk.CTkFont(size=42,weight="bold")); self.result.grid(row=1,column=0,sticky="sew",padx=20,pady=(0,18))
    def keys(self):
        f=ctk.CTkFrame(self,fg_color="transparent"); f.grid(row=2,column=0,sticky="nsew",padx=18,pady=(0,18)); self.keyframe=f
        for i in range(4): f.grid_columnconfigure(i,weight=1,uniform="x")
        for i in range(5): f.grid_rowconfigure(i,weight=1,uniform="y")
        rows=[["AC","⌫","%","÷"],["7","8","9","×"],["4","5","6","−"],["1","2","3","+"],["±","0",".","="]]
        self.btns={}
        for r,row in enumerate(rows):
            for c,x in enumerate(row):
                b=ctk.CTkButton(f,text=x,corner_radius=16,height=55,font=ctk.CTkFont(size=19,weight="bold"),command=lambda v=x:self.press(v))
                b.grid(row=r,column=c,sticky="nsew",padx=4,pady=4); self.btns[x]=b
    def press(self,x):
        if x=="AC": self.expr=""
        elif x=="⌫": self.expr=self.expr[:-1]
        elif x=="=":
            try:
                v=safe_eval(self.expr); v=int(v) if isinstance(v,float) and v.is_integer() else v
                self.history.insert(0,(self.expr,str(v))); self.expr=str(v)
            except: self.result.configure(text="Error"); self.after(900,lambda:self.result.configure(text=self.expr or "0")); return
        elif x=="±": self.expr="-("+self.expr+")" if self.expr else "-"
        elif x=="%": self.expr+="/100"
        else: self.expr+=x
        self.expression.configure(text=self.expr); self.result.configure(text=self.expr or "0")
    def key(self,e):
        m={"*":"×","/":"÷","-":"−","\r":"="}
        if e.char in "0123456789.+%": self.press(e.char)
        elif e.char in m:self.press(m[e.char])
        elif e.keysym=="BackSpace":self.press("⌫")
        elif e.keysym=="Escape":self.press("AC")
        elif e.keysym=="Return":self.press("=")
    def toggle(self):
        self.dark=not self.dark; ctk.set_appearance_mode("dark" if self.dark else "light"); self.theme()
    def theme(self):
        bg="#0b1020" if self.dark else "#f3f6fa"; panel="#11182a" if self.dark else "#fff"; text="#fff" if self.dark else "#172033"
        self.configure(fg_color=bg); self.panel.configure(fg_color=panel); self.title_lbl.configure(text_color=text); self.expression.configure(text_color="#8f9bb3"); self.result.configure(text_color=text)
        for x,b in self.btns.items():
            b.configure(fg_color="#263552" if x in "÷×−+=" else "#182136" if x.isdigit() or x=="." else "#202b42",text_color="white")
    def show_history(self):
        w=ctk.CTkToplevel(self); w.title("History"); w.geometry("360x450")
        for e,r in self.history[:30]: ctk.CTkLabel(w,text=f"{e} = {r}",anchor="e").pack(fill="x",padx=15,pady=6)

if __name__=="__main__":
    ctk.set_default_color_theme("blue"); ctk.set_appearance_mode("dark"); Calculator().mainloop()
