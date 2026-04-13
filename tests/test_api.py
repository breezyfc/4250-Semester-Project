# test for the API endpoints/environment

# setting up a sample here to ensure all tests follow the same format and to avoid repetition. 
# This is not a fixture since we want to be able to customize the user_id for some tests.
def _sample_assignment_json(user_id: int = 1):
    return {
        "user_id": user_id,
        "name": "Unit test assignment",
        "course": "CSCI 4250",
        "course_id": "4250",
        "due_date": "2026-04-18",
        "due_time": None,
        "assignment_type": "homework",
        "priority_level": 3,
        "points": 10.0,
        "color": "#517664",
    }

# should return a 201 status code for assignment created
def test_create_assignment_returns_201(api_client):
    response = api_client.post("/assignments/", json=_sample_assignment_json())
    assert response.status_code == 201
    body = response.json()
    assert body["id"] >= 1
    assert body["name"] == "Unit test assignment"
    assert body["course"] == "CSCI 4250"

# returns a 404 status for the assignment not found 
def test_read_assignment_not_found_returns_404(api_client):
    response = api_client.get("/assignments/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Assignment not found"

# pulling in all CRUD pieces at once for a single assignment and clarity purposes
def test_create_read_update_delete_round_trip(api_client):
    create = api_client.post("/assignments/", json=_sample_assignment_json(user_id=5))
    assert create.status_code == 201
    assignment_id = create.json()["id"]

    read = api_client.get(f"/assignments/{assignment_id}")
    assert read.status_code == 200
    assert read.json()["user_id"] == 5

    updated = api_client.put(
        f"/assignments/{assignment_id}",
        json={"name": "Renamed for pytest"},
    )
    assert updated.status_code == 200
    assert updated.json()["name"] == "Renamed for pytest"

    deleted = api_client.delete(f"/assignments/{assignment_id}")
    assert deleted.status_code == 204

    missing = api_client.get(f"/assignments/{assignment_id}")
    assert missing.status_code == 404