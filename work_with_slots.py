from models import *


def add_slot(slots) -> Tuple[str, int]:
    all_new_slots = []
    slots_for_edit = []

    for each in (Slot.query.filter(Slot.id.in_([slot["id"] for slot in slots])).all()):
        saved_slot = slots.pop(slots.index([slot for slot in slots if slot["id"] == each.id][0]))
        slots_for_edit.append({
            "id": saved_slot["id"],
            "start": saved_slot["start"],
            "end": saved_slot["end"],
            "title": saved_slot["title"]
        })

    for new_slot in slots:
        all_new_slots.append({
            "id": new_slot["id"],
            "start": new_slot["start"],
            "end": new_slot["end"],
            "title": new_slot["title"]
        })

    try:
        db.session.bulk_insert_mappings(Slot, all_new_slots)
        db.session.bulk_update_mappings(Slot, slots_for_edit)
        db.session.commit()

    except Exception as e:
        print(e)

        return "Chyba při vytváření volných termínů!", 400

    return "Všechny volné termíny byly úspěšně vytvořeny.", 200


def clear_slot(slot_id: str) -> Tuple[str, int]:
    try:
        slot = Slot.query.filter_by(id=slot_id).first()
        slot.title = "Volný slot"
        db.session.commit()

    except Exception:
        return f"Chyba při uvolnění termínu s ID {slot_id}!", 400

    return f"Termín s ID {slot_id} uvolněn.", 200


def delete_slot(slot_id: str) -> Tuple[str, int]:
    try:
        slot = Slot.query.filter_by(id=slot_id).first()
        slot.delete()
        db.session.commit()

    except Exception:
        return f"Chyba při mazání termínu s ID {slot_id}!", 400

    return f"Termín s ID {slot_id} smazán.", 200


def get_slots() -> Tuple[list, int]:
    slots = []

    try:
        slot_objects = Slot.query.all()

    except Exception:
        return ["Chyba při načítání termínů!"], 400

    for so in slot_objects:
        slots.append({
            "id": so.id,
            "start": so.start,
            "end": so.end,
            "title": so.title
        })

    return slots, 200


def get_free_slots(slot_update: bool = False) -> Tuple[list, int]:
    free_slots = []

    try:
        free_slot_objects = Slot.query.filter_by(title="Volný slot").filter(
            Slot.start > "2022-01-06T20:45:00.000Z").order_by(Slot.start).all()

    except Exception:
        return ["Chyba při načítání termínů!"], 400

    for so in free_slot_objects:
        free_slots.append({
            "id": so.id,
            "start": so.start,
            "end": so.end
        })

    return (["Žádný volný termín"], 400) if len(free_slots) == 0 else (free_slots, 200)


def book_slot(slot_data: dict) -> Tuple[str, int]:
    slot = Slot.query.filter_by(id=slot_data["id"]).first()

    if slot.title != "Volný slot":
        return f"Termín {slot.start} - {slot.end} je již obsazen!", 400

    slot.title = slot_data["title"]

    try:
        db.session.commit()

    except Exception as e:
        print(e)
        return f"Chyba při rezervování termínu {slot.start} - {slot.end}!", 400

    return f"Rezervován termín {slot.start} - {slot.end}", 200