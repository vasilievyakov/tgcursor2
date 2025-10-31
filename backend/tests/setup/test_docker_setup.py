"""
Basic integration test to verify Docker setup works.
"""
import pytest
import os
import subprocess


@pytest.mark.integration
class TestDockerSetup:
    """Test Docker setup and services."""
    
    @pytest.fixture(scope="class")
    def docker_compose_file(self):
        """Return path to docker-compose.yml."""
        return os.path.join(os.path.dirname(__file__), "../../../docker-compose.yml")
    
    def test_docker_compose_file_exists(self, docker_compose_file):
        """Test that docker-compose.yml file exists."""
        assert os.path.exists(docker_compose_file), "docker-compose.yml should exist"
    
    def test_docker_compose_valid(self, docker_compose_file):
        """Test that docker-compose.yml is valid."""
        try:
            result = subprocess.run(
                ["docker-compose", "-f", docker_compose_file, "config"],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0, f"docker-compose config failed: {result.stderr}"
        except FileNotFoundError:
            pytest.skip("docker-compose not installed")
        except subprocess.TimeoutExpired:
            pytest.skip("docker-compose config timed out")

