"""Этап 1 (Вариант Б): Моделирование пакета телеметрии куста, сохранение и чтение JSON."""

import json
from typing import Any


def build_telemetry_packet() -> dict[str, Any]:
    """Формирует пакет телеметрии со списком датчиков по индивидуальным числам пары (N = 10)."""
    return {
        "pad_id": "PAD-20",
        "well_id": "W-210",
        "p_res_mpa": 27.0,
        "p_bhp_mpa": 16.0,
        "mode": "PUMPING",
        "is_online": True,
        "sensors": [
            {"code": "T-01", "value": 60.0, "unit": "C"},
            {"code": "Q-01", "value": 100.0, "unit": "m3/d"},
            {"code": "P-01", "value": 14.0, "unit": "MPa"},
        ],
    }


def save_to_json(data: dict[str, Any], filename: str = "data.json") -> None:
    """Сериализует пакет телеметрии в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_from_json(filename: str = "data.json") -> dict[str, Any]:
    """Читает JSON-файл с диска обратно в словарь Python."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def print_telemetry_summary(packet: dict[str, Any]) -> None:
    """Выводит сводку по пакету телеметрии и считает депрессию на пласт."""
    drawdown = packet["p_res_mpa"] - packet["p_bhp_mpa"]
    print("=" * 58)
    print(f"ПАКЕТ ТЕЛЕМЕТРИИ: Куст {packet['pad_id']} | Скважина {packet['well_id']}")
    print("=" * 58)
    print(f"Режим работы:      {packet['mode']}")
    print(f"Связь со станцией: {'есть' if packet['is_online'] else 'нет'}")
    print(f"Давления:          Рпл = {packet['p_res_mpa']} МПа, Рзаб = {packet['p_bhp_mpa']} МПа (dP = {drawdown:.2f} МПа)")
    print(f"Опрошено датчиков: {len(packet['sensors'])} шт.")
    for s in packet["sensors"]:
        print(f"  -> Датчик {s['code']}: {s['value']} {s['unit']}")
    print("=" * 58)


if __name__ == "__main__":
    pkt = build_telemetry_packet()
    save_to_json(pkt, "data.json")
    print("[OK] Файл 'data.json' успешно записан на диск!")

    loaded_pkt = load_from_json("data.json")
    assert loaded_pkt == pkt, "Ошибка: данные при чтении JSON исказились!"
    print("[OK] Обратное чтение через json.load() прошло успешно!\n")

    print_telemetry_summary(loaded_pkt)
