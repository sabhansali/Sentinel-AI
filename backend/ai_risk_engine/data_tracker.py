"""
Data tracker to record all prompt analyses for dashboard metrics.
Stores data in memory (can be upgraded to database later).
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import threading

DATA_FILE = Path(__file__).parent / "analysis_log.json"
_lock = threading.Lock()


class AnalysisTracker:
    """Tracks all AI prompt analyses for the admin dashboard"""

    def __init__(self):
        self.analyses: List[Dict[str, Any]] = []
        self.load_from_file()

    def load_from_file(self):
        """Load existing analysis log from file"""
        if DATA_FILE.exists():
            try:
                with open(DATA_FILE, 'r') as f:
                    self.analyses = json.load(f)
            except Exception as e:
                print(f"Error loading analysis log: {e}")
                self.analyses = []

    def save_to_file(self):
        """Save analysis log to file"""
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(self.analyses, f, indent=2)
        except Exception as e:
            print(f"Error saving analysis log: {e}")

    def record_analysis(self, analysis_result: Dict[str, Any], device_id: str = "SYSTEM"):
        """Record a prompt analysis result"""
        with _lock:
            # Determine prompt type
            prompt_type = self._determine_prompt_type(analysis_result)
            
            # Create record
            record = {
                "timestamp": datetime.now().isoformat(),
                "device_id": device_id,
                "prompt_type": prompt_type,
                "decision": analysis_result["final"]["decision"],
                "total_risk": analysis_result["final"]["total_risk"],
                "code_detected": analysis_result["code_detected"],
                "semantic_similarity": round(analysis_result["semantic_similarity"], 2),
                "pii_risk": analysis_result["pii"]["risk_score"],
                "db_risk": analysis_result["db"]["risk_score"],
                "secret_risk": analysis_result["secrets"]["risk_score"],
                "prompt_length": len(analysis_result["original"])
            }
            
            self.analyses.append(record)
            self.save_to_file()
            return record

    def _determine_prompt_type(self, analysis_result: Dict[str, Any]) -> str:
        """Determine the type of prompt based on content analysis"""
        semantic_sim = analysis_result["semantic_similarity"]
        has_code = analysis_result["code_detected"]
        pii_risk = analysis_result["pii"]["risk_score"]
        db_risk = analysis_result["db"]["risk_score"]

        if has_code:
            if "debug" in analysis_result["original"].lower():
                return "Code Debugging"
            else:
                return "Proprietary Logic"
        
        if db_risk > 5:
            return "Data Analysis"
        
        if pii_risk > 10:
            return "General Queries"
        
        return "General Queries"

    def get_statistics(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        if not self.analyses:
            return self._get_seed_data()

        total = len(self.analyses)
        safe = sum(1 for a in self.analyses if a["decision"] == "ALLOW")
        sanitized = sum(1 for a in self.analyses if a["decision"] == "REVIEW")
        blocked = sum(1 for a in self.analyses if a["decision"] == "BLOCK")

        # Risk distribution
        low_risk = sum(1 for a in self.analyses if a["total_risk"] < 30)
        medium_risk = sum(1 for a in self.analyses if 30 <= a["total_risk"] < 70)
        high_risk = sum(1 for a in self.analyses if a["total_risk"] >= 70)

        # Prompt type distribution
        prompt_types = {}
        for a in self.analyses:
            pt = a["prompt_type"]
            prompt_types[pt] = prompt_types.get(pt, 0) + 1

        # Device activity
        devices = {}
        for a in self.analyses:
            dev = a["device_id"]
            if dev not in devices:
                devices[dev] = {
                    "prompts": 0,
                    "high_risk": 0,
                    "actions": {"Blocked": 0, "Sanitized": 0, "Allowed": 0}
                }
            devices[dev]["prompts"] += 1
            if a["total_risk"] >= 70:
                devices[dev]["high_risk"] += 1
            
            decision = a["decision"]
            if decision == "BLOCK":
                devices[dev]["actions"]["Blocked"] += 1
            elif decision == "REVIEW":
                devices[dev]["actions"]["Sanitized"] += 1
            else:
                devices[dev]["actions"]["Allowed"] += 1

        return {
            "total": total,
            "safe": safe,
            "sanitized": sanitized,
            "blocked": blocked,
            "risk_distribution": {
                "Low Risk": low_risk,
                "Medium Risk": medium_risk,
                "High Risk": high_risk
            },
            "prompt_types": prompt_types,
            "devices": devices,
            "recent_analyses": sorted(self.analyses, key=lambda x: x["timestamp"], reverse=True)[:20]
        }

    def get_device_analytics(self, device_id: str) -> Dict[str, Any]:
        """Get analytics for a specific device"""
        device_analyses = [a for a in self.analyses if a["device_id"] == device_id]
        
        if not device_analyses:
            return {
                "device_id": device_id,
                "total_prompts": 0,
                "prompt_types": {},
                "risk_distribution": []
            }

        prompt_types = {}
        for a in device_analyses:
            pt = a["prompt_type"]
            prompt_types[pt] = prompt_types.get(pt, 0) + 1

        return {
            "device_id": device_id,
            "total_prompts": len(device_analyses),
            "prompt_types": prompt_types,
            "risk_distribution": device_analyses
        }

    def _get_seed_data(self) -> Dict[str, Any]:
        """Return seed data structure for dashboard display"""
        return {
            "total": 427,
            "safe": 394,
            "sanitized": 21,
            "blocked": 12,
            "risk_distribution": {
                "Low Risk": 336,
                "Medium Risk": 68,
                "High Risk": 23
            },
            "prompt_types": {
                "General Queries": 171,
                "Code Debugging": 149,
                "Data Analysis": 64,
                "Proprietary Logic": 43
            },
            "devices": {
                "ENG-LAPTOP-21": {
                    "prompts": 34,
                    "high_risk": 2,
                    "actions": {"Blocked": 1, "Sanitized": 4, "Allowed": 29}
                },
                "DATA-LAPTOP-11": {
                    "prompts": 21,
                    "high_risk": 0,
                    "actions": {"Blocked": 0, "Sanitized": 2, "Allowed": 19}
                },
                "DEV-LAPTOP-87": {
                    "prompts": 44,
                    "high_risk": 4,
                    "actions": {"Blocked": 3, "Sanitized": 7, "Allowed": 34}
                }
            },
            "recent_analyses": []
        }


# Global tracker instance
tracker = AnalysisTracker()


def record_analysis(analysis_result: Dict[str, Any], device_id: str = "SYSTEM"):
    """Convenience function to record analysis"""
    return tracker.record_analysis(analysis_result, device_id)


def get_dashboard_stats():
    """Convenience function to get dashboard stats"""
    # Reload data from file to ensure fresh data
    tracker.load_from_file()
    return tracker.get_statistics()


def get_device_stats(device_id: str):
    """Convenience function to get device stats"""
    # Reload data from file to ensure fresh data
    tracker.load_from_file()
    return tracker.get_device_analytics(device_id)
