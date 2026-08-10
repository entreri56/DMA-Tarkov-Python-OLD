# 🎯 SPT Tarkov — DMA ESP Hack (Python)

> **⚠️ THIS WILL NOT WORK ON LIVE TARKOV SERVERS — Single Player Tarkov (SPT) ONLY**

A simple **Direct Memory Access (DMA)** hack for **Single Player Tarkov (SPT)** written in Python.  
Reads player positions from game memory via [MemProcFS](https://github.com/ufrisk/memprocfs) and renders an ESP overlay using **Pygame**.

---

## 📐 Tarkov In-Game Memory Topology

![Tarkov Memory Topology](https://github.com/user-attachments/assets/ecce6b31-e7ad-46d7-838b-baeffd234305)

---

## 🎥 Demo

[![Watch the demo](https://img.youtube.com/vi/8U7eld4m7B4/0.jpg)](https://youtu.be/8U7eld4m7B4)

🔗 **[Watch on YouTube](https://youtu.be/8U7eld4m7B4)**

---

## 🛠️ How It Works

1. **MemProcFS** connects to the DMA device (FPGA) and reads the game's memory.
2. Offsets are used to locate the **GameObjectManager (GOM)**, local game world, and player list.
3. Player X/Y coordinates are extracted and rendered on a **Pygame** overlay window.

---

## 📦 Requirements

- **Python 3.8+**
- [MemProcFS](https://github.com/ufrisk/memprocfs) — DMA memory analysis framework
- **FPGA DMA device** (e.g., PCIe Squirrel, Screamer, etc.)
- **SPT Tarkov** (Single Player Tarkov)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

1. Make sure your DMA device is connected and MemProcFS can access it.
2. Launch **SPT Tarkov**.
3. Run the script:

```bash
python "EFT Tarkov DMA OLD.py"
```

A Pygame window will open showing:
- 🔴 **Red circles** — Other players / entities
- 🟢 **Green circle** — Your player (local)

---

## 🧠 Memory Offsets

| Offset | Value | Description |
|--------|-------|-------------|
| `GOM` | `0x17FFD28` | GameObjectManager |
| `LocalGameWorld` | `(0x30, 0x18, 0x28)` | Chain to local game world |
| `MainPlayer` | `0x148` | Local player reference |
| `RegisteredPlayers` | `0xF0` | Player list |

---

## ⚠️ Disclaimer

> **FOR EDUCATIONAL PURPOSES ONLY.** This project is meant for learning about DMA, memory analysis, and reverse engineering in a **single-player offline environment**. Using cheats on live multiplayer servers is against the game's ToS and can result in bans. The author is not responsible for any misuse.

---

## 📄 License

MIT — do whatever you want, just don't ruin live servers.

---

## 🔗 Credits

- [MemProcFS](https://github.com/ufrisk/memprocfs) by Ulf Frisk — the backbone of this project
- [SPT Tarkov](https://sp-tarkov.com/) — the single-player mod that makes this possible

