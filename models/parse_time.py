import re
import arrow

ex = r'(?<!\S\S)(?<![^\,\.\;\:\?\!\"\'\`\[\]\{\}\(\)<>\s])(\b|^)(?P<YY>\d{2})/(?P<MM>\d{2})/(?P<DD>\d{2}),(?P<HH>\d{2}):(?P<mm>\d{2}):(?P<ss>\d{2})(?P<ZZ>([\+\-])(\d{2})(?:\:(\d{2}))?|Z)(?=[\,\.\;\:\?\!\"\'\`\[\]\{\}\(\)\<\>]?(?!\S))'
tokens = ['YY', 'MM', 'DD', 'HH', 'mm', 'ss', 'ZZ']

BC66_FORMAT = 'YYYY/MM/DD,HH:mm:ss'
BC660_FORMAT = "YY/MM/DD,HH:mm:ssZZ" # But 4XZZ

def parse_time(t):
    now = arrow.utcnow()
    fmt_pattern_re = re.compile(ex)
    try:
        match = fmt_pattern_re.search(t)
        parts = list(map(lambda x:int(match.group(x)), tokens))
    except AttributeError:
        try:
            tz = t.split('GMT')
            dt = arrow.get(tz[0], BC66_FORMAT)
            zone = int(tz[1])
            tzinfo = f'utc{zone}' if zone < 0 else f'utc+{zone}'
        except Exception as e:
            return t
    else:
        parts[0] = (now.year//100 * 100) + parts[0]
        parts[6] = parts[6]//4
        tzinfo = f'utc+{parts[6]}' if parts[6] > 0 else f'utc{parts[6]}'

        dt = arrow.Arrow(year=parts[0],
                         month=parts[1],
                         day=parts[2],
                         hour=parts[3],
                         minute=parts[4],
                         second=parts[5],
                         tzinfo='utc')

    return dt, tzinfo

if __name__ == "__main__":
    #t='2023/04/27,14:20:26GMT-4'
    #t = "23/04/24,16:29:00-16"
    t = "23/04/25,14:38:40-16"
    dt = parse_time(t)
    print(dt.isoformat())
