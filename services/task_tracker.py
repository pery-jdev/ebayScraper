from typing import Dict, Any, List
import uuid
from datetime import datetime
from models.task import Task
from config.database import get_db


class TaskTracker:
    def create_task(self, task_type: str) -> str:
        """Create a new task and return its ID."""
        task_id = str(uuid.uuid4())
        with get_db() as db:
            task = Task(
                id=task_id,
                type=task_type,
                status="pending",
                result=[],
                progress={"processed": 0, "total": 0}
            )
            db.add(task)
            db.commit()
        return task_id

    def update_task(
        self, 
        task_id: str, 
        status: str, 
        result: Any = None, 
        error: str = None, 
        progress: Dict[str, int] = None
    ):
        """Update task status and result."""
        with get_db() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = status
                task.updated_at = datetime.utcnow()
                
                if result is not None:
                    task.result = result
                if error is not None:
                    task.error = error
                if progress is not None:
                    task.progress = progress
                    
                db.commit()

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get task details by ID."""
        with get_db() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                return {
                    "id": task.id,
                    "type": task.type,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "result": task.result,
                    "error": task.error,
                    "progress": task.progress
                }
            return None

    def list_tasks(self) -> Dict[str, Dict[str, Any]]:
        """List all tasks."""
        with get_db() as db:
            tasks = db.query(Task).all()
            return {
                task.id: {
                    "id": task.id,
                    "type": task.type,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat(),
                    "result": task.result,
                    "error": task.error,
                    "progress": task.progress
                }
                for task in tasks
            }


# Create a global instance
task_tracker = TaskTracker() 