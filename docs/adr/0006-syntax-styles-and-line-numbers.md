# Syntax styles, Markdown headings, and line numbers

`build.py` used to fix every font style: comments in italics, Markdown headings plain and bold. JetBrains draws constants in italics in both Islands schemes, and its Markdown plugin draws headings through `HEADER_LEVEL` keys that fall back to `CONSTANT`, so Islands' headings, `#` markers included, are the constant colour in italics. A palette can now say so:

- A `[syntax_style]` table maps a syntax role to `"italic"` or `"bold"`. Every Zed capture and VS Code token rule, TextMate or semantic, drawn in that role takes the style, unless its mapping sets its own, as comments and Markdown emphasis do.
- `heading` in `[syntax]` names the role whose colour and style Markdown headings take: Zed's `title` and `markup.heading`, and VS Code's `markup.heading` and `punctuation.definition.heading`, the `#` markers, which VS Code's `punctuation` rule would otherwise claim. Without it, headings stay plain and bold.

Islands Dark and Light set `constant = "italic"` and `heading = "constant"`, so headings are `#ca7fbe` and `#871094` in italics. Whatever the shared mapping draws in the constant colour turns italic with it: booleans, though JetBrains draws them as keywords, enum members, Ruby symbols, CSS values, diff file headers, and, in Zed, commit hashes and branch names. Zed also gives the heading look to commit subjects and to Markdown's `---`, which it captures as headings, while VS Code leaves `---` plain. Static members stay upright: JetBrains italicises them, but `function_system` also covers library calls.

Styles reach only Zed and VS Code. Xcode's recipe, the terminals, and Claude Code take colours alone, so they stay as they were. Markdown table pipes stay plain. Zed captures them as `punctuation.markup`, along with block-quote markers and table delimiter rows, and with no key of that name it falls back to `punctuation`.

Line numbers get their own key. ADR 0004 has every target but Xcode draw them in `ui.quiet`, which holds 4.5:1 on the panel and the element as well as the background. JetBrains' line numbers are fainter, so a palette can set `line_number` in `[ui]`, held to 4.5:1 on the background alone, where the editor's gutter draws them. Zed's `editor.line_number` and VS Code's `editorLineNumber.foreground` take it, and it defaults to `quiet`. The current line's number stays the foreground colour. Islands Dark's `#7d828b` and Islands Light's `#717685` are JetBrains' `#4b5059` and `#aeb3c2`, each moved with its hue kept only as far as 4.5:1 needs.

VS Code also draws line numbers on two other grounds. The peek view's gutter defaults to the peek editor's background, `ui.panel`, where Islands' fall to 3.82:1 in Dark and 3.77:1 in Light. The diff editor's gutter takes each changed line's diff fill, where they fall to between 3.93:1 and 4.09:1. We accept both rather than move JetBrains' colours further, or give those gutters a different fill from the code beside them.

A palette that sets none of these generates what it did before, so Geist's, Ayu's, and Brzz's themes are unchanged.
