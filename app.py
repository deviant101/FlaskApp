from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

# In-memory data store
tasks = []
task_id_counter = 1


@app.route('/')
def home():
    """Home route - Web GUI"""
    return render_template('index.html', tasks=tasks)


@app.route('/api')
def api_home():
    """API documentation route"""
    return jsonify({
        'message': 'Welcome to Flask Task API',
        'endpoints': {
            '/health': 'GET - Health check',
            '/api/tasks': 'GET - List all tasks, POST - Create a task',
            '/api/tasks/<id>': 'GET - Get task, PUT - Update task, DELETE - Delete task'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/web/add', methods=['POST'])
def web_add_task():
    """Add task from web form"""
    global task_id_counter
    
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    if title:
        task = {
            'id': task_id_counter,
            'title': title,
            'description': description,
            'completed': False
        }
        tasks.append(task)
        task_id_counter += 1
    
    return redirect(url_for('home'))


@app.route('/web/toggle/<int:task_id>')
def web_toggle_task(task_id):
    """Toggle task completion status"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        task['completed'] = not task['completed']
    return redirect(url_for('home'))


@app.route('/web/delete/<int:task_id>')
def web_delete_task(task_id):
    """Delete task from web interface"""
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect(url_for('home'))


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify({'tasks': tasks}), 200


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    global task_id_counter
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False
    }
    
    tasks.append(task)
    task_id_counter += 1
    
    return jsonify(task), 201


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task), 200


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    return jsonify(task), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    global tasks
    
    task = next((t for t in tasks if t['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    
    return jsonify({'message': 'Task deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
