"""
Firebase Configuration and Initialization
"""
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime

class FirebaseConfig:
    def __init__(self):
        self.app = None
        self.db = None
        self.is_initialized = False
        
        # Try to initialize Firebase
        self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase with service account or environment variables"""
        try:
            # Check if already initialized
            if firebase_admin._apps:
                self.app = firebase_admin.get_app()
                self.db = firestore.client()
                self.is_initialized = True
                print("✅ Firebase already initialized")
                return True
            
            # Method 1: Try service account key file
            service_account_path = os.path.join(os.path.dirname(__file__), 'firebase-service-account.json')
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                self.app = firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.is_initialized = True
                print("✅ Firebase initialized with service account key")
                return True
            
            # Method 2: Try environment variables
            if os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY'):
                service_account_info = json.loads(os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY'))
                cred = credentials.Certificate(service_account_info)
                self.app = firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.is_initialized = True
                print("✅ Firebase initialized with environment variables")
                return True
            
            # Method 3: Try Google Application Default Credentials (for local development)
            if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
                cred = credentials.ApplicationDefault()
                self.app = firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.is_initialized = True
                print("✅ Firebase initialized with Application Default Credentials")
                return True
            
            print("⚠️ Firebase not configured. Please set up Firebase credentials.")
            print("   1. Download service account key as 'firebase-service-account.json'")
            print("   2. Or set FIREBASE_SERVICE_ACCOUNT_KEY environment variable")
            print("   3. Or run 'python setup_firebase.py' for guided setup")
            return False
            
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            return False
    
    def is_available(self):
        """Check if Firebase is available and initialized"""
        return self.is_initialized and self.db is not None
    
    def get_firestore_client(self):
        """Get Firestore database client"""
        if self.is_available():
            return self.db
        return None
    
    def create_sample_data(self):
        """Create sample data for testing"""
        if not self.is_available():
            print("❌ Firebase not available, cannot create sample data")
            return False
        
        try:
            # Create sample sensor data
            sensor_collection = self.db.collection('sensor_data')
            
            # Check if sample data already exists
            existing_data = sensor_collection.limit(1).get()
            if len(existing_data) > 0:
                print("📊 Sample data already exists")
                return True
            
            print("📊 Creating sample sensor data...")
            from datetime import timedelta
            import random
            
            # Generate sample data for the past 24 hours
            for hours_ago in range(24):
                timestamp = datetime.now() - timedelta(hours=hours_ago)
                
                sample_data = {
                    'timestamp': timestamp,
                    'temperature': round(random.uniform(20, 30), 1),
                    'dissolved_oxygen': round(random.uniform(4, 12), 2),
                    'ammonia': round(random.uniform(0, 5), 3),
                    'location': 'Tank A',
                    'sensor_id': 'SENSOR_001'
                }
                
                sensor_collection.add(sample_data)
            
            # Create sample alerts
            alerts_collection = self.db.collection('alerts')
            sample_alerts = [
                {
                    'timestamp': datetime.now() - timedelta(minutes=10),
                    'type': 'warning',
                    'message': 'Ammonia level approaching lower threshold',
                    'sensor_id': 'SENSOR_001',
                    'value': 2.5,
                    'threshold': 5.0,
                    'acknowledged': False
                },
                {
                    'timestamp': datetime.now() - timedelta(hours=2),
                    'type': 'info',
                    'message': 'Temperature sensor calibration completed',
                    'sensor_id': 'SENSOR_002',
                    'acknowledged': True
                },
                {
                    'timestamp': datetime.now() - timedelta(hours=4),
                    'type': 'success',
                    'message': 'Water quality parameters optimal',
                    'sensor_id': 'SENSOR_001',
                    'acknowledged': True
                }
            ]
            
            for alert in sample_alerts:
                alerts_collection.add(alert)
            
            # Create system settings
            settings_collection = self.db.collection('system_settings')
            system_settings = {
                'tank_settings': {
                    'tank_a': {
                        'name': 'Tank A - Main Production',
                        'capacity_liters': 10000,
                        'fish_species': 'Atlantic Salmon',
                        'fish_count': 500,
                        'optimal_ammonia_range': [0, 1.0],
                        'optimal_temp_range': [18, 24],
                        'optimal_do_range': [6, 12]
                    }
                },
                'alert_thresholds': {
                    'ammonia_min': 0,
                    'ammonia_max': 1.0,
                    'temp_min': 18,
                    'temp_max': 30,
                    'do_min': 4,
                    'do_max': 12},
                'system_info': {
                    'installation_date': datetime(2024, 1, 15),
                    'last_maintenance': datetime.now() - timedelta(days=3),
                    'next_maintenance': datetime.now() + timedelta(days=27),
                    'firmware_version': 'v2.1.3'
                },
                'created_at': datetime.now()
            }
            
            settings_collection.add(system_settings)
            
            print("✅ Sample data created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            return False

# Global Firebase configuration instance
firebase_config = FirebaseConfig()
