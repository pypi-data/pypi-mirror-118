from awesomeTaskPy.context.event import event
from awesomeTaskPy.task.baseTask import taskExecuteResult
#��������ִ�����ִ�еĴ������¼�
ON_CHILDREN_TASK_FINISHED = 'ON_CHILDREN_TASK_FINISHED'
class systemEventRegister:
    @staticmethod
    def register():
        def ON_CHILDREN_TASK_FINISHED_HANDLER(params):
            taskExecuteResult[params['taskId']]=params
        event.register(ON_CHILDREN_TASK_FINISHED,ON_CHILDREN_TASK_FINISHED_HANDLER)
