#!/usr/bin/env python3

from app import app
from models import db, Plant

with app.app_context():
    db.create_all()

    # Add sample plants (Make sure all have `name`, `image`, and `price`)
    plant1 = Plant(name="Aloe", image="https://example.com/aloe.jpg", price=11.50)
    plant2 = Plant(name="ZZ Plant", image="https://example.com/zz-plant.jpg", price=25.98)

    db.session.add_all([plant1, plant2])
    db.session.commit()

    print("Database seeded successfully!")