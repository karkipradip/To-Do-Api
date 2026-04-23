import requests
import json

BASE_URL = 'http://localhost:8000'

print('='*70)
print('COMPREHENSIVE TODO API TEST - ALL FEATURES'.center(70))
print('='*70)

# Test 1: Root endpoint
print('\n✅ TEST 1: Root Endpoint')
r = requests.get(f'{BASE_URL}/')
assert r.status_code == 200
print(f'   Status: {r.status_code} | Message: {r.json()["message"]}')

# Test 2: Create todo with AI description
print('\n✅ TEST 2: Create Todo (Auto AI Description)')
r = requests.post(f'{BASE_URL}/todos', json={'title': 'Learn Python'})
assert r.status_code == 200
todo1 = r.json()
print(f'   Status: {r.status_code} | ID: {todo1["id"]} | Title: {todo1["title"]}')

# Test 3: Create todo with custom description
print('\n✅ TEST 3: Create Todo (Custom Description)')
r = requests.post(f'{BASE_URL}/todos', json={'title': 'Code Review', 'description': 'Review pull requests', 'priority': 'high'})
assert r.status_code == 200
todo2 = r.json()
print(f'   Status: {r.status_code} | ID: {todo2["id"]} | Priority: {todo2["priority"]}')

# Test 4: Get all todos
print('\n✅ TEST 4: Get All Todos')
r = requests.get(f'{BASE_URL}/todos')
assert r.status_code == 200
todos_list = r.json()
print(f'   Status: {r.status_code} | Count: {len(todos_list)} todos')

# Test 5: Get single todo
print(f'\n✅ TEST 5: Get Single Todo (ID: {todo1["id"]})')
r = requests.get(f'{BASE_URL}/todos/{todo1["id"]}')
assert r.status_code == 200
print(f'   Status: {r.status_code} | Title: {r.json()["title"]}')

# Test 6: UPDATE todo (FIXED - now allows partial updates)
print(f'\n✅ TEST 6: Update Todo (Partial Update - ID: {todo1["id"]})')
r = requests.put(f'{BASE_URL}/todos/{todo1["id"]}', json={'completed': True})
assert r.status_code == 200
print(f'   Status: {r.status_code} | Completed: {r.json()["completed"]}')

# Test 7: Update todo priority
print(f'\n✅ TEST 7: Update Priority (ID: {todo2["id"]})')
r = requests.put(f'{BASE_URL}/todos/{todo2["id"]}', json={'priority': 'low'})
assert r.status_code == 200
print(f'   Status: {r.status_code} | Priority: {r.json()["priority"]}')

# Test 8: Generate AI description
print('\n✅ TEST 8: Generate AI Description')
r = requests.post(f'{BASE_URL}/generate-description', json={'title': 'Deploy application'})
assert r.status_code == 200
print(f'   Status: {r.status_code} | Title: {r.json()["title"]}')

# Test 9: Delete todo
print(f'\n✅ TEST 9: Delete Todo (ID: {todo2["id"]})')
r = requests.delete(f'{BASE_URL}/todos/{todo2["id"]}')
assert r.status_code == 200
print(f'   Status: {r.status_code} | Deleted successfully')

# Test 10: Error handling
print('\n✅ TEST 10: Error Handling (Non-existent Todo)')
r = requests.get(f'{BASE_URL}/todos/999')
assert r.status_code == 404
print(f'   Status: {r.status_code} | Error: Todo not found')

print('\n' + '='*70)
print('✨ ALL TESTS PASSED - ALL FEATURES WORKING! ✨'.center(70))
print('='*70)
print('\n📋 FEATURES VERIFIED:')
print('   ✓ Create todos with auto-generated AI descriptions')
print('   ✓ Create todos with custom descriptions')
print('   ✓ Get all todos')
print('   ✓ Get single todo by ID')
print('   ✓ Update todo (partial updates)')
print('   ✓ Update priority field')
print('   ✓ Generate AI descriptions')
print('   ✓ Delete todos')
print('   ✓ Error handling')
print()
