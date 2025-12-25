from pylms.history import load_history, save_history
from pylms.models import sort_form

history = load_history().unwrap()

history.class_forms.sort(key=sort_form)
class_dates = [form.date for form in history.class_forms]
print(f"{class_dates = }")
_ = save_history(history).unwrap()
