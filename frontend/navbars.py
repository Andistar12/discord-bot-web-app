#The navbar that a non-authenticated user will see
main_nav_bar = [
    # href, page id, page title
    ("/", "status", "Status"),
    ("/commands", "commands", "Commands"),
    ("/login", "login", "Login <img style=\"height: 1.4em\" src=\"https://discord.com/assets/1c8a54f25d101bdc607cec7228247a9a.svg\">")
]


#The navbar that an authenticated non-admin user will see
user_nav_bar = [
    # href, page id, page title
    ("/", "status", "Status"),
    ("/commands", "commands", "Commands"),
    ("/user", "user", "User Stats"),
    ("/logout", "logout", "Logout")
]


#The navbar that an authenticated admin user will see
admin_nav_bar = [
    # href, page id, page title
    ("/", "status", "Status"),
    ("/commands", "commands", "Commands"),
    ("/user", "user", "User Stats"),
    ("/admin/manage", "manage", "Manage"),
    ("/admin/servers", "servers", "Servers"),
    ("/admin/logs", "logs", "Logs"),
    ("/admin/cadvisor", "cadvisor", "CAdvisor"),
    ("/admin/adminer", "adminer", "Adminer"),
    ("/admin/redis", "redis", "Redis"),
    ("/logout", "logout", "Logout")
]
