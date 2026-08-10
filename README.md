# 🎯 SPT Tarkov — DMA ESP Hack (Python)

> **⚠️ THIS WILL NOT WORK ON LIVE TARKOV SERVERS — Single Player Tarkov (SPT) ONLY**

A simple **Direct Memory Access (DMA)** hack for **Single Player Tarkov (SPT)** written in Python.  
Reads player positions from game memory via [MemProcFS](https://github.com/ufrisk/memprocfs) and renders an ESP overlay using **Pygame**.

---

## 🎥 Demo

[![Watch the demo](https://img.youtube.com/vi/8U7eld4m7B4/0.jpg)](https://youtu.be/8U7eld4m7B4)

🔗 **[Watch on YouTube](https://youtu.be/8U7eld4m7B4)**

---

## 🖥️ DMA Hardware Setup (2-PC Architecture)

This hack uses a **two-computer DMA setup** to remain completely invisible to anti-cheat software:

```
┌─────────────────┐         ┌──────────────┐         ┌─────────────────┐
│                 │         │              │         │                 │
│   GAMING PC     │ ◄─PCIe─►│  DMA BOARD   │◄─USB/──►│   CHEAT PC      │
│  (runs Tarkov)  │         │  (FPGA)      │  PCIe   │ (runs this hack)│
│                 │         │              │         │                 │
└─────────────────┘         └──────────────┘         └─────────────────┘
```

<img width="1280" height="720" alt="pc3bsiiisrpc1" src="https://github.com/user-attachments/assets/f103ea35-8f71-4a9c-acd0-f8fb05bc56b3" />


### The 3 Components:

| Component | Role |
|-----------|------|
| **Gaming PC** | Runs Escape from Tarkov (SPT). The DMA board is plugged into a PCIe slot. |
| **DMA Board (FPGA)** | A hardware device (e.g. PCIe Squirrel, Screamer) that reads the Gaming PC's RAM **directly from the physical memory bus** — no software running on the gaming PC at all. |
| **Cheat PC** | A separate computer that receives the memory data from the DMA board and runs this Python script to parse entities and render the ESP overlay. |

---

## 🛠️ How It Works (Step by Step)

1. The **DMA board** is physically plugged into the Gaming PC's PCIe slot (or M.2 slot with adapter).
2. The DMA board reads **raw physical memory** directly from the RAM bus — this happens at the hardware level, outside the operating system.
3. The **Cheat PC** connects to the DMA board via USB or another PCIe cable, receiving a live stream of memory data.
4. [**MemProcFS**](https://github.com/ufrisk/memprocfs) on the Cheat PC mounts the Gaming PC's memory as a virtual filesystem and provides a Python API to read it.
5. The script walks the **GameObjectManager (GOM)** chain using known offsets to find the player list.
6. Player X/Y coordinates are extracted and drawn as colored dots on a **Pygame** overlay window on the Cheat PC.

---

## 🔒 Why DMA is Undetectable

Traditional software cheats run **on the same PC** as the game — they inject DLLs, hook functions, or read/write process memory through Windows APIs. Anti-cheat systems (BattlEye, EAC, Vanguard) easily detect these because they monitor:
- Open process handles (`OpenProcess`, `ReadProcessMemory`)
- DLL injection & code hooks
- Anomalous driver signatures
- Screen capture / overlay detection

**DMA bypasses all of this:**

| Detection Vector | DMA |
|------------------|-----|
| ❌ Process handles | DMA reads physical RAM — no `OpenProcess` call on the Gaming PC |
| ❌ DLL injection | Nothing runs on the Gaming PC — no code, no hooks, no threads |
| ❌ Driver signatures | The DMA board uses its own firmware, invisible to Windows |
| ❌ API monitoring | All memory access happens over the PCIe bus at hardware level |
| ❌ Screen capture | ESP overlay runs on the **Cheat PC**, not on the Gaming PC |

> The Gaming PC has **zero software** related to the cheat installed. From the perspective of the OS and any anti-cheat, the DMA board is just another PCIe device doing DMA — something every GPU, NVMe drive, and network card already does.

Anti-cheat cannot scan the **Cheat PC** because it's a physically separate machine with no connection to the game server.

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

## 📐 Tarkov In-Game Memory Topology

![Tarkov Memory Topology](https://github.com/user-attachments/assets/ecce6b31-e7ad-46d7-838b-baeffd234305)

---

## ⚠️ Disclaimer

> **FOR EDUCATIONAL PURPOSES ONLY.** This project is meant for learning about DMA, memory analysis, and reverse engineering in a **single-player offline environment**. Using cheats on live multiplayer servers is against the game's ToS and can result in bans. I am not responsible for any misuse.

---

## 📄 License

MIT — do whatever you want, just don't ruin live servers.

---

## 🔗 Credits

- [MemProcFS](https://github.com/ufrisk/memprocfs) by Ulf Frisk — the backbone of this project
- [SPT Tarkov](https://sp-tarkov.com/) — the single-player mod that makes this possible

