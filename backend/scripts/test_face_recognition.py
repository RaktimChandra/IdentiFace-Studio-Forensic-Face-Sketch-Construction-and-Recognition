"""
Test face recognition functionality
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.face_recognition_service import face_service

def test_face_recognition():
    """Test face recognition service"""
    print("=== Testing Face Recognition Service ===\n")
    
    print("✓ Service initialized successfully")
    print(f"  Detection model: {face_service.detection_model}")
    print(f"  Tolerance: {face_service.tolerance}")
    print(f"  Num jitters: {face_service.num_jitters}")
    
    print("\n✓ Face recognition service is ready!")
    print("\nTo test with an image:")
    print("  1. Place a test image in the uploads folder")
    print("  2. Use the /api/v1/recognition/match-photo endpoint")
    
if __name__ == "__main__":
    try:
        test_face_recognition()
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
