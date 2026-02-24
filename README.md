<p align="center">
      🌐 English | <a href="https://github.com/Berkwe/Valorant-instalocker/blob/main/readme.tr.md">Türkçe</a>
</p>

# 🛠️ Valorant Instalocker V1.9.0

## Promotional Video
<video src="https://github.com/user-attachments/assets/ff1e1677-f2c0-43a8-bd70-e4cf0cd09c0b" autoplay loop muted playsinline></video>
<a href="https://www.youtube.com/watch?v=BUttrI9untI">**FULL VIDEO**</a>

Valorant Instalocker is a fast and reliable auto agent locking tool for Riot Games’ Valorant. Often referred to as a Valorant instalock tool or agent picker. It automatically selects and locks your chosen agent using the official Valorant API. The ban risk is extremely low (I haven't been banned for 3-4 years). The program is written in Python, includes a simple CLI (console interface), and works as a lightweight instalocker script that speeds up the agent selection phase significantly. (And yes, this text was written by AI)

# ❗IMPORTANT
**This version is still in the testing phase. Please report any errors you encounter or share your development ideas in the [issues](https://github.com/Berkwe/Valorant-instalocker/issues) section.**

---

## 🆕 What's New v1.9

### 🌟 Major Updates (Map-Based Selection System)
* **Map-Specific Agent Selection/Locking:** Advanced macro system added that allows you to pre-define specific agents for every individual map.
* **Profile Creation Feature:** Customizable profile system implemented to save and manage your map-based configurations.
* **Quick Profile Selector & Shortcuts:** New fast-access mechanism added for seamless switching between saved profiles.
* **Automatic Map Updater:** Integrated function that automatically fetches the latest map list from the server to keep data up-to-date.

### 🔧 General Improvements & System Optimization
* **New Update Notifier :** Implemented a version check mechanism to keep users informed about the latest releases.
* **Bug Fixes:** Resolved all critical and general issues to improve overall application stability.
* **File Structure Reorganization:** All application data has been moved to a dedicated `VALORANT/Instalocker` directory to prevent file clutter.
* **Smart Cleaner:** Integrated a cleanup system that automatically removes "junk" files left behind by older versions.
* **Update Reminder:** New mechanism added to notify users when the agent list becomes outdated.
* **Detailed Debug Logs:** Troubleshooting logs have been expanded for faster error diagnosis and resolution.

---

## 🚀 Key Features

* **[Commands](#%EF%B8%8F-usage-of-commands):** Instalocker allows you to use specific customized commands.
* **[Map-Based Selection (Macro) Mode](#%EF%B8%8F-map-based-selection-usage):** Advanced profile system that automatically selects your pre-defined agent based on the current map.
* **[Quick Profile Selector & Shortcuts](#-using-the-filled-profile-file-):** Instant access to switch between your saved map profiles (last 3 profiles).
* **[Automatic Map Updater](#%EF%B8%8F-usage-of-commands):** Infrastructure that automatically refreshes the map list from the server when new maps are added to the game.
* **[Agent Lock Mode](#%EF%B8%8F-agent-selection-and-usage-of-modes):** Locks the selected agent — classic instalock.
* **[Pick Only Mode](#%EF%B8%8F-agent-selection-and-usage-of-modes):** Selects the agent but does not lock it. You don't need to be at your computer during the match screen.
* **Game Disruption Protection:** If the match is dodged/disrupted, Instalocker will automatically re-select the same agent and mode.
* **[Match Dodge Mechanic](#-match-dodge-mechanic-usage):** After an agent is locked, you can dodge the match with a single key and return to the main menu.
* **[Desktop Shortcut Creation](#-shortcut-usage):** You can create desktop shortcuts for specific agents and modes. Running the shortcut allows for a quick instalock.
* **Language Support:** Instalocker now supports multiple languages. This is an experimental feature, so please report bugs in the [Issues](https://github.com/Berkwe/Valorant-instalocker/issues) section.
* **Automatic Language Detection:** Automatically detects the language for language support (may vary based on Valorant settings). You can still change it manually using [specific commands](#%EF%B8%8F-usage-of-commands).
* **[Agent Name Shortening](#%EF%B8%8F-agent-name-shortening-usage):** You can quickly select agents by typing the shortened versions of their long names.
* **[Automatic Agent Updates](#%EF%B8%8F-automatic-agent-update-usage):** New agents are added automatically when released.
* **[Log System](#-log-system-explanation):** Records errors and makes it easy to report them to the developer.

---

## 📦 Installation

### 💾 With the EXE:

1. **Download the EXE:**
   [Instalocker.exe](https://github.com/Berkwe/Valorant-instalocker/releases/latest/download/Instalocker.exe)
2. **Run it:** Double-click and run.

### 🐍 With Python:

#### Requirements

* Python 3.9+
* Additional packages (requirements.txt)
* **_Note: Some features may not work_**

#### Steps

1. **Download the project:**

   - **[Download the ZIP file](https://github.com/Berkwe/Valorant-instalocker/archive/refs/heads/main.zip)** **OR** - **Clone with Git:**
   ```bash
   git clone https://github.com/Berkwe/Valorant-instalocker
   cd Valorant-instalocker
   ```
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
3. **Run:**

   ```bash
   python instalocker.py
   ```

---

## 🛠️ Usage

### ⚙️ Agent Selection and Usage of Modes

##### - Agent Lock Mode:
- Locks the agent, classic instalock.
  
##### - Pick Only Mode: 
- Picks the agent but does not lock it. This way, you can use Instalocker even if you don't want to instalock in competitive matches.

##### - Map-Based Selection Mode:
- Instalocker can now select agents according to the map using customized selection modes (pick only/lock) via profile files you create. Your last 3 used profiles are saved so you can quickly access them.

---
### 🗺️ Map-Based Selection Usage
#### - Map-Based Selection Feature: 
- Due to popular demand (advice from someone who is black and has an excess on the y-axis), an agent selection mechanic customizable by maps has been added. This mechanic can select the agent and mode (pick only or lock) according to the map of your current match. It does this using profile files.

#### - Profile File Usage:
- The profile file is automatically created on the desktop via Instalocker commands. Afterwards, you can right-click and edit it with Notepad. You just need to type the agent and mode. **AGENT NAMES MUST BE ENTERED COMPLETELY AND NO OTHER AREA SHOULD BE TOUCHED, OTHERWISE INSTALOCKER WILL NOT WORK!** The maps in a profile file look like this:
```json
{
    "ascent": {
        "ajan": "", # ? agent to be selected
        "mod": "" # ? mode to be used (enter 1 or 2, if left blank it defaults to mode 1 - lock mode)
    },
    "split": {
        "ajan": "", 
        "mod": ""
    },
```
#### - Example Filling:
```json
{
    "ascent": {
        "ajan": "jett", 
        "mod": "1"
    },
    "split": {
        "ajan": "brimstone", # ? you cannot write 'brim' here, you must enter the full name. I probably won't add the abbreviation feature for this later.
        "mod": "2"
    },
```

#### - Using the Filled Profile File: 
- **WARNING: FILES MUST BE USED AFTER SAVING.** You can save with ctrl+s or by closing notepad.
- This is a very easy process and can be done in 3 ways.
1. - If you filled out a newly created profile file via commands on Instalocker, Instalocker will give you a warning in parentheses like (default=c:/profile/path/dummy/). If that warning is visible, just press Enter after making sure you saved your file.
2. - If you are going to use a different file than the one you created before, you can copy the path of the file by right-clicking on the file and selecting 'copy as path' and then paste it to Instalocker.
3. - Instalocker saves the last 3 used profiles and shows them on the profile selection screen. You can quickly use your listed profiles by selecting their numbers (1,2,3).
---

### ⏩ Shortcut Usage

##### - Shortcut Mechanic:
- Instalocker can create a shortcut for you to quickly select your desired agent and mode (Except Map-Based Selection). This way, instead of opening the app from scratch and entering the info, you just run the shortcut.
  
##### - Usage:
- While waiting for the agent selection screen, Instalocker asks if you want to create a Shortcut. If you enter Y/N characters (case insensitive), an Instalocker shortcut containing the agent's image will appear on your desktop with the agent name and your usage mode.

##### - Execution:
- When you run the created shortcut, Instalocker will start with the settings you configured without needing to enter any settings.
---
### 🚫 Match Dodge Mechanic Usage
##### - Match Dodge Mechanic:
- Instalocker offers a function that allows you to dodge the game on the agent selection screen without having to close the game. All you have to do is type Y/N to the 'would you like to break the game?' question asked in Instalocker after the agent is selected.

##### - After Dodging: 
- After the match is dodged, you return to the main menu and your match dodge penalty is given. This mechanic does not bypass the penalty, it just means you don't have to quit the game to dodge.
---
### ⚙️ Usage of Commands
#### **You can use the following commands in the mode selection section:**

```text
- 1 : Selects and locks the agent. This is the normal (default) mode. 
      Press Enter to skip quickly.

- 2 : Selects the agent but does not lock it. This way, you can use Instalocker's auto-select feature even if you don't want to instalock in competitive matches. (At the end of the timer on the selection screen, Valorant locks the agent you selected so the match doesn't dodge and you enter the game.)

- 3 : Using profile files, you select the agent and mode you want according to the maps in the game. Profile files can be created by Instalocker with specific commands. (see agent name commands for more info)

- 4 help / yardım : Displays this help message.
```
#### **You can use the following commands in the agent name determination section:**
```text
#### 🦸 Agent Selection Commands
- -create-profile / cp / po
  → Creates a new profile file and returns its path.
- -r / random / rastgele
  → Randomly selects an agent from the list.
- -agents / ajanlar
  → Displays the current agent list in a readable and neat format.
- -agents-l / ajanlar-l
  → Returns the agent list in a raw list format.
```
#### 🛠️ General System Commands
```
- -clear / cls / temizle
  → Clears the terminal screen to remove clutter.
- -update / güncelle
  → Refreshes and updates the agent list, map list, and language files from the server.
- -re / yb
  → Restarts the application quickly without closing it.
- -english / türkçe
  → Changes the application interface language instantly.
- -agents-folder / liste-konumu
  → Shows the path to the folder where agent data is stored.
- -logs-folder / kayıt-konumu
  → Opens the folder where the application logs are kept.
- -help / yardım
  → Displays this help menu and command details.
```
---
### ✂️ Agent Name Shortening Usage
##### - Agent Name Shortening Mechanic: 
- Having to type the annoying and long names of Valorant agents over and over again can be frustrating. Instalocker has a mechanic to shorten these long names to provide a better experience. When agents with names longer than 5 characters are typed shortened (the abbreviation must be at least 4 letters), Instalocker selects the agent.

### Confused? Here is an example: 
  ```text
  ✅ brim → valid
  ❌ reyn → invalid
  ```
---
### 🔄 Server Detection Feature Explanation

##### - Auto Server Detection Feature: 
- By design, Instalocker needs to know the user's server to work. However, asking the user to enter their server every time can be as annoying as sand in your shoe (which was the method used in early Instalocker versions). Therefore, Instalocker can automatically detect which server the user is connected to. Of course, if it is not detected, that sand will still get in your shoe.
---
### ⬇️ Automatic Agent Update Usage

##### - Automatic Agent Update Mechanic:
- Another mechanic that creates hell, which was absent in older versions, was the need to add new agents to Instalocker **update by update**. This required a new update for every new agent, but now it can be updated with a single command. (See commands for more info)

##### - Manual Update:
- Since Instalocker was written by a human being, errors will inevitably occur when adding new agents. In this case, you can manually update by following the steps below.
    
    #### - Step 1:
    - **Open the CMD (Command Prompt) App.**
    #### - Step 2: 
    - **Paste the following code:**
    ####
      curl "https://raw.githubusercontent.com/Berkwe/Valorant-instalocker/refs/heads/main/agents.json" > %LOCALAPPDATA%\VALORANT\agents.json
---
### 🪲 Log System Explanation

* **Instalocker continuously logs records to facilitate debugging and management. To make logs detailed, you can type 'debug' in the console while on the mode selection screen. This way, when you send the log file to the developer, it will be easier to understand the error.**

* **To find the Instalocker.log file, you can enter the following command in the 'Run' window opened with the Windows+R key combination.**

* ```text
  %LOCALAPPDATA%/VALORANT
  ```

---

## ⓘ Performance and Feedback

* For performance issues or suggestions, please use the [Issues](https://github.com/Berkwe/Valorant-instalocker/issues) page.

---

## 🖤 Acknowledgements
- **Thanks to [techchrism](https://github.com/techchrism) for documenting the Valorant API and [colinhartigan](https://github.com/colinhartigan) for packaging this API into a module, even though they did not contribute directly to the project.**

---

## 🌟 Other Projects

* [ADB Brute-Force](https://github.com/Berkwe/ADB-bruteforce)
* [Audio Converter](https://github.com/Berkwe/Audio-converter)

---

## 📞 Contact

<a href="https://discord.gg/Xagnh5aYSy" target="blank"><img align="center" src="https://raw.githubusercontent.com/rahuldkjain/github-profile-readme-generator/master/src/images/icons/Social/discord.svg" alt="Berkwe" height="30" width="40" /></a>

---

## 📝 License

This project is licensed under the [MIT License](https://github.com/Berkwe/Valorant-instalocker/blob/main/LICENSE).

---

## ⚠️ Disclaimer

This software is developed strictly for **educational and personal use** purposes only. Any risks arising from the use of this software (including but not limited to in-game bans, account restrictions, or data loss) are entirely the **responsibility of the user.** The developer shall **not be held liable** for any damages resulting from the use of this software or for any violations of third-party terms of service (e.g., Riot Games). By using this tool, you agree to these terms.

---

### 🔑 Keywords
valorant instalocker, valorant auto lock, valorant agent locker, valorant instalock script, valorant agent picker, valorant instalocker tui
