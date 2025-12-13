"""
Docstring for Instalocker


/EN

- Instalocker is a simple TUI application designed to automate agent locking in Valorant.
- It is a hobby project and is not for sale.
- The application is in executable format and can be run by double clicking or by entering the command .\\Instalocker.exe in the command prompt (a cmd window must be opened in the same directory).
- It was created using valclient.


/TR
- Instalocker Valorantta ajan kitlemeyi otomatimize etmek için yapılmış basit bir TUI uygulamasıdır. 
- Hobi projesidir, parayla satılmaz.
- Uygulama executable formattadır, çift tıklanarak veya command promptdan .\\Instalocker.exe komutu ile çalıştırılabilir (aynı dizinde bir cmd açılmalıdır.)
- valclient kullanılarak yapılmıştır.


Version : V1.8.0--alpha-1.0
Version-Path : src/utils/version
Author/Maintainer : berkwe


~This code is not 'vibe coding'~

"""



from src.app import InstalockerApp


if __name__ == "__main__":
    app = InstalockerApp()
    app.run()
