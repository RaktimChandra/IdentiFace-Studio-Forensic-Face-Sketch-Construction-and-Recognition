"""
Face Recognition Service using dlib and face_recognition library
"""

import face_recognition
import numpy as np
import pickle
from PIL import Image
import cv2
from typing import List, Tuple, Optional, Dict
from loguru import logger

from app.core.config import settings


class FaceRecognitionService:
    """Service for face recognition operations"""
    
    def __init__(self):
        self.tolerance = settings.FACE_RECOGNITION_TOLERANCE
        self.detection_model = settings.FACE_DETECTION_MODEL
        self.num_jitters = settings.NUM_JITTERS
    
    def detect_faces(self, image_path: str) -> List[Tuple]:
        """
        Detect faces in an image
        
        Args:
            image_path: Path to image file
            
        Returns:
            List of face locations (top, right, bottom, left)
        """
        try:
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(
                image, 
                model=self.detection_model
            )
            logger.info(f"Detected {len(face_locations)} face(s) in {image_path}")
            return face_locations
        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            return []
    
    def generate_encoding(self, image_path: str) -> Optional[np.ndarray]:
        """
        Generate 128-dimensional face encoding from image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Face encoding as numpy array or None if no face detected
        """
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(
                image,
                num_jitters=self.num_jitters
            )
            
            if encodings:
                logger.info(f"Generated face encoding for {image_path}")
                return encodings[0]
            else:
                logger.warning(f"No face found in {image_path}")
                return None
        except Exception as e:
            logger.error(f"Error generating encoding: {e}")
            return None
    
    def compare_faces(
        self, 
        known_encoding: np.ndarray, 
        unknown_encoding: np.ndarray
    ) -> Tuple[bool, float]:
        """
        Compare two face encodings
        
        Args:
            known_encoding: Known face encoding
            unknown_encoding: Unknown face encoding to compare
            
        Returns:
            Tuple of (is_match, distance)
        """
        try:
            # Calculate face distance (lower is more similar)
            distance = face_recognition.face_distance(
                [known_encoding], 
                unknown_encoding
            )[0]
            
            # Check if match based on tolerance
            is_match = distance <= self.tolerance
            
            # Convert distance to similarity score (0-1)
            similarity = 1 - distance
            
            return is_match, float(similarity)
        except Exception as e:
            logger.error(f"Error comparing faces: {e}")
            return False, 0.0
    
    def batch_compare(
        self,
        query_encoding: np.ndarray,
        database_encodings: List[Tuple[int, np.ndarray]]
    ) -> List[Dict]:
        """
        Compare one face against multiple faces in database
        
        Args:
            query_encoding: Query face encoding
            database_encodings: List of (id, encoding) tuples
            
        Returns:
            List of matches sorted by similarity score
        """
        matches = []
        
        for suspect_id, encoding in database_encodings:
            try:
                is_match, similarity = self.compare_faces(encoding, query_encoding)
                
                if similarity >= settings.MIN_SIMILARITY_SCORE:
                    matches.append({
                        "suspect_id": suspect_id,
                        "similarity_score": similarity,
                        "is_match": is_match,
                        "confidence": "high" if similarity > 0.7 else "medium" if similarity > 0.5 else "low"
                    })
            except Exception as e:
                logger.error(f"Error comparing with suspect {suspect_id}: {e}")
                continue
        
        # Sort by similarity score (highest first)
        matches.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        # Limit results
        return matches[:settings.MAX_RESULTS]
    
    def get_face_landmarks(self, image_path: str) -> Optional[Dict]:
        """
        Get facial landmarks from image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary of facial landmarks or None
        """
        try:
            image = face_recognition.load_image_file(image_path)
            landmarks = face_recognition.face_landmarks(image)
            
            if landmarks:
                return landmarks[0]
            return None
        except Exception as e:
            logger.error(f"Error getting landmarks: {e}")
            return None
    
    def extract_face_crop(
        self, 
        image_path: str, 
        output_path: str,
        padding: int = 50
    ) -> bool:
        """
        Extract and crop face from image
        
        Args:
            image_path: Path to source image
            output_path: Path to save cropped face
            padding: Padding around face in pixels
            
        Returns:
            True if successful, False otherwise
        """
        try:
            image = cv2.imread(image_path)
            face_locations = self.detect_faces(image_path)
            
            if not face_locations:
                return False
            
            # Get first face
            top, right, bottom, left = face_locations[0]
            
            # Add padding
            top = max(0, top - padding)
            right = min(image.shape[1], right + padding)
            bottom = min(image.shape[0], bottom + padding)
            left = max(0, left - padding)
            
            # Crop face
            face_image = image[top:bottom, left:right]
            
            # Save
            cv2.imwrite(output_path, face_image)
            logger.info(f"Saved face crop to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error extracting face: {e}")
            return False
    
    def serialize_encoding(self, encoding: np.ndarray) -> bytes:
        """
        Serialize face encoding for database storage
        
        Args:
            encoding: Face encoding numpy array
            
        Returns:
            Pickled bytes
        """
        return pickle.dumps(encoding)
    
    def deserialize_encoding(self, data: bytes) -> np.ndarray:
        """
        Deserialize face encoding from database
        
        Args:
            data: Pickled bytes
            
        Returns:
            Face encoding numpy array
        """
        return pickle.loads(data)
    
    def estimate_face_quality(self, image_path: str) -> float:
        """
        Estimate quality of face image (0-1 score)
        
        Args:
            image_path: Path to image
            
        Returns:
            Quality score (0-1)
        """
        try:
            image = cv2.imread(image_path)
            
            # Calculate sharpness using Laplacian variance
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Normalize (empirically determined thresholds)
            quality = min(laplacian_var / 1000, 1.0)
            
            return float(quality)
            
        except Exception as e:
            logger.error(f"Error estimating quality: {e}")
            return 0.5


# Singleton instance
face_service = FaceRecognitionService()
