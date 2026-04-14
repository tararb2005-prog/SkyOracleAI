import os

print("🚀 Running SkyOracle AI Pipeline...")

os.system("python services/fetch.py Bangalore")
os.system("python services/process.py")
os.system("python services/predict.py")

print("✅ All steps completed successfully!")