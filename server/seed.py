#!/usr/bin/env python3

from app import app
from models import db, Plant

with app.app_context():
    # Clear existing data
    Plant.query.delete()

    # Sample plant data
    plants = [
        Plant(
            id=1,
            name="Aloe",
            image="./images/aloe.jpg",
            price=11.50,
            is_in_stock=True,
        ),
        Plant(
            id=2,
            name="ZZ Plant",
            image="./images/zz-plant.jpg",
            price=25.98,
            is_in_stock=False,
        ),
        Plant(
            id=3,
            name="Fiddle Leaf Fig",
            image="./images/fiddle-leaf-fig.jpg",
            price=45.00,
            is_in_stock=True,
        ),
        Plant(
            id=4,
            name="Snake Plant",
            image="./images/snake-plant.jpg",
            price=19.75,
            is_in_stock=True,
        ),
    ]

    # Add all plants and commit
    db.session.add_all(plants)
    db.session.commit()

    print(f"Seeded {len(plants)} plants into the database!")
