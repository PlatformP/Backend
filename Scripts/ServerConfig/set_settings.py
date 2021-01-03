def set_on_server(Base_Dir):
    if '/home/ubuntu' in str(Base_Dir):
        return True
    else:
        return False