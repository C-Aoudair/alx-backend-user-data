import unittest
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from db import DB
from user import Base, User

class TestDB(unittest.TestCase):

    def setUp(self):
        """Set up the test database and the DB instance."""
        self.db = DB()

    def tearDown(self):
        """Tear down the test database."""
        Base.metadata.drop_all(self.db._engine)

    def test_find_user_by_id(self):
        """Test finding a user by ID."""
        user = self.db.add_user(email="test@test.com", hashed_password="SuperHashedPwd")
        found_user = self.db.find_user_by(id=user.id)
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.id, user.id)

    def test_find_user_by_email(self):
        """Test finding a user by email."""
        user = self.db.add_user(email="test@test.com", hashed_password="SuperHashedPwd")
        found_user = self.db.find_user_by(email=user.email)
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.email, user.email)

    def test_find_user_by_nonexistent_attribute(self):
        """Test finding a user by a nonexistent attribute."""
        with self.assertRaises(InvalidRequestError):
            self.db.find_user_by(nonexistent_attribute="nonexistent")

    def test_find_user_by_multiple_attributes(self):
        """Test finding a user by multiple attributes."""
        user = self.db.add_user(email="test@test.com", hashed_password="SuperHashedPwd")
        found_user = self.db.find_user_by(email=user.email, hashed_password=user.hashed_password)
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.email, user.email)
        self.assertEqual(found_user.hashed_password, user.hashed_password)

    def test_find_user_by_no_result(self):
        """Test finding a user when no result is found."""
        with self.assertRaises(NoResultFound):
            self.db.find_user_by(email="test@he")

if __name__ == "__main__":
    unittest.main()
