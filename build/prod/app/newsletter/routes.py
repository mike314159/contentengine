from flask import Blueprint, jsonify, request, Response
import pandas as pd
import uuid
import json
import html as html_module
from .objectfactory import ObjectFactory
from uilib.components import SimpleTableComponent
from .work_queue_mgr import WorkQueueManager
from .work_queue_db import WorkQueueDBEntry
from .work_queue_task_db import WorkQueueTaskDBEntry
from .prompt_db import PromptDBEntry

newsletter_blp = Blueprint('newsletter', __name__)


def generate_action_buttons_html(snippet_db, snippet_id, approval_state_id, published_ts=None):
    """Generate HTML for action buttons based on approval_state."""
    # If published_ts > 0, don't show approval buttons
    if published_ts is not None and pd.notna(published_ts) and int(published_ts) > 0:
        return '<span class="badge bg-success">Published</span>'
    
    choices = snippet_db.get_approved_state_choices(approval_state_id)
    
    if choices is None or len(choices) == 0:
        # No choices available, find and show current state label
        state_label = None
        for label, details in snippet_db.approved_states.items():
            if details["id"] == approval_state_id:
                state_label = label
                break
        if state_label:
            return f'<span class="badge bg-secondary">{state_label.capitalize()}</span>'
        return '<span class="badge bg-secondary">Unknown</span>'
    
    buttons_html = []
    for button_label, new_state_label in choices:
        new_state_id = snippet_db.map_approved_state_label_to_id.get(new_state_label)
        if new_state_id is not None:
            buttons_html.append(
                f'<button class="btn btn-primary btn-sm me-1" '
                f'hx-post="/newsletter/snippets/{snippet_id}/update-state/{new_state_id}" '
                f'hx-target="closest tr" hx-swap="outerHTML">{button_label.capitalize()}</button>'
            )
    if buttons_html:
        return f'<span style="white-space: nowrap;">{"&nbsp;".join(buttons_html)}</span>'
    return '<span class="badge bg-secondary">No actions</span>'


def get_nav_bar():
    """Generate navigation bar for newsletter pages."""
    return """
    <nav class="navbar navbar-light bg-light mb-4">
        <div class="container-fluid">
            <a class="navbar-brand" href="/newsletter">Home</a>
            <a class="nav-link" href="/newsletter/snippets">Show snippets</a>
        </div>
    </nav>
    """


def get_breadcrumb(items):
    """
    Generate a Bootstrap breadcrumb navigation.
    
    Args:
        items: List of tuples (label, url) or (label,) for non-clickable items.
               The last item should not have a URL (will be active/current page).
    
    Returns:
        HTML string for the breadcrumb navigation.
    
    Example:
        get_breadcrumb([
            ("work queue", "/newsletter/work-queue"),
            ("pc", "/newsletter/work-queue/pc"),
            ("images",)  # Last item, no URL
        ])
    """
    if not items:
        return ""
    
    breadcrumb_items = []
    for i, item in enumerate(items):
        if len(item) == 2:
            # Has URL - make it a link
            label, url = item
            breadcrumb_items.append(
                f'<li class="breadcrumb-item"><a href="{url}">{label}</a></li>'
            )
        else:
            # No URL - active/current page
            label = item[0]
            breadcrumb_items.append(
                f'<li class="breadcrumb-item active" aria-current="page">{label}</li>'
            )
    
    return f'<nav aria-label="breadcrumb"><ol class="breadcrumb">{"".join(breadcrumb_items)}</ol></nav>'


@newsletter_blp.route("/")
def newsletter_home():
    """Newsletter home page."""
    nav_bar = get_nav_bar()
    html = f"""
    <html>
    <head>
        <title>Newsletter</title>
        <script src='https://unpkg.com/htmx.org@1.9.10'></script>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        {nav_bar}
        <div class="container mt-4">
            <h1>Newsletter</h1>
            <button class="btn btn-primary" 
                    hx-post="/newsletter/add-test-snippets" 
                    hx-target="#status-message"
                    hx-swap="innerHTML">
                Add 5 Test Snippets
            </button>
            <div id="status-message" class="mt-3"></div>
        </div>
    </body>
    </html>
    """
    return html, 200


