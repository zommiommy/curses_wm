

def offsettable(f, row_or_cols="row"):
	"""Decorators ment to add the offsettability to the position methods of the Window class. it add the offset kwarg to those methods."""
	# Create the new fake method
	def wrapped(self, offset=0):
		"""Default docs that will be overwritten"""
		# calc the result
		result = f(self) + offset
		# check / clip the bounds
		if offset != 0:
			if row_or_cols == "row":
				result = self.clip_to_bounds_y(result)
			else:
				result = self.clip_to_bounds_x(result)
		return result
	# Copy the wrapped functions name
	if f.__name__:
		wrapped.__name__ = f.__name__
	# If it has any copy the docs of the function
	if f.__doc__:
		wrapped.__doc__  = f.__doc__
	# Append the added decorated functionality to the doc of the functionality
	wrapped.__doc__ += "\n\n" + offsettable.__doc__
	return wrapped


def offsettable_row(f):
	return offsettable(f, "row")

def offsettable_col(f):
	return offsettable(f, "col")