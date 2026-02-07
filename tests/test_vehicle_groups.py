import pytest
from unittest import mock
import json
import importlib
import builtins
import sys
from typing import Any

# Import modules to be tested
import vehicle_groups
import products
import materials

class TestVehicleGroups:
    def teardown_method(self):
        # Reset modules to original state after each test
        importlib.reload(products)
        importlib.reload(vehicle_groups)

    def test_happy_path_groups(self):
        """Test that vehicle groups are populated correctly with standard data."""
        # Ensure we are using the real data (or at least valid data)
        importlib.reload(products)
        importlib.reload(vehicle_groups)
        
        # Check specific vehicles exist in groups
        # Based on products.json content provided in context
        
        # Warden
        if "Chieftain" in vars(products):
            assert "Chieftain" in vehicle_groups.Warden
            assert vehicle_groups.Warden["Chieftain"].faction == "warden"
        
        # Colonial
        if "Ares" in vars(products):
            assert "Ares" in vehicle_groups.Colonial
            assert vehicle_groups.Colonial["Ares"].faction == "colonial"
        
        # All
        if "RSC" in vars(products):
            assert "RSC" in vehicle_groups.All
            assert vehicle_groups.All["RSC"].faction == "all"
        
        # Verify no overlap (simplistic check)
        # Note: Chieftain is Warden, so shouldn't be in Colonial or All
        if "Chieftain" in vehicle_groups.Warden:
            assert "Chieftain" not in vehicle_groups.Colonial
            assert "Chieftain" not in vehicle_groups.All

    def test_invalid_materials_skipped(self):
        """Test that products with invalid materials are skipped."""
        mock_data = {
            "ValidVehicle": {
                "faction": "warden",
                "cost": {"PCmat": 10.0} # Valid
            },
            "InvalidVehicle": {
                "faction": "warden",
                "cost": {"Unobtainium": 10.0} # Invalid material
            }
        }
        
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(mock_data))):
            with mock.patch("json.load", return_value=mock_data):
                importlib.reload(products)
                importlib.reload(vehicle_groups)
                
                # Check results
                assert "ValidVehicle" in vehicle_groups.Warden
                assert "InvalidVehicle" not in vehicle_groups.Warden
                
                # Verify it was not created in products module
                assert hasattr(products, "ValidVehicle")
                assert not hasattr(products, "InvalidVehicle")

    def test_missing_faction_defaults_to_all(self):
        """Test that products with missing faction default to 'all'."""
        mock_data = {
            "NoFactionVehicle": {
                "cost": {"PCmat": 10.0}
                # Missing faction key
            }
        }
        
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(mock_data))):
            with mock.patch("json.load", return_value=mock_data):
                importlib.reload(products)
                importlib.reload(vehicle_groups)
                
                assert "NoFactionVehicle" in vehicle_groups.All
                assert vehicle_groups.All["NoFactionVehicle"].faction == "all"

    def test_empty_faction_defaults_to_all(self):
        """Test that products with empty string faction default to 'all'."""
        mock_data = {
            "EmptyFactionVehicle": {
                "faction": "",
                "cost": {"PCmat": 10.0}
            }
        }
        
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(mock_data))):
            with mock.patch("json.load", return_value=mock_data):
                importlib.reload(products)
                importlib.reload(vehicle_groups)
                
                assert "EmptyFactionVehicle" in vehicle_groups.All
                assert vehicle_groups.All["EmptyFactionVehicle"].faction == "all"

    def test_invalid_faction_skipped(self):
        """Test that products with invalid faction are skipped."""
        mock_data = {
            "AlienVehicle": {
                "faction": "aliens",
                "cost": {"PCmat": 10.0}
            }
        }
        
        with mock.patch("builtins.open", mock.mock_open(read_data=json.dumps(mock_data))):
            with mock.patch("json.load", return_value=mock_data):
                importlib.reload(products)
                importlib.reload(vehicle_groups)
                
                assert "AlienVehicle" not in vehicle_groups.Warden
                assert "AlienVehicle" not in vehicle_groups.Colonial
                assert "AlienVehicle" not in vehicle_groups.All
                assert not hasattr(products, "AlienVehicle")
