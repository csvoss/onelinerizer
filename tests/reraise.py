try:
    try:
        0/0
    except Exception:
        raise
except Exception as e:
    print repr(e)
