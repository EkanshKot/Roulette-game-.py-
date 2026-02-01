# -*- coding: utf-8 -*-
"""
Created on Sun Jun  16 11:21:06 2024

@author: ekansh
"""
import tkinter as tk
import math
import random
import json
import os

root = tk.Tk()
root.title("Roulette")
root.geometry("1600x800")
root.configure(bg="white")

canvas_size = 520
center = canvas_size // 2
radius = 240

numbers = [
    "00",27,10,25,29,12,8,19,31,18,6,21,33,16,4,
    23,35,14,2,0,28,9,26,30,11,7,20,32,17,5,
    22,34,15,3,24,36,13,1
]

reds = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
slice_angle = 360 / len(numbers)
rotation = 0
spinning = False

balance = tk.IntVar()
net = tk.IntVar(value=0)
spins = tk.IntVar(value=0)
wins = tk.IntVar(value=0)
losses = tk.IntVar(value=0)
bets_list = []

save_file = "roulette_save.json"
if os.path.exists(save_file):
    with open(save_file, "r") as f:
        balance.set(json.load(f)["balance"])
else:
    balance.set(1000)

layout = tk.Frame(root, bg="white")
layout.pack(fill="both", expand=True)

left = tk.Frame(layout, bg="#f0f0f0", width=320)
left.pack(side="left", fill="y", padx=10, pady=10)

center_frame = tk.Frame(layout, bg="white")
center_frame.pack(side="left", expand=True)

right = tk.Frame(layout, bg="#f0f0f0", width=360)
right.pack(side="right", fill="y", padx=10, pady=10)

canvas = tk.Canvas(center_frame, width=canvas_size, height=canvas_size, bg="white", highlightthickness=0)
canvas.pack(pady=20)

winning_slices = []

def draw_wheel(highlight=[]):
    canvas.delete("all")
    for i, n in enumerate(numbers):
        start = rotation + i * slice_angle
        color = "#2ecc71" if n in ("0","00") else "#c0392b" if isinstance(n,int) and n in reds else "#111111"
        if i in highlight:
            color = "#f1c40f"
        canvas.create_arc(center-radius, center-radius, center+radius, center+radius,
                          start=start, extent=slice_angle, fill=color, outline="#d4af37", width=2)
        mid = math.radians(start + slice_angle / 2)
        x = center + math.cos(mid) * (radius - 35)
        y = center - math.sin(mid) * (radius - 35)
        canvas.create_text(x, y, text=str(n), fill="white", font=("Arial", 12, "bold"))
    canvas.create_polygon(center-12, 6, center+12, 6, center, 32, fill="#d4af37")

def show_tooltip(event):
    x, y = event.x, event.y
    dx = x - center
    dy = center - y
    angle = math.degrees(math.atan2(dy, dx))
    angle = (angle + 360) % 360
    idx = int((angle - rotation) % 360 / slice_angle)
    n = numbers[idx]
    if n in ("0","00"): color = "Green"
    elif isinstance(n,int) and n in reds: color = "Red"
    else: color = "Black"
    prob = 1/len(numbers)*100
    tooltip_label.config(text=f"Number: {n}\nColor: {color}\nOdds: {prob:.1f}%")
    tooltip_label.place(x=event.x+15, y=event.y+15)

def hide_tooltip(event):
    tooltip_label.place_forget()

canvas.bind("<Motion>", show_tooltip)
canvas.bind("<Leave>", hide_tooltip)

def spin():
    global spinning
    if spinning or not bets_list:
        return
    spinning = True
    total_steps = random.randint(120,180)
    animate(total_steps, 20)

def animate(steps, speed):
    global rotation
    if steps <= 0:
        finish_spin()
        return
    rotation += 7
    draw_wheel()
    next_speed = int(speed * 1.03)
    root.after(speed, lambda: animate(steps-1, next_speed))

def finish_spin():
    global spinning, winning_slices
    spins.set(spins.get()+1)
    idx = int((-rotation % 360) / slice_angle)
    result = numbers[idx]
    total_bet = sum(bet["amount"] for bet in bets_list)
    balance.set(balance.get() - total_bet)
    net_change = -total_bet
    win_count = 0
    winning_slices.clear()
    for bet in bets_list:
        win=False
        payout=0
        btype=bet["type"]
        bnumber=bet.get("number","")
        amount=bet["amount"]
        if btype=="Red" and isinstance(result,int) and result in reds: win=True; payout=amount*2
        elif btype=="Black" and isinstance(result,int) and result not in reds: win=True; payout=amount*2
        elif btype=="Even" and isinstance(result,int) and result%2==0: win=True; payout=amount*2
        elif btype=="Odd" and isinstance(result,int) and result%2==1: win=True; payout=amount*2
        elif btype=="Number" and str(result)==str(bnumber): win=True; payout=amount*36
        if win:
            balance.set(balance.get()+payout)
            net_change+=payout
            wins.set(wins.get()+1)
            win_count+=1
            winning_slices.append(numbers.index(result))
        else:
            losses.set(losses.get()+1)
    net.set(net.get()+net_change)
    result_text.set(f"Result: {result} → {win_count} Winning Bets!")
    highlight_winning_slice()
    history.insert(0,result)
    bets_list.clear()
    update_bets_display()
    spinning=False
    update_stats()

def highlight_winning_slice():
    for _ in range(6):
        draw_wheel(highlight=winning_slices)
        root.update()
        root.after(150)
        draw_wheel()
        root.update()
        root.after(150)

