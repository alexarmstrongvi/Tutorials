# JavaScript
## Running Code
There are several methods for running JavaScript:

1. **Command Line** -  Various runtime systems exist that can run `.js` files or open an interactive shell. The most common is [Node.js](https://nodejs.org/en/) but smaller alternatives are RingoJS and PurpleJS as well as the more recent Deno.
    * Run as `> node myscript.js`

1. **Within HTML** - JavaScript can be included in HTML files and will be run by browsers reading the files
    * Inline:
    ```html
    <script>alert("Hello World")</script>
    ```
    * External (preferred)
    ```html
    <script src="./index.js"></script>
    ```

1. **Browser Console** - Web browsers usually provide a console (a.k.a. [REPL](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop), language shell) for running JS code. It is basically an IDE. The console environment will be set by the browser window/tab from which the console was opened.
    * [Chrome](https://developer.chrome.com/docs/devtools/console/): Settings &rarr; More Tools &rarr; Developer Tools. You can undock the console to write code in a separate window instead of in split-screen mode.
    * Safari, Firefox, etc...

1. **Web App** - A few online IDEs exist, such as [StackBlitz](https://stackblitz.com/), that can run code in various environments.