@newsletter_blp.route("/work-queue", methods=['GET'])
def view_work_queue():
    """View WorkQueue and WorkQueueTask tables to inspect queue state."""
    try:
        factory = ObjectFactory()
        work_queue_db = factory.get_obj(ObjectFactory.WORK_QUEUE_DB)
        work_queue_task_db = factory.get_obj(ObjectFactory.WORK_QUEUE_TASK_DB)

        # Summary of number of items in each queue
        df_summary = work_queue_db.get_queue_summary_df()
        df_queue = work_queue_db.get_all_df()
        df_tasks = work_queue_task_db.get_all_df()

        nav_bar = get_nav_bar()

        # Build HTML for summary table (project, queue, count)
        summary_table_html = "<p>No work queue summary.</p>"
        if not df_summary.empty:
            df_summary_display = df_summary.copy()
            # Add link to queue-specific page in a separate column
            def make_queue_link(row):
                proj = row.get("project", "")
                q = row.get("queue", "")
                return f"<a href=\"/newsletter/work-queue/{proj}/{q}\">View queue</a>"

            df_summary_display["Link"] = df_summary_display.apply(make_queue_link, axis=1)
            cols_summary = list(df_summary_display.columns)
            summary_component = SimpleTableComponent(
                name="work_queue_summary",
                df=df_summary_display,
                cols=cols_summary,
            )
            summary_render = summary_component.render()
            summary_table_html = summary_render.get_html()

        # Build HTML for WorkQueue table
        queue_table_html = "<p>No work queue entries.</p>"
        if not df_queue.empty:
            df_queue_display = df_queue.copy()
            # Store full task_uuid for delete button before truncating display
            if "task_uuid" in df_queue_display.columns:
                # Add delete button column with full task_uuid
                def make_delete_button(row):
                    task_uuid = row.get("task_uuid", "")
                    if pd.notna(task_uuid) and task_uuid:
                        return (
                            f'<button class="btn btn-danger btn-sm" '
                            f'hx-post="/newsletter/work-queue/delete" '
                            f'hx-vals=\'{{"task_uuid": "{task_uuid}"}}\' '
                            f'hx-target="closest tr" '
                            f'hx-swap="outerHTML">Delete</button>'
                        )
                    return ""
                
                df_queue_display["Delete"] = df_queue_display.apply(make_delete_button, axis=1)
                # Show only first 7 characters of task_uuid for readability
                df_queue_display["task_uuid"] = df_queue_display["task_uuid"].apply(
                    lambda x: str(x)[:7] if pd.notna(x) else ""
                )
            cols_queue = list(df_queue_display.columns)
            queue_component = SimpleTableComponent(
                name="work_queue",
                df=df_queue_display,
                cols=cols_queue,
            )
            queue_render = queue_component.render()
            queue_table_html = queue_render.get_html()

        # Build HTML for WorkQueueTask table
        task_table_html = "<p>No work queue tasks.</p>"
        if not df_tasks.empty:
            df_tasks_display = df_tasks.copy()
            # Show only first 7 characters of task_uuid for readability
            if "task_uuid" in df_tasks_display.columns:
                df_tasks_display["task_uuid"] = df_tasks_display["task_uuid"].apply(
                    lambda x: str(x)[:7] if pd.notna(x) else ""
                )
            cols_tasks = list(df_tasks_display.columns)
            task_component = SimpleTableComponent(
                name="work_queue_tasks",
                df=df_tasks_display,
                cols=cols_tasks,
            )
            task_render = task_component.render()
            task_table_html = task_render.get_html()

        html = f"""
        <html>
        <head>
            <title>Work Queue</title>
            <script src='https://unpkg.com/htmx.org@1.9.10'></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            {nav_bar}
            <div class="container mt-4">
                <h1>Work Queue</h1>
                <h2 class="mt-4">Queue Summary</h2>
                {summary_table_html}
                <h2 class="mt-4">WorkQueue</h2>
                {queue_table_html}
                <h2 class="mt-5">WorkQueueTask</h2>
                {task_table_html}
            </div>
        </body>
        </html>
        """
        return html, 200
    except Exception as e:
        nav_bar = get_nav_bar()
        return f"<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet'></head><body>{nav_bar}<div class='container mt-4'><h1>Error</h1><p>{str(e)}</p></div></body></html>", 500


