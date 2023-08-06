import functools

def _except_return_none(func):

  @functools.wraps(func)
  def wrapper_except_return_none(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except:
      return None

  return wrapper_except_return_none
