import sys
import os
import time
import subprocess
import urllib.request
import json
import asyncio
from database import init_db, get_db
from models import Lead
from sqlalchemy import select, delete

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

PORT = 8002
BASE_URL = f"http://127.0.0.1:{PORT}"

async def setup_test_data():
    print("Setting up test data directly in DB...")
    await init_db()
    async for db in get_db():
        # Clean up first
        await db.execute(delete(Lead).where(Lead.email == "api_test@example.com"))
        await db.commit()
        
        # Create lead
        lead = Lead(name="API Test", email="api_test@example.com", status="Pending")
        db.add(lead)
        await db.commit()
        await db.refresh(lead)
        print(f"Created test lead with ID: {lead.id}")
        return lead.id

def test_delete_api(lead_id):
    print(f"Testing DELETE API for lead_id: {lead_id}...")
    url = f"{BASE_URL}/leads/delete"
    data = {
        "lead_ids": [lead_id],
        "all": False
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = response.read().decode('utf-8')
            print(f"Response Status: {status}")
            print(f"Response Body: {body}")
            
            if status == 200:
                print(f"{GREEN}API Call Successful{RESET}")
                return True
            else:
                print(f"{RED}API Call Failed{RESET}")
                return False
    except urllib.error.HTTPError as e:
        print(f"{RED}HTTP Error: {e.code} - {e.read().decode('utf-8')}{RESET}")
        return False
    except Exception as e:
        print(f"{RED}Connection Error: {e}{RESET}")
        return False

def run_test():
    # 1. Setup Data
    lead_id = asyncio.run(setup_test_data())
    
    # 2. Start Server
    print("Starting Uvicorn server...")
    # Using sys.executable to ensure we use the same python environment
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", str(PORT)],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        # Check if process is still alive
        if proc.poll() is not None:
            print(f"{RED}Server failed to start!{RESET}")
            out, err = proc.communicate()
            print(out.decode())
            print(err.decode())
            return
            
        # 3. Call API
        success = test_delete_api(lead_id)
        
        # 4. Cleanup/Result
        if success:
            print(f"{GREEN}TEST PASSED: Delete endpoint works via HTTP.{RESET}")
        else:
            print(f"{RED}TEST FAILED: Delete endpoint failed.{RESET}")
            
    finally:
        print("Killing server...")
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()

if __name__ == "__main__":
    run_test()