@newsletter_blp.route("/work-queue/<project>/<queue>/add", methods=['POST'])
def api_add_work_queue_task(project, queue):
    """
    API to add a new work queue task using WorkQueueManager.add_task.

    Example:
        POST /newsletter/work-queue/test/test_queue/add
        Body (JSON):
        {
            "task_type": "text",
            "text": "Some task text"
        }
        for an image payload looks like this
        {
            "task_type": "image",
            "image": image_base64,
        }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        #print(f"JSON data: {json.dumps(data, indent=4)}")
        task_type = data.get("task_type", "text")
        image = None
        if task_type == "image":
            image_data = data.get("image")

            # Decode base64 image data if provided
            if image_data is not None:
                import base64
                try:
                    image = base64.b64decode(image_data)
                except Exception as e:
                    return jsonify({"error": f"Failed to decode base64 image data: {e}"}), 400

        if task_type == "json":
            json_str = json.dumps(data)
        else:
            json_str = None


        factory = ObjectFactory()
        mgr = WorkQueueManager(factory=factory)

        #json_str = json.dumps(data)
        task_uuid = mgr.add_task(factory, project, queue, task_type=task_type, text=json_str, image=image)

        if task_uuid is None:
            return jsonify({"error": "Failed to add work queue task"}), 500

        return jsonify(
            {
                "status": "success",
                "task_uuid": task_uuid,
                # "project": project,
                # "queue": queue,
                # "task_type": task_type,
            }
        ), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@newsletter_blp.route("/work-queue/image", methods=['GET'])
def work_queue_image():
    """
    Serve an image from a work queue task.
    
    Query parameter:
        task_uuid: UUID of the task containing the image
    
    Returns:
        Image data with appropriate content type, or 404 if not found
    """
    try:
        task_uuid = request.args.get("task_uuid")
        if not task_uuid:
            return jsonify({"error": "task_uuid query parameter is required"}), 400
        
        factory = ObjectFactory()
        work_queue_task_db = factory.get_obj(ObjectFactory.WORK_QUEUE_TASK_DB)
        
        # Query the database directly
        try:
            task_entry = WorkQueueTaskDBEntry.get(WorkQueueTaskDBEntry.task_uuid == task_uuid)
            image_data = task_entry.image
        except WorkQueueTaskDBEntry.DoesNotExist:
            return jsonify({"error": "Task not found"}), 404
        
        # If image field is None, check if image is in JSON text field (base64 encoded)
        if image_data is None:
            # Check if task_type is json and image might be in the JSON structure
            if task_entry.task_type == "json" and task_entry.text:
                try:
                    task_json = json.loads(task_entry.text)
                    # Check if there's an "image" field in the JSON
                    if "image" in task_json and task_json["image"]:
                        import base64
                        # Try to decode base64 image
                        try:
                            image_data = base64.b64decode(task_json["image"])
                        except Exception as e:
                            return jsonify({"error": f"Failed to decode base64 image from JSON: {e}"}), 400
                except (json.JSONDecodeError, TypeError) as e:
                    return jsonify({"error": f"Failed to parse JSON text: {e}"}), 400
        
        if image_data is None:
            return jsonify({"error": "Task does not contain an image"}), 404
        
        # Check if image_data is empty
        if isinstance(image_data, (bytes, bytearray)) and len(image_data) == 0:
            return jsonify({"error": "Task image is empty"}), 404
        
        # Determine content type (default to jpeg, but could be enhanced to detect actual type)
        # For now, assume JPEG
        return Response(image_data, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_task_view_html(task_dict, factory=None):
    """
    Render a task dictionary from get_task_by_uuid into HTML for viewing.
    
    Args:
        task_dict: Dictionary returned by WorkQueueTaskDBPostgres.get_task_by_uuid
        factory: Optional ObjectFactory instance (needed to fetch image data for image task types)
        
    Returns:
        Tuple of (content_display, image_display) HTML strings
    """
    if not task_dict:
        return "", ""
    
    text = task_dict.get("text") or ""
    #image_value = task_dict.get("image")
    task_type = task_dict.get("task_type", "")
    task_uuid = task_dict.get("uuid", "")
    
    image_data = None
    if task_type == "image":
        content_display = ""
        image_display = f"<img src='/newsletter/work-queue/image?task_uuid={task_uuid}' class='img-fluid' alt='Task image' style='max-width: 500px; margin-top: 10px;' />"
    
    if task_type == "json" and text:
        try:
            task_data = json.loads(text)
            # Display entire JSON object formatted
            content_display = f"<pre>{json.dumps(task_data, indent=4)}</pre>"
        except (json.JSONDecodeError, TypeError):
            # If JSON parsing fails, display raw text
            content_display = f"<pre>{text}</pre>"

    
    return content_display, image_display

@newsletter_blp.route("/work-queue/<project>/<queue>", methods=['GET'])
def view_work_queue_tasks(project, queue):
    """
    View tasks for a specific project/queue without using DataFrames.

    Renders tasks linearly with action buttons for each task.
    """
    try:
        factory = ObjectFactory()
        # Ensure DB proxies are bound
        factory.get_obj(ObjectFactory.WORK_QUEUE_DB)
        factory.get_obj(ObjectFactory.WORK_QUEUE_TASK_DB)
        
        # Get available actions for this queue
        mgr = WorkQueueManager(factory=factory)
        actions = mgr.get_actions(queue)

        # Fetch all queue entries for this project/queue
        queue_entries = (
            WorkQueueDBEntry.select()
            .where(
                (WorkQueueDBEntry.project == project)
                & (WorkQueueDBEntry.queue == queue)
            )
            .order_by(WorkQueueDBEntry.added_to_queue_ts.desc())
        )

        tasks_html_parts = []
        work_queue_task_db = factory.get_obj(ObjectFactory.WORK_QUEUE_TASK_DB)
        for entry in queue_entries:
            task_dict = work_queue_task_db.get_task_by_uuid(entry.task_uuid)
            if not task_dict:
                continue
            
            # Get HTML for task content and image display
            content_display, image_display = get_task_view_html(task_dict, factory=factory)
            
            task_uuid = task_dict.get("uuid")
            task_type = task_dict.get("task_type", "")

            # Build action buttons HTML
            # Check if any action requires feedback
            any_feedback_required = any(
                action_info.get("feedback_required", False) 
                for action_info in actions.values()
            ) if actions else False
            
            actions_html_parts = []
            if actions:
                # Show text field if any action requires feedback
                if any_feedback_required:
                    actions_html_parts.append(
                        f"<div id='feedback-error-{task_uuid}' class='text-danger mb-2' style='display: none;'>Feedback is required</div>"
                        f"<input type='text' class='form-control mb-2' id='feedback-{task_uuid}' placeholder='Enter feedback...' "
                        f"oninput=\"document.getElementById('feedback-error-{task_uuid}').style.display = 'none';\" />"
                    )
                
                # Show all buttons in a single row
                buttons_html_parts = []
                for action_key, action_info in actions.items():
                    feedback_required = action_info.get("feedback_required", False)
                    label = action_info.get("label", action_key)
                    
                    action_queue = action_info.get("queue", "")
                    hx_target = f"#task-{task_uuid}"
                    
                    if feedback_required:
                        # Button that requires feedback - use fetch to send JSON
                        # Validate that feedback field is not blank before submitting
                        buttons_html_parts.append(
                            f"<button class='btn btn-primary btn-sm me-2' "
                            f"onclick=\"const feedbackEl = document.getElementById('feedback-{task_uuid}'); "
                            f"const errorEl = document.getElementById('feedback-error-{task_uuid}'); "
                            f"const feedback = feedbackEl.value.trim(); "
                            f"if (!feedback) {{ "
                            f"errorEl.style.display = 'block'; "
                            f"feedbackEl.focus(); "
                            f"return false; "
                            f"}} "
                            f"errorEl.style.display = 'none'; "
                            f"fetch('/newsletter/work-queue/action', {{"
                            f"method: 'POST', "
                            f"headers: {{'Content-Type': 'application/json'}}, "
                            f"body: JSON.stringify({{"
                            f"task_uuid: '{task_uuid}', "
                            f"action: '{action_key}', "
                            f"queue: '{action_queue}', "
                            f"feedback: feedback"
                            f"}})"
                            f"}}).then(r => r.text()).then(() => {{"
                            f"document.getElementById('task-{task_uuid}').outerHTML = '';"
                            f"}}); return false;\">{label}</button>"
                        )
                    else:
                        # Button that doesn't require feedback - use fetch to send JSON
                        buttons_html_parts.append(
                            f"<button class='btn btn-primary btn-sm me-2' "
                            f"onclick=\"fetch('/newsletter/work-queue/action', {{"
                            f"method: 'POST', "
                            f"headers: {{'Content-Type': 'application/json'}}, "
                            f"body: JSON.stringify({{"
                            f"task_uuid: '{task_uuid}', "
                            f"action: '{action_key}', "
                            f"queue: '{action_queue}'"
                            f"}})"
                            f"}}).then(r => r.text()).then(() => {{"
                            f"document.getElementById('task-{task_uuid}').outerHTML = '';"
                            f"}}); return false;\">{label}</button>"
                        )
                
                # Wrap buttons in a div to keep them in a row
                actions_html_parts.append(
                    f"<div class='d-flex flex-wrap gap-2'>"
                    f"{''.join(buttons_html_parts)}"
                    f"</div>"
                )
            
            actions_html = "".join(actions_html_parts) if actions_html_parts else "<p><em>No actions available</em></p>"

            # image_display already contains HTML (img tag), so don't wrap in <pre>
            image_html = image_display if image_display else ""
            tasks_html_parts.append(
                f"<div class='mb-4 p-3 border rounded' id='task-{task_uuid}'>"
                f"<p><strong>Task:</strong> {task_uuid}</p>"
                f"<p><strong>Type:</strong> {task_type}</p>"
                f"{content_display}"
                f"{image_html}"
                f"<div class='mt-3'>"
                f"<strong>Actions:</strong><br/>"
                f"{actions_html}"
                f"</div>"
                f"</div>"
            )

        tasks_html = "".join(tasks_html_parts) if tasks_html_parts else "<p>No tasks found for this queue.</p>"

        nav_bar = get_nav_bar()
        breadcrumb = get_breadcrumb([
            ("work queue", "/newsletter/work-queue"),
            (project, "/newsletter/work-queue"),  # Project link goes to main work queue page
            (queue,)  # Current page, not clickable
        ])
        html = f"""
        <html>
        <head>
            <title>Work Queue - {project} / {queue}</title>
            <script src='https://unpkg.com/htmx.org@1.9.10'></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            {nav_bar}
            <div class="container mt-4">
                {breadcrumb}
                <hr/>
                {tasks_html}
            </div>
        </body>
        </html>
        """
        return html, 200
    except Exception as e:
        nav_bar = get_nav_bar()
        return f"<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet'></head><body>{nav_bar}<div class='container mt-4'><h1>Error</h1><p>{str(e)}</p></div></body></html>", 500


@newsletter_blp.route("/work-queue/action", methods=['POST'])
def work_queue_action():
    """
    Handle action on a work queue task.
    
    Accepts form data or JSON with:
        - task_uuid: UUID of the task
        - action: Action key (e.g., "approve", "reject", "rewrite")
        - feedback: Optional feedback text (for actions that require feedback)
    
    Returns empty response to remove the task from the list.
    """
    #print(f"Form data 2: {request.form}")
    #print(f"JSON data: {request.get_json()}")
    
    #try:
        # HTMX now sends JSON, so we can expect JSON
    if request.is_json:
        data = request.get_json()
        task_uuid = data.get("task_uuid")
        action = data.get("action")
        queue = data.get("queue")
        feedback = data.get("feedback")
        print(f"JSON data: {json.dumps(data, indent=4)}")
        """
        JSON data: {
            "task_uuid": "5cc3b11b12a640b6bbbd2eee7a43d9c4",
            "action": "reject",
            "queue": "rejected_quotes"
        }
        """
    else:
        return jsonify({"error": "Invalid content"}), 400
        # else:
        #     # Fallback for form data (shouldn't happen now, but keep for compatibility)
        #     task_uuid = request.form.get("task_uuid")
        #     action = request.form.get("action")
        #     queue = request.form.get("queue")
        #     feedback = request.form.get("feedback")


    if not task_uuid or not action:
        return jsonify({"error": "task_uuid and action are required"}), 400
    
    if not queue:
        return jsonify({"error": "queue is required"}), 400
    
    # Move the task to the appropriate queue
    try:
        factory = ObjectFactory()
        work_queue_db = factory.get_obj(ObjectFactory.WORK_QUEUE_DB)
        
        # Find the work queue entry by task_uuid
        try:
            entry = WorkQueueDBEntry.get(WorkQueueDBEntry.task_uuid == task_uuid)
        except WorkQueueDBEntry.DoesNotExist:
            return jsonify({"error": f"Task with uuid {task_uuid} not found"}), 404
        
        # Move the task to the destination queue
        success = work_queue_db.move_task_queue(entry.id, queue)
        if not success:
            return jsonify({"error": "Failed to move task to queue"}), 500
        
        # Return empty string to remove the task from the list
        return "", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@newsletter_blp.route("/work-queue/delete", methods=['POST'])
def work_queue_delete():
    """
    Delete a task from both WorkQueue and WorkQueueTask tables.
    
    Accepts form data or JSON with:
        - task_uuid: UUID of the task to delete
    
    Returns empty response to remove the row from the table.
    """
    try:
        # HTMX sends form data by default, but we can also handle JSON
        if request.is_json:
            data = request.get_json()
            task_uuid = data.get("task_uuid")
        else:
            # HTMX form data
            task_uuid = request.form.get("task_uuid")
        
        if not task_uuid:
            return jsonify({"error": "task_uuid is required"}), 400
        
        factory = ObjectFactory()
        work_queue_db = factory.get_obj(ObjectFactory.WORK_QUEUE_DB)
        work_queue_task_db = factory.get_obj(ObjectFactory.WORK_QUEUE_TASK_DB)
        
        # Delete from WorkQueue table
        try:
            queue_entry = WorkQueueDBEntry.get(WorkQueueDBEntry.task_uuid == task_uuid)
            queue_entry.delete_instance()
        except WorkQueueDBEntry.DoesNotExist:
            # Task might not exist in queue, continue to delete from task table
            pass
        except Exception as e:
            print(f"ERROR: Failed to delete from work_queue: {e}")
            return jsonify({"error": f"Failed to delete from work_queue: {e}"}), 500
        
        # Delete from WorkQueueTask table
        try:
            task_entry = WorkQueueTaskDBEntry.get(WorkQueueTaskDBEntry.task_uuid == task_uuid)
            task_entry.delete_instance()
        except WorkQueueTaskDBEntry.DoesNotExist:
            # Task payload might not exist, that's okay
            pass
        except Exception as e:
            print(f"ERROR: Failed to delete from work_queue_task: {e}")
            return jsonify({"error": f"Failed to delete from work_queue_task: {e}"}), 500
        
        # Return empty string to remove the row from the table
        return "", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@newsletter_blp.route("/api/get", methods=['GET'])
def api_get_work_queue_items():
    """
    Get items from work queues.
    
    Query parameters:
        project: Required, project name
        queues: Required, comma-separated list of queue names (e.g., "approved_quotes,rejected_quotes")
        count: Optional, number of items to return per queue (default: 1)
    
    Returns JSON with a list of queue items.
    """
    try:
        # Get project from query parameter
        project = request.args.get('project')
        if not project:
            return jsonify({"error": "project parameter is required"}), 400
        
        # Get queue names from query parameter
        queues_param = request.args.get('queues')
        if not queues_param:
            return jsonify({"error": "queues parameter is required (comma-separated queue names)"}), 400
        
        # Parse CSV of queue names
        queue_names = [q.strip() for q in queues_param.split(',') if q.strip()]
        if not queue_names:
            return jsonify({"error": "At least one queue name is required"}), 400
        
        # Get count parameter, default to 1
        count = request.args.get('count', default=1, type=int)
        if count < 1:
            return jsonify({"error": "count must be at least 1"}), 400
        
        factory = ObjectFactory()
        work_queue_db = factory.get_obj(ObjectFactory.WORK_QUEUE_DB)
        work_queue_task_db = factory.get_obj(ObjectFactory.WORK_QUEUE_TASK_DB)
        
        # Get queue entries for this project and any of the specified queues, ordered by added_to_queue_ts (oldest first)
        queue_entries = (
            WorkQueueDBEntry.select()
            .where(
                (WorkQueueDBEntry.project == project)
                & (WorkQueueDBEntry.queue.in_(queue_names))
            )
            .order_by(WorkQueueDBEntry.added_to_queue_ts.asc())
            .limit(count)
        )
        
        items = []
        for entry in queue_entries:
            queue = entry.queue
            task = work_queue_task_db.get_task_by_uuid(entry.task_uuid)
            task["queue"] = queue
            items.append(task)
        
        return jsonify({"items": items, "count": len(items)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@newsletter_blp.route("/prompts", methods=['GET'])
def view_prompts():
    """View all prompts in a table."""
    try:
        factory = ObjectFactory()
        prompt_db = factory.get_obj(ObjectFactory.PROMPT_DB)

        df_prompts = prompt_db.get_all_df()

        nav_bar = get_nav_bar()
        breadcrumb = get_breadcrumb([
            ("prompts",),
        ])

        # Build HTML for prompts table
        prompts_table_html = "<p>No prompts found.</p>"
        if not df_prompts.empty:
            df_prompts_display = df_prompts.copy()
            # Add link to edit prompt in a separate column
            def make_prompt_link(row):
                prompt_id = row.get("prompt_id", "")
                if pd.notna(prompt_id) and prompt_id:
                    return f"<a href=\"/newsletter/prompt?id={prompt_id}\">Edit</a>"
                return ""

            df_prompts_display["Action"] = df_prompts_display.apply(make_prompt_link, axis=1)
            
            # Truncate prompt_desc for display in table if it's too long
            if "prompt_desc" in df_prompts_display.columns:
                df_prompts_display["prompt_desc"] = df_prompts_display["prompt_desc"].apply(
                    lambda x: str(x)[:100] + "..." if pd.notna(x) and len(str(x)) > 100 else (str(x) if pd.notna(x) else "")
                )
            
            cols_prompts = list(df_prompts_display.columns)
            prompts_component = SimpleTableComponent(
                name="prompts",
                df=df_prompts_display,
                cols=cols_prompts,
            )
            prompts_render = prompts_component.render()
            prompts_table_html = prompts_render.get_html()

        html = f"""
        <html>
        <head>
            <title>Prompts</title>
            <script src='https://unpkg.com/htmx.org@1.9.10'></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            {nav_bar}
            <div class="container mt-4">
                {breadcrumb}
                <hr/>
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h1>Prompts</h1>
                    <a href="/newsletter/prompt/add" class="btn btn-primary">Add New Prompt</a>
                </div>
                {prompts_table_html}
            </div>
        </body>
        </html>
        """
        return html, 200
    except Exception as e:
        nav_bar = get_nav_bar()
        return f"<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet'></head><body>{nav_bar}<div class='container mt-4'><h1>Error</h1><p>{str(e)}</p></div></body></html>", 500


@newsletter_blp.route("/prompt", methods=['GET'])
def view_prompt():
    """View and edit a single prompt by prompt_id."""
    try:
        prompt_id = request.args.get('id')
        if not prompt_id:
            return "Error: id parameter is required", 400

        factory = ObjectFactory()
        prompt_db = factory.get_obj(ObjectFactory.PROMPT_DB)

        prompt_data = prompt_db.get_prompt_by_id(prompt_id)
        if not prompt_data:
            return "Error: Prompt not found", 404

        nav_bar = get_nav_bar()
        breadcrumb = get_breadcrumb([
            ("prompts", "/newsletter/prompts"),
            (prompt_id,),
        ])

        prompt_desc_raw = prompt_data.get("prompt_desc", "") or ""
        prompt_desc_escaped = html_module.escape(prompt_desc_raw)
        project_raw = prompt_data.get("project", "")
        project_escaped = html_module.escape(project_raw)
        prompt_id_escaped = html_module.escape(prompt_id)
        created_ts = prompt_data.get("created_ts", 0)

        html_content = f"""
        <html>
        <head>
            <title>Edit Prompt - {prompt_id_escaped}</title>
            <script src='https://unpkg.com/htmx.org@1.9.10'></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            {nav_bar}
            <div class="container mt-4">
                {breadcrumb}
                <hr/>
                <h1>Edit Prompt: {prompt_id_escaped}</h1>
                <div class="mb-3">
                    <label class="form-label"><strong>Project:</strong></label>
                    <input type="text" class="form-control" id="project" value="{project_escaped}" readonly>
                </div>
                <div class="mb-3">
                    <label class="form-label"><strong>Prompt ID:</strong></label>
                    <input type="text" class="form-control" id="prompt_id" value="{prompt_id_escaped}" readonly>
                </div>
                <div class="mb-3">
                    <label class="form-label"><strong>Created:</strong></label>
                    <input type="text" class="form-control" value="{created_ts}" readonly>
                </div>
                <form id="prompt-form" onsubmit="return savePrompt(event);">
                    <div class="mb-3">
                        <label for="prompt_desc" class="form-label"><strong>Prompt Description:</strong></label>
                        <textarea class="form-control" id="prompt_desc" name="prompt_desc" rows="15" style="font-family: monospace;">{prompt_desc_escaped}</textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Save Changes</button>
                    <a href="/newsletter/prompts" class="btn btn-secondary">Cancel</a>
                    <div id="status-message" class="mt-3"></div>
                </form>
            </div>
            <script>
                function savePrompt(event) {{
                    event.preventDefault();
                    const promptId = document.getElementById('prompt_id').value;
                    const promptDesc = document.getElementById('prompt_desc').value;
                    const statusMsg = document.getElementById('status-message');
                    
                    fetch('/newsletter/prompt/update', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            prompt_id: promptId,
                            prompt_desc: promptDesc
                        }})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.status === 'success') {{
                            statusMsg.innerHTML = '<div class="alert alert-success">Prompt updated successfully! Redirecting...</div>';
                            setTimeout(() => {{
                                window.location.href = '/newsletter/prompts';
                            }}, 1500);
                        }} else {{
                            statusMsg.innerHTML = '<div class="alert alert-danger">Error: ' + (data.error || 'Failed to update prompt') + '</div>';
                        }}
                    }})
                    .catch(error => {{
                        statusMsg.innerHTML = '<div class="alert alert-danger">Error: ' + error.message + '</div>';
                    }});
                    return false;
                }}
            </script>
        </body>
        </html>
        """
        return html_content, 200
    except Exception as e:
        nav_bar = get_nav_bar()
        return f"<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet'></head><body>{nav_bar}<div class='container mt-4'><h1>Error</h1><p>{str(e)}</p></div></body></html>", 500


@newsletter_blp.route("/prompt/update", methods=['POST'])
def update_prompt():
    """
    Update a prompt.
    
    Accepts JSON with:
        - prompt_id: Prompt identifier (required)
        - prompt_desc: Prompt description/content (optional)
        - project: Project name (optional)
    
    Returns JSON response.
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        prompt_id = data.get("prompt_id")
        prompt_desc = data.get("prompt_desc")
        project = data.get("project")
        
        if not prompt_id:
            return jsonify({"error": "prompt_id is required"}), 400
        
        factory = ObjectFactory()
        prompt_db = factory.get_obj(ObjectFactory.PROMPT_DB)
        
        success = prompt_db.update_prompt(
            prompt_id=prompt_id,
            project=project,
            prompt_desc=prompt_desc
        )
        
        if success:
            return jsonify({"status": "success", "message": "Prompt updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update prompt. Prompt may not exist."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@newsletter_blp.route("/prompt/add", methods=['GET'])
def add_prompt_form():
    """Show form to add a new prompt."""
    try:
        nav_bar = get_nav_bar()
        breadcrumb = get_breadcrumb([
            ("prompts", "/newsletter/prompts"),
            ("add",),
        ])

        html_content = f"""
        <html>
        <head>
            <title>Add New Prompt</title>
            <script src='https://unpkg.com/htmx.org@1.9.10'></script>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            {nav_bar}
            <div class="container mt-4">
                {breadcrumb}
                <hr/>
                <h1>Add New Prompt</h1>
                <form id="add-prompt-form" onsubmit="return submitPrompt(event);">
                    <div class="mb-3">
                        <label for="project" class="form-label"><strong>Project:</strong></label>
                        <input type="text" class="form-control" id="project" name="project" required>
                    </div>
                    <div class="mb-3">
                        <label for="prompt_id" class="form-label"><strong>Prompt ID:</strong></label>
                        <input type="text" class="form-control" id="prompt_id" name="prompt_id" required>
                    </div>
                    <div class="mb-3">
                        <label for="prompt_desc" class="form-label"><strong>Prompt Description:</strong></label>
                        <textarea class="form-control" id="prompt_desc" name="prompt_desc" rows="15" style="font-family: monospace;"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                    <a href="/newsletter/prompts" class="btn btn-secondary">Cancel</a>
                    <div id="status-message" class="mt-3"></div>
                </form>
            </div>
            <script>
                function submitPrompt(event) {{
                    event.preventDefault();
                    const project = document.getElementById('project').value.trim();
                    const promptId = document.getElementById('prompt_id').value.trim();
                    const promptDesc = document.getElementById('prompt_desc').value;
                    const statusMsg = document.getElementById('status-message');
                    
                    if (!project || !promptId) {{
                        statusMsg.innerHTML = '<div class="alert alert-danger">Project and Prompt ID are required.</div>';
                        return false;
                    }}
                    
                    fetch('/newsletter/prompt/add', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            project: project,
                            prompt_id: promptId,
                            prompt_desc: promptDesc
                        }})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.status === 'success') {{
                            statusMsg.innerHTML = '<div class="alert alert-success">Prompt added successfully! Redirecting...</div>';
                            setTimeout(() => {{
                                window.location.href = '/newsletter/prompts';
                            }}, 1500);
                        }} else {{
                            statusMsg.innerHTML = '<div class="alert alert-danger">Error: ' + (data.error || 'Failed to add prompt') + '</div>';
                        }}
                    }})
                    .catch(error => {{
                        statusMsg.innerHTML = '<div class="alert alert-danger">Error: ' + error.message + '</div>';
                    }});
                    return false;
                }}
            </script>
        </body>
        </html>
        """
        return html_content, 200
    except Exception as e:
        nav_bar = get_nav_bar()
        return f"<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css' rel='stylesheet'></head><body>{nav_bar}<div class='container mt-4'><h1>Error</h1><p>{str(e)}</p></div></body></html>", 500


@newsletter_blp.route("/prompt/add", methods=['POST'])
def add_prompt():
    """
    Add a new prompt.
    
    Accepts JSON with:
        - project: Project name (required)
        - prompt_id: Prompt identifier (required)
        - prompt_desc: Prompt description/content (optional)
    
    Returns JSON response.
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        project = data.get("project")
        prompt_id = data.get("prompt_id")
        prompt_desc = data.get("prompt_desc")
        
        if not project or not prompt_id:
            return jsonify({"error": "project and prompt_id are required"}), 400
        
        factory = ObjectFactory()
        prompt_db = factory.get_obj(ObjectFactory.PROMPT_DB)
        
        # Check if prompt_id already exists
        existing = prompt_db.get_prompt_by_id(prompt_id)
        if existing:
            return jsonify({"error": f"Prompt with ID '{prompt_id}' already exists"}), 400
        
        result_id = prompt_db.add_prompt(
            project=project,
            prompt_id=prompt_id,
            prompt_desc=prompt_desc
        )
        
        if result_id:
            return jsonify({"status": "success", "message": "Prompt added successfully", "id": result_id}), 201
        else:
            return jsonify({"error": "Failed to add prompt"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @newsletter_blp.route("/snippets", methods=['POST'])
# def add_snippet():
#     """Add a new snippet."""
#     try:
#         if not request.is_json:
#             return jsonify({"error": "Content-Type must be application/json"}), 400
        
#         data = request.get_json()
#         project = data.get("project")
#         category = data.get("category")
#         text = data.get("text")
#         approval_state = data.get("approval_state", 0)
#         deleted = data.get("deleted", 0)
        
#         if not project or not category or not text:
#             return jsonify({"error": "project, category, and text are required"}), 400
        
#         factory = ObjectFactory()
#         snippet_db = factory.get_obj(ObjectFactory.SNIPPET_DB)
        
#         success = snippet_db.add(project, category, text, approval_state=approval_state, deleted=deleted)
        
#         if success:
#             return jsonify({"status": "success", "message": "Snippet added successfully"}), 201
#         else:
#             return jsonify({"error": "Failed to add snippet"}), 500
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @newsletter_blp.route("/api/publish-snippet", methods=['POST'])
# def api_publish_snippet():
#     """Publish a snippet by UUID prefix."""
#     try:
#         if not request.is_json:
#             return jsonify({"error": "Content-Type must be application/json"}), 400
        
#         data = request.get_json()
#         uuid_prefix = data.get("uuid")
#         published_value = data.get("published")
        
#         if not uuid_prefix:
#             return jsonify({"error": "uuid is required"}), 400
        
#         if not published_value:
#             return jsonify({"error": "published is required"}), 400
        
#         # Validate UUID prefix is 7 characters
#         if len(uuid_prefix) != 7:
#             return jsonify({"error": "uuid must be exactly 7 characters"}), 400
        
#         factory = ObjectFactory()
#         snippet_db = factory.get_obj(ObjectFactory.SNIPPET_DB)
        
#         success, error_code, error_message = snippet_db.publish_snippet(uuid_prefix, published_value)
        
#         if success:
#             return jsonify({"status": "success", "message": "Snippet published successfully"}), 200
#         else:
#             # Map error codes to HTTP status codes
#             status_code_map = {
#                 "NOT_FOUND": 404,
#                 "MULTIPLE_MATCHES": 400,
#                 "NOT_APPROVED": 400,
#                 "ALREADY_PUBLISHED": 400,
#                 "INTERNAL_ERROR": 500
#             }
#             status_code = status_code_map.get(error_code, 500)
#             return jsonify({"error": error_message, "error_code": error_code}), status_code
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

