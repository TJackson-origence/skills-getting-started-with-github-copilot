"""Tests for the Mergington High School API endpoints"""

import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Test the /activities endpoint"""
    
    def test_get_activities_returns_200(self, client):
        """Test that /activities returns a 200 status code"""
        response = client.get("/activities")
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that /activities returns a dictionary"""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)
    
    def test_get_activities_contains_expected_activities(self, client):
        """Test that the response contains expected activities"""
        response = client.get("/activities")
        activities = response.json()
        
        expected_activities = ["Chess Club", "Programming Class", "Gym Class", 
                              "Basketball Team", "Soccer Club", "Art Studio", 
                              "Theater Club", "Debate Team", "Science Club"]
        
        for activity in expected_activities:
            assert activity in activities
    
    def test_activity_has_required_fields(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignup:
    """Test the /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client):
        """Test successful signup for a new student"""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        assert "Signed up newstudent@mergington.edu" in response.json()["message"]
    
    def test_signup_updates_participants_list(self, client):
        """Test that signup adds the student to participants"""
        email = "testuser@mergington.edu"
        
        # Sign up
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 200
        
        # Verify in activities list
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
    
    def test_signup_invalid_activity_returns_404(self, client):
        """Test that signing up for non-existent activity returns 404"""
        response = client.post(
            "/activities/NonExistent%20Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_student_returns_400(self, client):
        """Test that duplicate signup returns 400"""
        email = "michael@mergington.edu"
        
        # First signup (will fail because already registered)
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_without_email_returns_error(self, client):
        """Test that signup without email returns error"""
        response = client.post("/activities/Chess%20Club/signup")
        assert response.status_code == 422


class TestUnregister:
    """Test the /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client):
        """Test successful unregister of a student"""
        email = "test_unregister@mergington.edu"
        
        # First, sign up the student
        client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        
        # Then unregister
        response = client.delete(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
        assert f"Unregistered {email}" in response.json()["message"]
    
    def test_unregister_removes_participant(self, client):
        """Test that unregister removes student from participants"""
        email = "test_participant@mergington.edu"
        
        # Sign up
        client.post(
            f"/activities/Programming%20Class/signup?email={email}"
        )
        
        # Verify signed up
        activities_response = client.get("/activities")
        assert email in activities_response.json()["Programming Class"]["participants"]
        
        # Unregister
        client.delete(
            f"/activities/Programming%20Class/unregister?email={email}"
        )
        
        # Verify removed
        activities_response = client.get("/activities")
        assert email not in activities_response.json()["Programming Class"]["participants"]
    
    def test_unregister_invalid_activity_returns_404(self, client):
        """Test that unregistering from non-existent activity returns 404"""
        response = client.delete(
            "/activities/Fake%20Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_student_not_registered_returns_400(self, client):
        """Test that unregistering non-registered student returns 400"""
        response = client.delete(
            "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
        )
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_without_email_returns_error(self, client):
        """Test that unregister without email returns error"""
        response = client.delete("/activities/Chess%20Club/unregister")
        assert response.status_code == 422


class TestRootEndpoint:
    """Test the root / endpoint"""
    
    def test_root_redirects_to_static(self, client):
        """Test that / redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
