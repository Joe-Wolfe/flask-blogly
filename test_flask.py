import unittest
from app import app, db
from models import User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False


class BloglyTestCase(unittest.TestCase):
    """Tests for Blogly"""

    def setUp(self):
        """Add sample user."""

        db.drop_all()
        db.create_all()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_home_page_redirect(self):
        """Test if home page redirects to user_list"""

        with app.test_client() as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "user_list")

    def test_list_users(self):
        """Test if list_users shows all users"""

        with app.test_client() as client:
            resp = client.get("/user_list")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_create_user(self):
        """Test if create_user adds a new user"""

        with app.test_client() as client:
            data = {"first_name": "New", "last_name": "User", "url": ""}
            resp = client.post("/create_user", data=data,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New User", html)

    def test_show_user(self):
        """Test if show_user displays the selected user's profile"""

        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_edit_user(self):
        """Test if edit_user updates the user's info"""

        with app.test_client() as client:
            data = {"id": self.user_id, "first_name": "Edited",
                    "last_name": "User", "url": ""}
            resp = client.post("/edit_user", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edited User", html)

    def test_delete_user(self):
        """Test if delete_user removes the selected user"""

        with app.test_client() as client:
            resp = client.post(
                f"/delete_user/{self.user_id}", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test User", html)
