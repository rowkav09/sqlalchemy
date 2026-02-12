import datetime
import random
import sqlalchemy.orm as orm
from faker import Faker
from database import engine
from models import Pupil, House, Society, create_database


def populate_database():
    create_database()
    fake = Faker()
    
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    try:
        if session.query(Pupil).count() > 0:
            print("Database already populated. Skipping...\n")
            return

        # Seed societies if they don't exist
        if session.query(Society).count() == 0:
            societies_data = [
                Society(name="Masaryk Society", room="7", week="A and B", time="1pm"),
                Society(name="Vinyl & Philosophy", room="17", week="A and B", time="1pm"),
                Society(name="Formula 1 Society", room="18", week="A and B", time="1pm"),
                Society(name="Dungeons and Dragons", room="17", week="A and B", time="1pm"),
                Society(name="Medical Society", room="P3", week="A and B", time="1pm"),
                Society(name="Meteorological Society", room="C1", week="B", time="4pm"),
            ]
            session.add_all(societies_data)
            session.flush()

        # Create houses
        house_names = ["Eastgate", "Westbrook", "Northfield", "Southside"]
        houses = [House(house_name=name) for name in house_names]
        session.add_all(houses)
        session.flush()
        
        print(f"Created {len(houses)} houses")

        # Generate pupils (20 per house)
        pupils = []
        for house in houses:
            for _ in range(20):
                pupil = Pupil(
                    first_name=fake.first_name(),
                    second_name=fake.last_name(),
                    date_of_birth=fake.date_of_birth(minimum_age=13, maximum_age=18),
                )
                pupil.house = house
                pupils.append(pupil)

        session.add_all(pupils)
        session.flush()

        print(f"Created {len(pupils)} pupils ({len(pupils) // len(houses)} per house)")

        societies = session.query(Society).all()
        
        societies_by_time = {}
        for society in societies:
            time = society.time
            if time not in societies_by_time:
                societies_by_time[time] = []
            societies_by_time[time].append(society)

        enrollments = 0
        for pupil in pupils:
            num_slots_to_join = random.randint(0, 2)
            
            selected_times = random.sample(list(societies_by_time.keys()), min(num_slots_to_join, len(societies_by_time)))
            
            for time_slot in selected_times:
                society = random.choice(societies_by_time[time_slot])
                if society not in pupil.societies:
                    pupil.societies.append(society)
                    enrollments += 1

        session.commit()
        print(f"Enrolled pupils in societies ({enrollments} total enrollments)\n")

        print("=" * 50)
        print("DATABASE POPULATION SUMMARY")
        print("=" * 50)
        for house in houses:
            pupil_count = session.query(Pupil).filter_by(house_id=house.house_id).count()
            print(f"  {house.house_name}: {pupil_count} pupils")
        
        print(f"\nTotal societies: {len(societies)}")
        for time_slot, socs in societies_by_time.items():
            print(f"  {time_slot}: {len(socs)} societies")
        
        avg_societies_per_pupil = enrollments / len(pupils) if pupils else 0
        print(f"\nTotal enrollments: {enrollments}")
        print(f"Avg societies per pupil: {avg_societies_per_pupil:.1f}")
        print("=" * 50 + "\n")

    finally:
        session.close()


if __name__ == "__main__":
    populate_database()