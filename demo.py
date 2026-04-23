"""
Quick Demo Script for Todo API
This script demonstrates how to interact with the Todo API programmatically.

Run this AFTER starting the server with: uvicorn main:app --reload
"""

import requests
import json
from typing import Dict, List

# API Base URL
BASE_URL = "http://localhost:8000"

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print(f"{text.center(60)}")
    print(f"{'='*60}{Colors.END}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


def print_request(method: str, endpoint: str, data: Dict = None):
    """Print request details"""
    print(f"{Colors.YELLOW}{method} {endpoint}{Colors.END}")
    if data:
        print(f"Request Body: {json.dumps(data, indent=2)}")


def print_response(response: requests.Response):
    """Print response details"""
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")


def check_server():
    """Check if server is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_success("Server is running! ✓")
            data = response.json()
            print_info(f"Status: {data['status']}")
            print_info(f"Todos in memory: {data['todos_count']}")
            return True
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to server!")
        print_info("Make sure to start the server first:")
        print_info("  uvicorn main:app --reload")
        return False


def demo_create_todos():
    """Demo: Create todos with auto-generated descriptions"""
    print_header("DEMO 1: Create Todos with Auto-Generated Descriptions")
    
    todos_to_create = [
        {"title": "Learn FastAPI"},
        {"title": "Build a REST API", "description": "Create endpoints for CRUD operations"},
        {"title": "Master async/await"},
    ]
    
    created_todos = []
    
    for todo_data in todos_to_create:
        print_request("POST", "/todos", todo_data)
        response = requests.post(f"{BASE_URL}/todos", json=todo_data)
        print_response(response)
        
        if response.status_code == 201:
            print_success(f"Todo created: {response.json()['title']}")
            created_todos.append(response.json())
        else:
            print_error(f"Failed to create todo")
        print()
    
    return created_todos


def demo_list_todos():
    """Demo: List all todos"""
    print_header("DEMO 2: List All Todos")
    
    print_request("GET", "/todos")
    response = requests.get(f"{BASE_URL}/todos")
    print_response(response)
    
    if response.status_code == 200:
        todos = response.json()
        print_success(f"Retrieved {len(todos)} todos")
    print()
    
    return response.json()


def demo_filter_todos(todos: List[Dict]):
    """Demo: Filter todos by completion status"""
    print_header("DEMO 3: Filter Todos by Status")
    
    # Get incomplete todos
    print_request("GET", "/todos?completed=false")
    response = requests.get(f"{BASE_URL}/todos", params={"completed": False})
    print_response(response)
    print_success(f"Retrieved {len(response.json())} incomplete todos")
    print()


def demo_get_single_todo(todo_id: int):
    """Demo: Get a specific todo"""
    print_header(f"DEMO 4: Get Single Todo (ID: {todo_id})")
    
    print_request("GET", f"/todos/{todo_id}")
    response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    print_response(response)
    
    if response.status_code == 200:
        print_success(f"Retrieved todo: {response.json()['title']}")
    print()


def demo_update_todo(todo_id: int):
    """Demo: Update a todo"""
    print_header(f"DEMO 5: Update Todo (ID: {todo_id})")
    
    update_data = {
        "completed": True,
        "description": "Updated description via demo script"
    }
    
    print_request("PUT", f"/todos/{todo_id}", update_data)
    response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
    print_response(response)
    
    if response.status_code == 200:
        print_success(f"Todo updated successfully")
    print()


def demo_generate_description():
    """Demo: Generate AI description"""
    print_header("DEMO 6: Generate AI Description")
    
    titles = [
        "Build a mobile app",
        "Write documentation",
        "Optimize performance"
    ]
    
    for title in titles:
        request_data = {"title": title}
        print_request("POST", "/generate-description", request_data)
        
        response = requests.post(f"{BASE_URL}/generate-description", json=request_data)
        print_response(response)
        
        if response.status_code == 200:
            print_success(f"Description generated for: {title}")
        print()


def demo_delete_todo(todo_id: int):
    """Demo: Delete a todo"""
    print_header(f"DEMO 7: Delete Todo (ID: {todo_id})")
    
    print_request("DELETE", f"/todos/{todo_id}")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    
    if response.status_code == 204:
        print_success(f"Todo deleted successfully")
        print("Response: (204 No Content - no response body)")
    else:
        print_error(f"Failed to delete todo")
    print()


def main():
    """Main demo function"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║    Todo API with AI - Interactive Demo Script            ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(Colors.END)
    
    # Check if server is running
    if not check_server():
        return
    
    print("\n" + "="*60)
    print("Starting API Demonstrations...")
    print("="*60)
    
    # Run demos
    todos = demo_create_todos()
    
    if todos:
        demo_list_todos()
        demo_filter_todos(todos)
        
        first_todo_id = todos[0]['id']
        demo_get_single_todo(first_todo_id)
        demo_update_todo(first_todo_id)
        
        demo_generate_description()
        
        demo_delete_todo(first_todo_id)
    
    # Final summary
    print_header("Demo Complete!")
    print_info("Next steps:")
    print_info("1. Visit http://localhost:8000/docs for interactive Swagger UI")
    print_info("2. Check README.md for full API documentation")
    print_info("3. View main.py source code for implementation details")
    print_info("4. Modify and extend the API with your own features!")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Demo interrupted by user.{Colors.END}")
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
