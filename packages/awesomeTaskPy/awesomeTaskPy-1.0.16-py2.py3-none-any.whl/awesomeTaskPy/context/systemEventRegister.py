from awesomeTaskPy.context.event import event
from awesomeTaskPy.task.baseTask import taskExecuteResult
#当子任务执行完成执行的触发的事件
ON_CHILDREN_TASK_FINISHED = 'ON_CHILDREN_TASK_FINISHED'
class systemEventRegister:
    @staticmethod
    def register():
        def ON_CHILDREN_TASK_FINISHED_HANDLER(params):
            taskExecuteResult[params['taskId']]=params
        event.register(ON_CHILDREN_TASK_FINISHED,ON_CHILDREN_TASK_FINISHED_HANDLER)
