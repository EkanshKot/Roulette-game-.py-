[roulette_readme.md](https://github.com/user-attachments/files/24990019/roulette_readme.md)
# Roulette Game - Python&#x20;





A desktop **Roulette game** featuring an interactive wheel, multiple bets, odds tracking, and persistent balance, built using Python's Tkinter.



I had built this originally a long back ago and it was incomplete,I have added some more features(odds etc for)and have also improved the UI.



However I built this program to understand for about Tkinter ,UI ,How to manage and save data and not for gambling purposes.I do not promote it nor partake in such activities.



## Features

- **Interactive Wheel**: Spins smoothly and lands precisely on a winning number.
- **Multiple Bets**: Place several bets per spin.
- **Bet Types**: Red, Black, Even, Odd, Number.
- **Odds & Expected Value**: Shows probability and expected payout per bet.
- **Stats Tracking**: Balance, net gain/loss, wins, losses, total bets, and spin history.
- **Tooltips**: Hover over wheel to see number, color, and odds.
- **Persistence**: Balance saved on exit in `roulette_save.json`.

## Game Interface

- **Left Panel** → Place bets, select bet type, enter number for "Number" bet, add or clear bets.
- **Center Panel** → Wheel canvas, spin button, result display, and tooltips.
- **Right Panel** → Balance, net, stats, total bets, and spin history.

## How to Play

1. Set **bet amount** using the entry or chip buttons (+10, +50, +100).
2. Select **bet type** (Red, Black, Even, Odd, Number).
3. Enter a **number** if choosing the “Number” bet type.
4. Click **Add Bet**. Repeat to place multiple bets.
5. Click **SPIN** → winning number is determined, balance updated, winning bets highlighted.

## File Structure

- `roulette.py` → Main Python script.
- `roulette_save.json` → Stores persistent balance.

## Here is the Detailed Function Explanation that I converted from a note file to md:

### 1. Setup & Global Variables

- `root` → Tkinter main window.
- `canvas_size`, `center`, `radius` → Wheel dimensions.
- `numbers` → Roulette numbers including "00".
- `reds` → Set of red numbers.
- `slice_angle` → Angle per slice.
- `rotation` → Current wheel rotation in degrees.
- `spinning` → Prevents multiple spins.
- `balance`, `net`, `spins`, `wins`, `losses` → Game stats stored as Tkinter `IntVar`.
- `bets_list` → Stores all active bets.
- `save_file` → JSON file for balance persistence.

### 2. Wheel Drawing Functions

**`draw_wheel(highlight=[])`**: Draws the wheel, slices, numbers, and optional highlight for winning number.

**`show_tooltip(event)`**\*\* / \*\*\*\*`hide_tooltip(event)`\*\*: Shows number info and odds on hover.

### 3. Betting Functions

**`add_bet()`**: Adds bet to `bets_list` and updates display.

**`update_bets_display()`**: Shows all current bets with type, amount, odds, and expected payout.

**`calculate_odds(bet)`**: Computes probability and expected payout for each bet type.

**`clear_bets()`**: Clears all active bets.

### 4. Spin Functions

**`spin()`**: Starts wheel spin if bets are present.

**`animate(steps, speed)`**: Animates wheel rotation, gradually slowing down.

**`finish_spin()`**: Determines winning number, resolves bets, updates balance/net/stats, highlights winning slices, clears bets.

**`highlight_winning_slice()`**: Flashes winning slice on the wheel.

### 5. Stats & UI Functions(Note\:i have also created a flowchart to showcase the program flow which is in the repo)

**`update_stats()`**: Updates spin stats, wins, losses, total bets.

**`update_bets_display()`**: Updates Left Panel with current bets and odds.

**`save_and_exit()`**: Saves balance to JSON and closes the app.

### 6. GUI Layout

- **Left Panel**: Bet amount, chip buttons, bet type selection, add/clear bets, current bets.
- **Center Panel**: Wheel, spin button, result, tooltip.
- **Right Panel**: Balance, net, stats, history.

### 7. Key Concepts Learned

1. **Tkinter GUI Design** →This took a lot of my time as I could not get the dimensions of the wheel to align at first and also could not get the panels right 

2. **Animation** →I tried to add a smooth effect to show the slow stopping of wheel

3. **Game Logic** → I had to figure out how to set payouts and handle multiple bets.



1. **Event Handling** →I have also shown odds for each number on the wheel using mouse hovering

2. **Persistent Data** →You can save the data wih JSON

3. **Data Management** →I had to use streamlined data formats like dictionaries of multiple Dimensions to store bets, winnings, etc

---

