# IMS.WebAPI

1. Установить переменную окружения CGI_REPORTS_PATH (путь до директории с отчетами):
```export CGI_REPORTS_PATH=/home/ims/reports```

2. Настройка lighttpd

* В modules.conf (или lighttpd.conf, если нет include "modules.conf") добавить или раскомментировать строки:
```
server.modules = (
    "mod_cgi",
    "mod_setenv",
)
```

* В lighttpd.conf добавить строки (заменить путь до интерпретатора python, если отличается):
```
alias.url += ( "/cgi-bin" => server_root + "/cgi-bin" )
$HTTP["url"] =~ "^/cgi-bin" {
    cgi.assign = ( "" => "/usr/local/bin/python3" )
    setenv.add-environment = ( "CGI_REPORTS_PATH" => env.CGI_REPORTS_PATH )
}
```

* Проверить конфигурацию lighhtpd:
```lighttpd -t -f /usr/local/etc/lighttpd/lighttpd.conf```

* Запустить lighttpd:
```lighttpd -f /usr/local/etc/lighttpd/lighttpd.conf```

3. Скопировать папки cgi-bin/, css/ и файл sample.html в server_root lighttpd (посмотреть в lighttpd.conf).

4. Добавить исполняемый флаг скрипту cmd:
```chmod +x cgi-bin/cmd```

5. Проверить работу сервера из браузера по адресу http://127.0.0.1:8080/sample.html
