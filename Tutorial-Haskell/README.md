Haskell
=======

# ToDos
* [] Get NeoVim LSP setup

# Resources
* Official page [haskell.org](https://www.haskell.org)
    * [GHCup](https://www.haskell.org/ghcup)
    * [Cabal](https://www.haskell.org/cabal) - system for building and packaging libraries and programs
* [Hackage](https://hackage.haskell.org) - central package archive
    * sandbox
* [Stack](https://docs.haskellstack.org) - 
* Tutorials
    * [learnyouahaskell.com](http://learnyouahaskell.com)

# Installation for MacOS
Install GHCup and use the interactive installer
```bash
brew install ghcup
ghcup tui
```
Add `~/.ghcup/bin` to PATH in `.bashrc`.

# Using the REPL
```bash
ghci
```

# Compiling executable
```bash
ghc hello.hs
```

# Package and environment management
```bash
cabal install --lib random
```

# Key concepts
* `main` function - the entry point for all compiled Haskell programs
    * Unlike most functions in Haskell, `main` can perform monadic (e.g. I/O)
      actions like printing to stdout
* `do` block - Sequence of instructions for a monadic (e.g. I/O) functions

