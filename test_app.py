import unittest
import json
import app as app_module


class FlaskAppTestCase(unittest.TestCase):
    """Test cases for Flask Task API"""
    
    def setUp(self):
        """Set up test client and reset data before each test"""
        self.app = app_module.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Reset global state
        app_module.tasks.clear()
        app_module.task_id_counter = 1
    
    def tearDown(self):
        """Clean up after each test"""
        pass
    
    def test_home_route(self):
        """Test the home route returns HTML"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Manager', response.data)
    
    def test_api_home_route(self):
        """Test the API documentation route"""
        response = self.client.get('/api')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('endpoints', data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_get_tasks_empty(self):
        """Test getting tasks when none exist"""
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['tasks'], [])
    
    def test_create_task(self):
        """Test creating a new task"""
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task'
        }
        response = self.client.post('/api/tasks',
                                   data=json.dumps(task_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'This is a test task')
        self.assertEqual(data['completed'], False)
        self.assertEqual(data['id'], 1)
    
    def test_create_task_without_title(self):
        """Test creating a task without title fails"""
        task_data = {'description': 'No title'}
        response = self.client.post('/api/tasks',
                                   data=json.dumps(task_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_tasks_with_data(self):
        """Test getting tasks after creating some"""
        # Create two tasks
        self.client.post('/api/tasks',
                        data=json.dumps({'title': 'Task 1'}),
                        content_type='application/json')
        self.client.post('/api/tasks',
                        data=json.dumps({'title': 'Task 2'}),
                        content_type='application/json')
        
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['tasks']), 2)
    
    def test_get_task_by_id(self):
        """Test getting a specific task"""
        # Create a task first
        create_response = self.client.post('/api/tasks',
                                          data=json.dumps({'title': 'Specific Task'}),
                                          content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Get the task
        response = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Specific Task')
    
    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist"""
        response = self.client.get('/api/tasks/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_update_task(self):
        """Test updating a task"""
        # Create a task first
        create_response = self.client.post('/api/tasks',
                                          data=json.dumps({'title': 'Original Title'}),
                                          content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Update the task
        update_data = {
            'title': 'Updated Title',
            'completed': True
        }
        response = self.client.put(f'/api/tasks/{task_id}',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Title')
        self.assertEqual(data['completed'], True)
    
    def test_update_nonexistent_task(self):
        """Test updating a task that doesn't exist"""
        update_data = {'title': 'New Title'}
        response = self.client.put('/api/tasks/999',
                                   data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)
    
    def test_delete_task(self):
        """Test deleting a task"""
        # Create a task first
        create_response = self.client.post('/api/tasks',
                                          data=json.dumps({'title': 'Task to Delete'}),
                                          content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Delete the task
        response = self.client.delete(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify it's gone
        get_response = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(get_response.status_code, 404)
    
    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist"""
        response = self.client.delete('/api/tasks/999')
        self.assertEqual(response.status_code, 404)
    
    def test_web_add_task(self):
        """Test adding a task through web form"""
        response = self.client.post('/web/add',
                                   data={'title': 'Web Task', 'description': 'Added via form'},
                                   follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(app_module.tasks), 1)
        self.assertEqual(app_module.tasks[0]['title'], 'Web Task')
    
    def test_web_toggle_task(self):
        """Test toggling task completion via web"""
        # Add a task first
        self.client.post('/web/add', data={'title': 'Toggle Task'})
        task_id = app_module.tasks[0]['id']
        
        # Toggle it
        response = self.client.get(f'/web/toggle/{task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(app_module.tasks[0]['completed'])
        
        # Toggle back
        self.client.get(f'/web/toggle/{task_id}')
        self.assertFalse(app_module.tasks[0]['completed'])
    
    def test_web_delete_task(self):
        """Test deleting task via web"""
        # Add a task first
        self.client.post('/web/add', data={'title': 'Delete Me'})
        task_id = app_module.tasks[0]['id']
        
        # Delete it
        response = self.client.get(f'/web/delete/{task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(app_module.tasks), 0)


if __name__ == '__main__':
    unittest.main()
