"""Shared pytest fixtures for FuncBench tests."""

import pytest
from funcbench import GaussianTranslation
from funcbench.agent import Agent, ACTION_STAY


@pytest.fixture
def gaussian_function():
    """Provide a standard GaussianTranslation function for testing.

    Returns a GaussianTranslation instance with default parameters.
    This fixture is used across multiple test modules for consistency.
    """
    return GaussianTranslation()


@pytest.fixture
def mock_agent():
    """Provide a simple mock agent for testing.

    Returns a basic Agent implementation that always returns ACTION_STAY.
    This fixture is useful for testing environment functionality without
    complex agent logic.
    """
    class MockAgent(Agent):
        def get_action(self, observation):
            return ACTION_STAY

    return MockAgent()
