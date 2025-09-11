#!/usr/bin/env python3
# test_imports.py
# Quick test script to verify all imports work

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    print("Testing imports...")
    
    from config import DemoConfig
    print("✅ config.py imported successfully")
    
    from utils.snowpark_session import get_snowpark_session
    print("✅ snowpark_session.py imported successfully")
    
    from data_generation.event_log import generate_master_event_log
    print("✅ event_log.py imported successfully")
    
    from data_generation.structured_data import generate_all_structured_data
    print("✅ structured_data.py imported successfully")
    
    from data_generation.unstructured_data import generate_all_unstructured_data
    print("✅ unstructured_data.py imported successfully")
    
    from ai_components.semantic_views import create_all_semantic_views
    print("✅ semantic_views.py imported successfully")
    
    from ai_components.search_services import create_all_search_services
    print("✅ search_services.py imported successfully")
    
    from utils.validation import validate_all_components
    print("✅ validation.py imported successfully")
    
    print("\n🎉 All imports successful! Ready to run demo setup.")
    print(f"📊 Demo will create {DemoConfig.NUM_COMPANIES} companies and {DemoConfig.NUM_CLIENTS} clients")
    print(f"🤖 Using Cortex model: {DemoConfig.CORTEX_MODEL_NAME}")
    print(f"🏔️  Company: Frost Markets Intelligence")
    print(f"🏗️  Compute warehouse: {DemoConfig.COMPUTE_WAREHOUSE}")
    print(f"🔍 Search warehouse: {DemoConfig.SEARCH_WAREHOUSE}")
    print(f"🔗 Default connection: {DemoConfig.SNOWFLAKE_CONNECTION_NAME}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
