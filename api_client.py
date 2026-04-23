"""
Python Client Library for Todo API
Helper module to interact with Todo API from Python code.

Usage:
    from api_client import TodoClient
    
    client = TodoClient()
    
    # Create a todo
    todo = await client.create_todo("Learn FastAPI")
    
    # List todos
    todos = await client.list_todos()
    
    # Update todo
    updated = await client.update_todo(todo['id'], completed=True)
    
    # Delete todo
    await client.delete_todo(todo['id'])
"""

import httpx
import asyncio
from typing import List, Dict, Optional


class TodoClient:
    """Client for interacting with Todo API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the Todo API client.
        
        Args:
            base_url: The base URL of the API (default: http://localhost:8000)
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)
    
    async def health_check(self) -> Dict:
        """
        Check if the API is healthy.
        
        Returns:
            Health status dictionary
        """
        response = await self.client.get("/health")
        return response.json()
    
    async def create_todo(
        self,
        title: str,
        description: Optional[str] = None,
        completed: bool = False
    ) -> Dict:
        """
        Create a new todo.
        
        Args:
            title: The todo title
            description: Optional description (will be auto-generated if not provided)
            completed: Whether the todo is completed (default: False)
        
        Returns:
            Created todo object
        """
        payload = {
            "title": title,
            "completed": completed
        }
        if description:
            payload["description"] = description
        
        response = await self.client.post("/todos", json=payload)
        return response.json()
    
    async def list_todos(self, completed: Optional[bool] = None) -> List[Dict]:
        """
        List all todos with optional filtering.
        
        Args:
            completed: Filter by completion status (None for all)
        
        Returns:
            List of todos
        """
        params = {}
        if completed is not None:
            params["completed"] = completed
        
        response = await self.client.get("/todos", params=params)
        return response.json()
    
    async def get_todo(self, todo_id: int) -> Dict:
        """
        Get a specific todo by ID.
        
        Args:
            todo_id: The ID of the todo
        
        Returns:
            Todo object
        """
        response = await self.client.get(f"/todos/{todo_id}")
        return response.json()
    
    async def update_todo(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Dict:
        """
        Update a todo.
        
        Args:
            todo_id: The ID of the todo to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
        
        Returns:
            Updated todo object
        """
        payload = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if completed is not None:
            payload["completed"] = completed
        
        response = await self.client.put(f"/todos/{todo_id}", json=payload)
        return response.json()
    
    async def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo.
        
        Args:
            todo_id: The ID of the todo to delete
        
        Returns:
            True if successful, False otherwise
        """
        response = await self.client.delete(f"/todos/{todo_id}")
        return response.status_code == 204
    
    async def generate_description(self, title: str) -> Dict:
        """
        Generate an AI description for a title.
        
        Args:
            title: The todo title
        
        Returns:
            Dictionary with title and generated_description
        """
        payload = {"title": title}
        response = await self.client.post("/generate-description", json=payload)
        return response.json()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Example usage and helper functions
async def example_usage():
    """Example of how to use the TodoClient"""
    
    # Initialize client
    client = TodoClient()
    
    try:
        # Check health
        print("Checking API health...")
        health = await client.health_check()
        print(f"Health: {health}")
        
        # Create todos
        print("\nCreating todos...")
        todo1 = await client.create_todo("Learn FastAPI")
        print(f"Created: {todo1['title']} (ID: {todo1['id']})")
        
        todo2 = await client.create_todo(
            "Build a project",
            description="Create a real-world project with FastAPI"
        )
        print(f"Created: {todo2['title']} (ID: {todo2['id']})")
        
        # List todos
        print("\nListing all todos...")
        todos = await client.list_todos()
        for todo in todos:
            print(f"- [{todo['id']}] {todo['title']} ({'✓' if todo['completed'] else '○'})")
        
        # Generate description
        print("\nGenerating AI description...")
        generated = await client.generate_description("Optimize database queries")
        print(f"Title: {generated['title']}")
        print(f"Description: {generated['generated_description']}")
        
        # Update todo
        print("\nUpdating todo...")
        updated = await client.update_todo(todo1['id'], completed=True)
        print(f"Updated: {updated['title']} - Completed: {updated['completed']}")
        
        # Get specific todo
        print("\nGetting specific todo...")
        todo = await client.get_todo(todo1['id'])
        print(f"Retrieved: {todo['title']}")
        
        # List incomplete todos
        print("\nListing incomplete todos...")
        incomplete = await client.list_todos(completed=False)
        print(f"Incomplete todos: {len(incomplete)}")
        
        # Delete todo
        print("\nDeleting todo...")
        success = await client.delete_todo(todo1['id'])
        print(f"Deleted: {success}")
        
    finally:
        await client.close()


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
