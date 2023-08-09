from datetime import datetime, date, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')
dt_utcnow = datetime.utcnow()
str = dt_utcnow.isoformat()
dt = datetime.fromisoformat(str) # naive
utc = dt.replace(tzinfo=timezone.utc) # aware(UTC)
jst = utc.astimezone(JST) # aware(JST)
dt_text = jst.strftime('%Y年%m月%d日 %H時の問題')
print(dt_text)