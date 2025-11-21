

Actor: quote_generator 
generates quote ideas and sends to "quotes"

Queue: quotes
New quotes are added here
Actor: quote_editor
Actions:
    approve (approved_quotes)
    reject (rejected_quotes)
    comment (quote_rewrite)

Queue: approved_quotes

Queue: rejected_quotes

Queue: quote_rewrite
Revises quotes
Actor: quote_rewriter
Destination: quotes



Class Name: WorkQueueDB
Filename: work_queue_db.py

Methods
    def add_task(project, queue, task_uuid) # adds a task in a queue
    def move_task_queue(id, dest_queue)  # moves a task to a different queue

WorkQueueDBEntry
    id = PrimaryKeyField(index=True, unique=True)
    project = CharField(max_length=255, index=True, null=False)
    queue = CharField(max_length=255, index=True, null=False)
    task_uuid = CharField(max_length=255, index=True, null=False)
    added_to_queue_ts = IntegerField(null=False)


Class Name: WorkQueueTaskDB
Filename: work_queue_task_db.py

Methods: 
    def add_task(task_type, text=None, image=None) --> task_uuid

WorkQueueTaskDBEntry
    task_uuid = CharField(max_length=255, index=True, null=False)
    task_type = CharField() # text, json, image
    text = TextField() # for storing text (raw or json)
    image = BinaryField() # for storing images
    created_ts = IntegerField


Class Name: WorkQueueManager
Filename: work_queue_mgr.py
Methods:

    # this method will first add the task to WorkQueueTaskDB and then 
    # call WorkQueueDB.add_task
    def add_task(factory, project, queue, task_type, text=None, image=None)





n8n -> adds quotes one at a time in queue "quote_text_approval"
quote_editor role approves/rejects or gives feedback




Object Versions
    uuid = CharField() # a unique id that stays the same for all versions
    text = TextField(null=False) only text or image will be set
    image = BinaryField(null=False)
    version = CharField(null=False)  # md5 of content that uniquely identifies this version
    created_ts

Object Action History
    uuid = CharField()
    action = approve | reject | comment
    version # the version this action happend on
    comment text  # if the action was comment, this is the text
    actor id # the id of the actor who did the action


    reserved_worker_uuid = CharField(null=False)
    reserved_ts = IntegerField(null=False)
    reserved_heartbeat_ts = IntegerField(null=False)
    done_ts = IntegerField(null=False)

