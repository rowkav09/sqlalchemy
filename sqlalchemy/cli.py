import sqlalchemy.orm as orm
from database import engine
from models import Pupil, Society, create_database


def get_session():
    Session = orm.sessionmaker(bind=engine)
    return Session()


def seed_societies():
    create_database()
    session = get_session()
    try:
        existing = session.query(Society).count()
        if existing == 0:
            societies = [
                Society(name="Masaryk Society", room="7", week="A and B", time="1pm"),
                Society(name="Vinyl & Philosophy", room="17", week="A and B", time="1pm"),
                Society(name="Formula 1 Society", room="18", week="A and B", time="1pm"),
                Society(name="Dungeons and Dragons", room="17", week="A and B", time="1pm"),
                Society(name="Medical Society", room="P3", week="A and B", time="1pm"),
                Society(name="Meteorological Society", room="C1", week="B", time="4pm"),
            ]
            session.add_all(societies)
            session.commit()
    finally:
        session.close()


def list_all_pupils():
    session = get_session()
    try:
        pupils = session.query(Pupil).all()
        if not pupils:
            print("No pupils found.")
        else:
            for pupil in pupils:
                print(pupil)
    finally:
        session.close()


def list_all_societies():
    session = get_session()
    try:
        societies = session.query(Society).all()
        if not societies:
            print("No societies found.")
        else:
            for society in societies:
                print(society)
    finally:
        session.close()


def enrol_pupil_into_society():
    session = get_session()
    try:
        pupils = session.query(Pupil).all()
        societies = session.query(Society).all()

        if not pupils or not societies:
            print("Not enough pupils or societies.")
            return

        print("\nPupils:")
        for i, pupil in enumerate(pupils, 1):
            print(f"{i}. {pupil}")

        try:
            pupil_choice = int(input("\nSelect pupil (number): "))
            if pupil_choice < 1 or pupil_choice > len(pupils):
                print("Invalid selection.")
                return
            selected_pupil = pupils[pupil_choice - 1]
        except ValueError:
            print("Invalid input.")
            return

        print("\nSocieties:")
        for i, society in enumerate(societies, 1):
            print(f"{i}. {society}")

        try:
            society_choice = int(input("\nSelect society (number): "))
            if society_choice < 1 or society_choice > len(societies):
                print("Invalid selection.")
                return
            selected_society = societies[society_choice - 1]
        except ValueError:
            print("Invalid input.")
            return

        if selected_society in selected_pupil.societies:
            print("Already enrolled.")
        else:
            selected_pupil.societies.append(selected_society)
            session.commit()
            print("Enrolled.")
    finally:
        session.close()


def remove_pupil_from_society():
    session = get_session()
    try:
        pupils = session.query(Pupil).all()
        if not pupils:
            print("No pupils found.")
            return

        print("\nPupils:")
        for i, pupil in enumerate(pupils, 1):
            print(f"{i}. {pupil}")

        try:
            pupil_choice = int(input("\nSelect pupil (number): "))
            if pupil_choice < 1 or pupil_choice > len(pupils):
                print("Invalid selection.")
                return
            selected_pupil = pupils[pupil_choice - 1]
        except ValueError:
            print("Invalid input.")
            return

        if not selected_pupil.societies:
            print("Not in any societies.")
        else:
            print(f"\n{selected_pupil.first_name}'s societies:")
            for i, society in enumerate(selected_pupil.societies, 1):
                print(f"{i}. {society}")

            try:
                society_choice = int(input("\nSelect society to remove (number): "))
                if society_choice < 1 or society_choice > len(selected_pupil.societies):
                    print("Invalid selection.")
                    return
                selected_society = selected_pupil.societies[society_choice - 1]
            except ValueError:
                print("Invalid input.")
                return

            selected_pupil.societies.remove(selected_society)
            session.commit()
            print("Removed.")
    finally:
        session.close()


def show_societies_for_pupil():
    session = get_session()
    try:
        pupils = session.query(Pupil).all()
        if not pupils:
            print("No pupils found.")
            return

        print("\nPupils:")
        for i, pupil in enumerate(pupils, 1):
            print(f"{i}. {pupil}")

        try:
            pupil_choice = int(input("\nSelect pupil (number): "))
            if pupil_choice < 1 or pupil_choice > len(pupils):
                print("Invalid selection.")
                return
            selected_pupil = pupils[pupil_choice - 1]
        except ValueError:
            print("Invalid input.")
            return

        if not selected_pupil.societies:
            print(f"\n{selected_pupil.first_name} is not in any societies.")
        else:
            print(f"\n{selected_pupil.first_name}'s societies:")
            for society in selected_pupil.societies:
                print(f"  {society}")
    finally:
        session.close()


def show_pupils_in_society():
    session = get_session()
    try:
        societies = session.query(Society).all()
        if not societies:
            print("No societies found.")
            return

        print("\nSocieties:")
        for i, society in enumerate(societies, 1):
            print(f"{i}. {society}")

        try:
            society_choice = int(input("\nSelect society (number): "))
            if society_choice < 1 or society_choice > len(societies):
                print("Invalid selection.")
                return
            selected_society = societies[society_choice - 1]
        except ValueError:
            print("Invalid input.")
            return

        if not selected_society.pupils:
            print(f"\n{selected_society.name} has no pupils.")
        else:
            print(f"\n{selected_society.name}'s pupils:")
            for pupil in selected_society.pupils:
                print(f"  {pupil}")
    finally:
        session.close()


def main():
    seed_societies()

    while True:
        print("\n1. List pupils")
        print("2. List societies")
        print("3. Enrol pupil")
        print("4. Remove pupil from society")
        print("5. Show societies for pupil")
        print("6. Show pupils in society")
        print("7. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            list_all_pupils()
        elif choice == "2":
            list_all_societies()
        elif choice == "3":
            enrol_pupil_into_society()
        elif choice == "4":
            remove_pupil_from_society()
        elif choice == "5":
            show_societies_for_pupil()
        elif choice == "6":
            show_pupils_in_society()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
