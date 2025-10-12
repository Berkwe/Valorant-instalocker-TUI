<p align="center">
      🌐 English | <a href=https://github.com/Berkwe/Valorant-instalocker/blob/main/readme.tr.md>Türkçe</a>
</p>


# 🛠️ Valorant Instalocker

Valorant Instalocker is a fast and reliable auto agent locker for Riot Games’ Valorant. Often called a Valorant instalock tool or agent picker, it automatically selects and locks your chosen agent using the official Valorant API. The program is written in Python, includes a simple CLI, and works as a lightweight instalocker script that speeds up the agent selection phase dramatically.

# ❗IMPORTANT
**This version is still in the testing phase. Please report any [issues](https://github.com/Berkwe/Valorant-instalocker/issues) you encounter in the issues section.**

---

## 🆕 New Features v1.7

* **Desktop Shortcut Creation:** You can create desktop shortcuts for specific agents and modes. Running the shortcut allows a quick instalock.
* **Language Support:** Instalocker now supports multiple languages. However, this is an experimental feature, so please report any bugs in the [Issues](https://github.com/Berkwe/Valorant-instalocker/issues) section.  
* **Automatic Language Detection:** The language support includes automatic detection, which may vary depending on your Valorant settings. You can still change it manually using specific commands.

---

## 🚀 Key Features

* **Agent Lock Mode:** Locks the selected agent — classic instalock behavior.
* **Pick Only Mode:** Selects the agent without locking. You do not need to be at the computer while the match is being found.
* **Match Cancel Mechanic:** After an agent is locked, you can cancel the match with a single key press and return to the main menu.
* **Agent Name Shortening:** Shortens long agent names so they can be selected quickly.
* **Automatic Agent Updates:** New agents are added automatically when released.
* **Logging System:** Records errors and makes it easy to report them to the developer.

---

## 📦 Installation

### 💾 With the EXE:

1. **Download the EXE:**
   [Instalocker.exe](https://github.com/Berkwe/Valorant-instalocker/releases/latest/download/Instalocker.exe)
2. **Run it:** Double-click to start.

### 🐍 With Python:

#### Requirements

* Python 3.9+
* Additional packages (see requirements.txt)
* ***Note: Some features may not work***

#### Steps

1. **Download the project:**

   * **Download the ZIP file:** [Main branch ZIP](https://github.com/Berkwe/Valorant-instalocker/archive/refs/heads/main.zip)

   **OR**

   * **Clone with Git:**

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

### Agent Selection and Modes

* **Agent Lock Mode:** Locks the agent — classic instalock.
* **Pick Only Mode:** Picks the agent but does not lock it. This allows the match to be found while you are away from the computer.
* **Manual Match Cancel:** Type e/y in the console to cancel.

### ⏩ Using Shortcuts

* To create a desktop shortcut, type E/H at the agent selection screen.
* A shortcut will appear on the desktop according to the agent name and the chosen mode.

### 🚫 Canceling a match through Instalocker:

* After the agent is locked, type e or y in the console to cancel. If you cancel, Instalocker restarts. After the agent is locked, simply type e or y on the console. If you break it, Instalocker will restart, and penalties will still be imposed.

### ✂️ Agent Name Shortening

* A simple mechanic was added so agents can be selected quickly. You may shorten agent names longer than 5 characters, but the typed name must be at least 4 characters.

Example:

```text
✅ brim → valid
❌ reyn → invalid
```

### 🔄 Server Detection

* **Server is detected automatically; manual input is available for exceptional cases.** (If this is unclear, skip it.)

### Automatic Agent Updates

* Instalocker now continuously updates the agent list automatically. However, since this is done by a human, mistakes may occur — in that case, manual update may be required. If so, follow the steps below:

  #### Step 1:

  * Open the CMD (Command Prompt).

  #### Step 2:

  * Paste the following command:

    ```bash
    curl "https://raw.githubusercontent.com/Berkwe/Valorant-instalocker/refs/heads/main/agents.json" > %LOCALAPPDATA%\VALORANT\agents.json
    ```

---

## ⓘ Performance and Feedback

* For performance issues or suggestions, please use the [Issues](https://github.com/Berkwe/Valorant-instalocker/issues) page.

---

## 🖤 Acknowledgements

* I would like to thank [techchrism](https://github.com/techchrism) for documenting the Valorant API and [colinhartigan](https://github.com/colinhartigan) for packaging this API into a module, even though they did not contribute directly to the project.
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

### 🔑 Keywords
valorant instalocker, valorant auto lock, valorant agent locker, valorant instalock script, valorant agent picker, valorant instalocker gui
