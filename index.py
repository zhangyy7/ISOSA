from core import handle

factory = handle.ObjFactory('s')
handler = factory.factory()

handler.enroll(1)
