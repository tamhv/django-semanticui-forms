from django.db.models.fields import BLANK_CHOICE_DASH
from django.conf import settings


def pad(value):
	"""
	Add one space padding around value if value is valid.

	Args:
		value (string): Value

	Returns:
		string: Value with padding if value was valid else one space
	"""
	return " %s " % value if value else " "


def get_placeholder_text():
	"""
	Return default or developer specified placeholder text.
	"""
	return getattr(settings, "SUI_PLACEHOLDER_TEXT", "Select")


def get_choices(field):
	"""
	Find choices of a field, whether it has choices or has a queryset.

	Args:
		field (BoundField): Django form boundfield

	Returns:
		list: List of choices
	"""	
	empty_label = getattr(field.field, "empty_label", False)
	needs_empty_value = False
	choices = []

	# Data is the choices
	if hasattr(field.field, "_choices"):
		choices = field.field._choices

	# Data is a queryset
	elif hasattr(field.field, "_queryset"):
		queryset = field.field._queryset
		field_name = getattr(field.field, "to_field_name") or "pk"
		choices += ((getattr(obj, field_name), str(obj)) for obj in queryset)

	# Determine if an empty value is needed
	ch = list(choices) if choices else None
	if ch and (ch[0][1] == BLANK_CHOICE_DASH[0][1] or ch[0][0]):
		needs_empty_value = True

		# Delete empty option
		if not ch[0][0]:
			del ch[0]

	# Remove dashed empty choice
	if empty_label == BLANK_CHOICE_DASH[0][1]:
		empty_label = None

	# Add custom empty value
	if ch and empty_label or not field.field.required:
		if needs_empty_value:
			ch.insert(0, ("", empty_label or BLANK_CHOICE_DASH[0][1]))

	return ch
