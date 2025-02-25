from includes.config import DatabaseConfig
import uuid
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

            # Fetch all activities
            fetch_query = "SELECT id, title, activity, color_hex, created_at FROM activity"
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