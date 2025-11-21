from .objectfactory import ObjectFactory


class WorkQueueManager:
    """
    High-level manager for work queue tasks.

    This class coordinates between:
      - WorkQueueTaskDB: stores the actual task payload (text / JSON / image)
      - WorkQueueDB: stores which tasks are in which project/queue
    """

    def __init__(self, factory: ObjectFactory | None = None):
        # Allow caller to pass an ObjectFactory, otherwise create one.
        self.factory = factory or ObjectFactory()

    def add_task(self, factory, project, queue, task_type, text=None, image=None):
        """
        Add a task to the work queue.

        This method will:
          1. Add the task payload to WorkQueueTaskDB (returns task_uuid)
          2. Add an entry to WorkQueueDB pointing to that task_uuid

        Args:
            factory: ObjectFactory instance (for compatibility with README signature)
            project: Project name
            queue: Queue name
            task_type: Type of task ('text', 'json', 'image', etc.)
            text: Optional text payload
            image: Optional binary payload

        Returns:
            task_uuid on success, or None on failure.
        """
        # Prefer the instance's factory if set; fall back to provided factory
        factory = self.factory or factory

        # Get DB helpers from the factory
        task_db = factory.get_obj(ObjectFactory.WORK_QUEUE_TASK_DB)
        queue_db = factory.get_obj(ObjectFactory.WORK_QUEUE_DB)

        # 1) Add to WorkQueueTaskDB
        task_uuid = task_db.add_task(task_type=task_type, text=text, image=image)
        if task_uuid is None:
            # Task creation failed
            return None

        # 2) Add to WorkQueueDB
        success = queue_db.add_task(project=project, queue=queue, task_uuid=task_uuid)
        if not success:
            # If queue insertion fails, we leave the task payload as-is but report failure.
            return None

        return task_uuid

    def get_actions(self, queue):
        """
        Return the available actions for a given queue.

        Structure:
            {
                action_key: {
                    "label": "...",
                    "description": "...",
                    "feedback_required": bool,
                    "queue": "destination_queue_name",
                },
                ...
            }
        """
        # Placeholder that maps a queue name to a list of possible actions.
        # The queue in each action is where the task will get moved if that
        # action is taken (not yet implemented).

        content_types = {
            "quotes": {
                "tmpl": ""
            },
            "trivia": {
                "tmpl": ""
            }
        }


        approve_action = {
            "label": "Approve",
            "feedback_required": False,
            "queue": "quotes_approved",
        }
        reject_action = {
            "label": "Reject",
            "feedback_required": False,
            "queue": "quotes_rejected",
        }
        rewrite_action = {
            "label": "Rewrite",
            "feedback_required": True,
            "queue": "quotes_rewrite",
        }

        queue_actions = {}
        for content_type, info in content_types.items():
            queues = ["new", "approved", "rejected"]
            for q in queues:
                key = f"{content_type}_{q}"
                queue_actions[key] = {
                    "approve": approve_action,
                    "reject": reject_action,
                    "rewrite": rewrite_action,
                }

        # queue_actions = {
        #     "quotes_new": {
        #         "approve": approve_action,
        #         "reject": reject_action,
        #         "rewrite": rewrite_action,
        #     },
        #     "quotes_approved": {
        #         "reject": reject_action,
        #         "rewrite": rewrite_action,
        #     },
        #     "quotes_rejected": {
        #         "approve": approve_action,
        #         "rewrite": rewrite_action,
        #     },

        #     "trivia_new": {
        #         "approve": approve_action,
        #         "reject": reject_action,
        #         "rewrite": rewrite_action,
        #     },
        #     "trivia_approved": {
        #         "reject": reject_action,
        #         "rewrite": rewrite_action,
        #     },
        #     "trivia_rejected": {
        #         "approve": approve_action,
        #         "rewrite": rewrite_action,
        #     },
        # }

        return queue_actions.get(queue, {})




