from google.cloud import storage
import os

def create_bucket():
    # Uses your local ADC credentials automatically
    client = storage.Client(project="youth-wellness-mcp")
    
    bucket_name = "youth-crisis-data-bucket"
    
    try:
        # Create bucket
        bucket = client.create_bucket(bucket_name, location="US")
        print(f"✅ Bucket {bucket.name} created successfully!")
        return bucket
    except Exception as e:
        if "already exists" in str(e):
            print(f"✅ Bucket {bucket_name} already exists - using it!")
            return client.bucket(bucket_name)
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_bucket()
