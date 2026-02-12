"""
Test script for the RAG Tutor API
Run this to verify the API is working correctly.
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("\n🔍 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_stats():
    """Test the stats endpoint."""
    print("\n📊 Testing stats endpoint...")
    response = requests.get(f"{BASE_URL}/api/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_chat():
    """Test the chat endpoint."""
    print("\n💬 Testing chat endpoint...")
    
    questions = [
        "What is democracy?",
        "What are the features of federalism?",
        "Explain nationalism in brief"
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={"question": question}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Answer: {data['answer'][:200]}...")
            print(f"📚 Sources: {len(data['sources'])} documents")
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    
    return True

def test_clear():
    """Test the clear endpoint."""
    print("\n🗑️  Testing clear endpoint...")
    response = requests.post(f"{BASE_URL}/api/clear")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def main():
    """Run all tests."""
    print("="*60)
    print("  CBSE RAG Tutor API Test Suite")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print("\nMake sure:")
    print("  1. Ollama is running (ollama serve)")
    print("  2. API is running (uvicorn api:app --reload)")
    print()
    
    try:
        # Run tests
        tests = [
            ("Health Check", test_health),
            ("Database Stats", test_stats),
            ("Chat", test_chat),
            ("Clear History", test_clear)
        ]
        
        results = []
        for name, test_func in tests:
            try:
                result = test_func()
                results.append((name, result))
            except Exception as e:
                print(f"❌ {name} failed: {str(e)}")
                results.append((name, False))
        
        # Summary
        print("\n" + "="*60)
        print("  Test Results")
        print("="*60)
        for name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status}: {name}")
        
        passed = sum(1 for _, r in results if r)
        total = len(results)
        print(f"\n{passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 All tests passed! API is ready for frontend integration!")
        else:
            print("\n⚠️  Some tests failed. Check the output above.")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API!")
        print("Make sure the API is running:")
        print("  uvicorn api:app --reload")

if __name__ == "__main__":
    main()
