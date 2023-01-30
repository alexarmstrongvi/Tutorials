# Regular Expressions (RegEx)

## Introduction
Regular expressions are character sequences that define a search pattern.
This can be studied independent of its implementation in programming.
However, the most familiar use of regular expressions is in string-searching algorithms.
While there exists a few standard syntaxes across tools, most tools implement there own 'flavor'.
This leads to different capabilities and idiosyncratic behvior for each tool.

At the bottom of everything is the RegEx engine which defines the limit on any implementation.
Each RegEx library or tool is responsible for passing user input to the engine and returning the results.
The syntax and capability or each library/tool depends on the developer and engine.
Generally, developers adhere to a common syntax in most use cases.
The big differences are in what capabilities each tool has implemented.

**RegEx engine types**

* Traditional NFA
* POSIX NFA
* DFA
* hybrid NFA/DFA (e.g. Henry Spencer's engine)

**RegEx Flavors/Implementations/Standards**

* POSIX Basic Regular Expressions (BRE)
* POSIX Extended Regular Expresions (ERE)
* Perl
* ECMA/JavaScript
* Others that tend to be defined relative to the above flavors:
	* BRE-like : GNU BRE
	* ERE-like : GNU ERE
	* Perl-like : PCRE, , Python, std::regex
	* EMCA-like : Java

	
**Features not (yet) included in tutorials**

* Character class subtraction and intersection (Java and XML)
* 


## References
**General**

* [regular-expressions.info](https://www.regular-expressions.info) - the online bible for RegEx
* "Mastering Regular Expressions: Understand Your Data and Be More Productive" by Jeffrey E. F. Friedl - the print bible for RegEx

**Under the hood**

* www.softec.lu : ["Regular Expression Engines"](http://www.softec.lu/site/RegularExpressions/RegularExpressionEngines) 
* Wikipedia : ['Comparison of regular-expression engines'](https://en.wikipedia.org/wiki/Comparison_of_regular-expression_engines)
* CMCDragonkai's GitHub : ['Regular Expression Engine Comparison Chart'](https://gist.github.com/CMCDragonkai/6c933f4a7d713ef712145c5eb94a1816)

**Testers**

* [regex101.com](https://regex101.com/)
* [regexr.com](https://regexr.com/)
