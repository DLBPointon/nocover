# NoCover

> STILL IN DEVELOPMENT - IT WILL BE BUGGY

A TUI application to supplement Hardcover.

## Why?

Yeah, a TUI for this doesn't need to be a thing. However, I've wanted to make a TUI for a while and Hardcover is a project i'm interested enough in to give it a go.

## Features

- Pull profile data from Hardcover API
- Pull books associated with account - ('want-to-read' and 'read').
    - books are displayed in a selectable list which then allows viewing of more data.
- Pull Series, Lists and Prompts associated with account.
    - So far this is based on internal csv.
    - Idea to be able to track these, while the site doesn't yet.

![Current Dev build](images/dev-build.png)

## TODO's

- [ ] Search for book to add to `want-to-read`, `read` or a local private list.
- [ ] General Improvements to displaying data
    - there's more data stord than shown, it's because it's not named the same that it isn't shown. I don't reaaaaly want to end up with `book if book elif list_book elif prompt_book elif series_book` sort of logic in there.
- [ ] Consolidate Series/Prompt/List brl reading and generation
    - Might be a pain considering that each have different named values.
- [ ] Tick toggle to add books to `want-to-read`
- [ ] Fully offline use
    - required downloading and storing of data in format that is easy to access.
    - use a local db such as DuckDB?
    - Won't matter for series downloaded as BRL file (yes I will push this as much as possible, i think it would be helpful.)
- [ ] Book Editor Modal
- [ ] Add book descriptions to brl file generation
- [ ] Add another...? To a modal.
- [X] Add Logging @ 21/10/2025

### Pre-November updates
- [X] In case it could be used in another tool, choose where to save a BRL whilst defaulting to Config.SeriesPath
- [X] Loading Screen
- [X] Quick add Series
- [X] Quick add Lists
- [X] Quick add Prompts
- [X] Better onboarding Modal
- [X] Move all config path into Config
    - Rewrote a couple of functions around this
    - Turns out I was manually building the path EVERY time i used it!
- [X] Convert to using TSV rather than CSV as many lists and prompts may have "," in title.
