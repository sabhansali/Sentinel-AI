"""
Test data generator to populate the admin dashboard with seed data.
This allows testing the dashboard with realistic metrics without needing
to run many actual analyses.
"""
from datetime import datetime, timedelta
import json
from pathlib import Path
from ai_risk_engine.data_tracker import tracker

# Data file
DATA_FILE = Path(__file__).parent / "analysis_log.json"


def generate_test_data():
    """Generate realistic seed data for testing"""
    
    # Clear existing data
    tracker.analyses = []
    
    # Sample prompts and their characteristics
    test_records = [
        # Device: ENG-LAPTOP-21
        {
            "timestamp": (datetime.now() - timedelta(hours=h)).isoformat(),
            "device_id": "ENG-LAPTOP-21",
            "prompt_type": "Code Debugging",
            "decision": "ALLOW",
            "total_risk": 15,
            "code_detected": True,
            "semantic_similarity": 0.25,
            "pii_risk": 2,
            "db_risk": 1,
            "secret_risk": 3,
            "prompt_length": 220
        }
        for h in range(1, 35)
    ]
    
    # Add some ALLOW decisions for ENG-LAPTOP-21
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=h)).isoformat(),
            "device_id": "ENG-LAPTOP-21",
            "prompt_type": "General Queries",
            "decision": "ALLOW",
            "total_risk": 12,
            "code_detected": False,
            "semantic_similarity": 0.18,
            "pii_risk": 1,
            "db_risk": 0,
            "secret_risk": 1,
            "prompt_length": 150
        }
        for h in range(15)
    ])
    
    # Add some REVIEW/SANITIZED decisions for ENG-LAPTOP-21
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=5)).isoformat(),
            "device_id": "ENG-LAPTOP-21",
            "prompt_type": "Code Debugging",
            "decision": "REVIEW",
            "total_risk": 45,
            "code_detected": True,
            "semantic_similarity": 0.55,
            "pii_risk": 8,
            "db_risk": 3,
            "secret_risk": 5,
            "prompt_length": 350
        }
    ])
    
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "device_id": "ENG-LAPTOP-21",
            "prompt_type": "General Queries",
            "decision": "REVIEW",
            "total_risk": 42,
            "code_detected": False,
            "semantic_similarity": 0.48,
            "pii_risk": 12,
            "db_risk": 2,
            "secret_risk": 7,
            "prompt_length": 280
        }
    ])
    
    # Add BLOCK decisions for ENG-LAPTOP-21
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
            "device_id": "ENG-LAPTOP-21",
            "prompt_type": "Proprietary Logic",
            "decision": "BLOCK",
            "total_risk": 78,
            "code_detected": True,
            "semantic_similarity": 0.72,
            "pii_risk": 25,
            "db_risk": 15,
            "secret_risk": 18,
            "prompt_length": 450
        }
    ])
    
    # Device: DATA-LAPTOP-11
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=h)).isoformat(),
            "device_id": "DATA-LAPTOP-11",
            "prompt_type": "Data Analysis",
            "decision": "ALLOW",
            "total_risk": 18,
            "code_detected": False,
            "semantic_similarity": 0.22,
            "pii_risk": 3,
            "db_risk": 2,
            "secret_risk": 2,
            "prompt_length": 190
        }
        for h in range(1, 22)
    ])
    
    # Add some REVIEW for DATA-LAPTOP-11
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
            "device_id": "DATA-LAPTOP-11",
            "prompt_type": "Data Analysis",
            "decision": "REVIEW",
            "total_risk": 48,
            "code_detected": False,
            "semantic_similarity": 0.51,
            "pii_risk": 15,
            "db_risk": 8,
            "secret_risk": 6,
            "prompt_length": 320
        }
    ])
    
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
            "device_id": "DATA-LAPTOP-11",
            "prompt_type": "Data Analysis",
            "decision": "REVIEW",
            "total_risk": 50,
            "code_detected": False,
            "semantic_similarity": 0.53,
            "pii_risk": 18,
            "db_risk": 12,
            "secret_risk": 8,
            "prompt_length": 280
        }
    ])
    
    # Device: DEV-LAPTOP-87
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=h)).isoformat(),
            "device_id": "DEV-LAPTOP-87",
            "prompt_type": "Code Debugging" if h % 2 == 0 else "Proprietary Logic",
            "decision": "ALLOW",
            "total_risk": 20 if h % 2 == 0 else 25,
            "code_detected": True,
            "semantic_similarity": 0.28 if h % 2 == 0 else 0.32,
            "pii_risk": 2 if h % 2 == 0 else 4,
            "db_risk": 1 if h % 2 == 0 else 2,
            "secret_risk": 2 if h % 2 == 0 else 4,
            "prompt_length": 240 if h % 2 == 0 else 310
        }
        for h in range(1, 35)
    ])
    
    # Add REVIEW for DEV-LAPTOP-87
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=7)).isoformat(),
            "device_id": "DEV-LAPTOP-87",
            "prompt_type": "Code Debugging",
            "decision": "REVIEW",
            "total_risk": 52,
            "code_detected": True,
            "semantic_similarity": 0.58,
            "pii_risk": 10,
            "db_risk": 4,
            "secret_risk": 8,
            "prompt_length": 380
        }
    ])
    
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(),
            "device_id": "DEV-LAPTOP-87",
            "prompt_type": "Proprietary Logic",
            "decision": "REVIEW",
            "total_risk": 55,
            "code_detected": True,
            "semantic_similarity": 0.62,
            "pii_risk": 12,
            "db_risk": 6,
            "secret_risk": 10,
            "prompt_length": 420
        }
    ])
    
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=9)).isoformat(),
            "device_id": "DEV-LAPTOP-87",
            "prompt_type": "Proprietary Logic",
            "decision": "REVIEW",
            "total_risk": 58,
            "code_detected": True,
            "semantic_similarity": 0.65,
            "pii_risk": 14,
            "db_risk": 7,
            "secret_risk": 11,
            "prompt_length": 450
        }
    ])
    
    # Add BLOCK decisions for DEV-LAPTOP-87
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=10)).isoformat(),
            "device_id": "DEV-LAPTOP-87",
            "prompt_type": "Proprietary Logic",
            "decision": "BLOCK",
            "total_risk": 81,
            "code_detected": True,
            "semantic_similarity": 0.74,
            "pii_risk": 28,
            "db_risk": 18,
            "secret_risk": 20,
            "prompt_length": 520
        }
    ])
    
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=11)).isoformat(),
            "device_id": "DEV-LAPTOP-87",
            "prompt_type": "Code Debugging",
            "decision": "BLOCK",
            "total_risk": 75,
            "code_detected": True,
            "semantic_similarity": 0.68,
            "pii_risk": 22,
            "db_risk": 13,
            "secret_risk": 16,
            "prompt_length": 480
        }
    ])
    
    test_records.extend([
        {
            "timestamp": (datetime.now() - timedelta(hours=12)).isoformat(),
            "device_id": "DEV-LAPTOP-87",
            "prompt_type": "Proprietary Logic",
            "decision": "BLOCK",
            "total_risk": 83,
            "code_detected": True,
            "semantic_similarity": 0.76,
            "pii_risk": 30,
            "db_risk": 20,
            "secret_risk": 22,
            "prompt_length": 550
        }
    ])
    
    # Load all records
    tracker.analyses = test_records
    tracker.save_to_file()
    
    print(f"✅ Generated {len(test_records)} test records")
    print(f"📁 Data saved to: {DATA_FILE}")
    
    # Print summary
    stats = tracker.get_statistics()
    print(f"\n📊 Summary:")
    print(f"   Total Prompts: {stats['total']}")
    print(f"   Safe (ALLOW): {stats['safe']}")
    print(f"   Sanitized (REVIEW): {stats['sanitized']}")
    print(f"   Blocked (BLOCK): {stats['blocked']}")


if __name__ == "__main__":
    generate_test_data()
