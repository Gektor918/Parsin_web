Minimalistic implementation of auto-posting articles in Telegram from a third-party website. 



This project implements the parsing of articles from a third-party website using the Beautiful Soup library, saving the parsing result in a local database (SQLite).
The next step was the implementation of sending an actual article to telegram using libraries (Request,
Telegraph). This code implements the logic for updating the database for sending content, and much more: packing the article, sorting in the database, parsing the cover of the article, storing and transferring.
In the code, there is no registration of an account in telegrams, as well as the creation of the database itself, for brevity and readability of the code itself. 
