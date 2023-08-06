from email.utils import parsedate_to_datetime

def parse_date_header(s):
    return parsedate_to_datetime(s).timestamp()

def format_timestamp(t):
    return "<t:%d:D> at <t:%d:T> (<t:%d:R>)" % (t, t, t)

def hyperlink(text, url):
    return "[%s](%s)" % (text, url)

def escape_backticks(txt):
    # a truly terrible solution
    # sorry that Discord-flavored markdown
    # doesn't have a better option (backslash doesn't work)
    return txt.replace("`", "\u200b`\u200b")

def get_inline_code(txt):
    return "``%s``" % escape_backticks(txt)

def get_code_block(txt):
    return "```%s```" % escape_backticks(txt)

def mention_role(role):
    return "<@&%s>" % role

def make_flags(*values):
    x = 0
    for v in values:
        x |= 1 << v
    return x
get_flags = make_flags

def col32(r,g,b):
    return (r % 256) << 16 | (g % 256) << 8 | (b % 256)

def format_time(seconds):
    integral, decimal, decimal_magnitude = 0, 0, 0
    past = False
    if isinstance(seconds, str):
        past = seconds.startswith("-")
        if past:
            seconds = seconds[1:]
        
        if "." in seconds:
            [integral, decimal] = seconds.split(".")
            decimal_magnitude = len(decimal)
            integral, decimal = int(integral), int(decimal)
        else:
            integral = int(seconds)
    else:
        past = seconds < 0
        seconds = abs(seconds)
        
        integral, decimal = seconds // 1, seconds % 1
        decimal_magnitude = 0
        while decimal % 1 != 0:
            decimal *= 10
            decimal_magnitude += 1
        decimal = int(decimal)
    
    integral_labels = [
        ["millennium", "millennia", 31_536_000_000],
        ["century", "centuries", 3_153_600_000],
        ["decade", "decades", 315_360_000],
        ["year", "years", 31_536_000],
        ["week", "weeks", 604_800],
        ["day", "days", 86_400],
        ["hour", "hours", 3_600],
        ["minute", "minutes", 60],
        ["second", "seconds", 1]
    ]
    decimal_labels = [
        ["millisecond", "milliseconds", 3],
        ["microsecond", "microseconds", 6],
        ["nanosecond", "nanoseconds", 9]
        # not showing smaller units so that numbers like 123.999999999999999999974 will get rounded
    ]
    decimal_precision = decimal_labels[-1][-1]
    
    if decimal_magnitude > decimal_precision:
        offset_decimal = 10 ** (decimal_magnitude - decimal_precision)
        round_using = decimal % offset_decimal
        if round_using >= offset_decimal * 0.5: # round up
            decimal //= offset_decimal
            decimal += 1 # might have been 999999
            if decimal >= 10 ** (decimal_precision + 1):
                decimal = 0
                decimal_magnitude = 0
                integral += 1
        else: # round down
            decimal //= offset_decimal
        decimal_magnitude = decimal_precision
        
    # remove trailing zeros on decimal
    while decimal % 10 == 0 and decimal_magnitude > 0:
        decimal //= 10
        decimal_magnitude -= 1
    
    if integral == 0 and decimal == 0:
        return "now"
    
    sections = []
    for [singular, plural, period] in integral_labels:
        if integral >= period:
            count = integral // period
            integral %= period
            sections.append("%d %s" % (count, singular if count == 1 else plural))
    
    for i in range(len(decimal_labels)):
        if decimal_magnitude > 0:
            [singular, plural, magnitude] = decimal_labels[i]
            relative_magnitude = magnitude - (0 if i == 0 else decimal_labels[i - 1][-1])
            
            count = 0
            if decimal_magnitude > relative_magnitude:
                count = decimal // 10 ** (decimal_magnitude - relative_magnitude)
            else:
                count = decimal * 10 ** (relative_magnitude - decimal_magnitude)
            
            decimal %= 10 ** (decimal_magnitude - relative_magnitude)
            decimal_magnitude -= relative_magnitude
            
            if count > 0:
                sections.append("%d %s" % (count, singular if count == 1 else plural))
    
    out = ""
    if len(sections) == 1:
        out = sections[0]
    else:
        out = ", ".join(sections[:-1]) + " and " + sections[-1]
    
    if past:
        out += " ago"
    
    return out

import asyncio
async def call_func(f, *args, **kwargs):
    if asyncio.iscoroutinefunction(f):
        return await f(*args, **kwargs)
    else:
        return f(*args, **kwargs)

def error_caused_by(inst, err_class):
    if isinstance(inst, err_class) or issubclass(inst.__class__, err_class):
        return inst
    elif inst.__cause__ != None:
        return error_caused_by(inst.__cause__, err_class)
    else:
        return None