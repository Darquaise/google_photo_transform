from datetime import datetime


def dt2text(dt: datetime):
    return dt.strftime("%d.%m.%Y %H:%M:%S")


def dt_now_as_text():
    return dt2text(datetime.utcnow())


def verbose_print(text, verbose: bool):
    if verbose:
        print(text)


def letlon2dms(dd: float):
    mult = -1 if dd < 0 else 1
    mnt, sec = divmod(abs(dd)*3600, 60)
    deg, mnt = divmod(mnt, 60)
    return (int(mult * deg), 1), (int(mult * mnt), 1), (int(mult * sec * 1000000), 1000000)