def add_bet():
    try:
        amount=int(bet_amount.get())
        if amount<=0 or amount>balance.get(): return
        bet={"type":bet_type.get(),"number":bet_number.get(),"amount":amount}
        bets_list.append(bet)
        update_bets_display()
    except: pass

def update_bets_display():
    bets_box.delete(0, tk.END)
    for bet in bets_list:
        display=f"{bet['type']}"
        if bet['type']=="Number": display+=f" ({bet['number']})"
        prob, exp=calculate_odds(bet)
        display+=f" → ${bet['amount']} | Odds: {prob:.1f}% | Exp: {exp:.2f}"
        bets_box.insert(tk.END, display)

def calculate_odds(bet):
    btype=bet['type']
    if btype=="Red": prob=len(reds)/len(numbers)*100; exp=bet['amount']*2*len(reds)/len(numbers)
    elif btype=="Black": prob=(len(numbers)-len(reds)-2)/len(numbers)*100; exp=bet['amount']*2*(len(numbers)-len(reds)-2)/len(numbers)
    elif btype=="Even": prob=18/len(numbers)*100; exp=bet['amount']*2*18/len(numbers)
    elif btype=="Odd": prob=18/len(numbers)*100; exp=bet['amount']*2*18/len(numbers)
    elif btype=="Number": prob=1/len(numbers)*100; exp=bet['amount']*36/len(numbers)
    return prob, exp

def clear_bets():
    bets_list.clear()
    update_bets_display()

def update_stats():
    stats_text.set(
        f"Total Spins: {spins.get()}\nWins: {wins.get()}\nLosses: {losses.get()}\n"
        f"Total Bets Placed: {sum(bet['amount'] for bet in bets_list)}"
    )

def save_and_exit():
    with open(save_file,"w") as f:
        json.dump({"balance":balance.get()},f)
    root.destroy()

# LEFT PANEL (BETS)
tk.Label(left,text="BET AMOUNT",fg="black",bg="#f0f0f0",font=("Arial",14,"bold")).pack(pady=10)
bet_amount=tk.IntVar(value=50)
tk.Entry(left,textvariable=bet_amount,justify="center",font=("Arial",14)).pack()
chips=tk.Frame(left,bg="#f0f0f0"); chips.pack(pady=6)
tk.Button(chips,text="+10",command=lambda: bet_amount.set(bet_amount.get()+10)).pack(side="left",padx=4)
tk.Button(chips,text="+50",command=lambda: bet_amount.set(bet_amount.get()+50)).pack(side="left",padx=4)
tk.Button(chips,text="+100",command=lambda: bet_amount.set(bet_amount.get()+100)).pack(side="left",padx=4)
tk.Button(chips,text="Clear",command=lambda: bet_amount.set(0)).pack(side="left",padx=4)
tk.Label(left,text="BET TYPE",fg="black",bg="#f0f0f0",font=("Arial",14,"bold")).pack(pady=10)
bet_type=tk.StringVar(value="Red")
for o in ["Red","Black","Even","Odd","Number"]:
    tk.Radiobutton(left,text=o,variable=bet_type,value=o,fg="black",bg="#f0f0f0",selectcolor="#f0f0f0",font=("Arial",12)).pack(anchor="w")
bet_number=tk.StringVar()
tk.Entry(left,textvariable=bet_number,justify="center",font=("Arial",12)).pack(pady=5)
tk.Button(left,text="Add Bet",command=add_bet,font=("Arial",12,"bold")).pack(pady=6)
tk.Button(left,text="Clear Bets",command=clear_bets,font=("Arial",12,"bold")).pack(pady=4)
tk.Label(left,text="Current Bets",fg="black",bg="#f0f0f0",font=("Arial",14,"bold")).pack(pady=6)
bets_box=tk.Listbox(left,height=12,font=("Arial",12))
bets_box.pack(fill="both",padx=5,pady=4)

# CENTER PANEL
tk.Button(center_frame,text="SPIN",font=("Arial",30,"bold"),bg="#d4af37",fg="black",width=12,command=spin).pack(pady=12)
result_text=tk.StringVar(value="")
tk.Label(center_frame,textvariable=result_text,fg="#d4af37",bg="white",font=("Arial",18,"bold")).pack()
tooltip_label=tk.Label(center_frame,text="",bg="#f1c40f",fg="black",font=("Arial",10,"bold"),bd=1,relief="solid")

# RIGHT PANEL 
tk.Label(right,text="BALANCE",fg="black",bg="#f0f0f0",font=("Arial",14,"bold")).pack(pady=8)
tk.Label(right,textvariable=balance,fg="black",bg="#f0f0f0",font=("Arial",16,"bold")).pack()
tk.Label(right,text="NET",fg="black",bg="#f0f0f0",font=("Arial",14,"bold")).pack(pady=6)
tk.Label(right,textvariable=net,fg="black",bg="#f0f0f0",font=("Arial",16,"bold")).pack()
stats_text=tk.StringVar()
tk.Label(right,text="STATS",fg="black",bg="#f0f0f0",font=("Arial",14,"bold")).pack(pady=8)
tk.Label(right,textvariable=stats_text,fg="black",bg="#f0f0f0",font=("Arial",12),justify="left").pack()
update_stats()
tk.Label(right,text="HISTORY",fg="black",bg="#f0f0f0",font=("Arial",14,"bold")).pack(pady=8)
history=tk.Listbox(right,height=18,font=("Arial",12))
history.pack(fill="y",padx=10)

draw_wheel()
root.protocol("WM_DELETE_WINDOW",save_and_exit)
root.mainloop()
