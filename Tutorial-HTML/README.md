# Web Design Tutorial
## HTML
## CSS
* **Box Model** - every HTML element (e.g. `<html>`, `<body>`, `<div>`, `<p>`, etc.) is modeled as a layered box with the content in the center and 3 surrounding layers.
    * Layers 
        * (1) Content
        * (3) `border` - A stylizable border around the content 
        * (2) `padding` - buffer space between content and border
        * (4) `margin` - buffer space between border and parent element
    * `background` - style (i.e. color or image) beneath border, padding, and content. Margin style conforms to background of parent element.
    * `height`/`width` sets dimensions for content only. The total dimensions of an element are given by the sum of content + padding + border + margin dimensions barring things like margin collapse and element overlap.
    * `display` - specify how an element's box is displayed and able to be configured
        * `block` - formattable box; occupies its own line (`div`, `h1`, `p`, `li`, `section`)
        * `inline-block` - formattable box; continues on same line
        * `inline` - non-formattable box; continues on same line (e.g. `em`, `i`, `span`, `a`, `img`)
        * `flow`
        * `flex`
        * `grid`
    * **Margin Collapse** - adjoining top and/or bottom margins of any two elements (siblings or nested) collapse into a single margin. Side margins are never collapsed.
* **Replacement Element** - an element (e.g. `<img>`, `<video>`) that gets replaced during browser display by an object that cannot be formatted by CSS beyond how it fits into and is positioned within its box area 
    * `object-fit`

## References
* [WHATWG Standards](https://spec.whatwg.org/) - The standardization community for HTML and related web technology. Their documentation should provide the common denominator of all technologies even if a specific browser extends on these standards
    * [HTML Standard](https://html.spec.whatwg.org/multipage/)
    * [DOM Standard](https://dom.spec.whatwg.org/)
* [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web) - reference documentation maintained by Mozilla Development Network for several web technologies. Comes up often in google search results and is more readable than WHATWG
