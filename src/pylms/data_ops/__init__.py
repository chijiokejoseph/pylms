from pylms.data_ops.add import add
from pylms.data_ops.append import append_update
from pylms.data_ops.edit import edit
from pylms.data_ops.load import load
from pylms.data_ops.new import new
from pylms.data_ops.record import record
from pylms.data_ops.remove import remove_students
from pylms.data_ops.save import save
from pylms.data_ops.sub import sub
from pylms.data_ops.view import view

__all__: list[str] = [
    "add",
    "edit",
    "load",
    "new",
    "record",
    "save",
    "sub",
    "view",
    "append_update",
    "remove_students",
]
