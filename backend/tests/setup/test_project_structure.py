"""
Tests for project setup and structure.
"""
import os
import pytest


class TestProjectStructure:
    """Test that project structure is correctly set up."""
    
    def test_docker_compose_exists(self):
        """Test that docker-compose.yml exists."""
        assert os.path.exists("docker-compose.yml"), "docker-compose.yml should exist"
    
    def test_backend_directory_exists(self):
        """Test that backend directory exists."""
        assert os.path.isdir("backend"), "backend directory should exist"
    
    def test_frontend_directory_exists(self):
        """Test that frontend directory exists."""
        assert os.path.isdir("frontend"), "frontend directory should exist"
    
    def test_env_example_exists(self):
        """Test that .env.example exists."""
        assert os.path.exists(".env.example"), ".env.example should exist"
    
    def test_backend_requirements_exists(self):
        """Test that backend requirements.txt exists."""
        assert os.path.exists("backend/requirements.txt"), "backend/requirements.txt should exist"
    
    def test_backend_dockerfile_exists(self):
        """Test that backend Dockerfile exists."""
        assert os.path.exists("backend/Dockerfile"), "backend/Dockerfile should exist"
    
    def test_frontend_package_json_exists(self):
        """Test that frontend package.json exists."""
        assert os.path.exists("frontend/package.json"), "frontend/package.json should exist"
    
    def test_frontend_dockerfile_exists(self):
        """Test that frontend Dockerfile exists."""
        assert os.path.exists("frontend/Dockerfile"), "frontend/Dockerfile should exist"
    
    def test_ci_workflow_exists(self):
        """Test that CI workflow exists."""
        assert os.path.exists(".github/workflows/ci.yml"), "CI workflow should exist"
    
    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        assert os.path.exists(".gitignore"), ".gitignore should exist"


class TestDockerComposeConfig:
    """Test docker-compose.yml configuration."""
    
    def test_docker_compose_has_postgres(self):
        """Test that docker-compose.yml has postgres service."""
        with open("docker-compose.yml", "r") as f:
            content = f.read()
            assert "postgres:" in content, "PostgreSQL service should be configured"
    
    def test_docker_compose_has_redis(self):
        """Test that docker-compose.yml has redis service."""
        with open("docker-compose.yml", "r") as f:
            content = f.read()
            assert "redis:" in content, "Redis service should be configured"
    
    def test_docker_compose_has_backend(self):
        """Test that docker-compose.yml has backend service."""
        with open("docker-compose.yml", "r") as f:
            content = f.read()
            assert "backend:" in content, "Backend service should be configured"
    
    def test_docker_compose_has_frontend(self):
        """Test that docker-compose.yml has frontend service."""
        with open("docker-compose.yml", "r") as f:
            content = f.read()
            assert "frontend:" in content, "Frontend service should be configured"

