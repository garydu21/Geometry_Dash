import serial
import serial.tools.list_ports
import time

_ser = None

def _detect_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if any(kw in (p.description or "").lower() for kw in ("arduino", "ch340", "cp210", "ftdi", "usb serial")):
            return p.device
    return ports[0].device if ports else None

def arduino_init(port=None, baud=115200):
    global _ser
    if port is None:
        port = _detect_port()
    if port is None:
        print("[Arduino] Aucun port trouvé.")
        return
    try:
        _ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)
        print(f"[Arduino] Connecté sur {port}")
    except serial.SerialException as e:
        print(f"[Arduino] Erreur : {e}")

def arduino_send_level(level_index):
    if _ser is None or not _ser.is_open:
        return
    _ser.write(f"L:{level_index}\n".encode("ascii"))

def arduino_send_death(deaths):
    if _ser is None or not _ser.is_open:
        return
    _ser.write(f"D:{deaths}\n".encode("ascii"))

def arduino_send_progress(pct):
    if _ser is None or not _ser.is_open:
        return
    _ser.write(f"P:{pct}\n".encode("ascii"))

def arduino_close():
    if _ser and _ser.is_open:
        _ser.close()