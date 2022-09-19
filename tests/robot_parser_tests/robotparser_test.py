import urllib.robotparser


rp = urllib.robotparser.RobotFileParser()
rp.set_url("robots.txt")
rp.read()
rrate = rp.request_rate("*")
print(rp.can_fetch("*", "http://www.musi-cal.com/wp-admin/gotj"))
print(rp.can_fetch("*", "http://www.musi-cal.com/wp-admin/admin-ajax.php"))