# NoCover

> STILL IN DEVELOPMENT - IT WILL BE BUGGY

A TUI application to supplement Hardcover.

## Why?

Yeah, a TUI doesn't need to be a thing. However, I've wanted to make a TUI for a while and Hardcover is a project i'm interested enough in to give it a go.

## Features

- Pull profile data from Hardcover API
- Pull books associated with account - ('want-to-read' and 'read').
    - books are displayed in a selectable list which then allows viewing of more data.
- Pull Series, Lists and Prompts associated with account.
    - So far this is based on internal csv.
    - Idea to be able to track these, while the site doesn't yet.

![Current Dev build](images/dev-build.png)

## TODO's

- [ ] In case it could be used in another tool, choose where to save a BRL whilst defaulting to Config.SeriesPath
- [ ] Search for book to add to `want-to-read`.
- [X] Quick add Series
- [ ] Quick add Lists - almost done
- [ ] Quick add Prompts
- [ ] Tick toggle to add books to `want-to-read`
- [ ] Fully offline use
    - required downloading and storing of data
    - use a local db such as DuckDB?
    - Won't matter for series downloaded as BRL file (yes I will push this as much as possible, i think it would be helpful.)

- [ ] Book Editor Modal
- [X] Better onboarding Modal
