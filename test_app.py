#!/usr/bin/env python3
"""
Activity 5.1-5.3: Integration and Testing
Citizen AI Platform - Unit and Integration Tests
"""

import pytest
import json
from app import app, db, get_ai_response


class TestFlaskApp:
    """Activity 5.1: Unit tests for Flask application"""
    
    @pytest.fixture
    def client(self):
        """Set up test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_index_route(self, client):
        """Activity 5.2: Test main index route"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'active'
        assert data['application'] == 'Citizen AI Platform'
    
    def test_health_check(self, client):
        """Activity 5.3: Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_config_endpoint(self, client):
        """Activity 1.1: Test model configuration endpoint"""
        response = client.get('/config')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'model_config' in data
        assert 'architecture' in data
    
    def test_chat_route(self, client):
        """Activity 2.2: Test chat endpoint"""
        payload = {'message': 'Hello'}
        response = client.post('/chat', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert 'sentiment' in data
    
    def test_feedback_route(self, client):
        """Activity 3.1: Test feedback submission"""
        payload = {'message': 'Great service'}
        response = client.post('/feedback', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'feedback_received'
        assert 'sentiment' in data
    
    def test_analytics_route(self, client):
        """Activity 4.2: Test analytics dashboard"""
        response = client.get('/analytics')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'dashboard' in data


class TestAIFunctionality:
    """Activity 2.x: Test AI response generation"""
    
    def test_ai_response_generation(self):
        """Test AI response function"""
        response = get_ai_response('hello')
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_ai_response_keywords(self):
        """Test keyword matching in AI responses"""
        response = get_ai_response('help')
        assert 'help' in response.lower() or 'assist' in response.lower()


class TestDataHandling:
    """Activity 3.x: Test data handling and storage"""
    
    def test_database_initialization(self):
        """Test database is initialized"""
        assert db is not None
    
    def test_sentiment_analysis(self):
        """Activity 2.3: Test sentiment analysis"""
        positive_text = 'This is excellent and great'
        negative_text = 'This is terrible and awful'
        neutral_text = 'This is neutral text'
        
        assert db.analyze_sentiment(positive_text) == 'Positive'
        assert db.analyze_sentiment(negative_text) == 'Negative'
        assert db.analyze_sentiment(neutral_text) == 'Neutral'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
