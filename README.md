# tc-bot
The crims bot.

One night project run.

Steps:

1. Put login.

`login_name = ""`
`password_text = ""`

2. Configure respect limits.

`attack_him = False`
`if visitor_rank != "Hitman":`
`    if visitor_name not in name_ignore:`
`        if visitor_prof not in ignore_list:`
`            if visitor_respect <=160000:`
`                    attack_him = True`
`else:`
 `   if visitor_respect <=70000:`
        `attack_him = True`
        
3. Select hunt in main.

Hunt config:

`if __name__ == "__main__":
    login()
    time.sleep(5)
    while True:
        goRaveMenu(sleep=2)
        scanPrey()
`
Rob config:
- for robbery put correct value from options
selector.select_by_value('48') -> Latino Kings

`if __name__ == "__main__":
    login()
    time.sleep(5)
    while True:
        robSingle()`

Working as of 6.06.2020
