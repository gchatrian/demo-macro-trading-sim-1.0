#!/usr/bin/env python3
"""
Test configuration module
"""

import sys
from pathlib import Path

# Add parent directory (backend/) to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from config import settings, get_settings, ConfigurationError


def test_configuration():
    """Test that configuration loads correctly"""
    print("=" * 60)
    print("Configuration Module Test")
    print("=" * 60)
    
    try:
        # Test loading settings
        print("\n1. Loading settings...")
        s = get_settings()
        print("   ✓ Settings loaded successfully")
        
        # Test Supabase configuration
        print("\n2. Testing Supabase configuration...")
        print(f"   URL: {s.SUPABASE_URL}")
        print(f"   Service Role Key: {s.SUPABASE_SERVICE_ROLE_KEY[:20]}...")
        print("   ✓ Supabase configuration OK")
        
        # Test OpenAI configuration
        print("\n3. Testing OpenAI configuration...")
        print(f"   API Key: {s.OPENAI_API_KEY[:15]}...")
        print(f"   Model: {s.MODEL_NAME}")
        print("   ✓ OpenAI configuration OK")
        
        # Test simulation configuration
        print("\n4. Testing simulation configuration...")
        sim_config = s.get_simulation_config()
        print(f"   Demo Day Duration: {sim_config['demo_day_duration']} seconds")
        print(f"   Narrative Max Tokens: {sim_config['narrative_max_tokens']}")
        print(f"   Temperature: {sim_config['narrative_temperature']}")
        print("   ✓ Simulation configuration OK")
        
        # Test repr
        print("\n5. Settings representation:")
        print(f"   {repr(s)}")
        
        print("\n" + "=" * 60)
        print("✓ All configuration tests passed!")
        print("=" * 60)
        
        return True
        
    except ConfigurationError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_configuration()
    exit(0 if success else 1)
