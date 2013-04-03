def get_all_launch_configuraions(auto_scale_connection, *args, **kwargs):
    all_rs = []
    next_token = None
    while True:
        kwargs['next_token'] = next_token
        rs = auto_scale_connection.get_all_launch_configurations(*args, **kwargs)
        all_rs.extend(list(rs))
        next_token = rs.next_token
        if next_token is None:
             return all_rs
