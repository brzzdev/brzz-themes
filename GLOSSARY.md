# Brzz Themes

Editor and terminal themes in three families, Geist (Geist Dark and Geist Light), Ayu (Ayu Dark Contrast), and Brzz (Brzz Dark), all generated from one palette per theme, except where a theme takes a port.

## Language

**Family**:
A set of themes that share a name and a source, such as Geist, whose themes are Geist Dark and Geist Light. Each family has a folder under `palettes/`, holding one palette per theme.
_Avoid_: Theme, for the set

**Port**:
Another project's theme for one app that a palette takes in place of generating that app's theme, swapping only the colours its recolour table lists. Ayu Dark Contrast's Zed and VS Code themes are ports of ayu's own.

**Selection**:
The background behind the active text selection in an editor.

**Inactive selection**:
The background behind a selection in a list or editor that doesn't have focus.

**Whitespace mark**:
A faint glyph an editor draws to show a space or tab.
_Avoid_: Invisible, whitespace dot

**Indent guide**:
A faint vertical line an editor draws at each indent level.
_Avoid_: Indent line

**Syntax role**:
A kind of source text that the palette gives its own colour, such as a comment, keyword or string.

**Tint**:
A status, accent, or magenta colour composited over the background at the appearance's tint alpha. A surface that takes that colour's meaning, such as a diff line or a badge, uses it as its fill, so every syntax role keeps 4.5:1 on it.
