from includes.config import DatabaseConfig
import uuid
import bcrypt
from datetime import datetime

class ActivityService:
    def __init__(self):
        """Initialize the ActivityService with database configuration."""
        self.db = DatabaseConfig()

    def insert_activity(self, title, activity_date, activity_end, color_hex):
        """
        Insert a new activity record into the activity table.

        Parameters:
        title (str): The title of the activity.
        activity_date (str): The start date of the activity in 'YYYY-MM-DD' format.
        activity_end (str): The end date of the activity in 'YYYY-MM-DD' format.
        color_hex (str): The color code in hex format.

        Returns:
        dict: Contains success status and any error message.
        """
        if not self.db.connect():
            return {
                "success": False,
                "message": "Database connection failed"
            }

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Insert the activity record
            insert_query = """
            INSERT INTO activity (id, title, activity, activity_end, color_hex, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            activity_id = str(uuid.uuid4())
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_query, (activity_id, title, activity_date, activity_end, color_hex, created_at))
            self.db.connection.commit()

            return {
                "success": True,
                "message": "Activity inserted successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error inserting activity: {str(e)}"
            }

        finally:
            cursor.close()
            self.db.disconnect()

    def fetch_activities(self):
        """
        Fetch all activities from the activity table.

        Returns:
        list: A list of dictionaries containing activity details.
        """
        if not self.db.connect():
            return {
                "success": False,
                "message": "Database connection failed"
            }

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Fetch all activities including activity_end
            fetch_query = "SELECT id, title, activity, activity_end, color_hex, created_at FROM activity"
            cursor.execute(fetch_query)
            activities = cursor.fetchall()

            return {
                "success": True,
                "activities": activities
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching activities: {str(e)}"
            }

        finally:
            cursor.close()
            self.db.disconnect()

    def fetch_activity_by_id(self, activity_id):
        """
        Fetch a specific activity by its ID from the activity table.

        Parameters:
        activity_id (str): The unique ID of the activity to fetch.

        Returns:
        dict: Contains success status and the activity details or an error message.
        """
        if not self.db.connect():
            return {
                "success": False,
                "message": "Database connection failed"
            }

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Fetch the activity by ID
            fetch_query = "SELECT id, title, activity, activity_end, color_hex, created_at FROM activity WHERE id = %s"
            cursor.execute(fetch_query, (activity_id,))
            activity = cursor.fetchone()

            if activity:
                return {
                    "success": True,
                    "activity": activity
                }
            else:
                return {
                    "success": False,
                    "message": "Activity not found"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching activity: {str(e)}"
            }

        finally:
            cursor.close()
            self.db.disconnect()

    def check_code(self, code):
        """
        Check if the provided code matches any hashed code in the web_development_team_code table.

        Parameters:
        code (str): The code to check.

        Returns:
        dict: Contains success status and any error message.
        """
        if not self.db.connect():
            return {
                "success": False,
                "message": "Database connection failed"
            }

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Fetch all hashed codes from the table
            check_query = "SELECT code FROM web_development_team_code"
            cursor.execute(check_query)
            results = cursor.fetchall()

            # Verify the provided code against each hashed code
            for result in results:
                hashed_code = result['code'].encode('utf-8')
                if bcrypt.checkpw(code.encode('utf-8'), hashed_code):
                    return {
                        "success": True,
                        "message": "Code is valid"
                    }

            return {
                "success": False,
                "message": "Invalid code"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error checking code: {str(e)}"
            }

        finally:
            cursor.close()
            self.db.disconnect()

    def update_activity(self, activity_id, title=None, activity_date=None, activity_end=None, color_hex=None):
        """
        Update an existing activity record in the activity table.

        Parameters:
        activity_id (str): The unique ID of the activity to update.
        title (str, optional): The new title of the activity.
        activity_date (str, optional): The new start date of the activity in 'YYYY-MM-DD' format.
        activity_end (str, optional): The new end date of the activity in 'YYYY-MM-DD' format.
        color_hex (str, optional): The new color code in hex format.

        Returns:
        dict: Contains success status and any error message.
        """
        if not self.db.connect():
            return {
                "success": False,
                "message": "Database connection failed"
            }

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Update the activity record
            update_query = "UPDATE activity SET "
            update_fields = []
            update_values = []

            if title is not None:
                update_fields.append("title = %s")
                update_values.append(title)
            if activity_date is not None:
                update_fields.append("activity = %s")
                update_values.append(activity_date)
            if activity_end is not None:
                update_fields.append("activity_end = %s")
                update_values.append(activity_end)
            if color_hex is not None:
                update_fields.append("color_hex = %s")
                update_values.append(color_hex)

            update_values.append(activity_id)
            update_query += ", ".join(update_fields) + " WHERE id = %s"

            cursor.execute(update_query, update_values)
            self.db.connection.commit()

            return {
                "success": True,
                "message": "Activity updated successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating activity: {str(e)}"
            }

        finally:
            cursor.close()
            self.db.disconnect()

    def delete_activity(self, activity_id):
        """
        Delete an activity record from the activity table.

        Parameters:
        activity_id (str): The unique ID of the activity to delete.

        Returns:
        dict: Contains success status and any error message.
        """
        if not self.db.connect():
            return {
                "success": False,
                "message": "Database connection failed"
            }

        try:
            cursor = self.db.connection.cursor(dictionary=True)

            # Delete the activity record
            delete_query = "DELETE FROM activity WHERE id = %s"
            cursor.execute(delete_query, (activity_id,))
            self.db.connection.commit()

            return {
                "success": True,
                "message": "Activity deleted successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error deleting activity: {str(e)}"
            }

        finally:
            cursor.close()
            self.db.disconnect()