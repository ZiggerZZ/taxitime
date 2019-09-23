def split_date_time(dt):
    '''
    Cast native datetime or date stamps into a pandas readable datetime object
    '''
    try:
        split_dt = dt.split()
        if len(split_dt) > 1: # in airport data, both date and time is in dt
            date, time = dt.split()
        else: # in weather data, only date (no time) is in their datestamp
            date = split_dt[0]
    except (ValueError, AttributeError):
        return np.nan
    try:
        month, day, year = date.split('/')
        if len(split_dt) == 1:
          return pd.Timestamp(year=int(year), month=int(month), day=int(day))
    except (ValueError, AttributeError):
        return np.nan
    try:
        hour, minute = time.split(':')
    except (ValueError, AttributeError):
        return np.nan
    return pd.Timestamp(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))