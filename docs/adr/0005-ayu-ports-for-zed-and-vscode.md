# Ayu's Zed and VS Code themes are ports

Ayu Dark Contrast is meant to look like ayu with only the background, text, and greys changed. The colours alone don't get there: every family shares `build.py`'s mapping of syntax roles to scopes and captures, which was written for Geist, so ayu's colours landed on the wrong text. In Zed, Markdown links came out cyan where ayu has orange italic link text and green URLs.

So in Zed and VS Code, where ayu has a theme of its own (Zed's built-in Ayu Dark and ayu's VS Code extension, both MIT), the palette takes that theme as a port and swaps only the colours its recolour table lists: backgrounds, text, and greys, plus the find, selection, hint, and error colours that the contrast gate fails. The other apps either have no popular ayu theme or theme few roles, so they keep the generated mapping.

The ports are copies under `palettes/ayu/ports/`, so ayu's later changes reach them only when someone copies them again, and each port's licence ships next to its output. The contrast gate checks every colour a port draws code in against its editor background, current line, selection, and find matches.
