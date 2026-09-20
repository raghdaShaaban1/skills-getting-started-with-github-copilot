from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_unregisters_student():
    activity_name = "Chess Club"
    email = "student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_delete_participant_returns_404_for_missing_activity():
    response = client.delete("/activities/Unknown Activity/participants/student@mergington.edu")
    assert response.status_code == 404
