# tests/test.py
import unittest
from datetime import datetime
from website import app, db  
from website.models import Reservation, RentalAgreement  

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_reservation_model(self):
        reservation = Reservation(user_id=1, vehicle_id=1, checkin=datetime.now(), checkout=datetime.now())
        db.session.add(reservation)
        db.session.commit()
        self.assertIsNotNone(reservation.id)

    def test_rental_agreement_model(self):
        rental_agreement = RentalAgreement(reservation_id=1, user_id=1, duration=5, price=100.00)
        db.session.add(rental_agreement)
        db.session.commit()
        self.assertIsNotNone(rental_agreement.id)

if __name__ == '__main__':
    unittest.main()

