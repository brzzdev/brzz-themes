#!/usr/bin/env python3
"""Generate every app's theme files from the family folders in palettes/."""

import json
import math
import plistlib
import textwrap
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
AUTHOR = "brzzdev"
FAMILY_FILE = "family.toml"
IDENTIFIER_PREFIX = "dev.brzz"
PACKAGE = "brzz-themes"
PACKAGE_NAME = "Brzz Themes"
# Backgrounds a port draws code over, besides its editor background and Zed's selection.
PORT_GROUNDS = {
    "vscode": [
        "editor.findMatchBackground",
        "editor.findMatchHighlightBackground",
        "editor.lineHighlightBackground",
        "editor.selectionBackground",
    ],
    "zed": [
        "editor.active_line.background",
        "search.active_match_background",
        "search.match_background",
    ],
}
REPOSITORY_URL = "https://github.com/brzzdev/brzz-themes"
SCROLLBAR_ALPHA = "50"
SCROLLBAR_HOVER_ALPHA = "80"
# Fills behind syntax text: see docs/adr/0003-tinted-fills-behind-syntax.md.
TINT_ALPHAS = {"dark": "33", "light": "1a"}
TRANSPARENT = "#00000000"
ZED_SCHEMA = "https://zed.dev/schema/themes/v0.2.0.json"
# The players between yours and the agent's, which Zed keeps last.
ZED_COLLABORATORS = 6
OPAQUE_HEX_LENGTH = len("#rrggbb")
ANSI_NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
# libm differs by an ulp between macOS and Linux, so unrounded output drifts across platforms.
OKLCH_DECIMALS = 6
CARD_CELL_WIDTH = 210
CARD_COLUMNS = 4
CARD_FONT = "ui-monospace, SFMono-Regular, Menlo, monospace"
CARD_HEADING_BASELINE = 20
CARD_HEX_BASELINE = 29
CARD_LABEL_GAP = 10
CARD_PADDING = 24
CARD_ROLE_BASELINE = 13
CARD_ROW_HEIGHT = 44
CARD_SWATCH = 32

MINIMUM_CONTRAST = 4.5
SLACK_BADGE_TEXT = "#ffffff"
# Each text colour reaches the minimum on the ground it's paired with.
TEXT_PAIRS = [
    ("ansi.normal.0", "ui.find_active_border"),
    ("status.hint", "ui.element"),
    ("status.hint", "ui.hover"),
    ("status.predictive", "ui.hover"),
    (SLACK_BADGE_TEXT, "ui.error_fill"),
    ("ui.accent", "ui.panel"),
    ("ui.foreground", "tint.accent"),
    ("ui.line_number", "ui.background"),
    ("ui.quiet", "ui.background"),
    ("ui.quiet", "ui.element"),
    ("ui.quiet", "ui.panel"),
]
# Terminal text: every ANSI colour but normal black, which programs use as a fill.
ANSI_TEXT_PATHS = [f"ansi.bright.{index}" for index in range(len(ANSI_NAMES))] + [
    f"ansi.normal.{index}" for index in range(1, len(ANSI_NAMES))
]
# Grounds every status colour reaches the minimum on.
STATUS_GROUNDS = ["background", "panel"]
# Every syntax role reaches the minimum on these, and on every tint.
SYNTAX_GROUNDS = [
    "background",
    "element",
    "find",
    "find_active",
    "highlight",
    "hover",
    "panel",
    "selection",
]
# Non-syntax colours held to the syntax grounds: drawn among code, or as badge text on a tint.
SYNTAX_LIKE_PATHS = [
    "ansi.bright.1",
    "ansi.normal.2",
    "ansi.normal.3",
    "ansi.normal.4",
    "ansi.normal.5",
    "ansi.normal.6",
    "status.hint",
    "status.predictive",
    "status.unreachable",
]
# The colours a palette's `tint` group composites over its background.
TINTS = {
    "accent": "ui.accent",
    "conflict": "status.conflict",
    "created": "status.created",
    "deleted": "status.deleted",
    "error": "status.error",
    "hidden": "status.hidden",
    "hint": "status.hint",
    "ignored": "status.ignored",
    "info": "status.info",
    "magenta": "ansi.normal.5",
    "modified": "status.modified",
    "predictive": "status.predictive",
    "renamed": "status.renamed",
    "success": "status.success",
    "unreachable": "status.unreachable",
    "warning": "status.warning",
}

type Palette = dict[str, Any]
type Family = dict[str, Any]
type Json = dict[str, Json] | list[Json] | str | int | float | bool | None

CLAUDE_CODE_COLOURS = {
    "autoAccept": "ansi.normal.5",
    "autoAcceptShimmer": "ansi.bright.5",
    "background": "status.info",
    "bashBorder": "ansi.bright.1",
    "bashMessageBackgroundColor": "ui.element",
    "blue_FOR_SUBAGENTS_ONLY": "ansi.normal.4",
    "briefLabelClaude": "ui.accent",
    "briefLabelYou": "ui.muted",
    "chromeYellow": "status.warning",
    "claude": "ui.accent",
    "claudeShimmer": "ui.accent_strong",
    "composerSidebarBackground": "ui.panel",
    "cyan_FOR_SUBAGENTS_ONLY": "ansi.normal.6",
    "effortUltra": "ansi.bright.5",
    "error": "status.error",
    "fastMode": "ansi.normal.3",
    "fastModeShimmer": "ansi.bright.3",
    "green_FOR_SUBAGENTS_ONLY": "ansi.normal.2",
    "ide": "status.info",
    "inactive": "ui.muted",
    "inactiveShimmer": "ui.foreground",
    "inverseText": "ui.background",
    "memoryBackgroundColor": "tint.info",
    "merged": "ansi.normal.5",
    "orange_FOR_SUBAGENTS_ONLY": "ansi.normal.3",
    "permission": "status.info",
    "permissionShimmer": "ansi.bright.4",
    "pink_FOR_SUBAGENTS_ONLY": "ansi.bright.1",
    "planMode": "ansi.normal.6",
    "professionalBlue": "status.info",
    "promptBorder": "ui.quiet",
    "promptBorderShimmer": "ui.muted",
    "purple_FOR_SUBAGENTS_ONLY": "ansi.normal.5",
    "rainbow_blue": "ansi.normal.6",
    "rainbow_blue_shimmer": "ansi.bright.6",
    "rainbow_green": "ansi.normal.2",
    "rainbow_green_shimmer": "ansi.bright.2",
    "rainbow_indigo": "ansi.normal.4",
    "rainbow_indigo_shimmer": "ansi.bright.4",
    "rainbow_orange": "ansi.normal.3",
    "rainbow_orange_shimmer": "ansi.bright.3",
    "rainbow_red": "ansi.normal.1",
    "rainbow_red_shimmer": "ansi.bright.1",
    "rainbow_violet": "ansi.normal.5",
    "rainbow_violet_shimmer": "ansi.bright.5",
    "rainbow_yellow": "ansi.bright.3",
    "rainbow_yellow_shimmer": "ansi.bright.3",
    "rate_limit_empty": "ui.element",
    "rate_limit_fill": "ui.accent",
    "red_FOR_SUBAGENTS_ONLY": "ansi.normal.1",
    "remember": "ansi.bright.5",
    "selectionBg": "ui.selection",
    "skill": "ansi.normal.5",
    "subtle": "ui.quiet",
    "success": "status.success",
    "suggestion": "status.info",
    "text": "ui.foreground",
    "userMessageBackground": "ui.element",
    "userMessageBackgroundHover": "ui.hover",
    "warning": "status.warning",
    "warningShimmer": "ansi.bright.3",
    "yellow_FOR_SUBAGENTS_ONLY": "ansi.bright.3",
}
# Diff fills at the appearance's tint whatever the palette's, since Claude Code draws diff code in its own highlighter: see docs/adr/0003-tinted-fills-behind-syntax.md.
CLAUDE_CODE_DIFF_FILLS = {
    "diffAdded": ("status.created", 1),
    "diffAddedDimmed": ("status.created", 0.5),
    "diffAddedWord": ("status.created", 2.25),
    "diffRemoved": ("status.deleted", 1),
    "diffRemovedDimmed": ("status.deleted", 0.5),
    "diffRemovedWord": ("status.deleted", 2.25),
}
CLAUDE_CODE_TEXT_PAIRS = [
    ("bashBorder", "bashMessageBackgroundColor"),
    ("error", "userMessageBackgroundHover"),
    ("inactive", "userMessageBackground"),
    ("inactive", "userMessageBackgroundHover"),
    ("remember", "memoryBackgroundColor"),
    ("success", "userMessageBackground"),
    ("suggestion", "userMessageBackground"),
    ("text", "bashMessageBackgroundColor"),
    ("text", "composerSidebarBackground"),
    ("text", "diffAdded"),
    ("text", "diffAddedDimmed"),
    ("text", "diffRemoved"),
    ("text", "diffRemovedDimmed"),
    ("text", "memoryBackgroundColor"),
    ("text", "userMessageBackground"),
    ("text", "userMessageBackgroundHover"),
]
# The badge fills Claude Code draws `inverseText` on.
CLAUDE_CODE_BADGE_GROUNDS = [
    "blue_FOR_SUBAGENTS_ONLY",
    "claude",
    "cyan_FOR_SUBAGENTS_ONLY",
    "error",
    "green_FOR_SUBAGENTS_ONLY",
    "orange_FOR_SUBAGENTS_ONLY",
    "permission",
    "pink_FOR_SUBAGENTS_ONLY",
    "purple_FOR_SUBAGENTS_ONLY",
    "red_FOR_SUBAGENTS_ONLY",
    "success",
    "warning",
    "yellow_FOR_SUBAGENTS_ONLY",
]
# Fills, and text drawn on a colour; every other token is text on the background.
CLAUDE_CODE_NOT_TEXT_ON_BACKGROUND = {
    "bashMessageBackgroundColor",
    "composerSidebarBackground",
    "diffAdded",
    "diffAddedDimmed",
    "diffAddedWord",
    "diffRemoved",
    "diffRemovedDimmed",
    "diffRemovedWord",
    "inverseText",
    "memoryBackgroundColor",
    "rate_limit_empty",
    "rate_limit_fill",
    "selectionBg",
    "userMessageBackground",
    "userMessageBackgroundHover",
}

# Herdr's own alpha for the `blocked` fill behind its "Needs you" badge; no theme key sets it.
HERDR_APP_BADGE_ALPHA = "26"
HERDR_APP_COLOURS = {
    "accent": "ui.accent",
    "accent_foreground": "ui.background",
    "blocked": "ansi.bright.1",
    "border": "ui.border",
    "canvas": "ui.panel",
    "chrome": "ui.panel",
    "dim": "ui.quiet",
    "done": "status.success",
    "foreground": "ui.foreground",
    "hover": "ui.hover",
    "idle": "ui.quiet",
    "input": "ui.border_strong",
    "muted": "ui.muted",
    "popover": "ui.panel",
    "raised": "ui.element",
    "ring": "ui.accent",
    "selected": "ui.selection",
    "solid": "ui.foreground",
    "solid_foreground": "ui.background",
    "surface": "ui.panel",
    "unknown": "ui.quiet",
    "working": "status.warning",
}
# Herdr text colours and a ground Herdr draws each on, by Herdr's colour names.
HERDR_APP_TEXT_PAIRS = [
    ("accent_foreground", "accent"),
    ("blocked", "chrome"),
    ("done", "chrome"),
    ("idle", "chrome"),
    ("unknown", "chrome"),
    ("working", "chrome"),
]

# Dark takes the unsuffixed table, the one herdr keeps when auto_switch is off.
HERDR_TABLES = {"dark": "theme.custom", "light": "theme.custom.light"}

FONT_STYLES = ("bold", "italic")
# Markdown headings: the role a palette's `syntax.heading` names, or plain bold text.
HEADING = "heading"

ZED_SYNTAX = {
    "attribute": ("syntax.attribute", None),
    "boolean": ("syntax.constant", None),
    "comment": ("syntax.comment", "italic"),
    "comment.doc": ("syntax.comment", "italic"),
    "concept": ("syntax.type", None),
    "constant": ("syntax.constant", None),
    "constructor": ("syntax.type", None),
    "diff.delta": ("ansi.normal.4", None),
    "diff.minus": ("ansi.bright.1", None),
    "diff.plus": ("ansi.normal.2", None),
    "emphasis": ("syntax.plain", "italic"),
    "emphasis.strong": ("syntax.plain", "bold"),
    "enum": ("syntax.type", None),
    "function": ("syntax.function", None),
    "function.builtin": ("syntax.function_system", None),
    "function.macro": ("syntax.attribute", None),
    "keyword": ("syntax.keyword", None),
    "label": ("syntax.attribute", None),
    "lifetime": ("syntax.type_parameter", None),
    "link_text": ("syntax.link", None),
    "link_uri": ("syntax.link", None),
    "markup.heading": (HEADING, None),
    "module": ("syntax.namespace", None),
    "namespace": ("syntax.namespace", None),
    "number": ("syntax.number", None),
    "operator": ("syntax.punctuation", None),
    "preproc": ("syntax.attribute", None),
    "property": ("syntax.variable", None),
    "punctuation": ("syntax.punctuation", None),
    "selector": ("syntax.attribute", None),
    "string": ("syntax.string", None),
    "string.escape": ("syntax.number", None),
    "string.regex": ("syntax.regex", None),
    "string.special": ("syntax.string", None),
    "string.special.symbol": ("syntax.constant", None),
    "tag": ("syntax.tag", None),
    "text.literal": ("syntax.literal", None),
    "title": (HEADING, None),
    "type": ("syntax.type", None),
    "type.builtin": ("syntax.type_system", None),
    "type.parameter": ("syntax.type_parameter", None),
    "variable": ("syntax.variable", None),
    "variable.builtin": ("syntax.keyword", None),
    "variable.parameter": ("syntax.variable", None),
    "variable.special": ("syntax.keyword", None),
    "variant": ("syntax.constant", None),
}

NETNEWSWIRE_VARIABLES = {
    "accent": "ui.accent",
    "background": "ui.background",
    "border": "ui.border",
    "border-variant": "ui.border_variant",
    "code-background": "ui.element",
    "find": "ui.find",
    "foreground": "ui.foreground",
    "link": "ui.accent_strong",
    "muted": "ui.muted",
    "panel": "ui.panel",
    "quiet": "ui.quiet",
    "selection": "ui.selection",
}

XCODE_OVERRIDES = {
    "codeFoldingRibbon": "ui.hover",
    "comment": "syntax.comment",
    "commentEmphasized": "syntax.comment_emphasized",
    "consoleBackground": "ui.background",
    "currentLineHighlight": "ui.hover",
    "debugger": "ui.accent",
    "diffAddition": "status.created",
    "diffDeletion": "status.deleted",
    "insertionPointColor": "ui.cursor",
    "invisibles": "ui.invisible",
    "keyword": "syntax.keyword",
    "keyword.attribute": "syntax.attribute",
    "link": "syntax.link",
    "markdown": "syntax.literal",
    "markdownEmphasized": "syntax.plain",
    "memberDeclaration": "syntax.function",
    "number": "syntax.number",
    "number.character": "syntax.number",
    "otherMember": "syntax.variable",
    "otherMember.constant": "syntax.constant",
    "otherMember.function": "syntax.function_system",
    "otherMember.variable": "syntax.variable",
    "otherType": "syntax.type_system",
    "otherType.class": "syntax.type_system",
    "otherType.type": "syntax.type_system",
    "plainText": "syntax.plain",
    "preprocessor": "syntax.attribute",
    "preprocessor.macro": "syntax.attribute",
    "preprocessor.macroSystem": "syntax.attribute",
    "projectMember": "syntax.variable",
    "projectMember.constant": "syntax.constant",
    "projectMember.function": "syntax.function",
    "projectMember.variable": "syntax.variable",
    "projectType": "syntax.type",
    "projectType.class": "syntax.type",
    "projectType.type": "syntax.type",
    "scopeGuides": "ui.indent",
    "selectedTextBackgroundColor": "ui.selection",
    "string": "syntax.string",
    "string.regex": "syntax.regex",
    "typeDeclaration": "syntax.type",
}


# The selection colour at this alpha keeps syntax at or above its contrast on the selection.
VSCODE_RANGE_ALPHA = "60"
# VS Code draws decorations over the selection and the cursor line, so their fills stay
# translucent and land on their checked colour over the cursor line, fainter elsewhere.
VSCODE_DECORATION_ALPHA = "80"
VSCODE_UI_THEMES = {"dark": "vs-dark", "light": "vs"}

# Diff and patch files, in the ANSI colours Zed's diff captures use.
VSCODE_DIFF_TOKENS = [
    (["markup.changed", "punctuation.definition.changed.diff"], "ansi.normal.4"),
    (["markup.deleted", "punctuation.definition.deleted.diff"], "ansi.bright.1"),
    (["markup.inserted", "punctuation.definition.inserted.diff"], "ansi.normal.2"),
]
# Markdown headings and their `#` markers, which the `punctuation` rule would otherwise claim.
VSCODE_HEADING_SCOPES = ["markup.heading", "punctuation.definition.heading"]
VSCODE_TOKENS = [
    (
        [
            "entity.name.function.decorator",
            "entity.name.function.preprocessor",
            "entity.other.attribute-name",
            "keyword.control.directive",
            "meta.decorator",
            "meta.preprocessor",
            "punctuation.decorator",
            "storage.type.annotation",
        ],
        "attribute",
        None,
    ),
    (["comment", "punctuation.definition.comment"], "comment", "italic"),
    (
        [
            "constant.language",
            "meta.diff",
            "punctuation.definition.from-file.diff",
            "punctuation.definition.to-file.diff",
            "support.constant",
            "variable.other.enummember",
        ],
        "constant",
        None,
    ),
    (["entity.name.function", "meta.function-call.generic"], "function", None),
    (["support.function"], "function_system", None),
    (
        [
            "keyword",
            "keyword.operator.alignas",
            "keyword.operator.alignof",
            "keyword.operator.cast",
            "keyword.operator.expression",
            "keyword.operator.instanceof",
            "keyword.operator.logical.python",
            "keyword.operator.new",
            "keyword.operator.noexcept",
            "keyword.operator.sizeof",
            "keyword.operator.type.asserts",
            "keyword.operator.typeid",
            "keyword.operator.wordlike",
            "storage",
            "variable.language",
        ],
        "keyword",
        None,
    ),
    (["markup.underline.link"], "link", None),
    (["markup.fenced_code", "markup.inline.raw"], "literal", None),
    (["entity.name.namespace", "entity.name.type.module"], "namespace", None),
    (["constant.character", "constant.numeric"], "number", None),
    (["markup.bold", "markup.heading"], "plain", "bold"),
    (["markup.italic"], "plain", "italic"),
    (["keyword.operator", "meta.brace", "punctuation"], "punctuation", None),
    (["string.regexp"], "regex", None),
    (["punctuation.definition.string", "string"], "string", None),
    (["entity.name.tag"], "tag", None),
    (
        ["entity.name.class", "entity.name.type", "entity.other.inherited-class"],
        "type",
        None,
    ),
    (["entity.name.type.parameter"], "type_parameter", None),
    (["support.class", "support.type"], "type_system", None),
    (
        [
            "meta.definition.variable",
            "support.type.property-name",
            "support.variable",
            "variable",
        ],
        "variable",
        None,
    ),
]

VSCODE_SEMANTIC = {
    "class": "type",
    "class.defaultLibrary": "type_system",
    "decorator": "attribute",
    "enum": "type",
    "enum.defaultLibrary": "type_system",
    "enumMember": "constant",
    "function": "function",
    "function.defaultLibrary": "function_system",
    "interface": "type",
    "interface.defaultLibrary": "type_system",
    "macro": "attribute",
    "method": "function",
    "method.defaultLibrary": "function_system",
    "namespace": "namespace",
    "parameter": "variable",
    "property": "variable",
    "struct": "type",
    "struct.defaultLibrary": "type_system",
    "type": "type",
    "type.defaultLibrary": "type_system",
    "typeParameter": "type_parameter",
    "variable": "variable",
}


def slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def palette_colour(palette: Palette, path: str) -> str:
    if path.startswith("#"):
        return path
    group, key, *index = path.split(".")
    value = palette[group][key]
    return value[int(index[0])] if index else value


def heading_look(palette: Palette) -> tuple[str, str | None]:
    syntax, role = palette["syntax"], palette["heading"]
    if role is None:
        return syntax["plain"], "bold"
    return syntax[role], palette["syntax_style"].get(role)


def syntax_look(
    palette: Palette, path: str, style: str | None
) -> tuple[str, str | None]:
    if path == HEADING:
        return heading_look(palette)
    group, _, role = path.partition(".")
    if group == "syntax":
        style = style or palette["syntax_style"].get(role)
    return palette_colour(palette, path), style


def zed_syntax_style(colour: str, style: str | None) -> dict[str, Any]:
    if style == "bold":
        return {"color": colour, "font_weight": 700}
    if style == "italic":
        return {"color": colour, "font_style": "italic"}
    return {"color": colour}


def zed_style(palette: Palette) -> dict[str, Any]:
    ui, ansi = palette["ui"], palette["ansi"]
    status, tints = palette["status"], palette["tint"]
    thumb, hover_thumb = scrollbar_thumbs(palette)
    style = {
        "accents": ui["accents"],
        "background": ui["panel"],
        "border": ui["border"],
        "border.disabled": ui["border"],
        "border.focused": ui["accent"],
        "border.selected": ui["accent"],
        "border.transparent": TRANSPARENT,
        "border.variant": ui["border_variant"],
        "debugger.accent": status["error"],
        "drop_target.background": ui["selection_overlay"],
        "drop_target.border": ui["foreground"],
        "editor.active_line.background": ui["hover"],
        "editor.active_line_number": ui["foreground"],
        "editor.active_wrap_guide": ui["border"],
        "editor.background": ui["background"],
        "editor.debugger_active_line.background": tints["accent"],
        "editor.diff_hunk.added.background": tints["created"],
        "editor.diff_hunk.deleted.background": tints["deleted"],
        "editor.document_highlight.bracket_background": ui["highlight"],
        "editor.document_highlight.read_background": ui["highlight"],
        "editor.document_highlight.write_background": ui["highlight"],
        "editor.foreground": ui["foreground"],
        "editor.gutter.background": ui["background"],
        "editor.highlighted_line.background": ui["hover"],
        "editor.hover_line_number": ui["foreground"],
        "editor.indent_guide": ui["indent"],
        "editor.indent_guide_active": ui["indent_active"],
        "editor.invisible": ui["invisible"],
        "editor.line_number": ui["line_number"],
        "editor.subheader.background": ui["panel"],
        "editor.wrap_guide": ui["border"],
        "element.active": ui["selection"],
        "element.background": ui["element"],
        "element.disabled": ui["element"],
        "element.hover": ui["hover"],
        "element.selected": ui["selection"],
        "elevated_surface.background": ui["background"],
        "ghost_element.active": ui["selection"],
        "ghost_element.background": TRANSPARENT,
        "ghost_element.disabled": ui["element"],
        "ghost_element.hover": ui["hover"],
        "ghost_element.selected": ui["element"],
        # The inlay hint pill, opaque like the other editors' so hint text keeps 4.5:1.
        "hint.background": ui["element"],
        "icon": ui["foreground"],
        "icon.accent": ui["accent"],
        "icon.disabled": ui["quiet"],
        "icon.muted": ui["muted"],
        "icon.placeholder": ui["quiet"],
        "link_text.hover": ui["accent_strong"],
        "pane.focused_border": ui["accent"],
        "pane_group.border": ui["border"],
        "panel.background": ui["panel"],
        "panel.focused_border": ui["accent"],
        "panel.indent_guide": ui["indent"],
        "panel.indent_guide_active": ui["indent_active"],
        "panel.indent_guide_hover": ui["indent_active"],
        "players": zed_players(palette),
        "scrollbar.thumb.active_background": hover_thumb,
        "scrollbar.thumb.background": thumb,
        "scrollbar.thumb.hover_background": hover_thumb,
        "scrollbar.track.background": TRANSPARENT,
        "scrollbar.track.border": TRANSPARENT,
        "search.active_match_background": ui["find_active"],
        "search.match_background": ui["find"],
        "status_bar.background": ui["panel"],
        "surface.background": ui["panel"],
        "syntax": {
            token: zed_syntax_style(*syntax_look(palette, path, font))
            for token, (path, font) in ZED_SYNTAX.items()
        },
        "tab.active_background": ui["background"],
        "tab.inactive_background": ui["panel"],
        "tab_bar.background": ui["panel"],
        "terminal.ansi.background": ui["background"],
        "terminal.ansi.dim_white": ui["quiet"],
        "terminal.background": ui["background"],
        "terminal.bright_foreground": ansi["bright"][7],
        "terminal.dim_foreground": ui["quiet"],
        "terminal.foreground": ui["foreground"],
        "text": ui["foreground"],
        "text.accent": ui["accent_strong"],
        "text.disabled": ui["quiet"],
        "text.muted": ui["muted"],
        "text.placeholder": ui["quiet"],
        "title_bar.background": ui["panel"],
        "title_bar.inactive_background": ui["panel"],
        "toolbar.background": ui["background"],
        "version_control.conflict": status["conflict"],
        "version_control.conflict_marker.ours": tints["created"],
        "version_control.conflict_marker.theirs": tints["info"],
        "version_control.word_added": tints["created"],
        "version_control.word_deleted": tints["deleted"],
    }
    for name, colour in status.items():
        style[name] = colour
        style.setdefault(f"{name}.background", tints[name])
        style[f"{name}.border"] = colour
    for index, name in enumerate(ANSI_NAMES):
        style[f"terminal.ansi.{name}"] = ansi["normal"][index]
        style[f"terminal.ansi.bright_{name}"] = ansi["bright"][index]
        style.setdefault(f"terminal.ansi.dim_{name}", ansi["normal"][index])
    return dict(sorted(style.items()))


def zed_players(palette: Palette) -> list[dict[str, str]]:
    ui = palette["ui"]
    *others, agent = ui["accents"]
    collaborators = [others[i % len(others)] for i in range(ZED_COLLABORATORS)]
    return [
        {"background": cursor, "cursor": cursor, "selection": ui["selection_overlay"]}
        for cursor in [ui["cursor"], *collaborators, agent]
    ]


def zed_family(family: Family) -> dict[str, Any]:
    return {
        "$schema": ZED_SCHEMA,
        "name": family["name"],
        "author": AUTHOR,
        "themes": [
            {
                "name": p["name"],
                "appearance": p["appearance"],
                "style": port_theme(p, "zed") if "zed" in p["ports"] else zed_style(p),
            }
            for p in family["palettes"]
        ],
    }


def port_theme(palette: Palette, app: str) -> dict[str, Any]:
    port = palette["ports"][app]
    theme = recoloured(port["source"], palette, port["recolour"])
    if colors := port.get("colors"):
        theme["colors"] |= {
            key: palette_colour(palette, path) for key, path in colors.items()
        }
    return theme


def recoloured(value: Json, palette: Palette, table: dict[str, str]) -> Json:
    if isinstance(value, dict):
        return {key: recoloured(v, palette, table) for key, v in value.items()}
    if isinstance(value, list):
        return [recoloured(v, palette, table) for v in value]
    if not isinstance(value, str) or not value.startswith("#"):
        return value
    colour = value.lower()
    if colour in table:
        return palette_colour(palette, table[colour])
    base, alpha = colour[:OPAQUE_HEX_LENGTH], colour[OPAQUE_HEX_LENGTH:]
    if base in table:
        return palette_colour(palette, table[base]) + alpha
    return value


def ghostty(palette: Palette) -> str:
    ui, ansi = palette["ui"], palette["ansi"]
    lines = [
        f"background = {ui['background']}",
        f"foreground = {ui['foreground']}",
        f"cursor-color = {ui['cursor']}",
        f"cursor-text = {ui['background']}",
        f"selection-background = {ui['selection']}",
        f"selection-foreground = {ui['foreground']}",
        f"search-background = {ui['find']}",
        f"search-foreground = {ui['foreground']}",
        f"search-selected-background = {ui['find_active_border']}",
        f"search-selected-foreground = {ansi['normal'][0]}",
        f"split-divider-color = {ui['border']}",
        "",
    ]
    colours = ansi["normal"] + ansi["bright"]
    lines += [f"palette = {index}={colour}" for index, colour in enumerate(colours)]
    return "\n".join(lines) + "\n"


def herdr_colours(palette: Palette) -> dict[str, str]:
    ui, status = palette["ui"], palette["status"]
    normal = dict(zip(ANSI_NAMES, palette["ansi"]["normal"]))
    bright = dict(zip(ANSI_NAMES, palette["ansi"]["bright"]))
    return {
        "accent": ui["accent"],
        "active_row_bg": ui["element"],
        "blue": status["info"],
        "green": status["success"],
        "mauve": normal["magenta"],
        "overlay0": ui["quiet"],
        "overlay1": ui["muted"],
        "panel_bg": ui["panel"],
        "peach": bright["yellow"],
        "red": status["error"],
        "selection_bg": ui["selection"],
        "sidebar_bg": ui["background"],
        "subtext0": ui["muted"],
        "surface0": ui["element"],
        "surface1": ui["selection"],
        "surface_dim": ui["hover"],
        "teal": normal["cyan"],
        "text": ui["foreground"],
        "yellow": status["warning"],
    }


def herdr_table(header: str, colours: dict[str, str]) -> str:
    rows = [f'{token} = "{colour}"' for token, colour in colours.items()]
    return "\n".join([f"[{header}]", *rows]) + "\n"


def herdr(palettes: list[Palette]) -> str:
    tables = [
        herdr_table(HERDR_TABLES[p["appearance"]], herdr_colours(p)) for p in palettes
    ]
    has_both_appearances = {p["appearance"] for p in palettes} == HERDR_TABLES.keys()
    auto_switch = "true" if has_both_appearances else "false"
    return f"[theme]\nauto_switch = {auto_switch}\n\n" + "\n".join(tables)


def claude_code_theme(palette: Palette) -> dict[str, Any]:
    colours = {
        token: palette_colour(palette, path)
        for token, path in CLAUDE_CODE_COLOURS.items()
    }
    appearance_tint = palette | {"tint_alpha": TINT_ALPHAS[palette["appearance"]]}
    for token, (status, weight) in CLAUDE_CODE_DIFF_FILLS.items():
        colours[token] = tint(appearance_tint, palette_colour(palette, status), weight)
    return {
        "name": palette["name"],
        "base": palette["appearance"],
        "overrides": dict(sorted(colours.items())),
    }


def claude_code_contrast_pairs(palette: Palette) -> list[tuple[str, str, str]]:
    colours = claude_code_theme(palette)["overrides"]
    text_pairs = CLAUDE_CODE_TEXT_PAIRS + [
        ("inverseText", ground) for ground in CLAUDE_CODE_BADGE_GROUNDS
    ]
    pairs = [
        (f"Claude Code's {text} on {ground}", colours[text], colours[ground])
        for text, ground in text_pairs
    ]
    background = palette["ui"]["background"]
    pairs += [
        (f"Claude Code's {token} on the background", colour, background)
        for token, colour in colours.items()
        if token not in CLAUDE_CODE_NOT_TEXT_ON_BACKGROUND
    ]
    return pairs


def herdr_app_theme(palette: Palette) -> dict[str, Any]:
    ui, ansi = palette["ui"], palette["ansi"]
    return {
        "background": ui["background"],
        "foreground": ui["foreground"],
        "selection": ui["selection"],
        "cursor": ui["cursor"],
        "ansi": ansi["normal"] + ansi["bright"],
        "colors": {
            name: palette_colour(palette, path)
            for name, path in HERDR_APP_COLOURS.items()
        },
    }


def herdr_app_contrast_pairs(palette: Palette) -> list[tuple[str, str, str]]:
    theme = herdr_app_theme(palette)
    colours = theme["colors"]
    pairs = [
        (f"Herdr's {text} on {ground}", colours[text], colours[ground])
        for text, ground in HERDR_APP_TEXT_PAIRS
    ]
    blocked = colours["blocked"]
    badge = opaque(blocked + HERDR_APP_BADGE_ALPHA, theme["background"])
    return [*pairs, ("Herdr's blocked on its Needs you badge", blocked, badge)]


def linear_rgb(hex_colour: str) -> tuple[float, float, float]:
    def linear(channel: str) -> float:
        c = int(channel, 16) / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linear(hex_colour[i : i + 2]) for i in (1, 3, 5))
    return r, g, b


def oklch(hex_colour: str) -> tuple[float, float, float]:
    r, g, b = linear_rgb(hex_colour)
    lms = (
        0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b,
        0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b,
        0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b,
    )
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in lms)
    lightness = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    b = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    return lightness, math.hypot(a, b), math.atan2(b, a) % math.tau


def xcode_colour(hex_colour: str) -> dict[str, Any]:
    lightness, chroma, hue = (round(v, OKLCH_DECIMALS) for v in oklch(hex_colour))
    if chroma == 0:
        # A grey's hue is noise from cancelling terms and can straddle a rounding boundary.
        hue = 0.0
    return {
        "wrapped": {
            "oklch": {
                "chroma": {"kind": {"exact": {"_0": chroma}}},
                "gamut": {"P3": {}},
                "hue": {"radiansValue": hue},
                "lightness": {"kind": {"exact": {"_0": lightness}}},
                "opacity": 1,
            },
        },
    }


def xcode_recipe(palette: Palette) -> dict[str, Any]:
    overrides: list[Any] = []
    for token, path in XCODE_OVERRIDES.items():
        overrides += [
            token,
            {"color": {"_0": xcode_colour(palette_colour(palette, path))}},
        ]
    return {
        "name": palette["name"],
        "recipe": {
            "background": {
                "customColor": {"_0": xcode_colour(palette["ui"]["background"])}
            },
            "colorScheme": {palette["appearance"]: {}},
            "palette": {
                "colorGranularity": "expanded",
                "colorOverrides": overrides,
                "primary": {
                    "custom": {"_0": xcode_colour(palette["ansi"]["normal"][5])}
                },
                "secondary": {
                    "custom": {"_0": xcode_colour(palette["ui"]["background"])}
                },
            },
        },
    }


def netnewswire_variables(palette: Palette) -> str:
    declarations = {"color-scheme": palette["appearance"]} | {
        f"--{name}": palette_colour(palette, path)
        for name, path in NETNEWSWIRE_VARIABLES.items()
    }
    body = "".join(f"\t{key}: {value};\n" for key, value in declarations.items())
    return f":root {{\n{body}}}\n"


def netnewswire_stylesheet(palettes: list[Palette]) -> str:
    default, *others = sorted(palettes, key=lambda p: p["appearance"] != "dark")
    blocks = [netnewswire_variables(default)]
    blocks += [
        f"@media (prefers-color-scheme: {p['appearance']}) {{\n"
        + textwrap.indent(netnewswire_variables(p), "\t")
        + "}\n"
        for p in others
    ]
    rules = (ROOT / "templates" / "netnewswire.css").read_text()
    return "\n".join([*blocks, rules])


def netnewswire_info(family: Family) -> str:
    info = {
        "CreatorHomePage": REPOSITORY_URL,
        "CreatorName": AUTHOR,
        "Name": family["name"],
        "ThemeIdentifier": f"{IDENTIFIER_PREFIX}.{family['identifier']}.netnewswire",
        "Version": 1,
    }
    return plistlib.dumps(info).decode()


def slack(palette: Palette) -> str:
    ui = palette["ui"]
    colours = [
        ui["background"],
        ui["selection"],
        palette["status"]["success"],
        ui["error_fill"],
    ]
    return ",".join(colours).upper() + "\n"


def vscode_colours(palette: Palette) -> dict[str, str]:
    ui, status, syntax = palette["ui"], palette["status"], palette["syntax"]
    ansi, tints = palette["ansi"], palette["tint"]
    thumb, hover_thumb = scrollbar_thumbs(palette)

    range_highlight = ui["selection"] + VSCODE_RANGE_ALPHA

    def decoration(colour: str) -> str:
        return translucent(colour, ui["hover"], VSCODE_DECORATION_ALPHA)

    colours = {
        "activityBar.background": ui["panel"],
        "activityBar.border": ui["border"],
        "activityBar.foreground": ui["foreground"],
        "activityBar.inactiveForeground": ui["quiet"],
        "activityBarBadge.background": ui["accent"],
        "activityBarBadge.foreground": ui["background"],
        "activityBarTop.foreground": ui["foreground"],
        "activityBarTop.inactiveForeground": ui["quiet"],
        "activityErrorBadge.background": status["error"],
        "activityErrorBadge.foreground": ui["background"],
        "activityWarningBadge.background": status["warning"],
        "activityWarningBadge.foreground": ui["background"],
        "badge.background": ui["element"],
        "badge.foreground": ui["foreground"],
        "button.background": ui["accent"],
        "button.foreground": ui["background"],
        "button.hoverBackground": ui["accent_strong"],
        "commandCenter.activeBackground": ui["element"],
        "commandCenter.background": ui["hover"],
        "debugExceptionWidget.background": tints["error"],
        "debugExceptionWidget.border": status["error"],
        "debugIcon.breakpointCurrentStackframeForeground": status["warning"],
        "debugIcon.breakpointDisabledForeground": ui["quiet"],
        "debugIcon.breakpointForeground": status["error"],
        "debugIcon.breakpointStackframeForeground": status["success"],
        "debugIcon.breakpointUnverifiedForeground": ui["quiet"],
        "debugIcon.continueForeground": ui["accent"],
        "debugIcon.disconnectForeground": status["error"],
        "debugIcon.pauseForeground": ui["accent"],
        "debugIcon.restartForeground": status["success"],
        "debugIcon.startForeground": status["success"],
        "debugIcon.stepBackForeground": ui["accent"],
        "debugIcon.stepIntoForeground": ui["accent"],
        "debugIcon.stepOutForeground": ui["accent"],
        "debugIcon.stepOverForeground": ui["accent"],
        "debugIcon.stopForeground": status["error"],
        "debugTokenExpression.boolean": syntax["constant"],
        "debugTokenExpression.error": status["error"],
        "debugTokenExpression.name": syntax["variable"],
        "debugTokenExpression.number": syntax["number"],
        "debugTokenExpression.string": syntax["string"],
        "debugTokenExpression.type": syntax["type"],
        "debugTokenExpression.value": ui["muted"],
        "debugToolBar.background": ui["element"],
        "debugView.exceptionLabelBackground": status["error"],
        "debugView.exceptionLabelForeground": ui["background"],
        "debugView.stateLabelBackground": ui["element"],
        "debugView.valueChangedHighlight": ui["accent"],
        "descriptionForeground": ui["muted"],
        "diffEditor.diagonalFill": ui["border"],
        "diffEditor.insertedLineBackground": decoration(tints["created"]),
        "diffEditor.insertedTextBackground": TRANSPARENT,
        "diffEditor.moveActive.border": status["warning"],
        "diffEditor.removedLineBackground": decoration(tints["deleted"]),
        "diffEditor.removedTextBackground": TRANSPARENT,
        "disabledForeground": ui["quiet"],
        "dropdown.background": ui["element"],
        "dropdown.border": ui["border"],
        "dropdown.foreground": ui["foreground"],
        "editor.background": ui["background"],
        "editor.findMatchBackground": ui["find_active"],
        "editor.findMatchBorder": ui["find_active_border"],
        "editor.findMatchHighlightBackground": ui["find"],
        "editor.findMatchHighlightBorder": ui["find_border"],
        "editor.findRangeHighlightBackground": range_highlight,
        "editor.focusedStackFrameHighlightBackground": decoration(tints["accent"]),
        "editor.foldPlaceholderForeground": ui["quiet"],
        "editor.foreground": ui["foreground"],
        "editor.hoverHighlightBackground": decoration(ui["highlight"]),
        "editor.inlineValuesBackground": ui["element"],
        "editor.inlineValuesForeground": status["hint"],
        "editor.lineHighlightBackground": ui["hover"],
        "editor.lineHighlightBorder": ui["hover"],
        "editor.linkedEditingBackground": decoration(ui["highlight"]),
        "editor.rangeHighlightBackground": range_highlight,
        "editor.selectionBackground": ui["selection"],
        "editor.snippetFinalTabstopHighlightBorder": ui["indent_active"],
        "editor.snippetTabstopHighlightBackground": decoration(ui["highlight"]),
        "editor.stackFrameHighlightBackground": decoration(ui["highlight"]),
        "editor.wordHighlightBackground": decoration(ui["highlight"]),
        "editor.wordHighlightStrongBackground": decoration(tints["magenta"]),
        "editorBracketHighlight.unexpectedBracket.foreground": ansi["bright"][1],
        "editorBracketMatch.background": ui["highlight"],
        "editorBracketMatch.border": ui["indent_active"],
        "editorCodeLens.foreground": status["hint"],
        "editorCursor.foreground": ui["cursor"],
        "editorError.foreground": status["error"],
        "editorGhostText.foreground": status["predictive"],
        "editorGroup.border": ui["border"],
        "editorGroup.dropBackground": ui["selection_overlay"],
        "editorGroupHeader.tabsBackground": ui["panel"],
        "editorGutter.addedBackground": status["created"],
        "editorGutter.background": ui["background"],
        "editorGutter.deletedBackground": status["deleted"],
        "editorGutter.modifiedBackground": status["modified"],
        "editorHint.foreground": status["hint"],
        "editorIndentGuide.activeBackground1": ui["indent_active"],
        "editorIndentGuide.background1": ui["indent"],
        "editorInfo.foreground": status["info"],
        "editorInlayHint.background": ui["element"],
        "editorInlayHint.foreground": status["hint"],
        "editorLightBulb.foreground": status["warning"],
        "editorLightBulbAutoFix.foreground": status["info"],
        "editorLineNumber.activeForeground": ui["foreground"],
        "editorLineNumber.foreground": ui["line_number"],
        "editorLink.activeForeground": syntax["link"],
        "editorOverviewRuler.border": ui["border"],
        "editorOverviewRuler.errorForeground": status["error"],
        "editorOverviewRuler.findMatchForeground": ui["find_active_border"],
        "editorOverviewRuler.rangeHighlightForeground": ui["accent"],
        "editorOverviewRuler.wordHighlightStrongForeground": ansi["normal"][5],
        "editorRuler.foreground": ui["border"],
        "editorStickyScrollHover.background": ui["hover"],
        "editorSuggestWidgetStatus.foreground": status["hint"],
        "editorWarning.foreground": status["warning"],
        "editorWhitespace.foreground": ui["invisible"],
        "editorWidget.background": ui["panel"],
        "editorWidget.border": ui["border"],
        "errorForeground": status["error"],
        "focusBorder": ui["accent"],
        "foreground": ui["foreground"],
        "gitDecoration.addedResourceForeground": status["created"],
        "gitDecoration.conflictingResourceForeground": status["conflict"],
        "gitDecoration.deletedResourceForeground": status["deleted"],
        "gitDecoration.ignoredResourceForeground": status["ignored"],
        "gitDecoration.modifiedResourceForeground": status["modified"],
        "gitDecoration.renamedResourceForeground": status["renamed"],
        "gitDecoration.stageDeletedResourceForeground": status["deleted"],
        "gitDecoration.stageModifiedResourceForeground": status["modified"],
        "gitDecoration.submoduleResourceForeground": ui["accent_strong"],
        "gitDecoration.untrackedResourceForeground": status["created"],
        "icon.foreground": ui["muted"],
        "input.background": ui["element"],
        "input.border": ui["border"],
        "input.placeholderForeground": ui["quiet"],
        "inputOption.activeBorder": ui["accent"],
        "inputOption.activeForeground": ui["foreground"],
        "inputOption.hoverBackground": ui["selection"],
        "inputValidation.errorBackground": ui["panel"],
        "inputValidation.errorBorder": status["error"],
        "inputValidation.infoBackground": ui["panel"],
        "inputValidation.infoBorder": status["info"],
        "inputValidation.warningBackground": ui["panel"],
        "inputValidation.warningBorder": status["warning"],
        "keybindingLabel.background": ui["element"],
        "keybindingLabel.border": ui["border"],
        "keybindingLabel.bottomBorder": ui["border"],
        "keybindingLabel.foreground": ui["foreground"],
        "list.activeSelectionBackground": ui["selection"],
        "list.activeSelectionForeground": ui["foreground"],
        "list.deemphasizedForeground": ui["quiet"],
        "list.dropBackground": ui["highlight"],
        "list.errorForeground": status["error"],
        "list.focusOutline": ui["accent"],
        "list.highlightForeground": ui["accent_strong"],
        "list.hoverBackground": ui["hover"],
        "list.inactiveSelectionBackground": ui["element"],
        "list.invalidItemForeground": status["warning"],
        "list.warningForeground": status["warning"],
        "listFilterWidget.noMatchesOutline": status["error"],
        "markdownAlert.important.foreground": ansi["normal"][5],
        "markdownAlert.tip.foreground": status["success"],
        "menu.background": ui["panel"],
        "menu.border": ui["border"],
        "minimap.errorHighlight": status["error"],
        "modernActivityBar.background": ui["panel"],
        "modernActivityBar.border": ui["border"],
        "modernActivityBar.inactiveBackground": ui["panel"],
        "modernActivityBarItem.activeBackground": ui["element"],
        "modernActivityBarItem.activeForeground": ui["foreground"],
        "modernActivityBarItem.hoverBackground": ui["hover"],
        "modernActivityBarItem.hoverForeground": ui["foreground"],
        "modernEditorTab.activeActionBackground": ui["highlight"],
        "modernEditorTab.activeBackground": ui["element"],
        "modernEditorTab.activeForeground": ui["foreground"],
        "modernEditorTab.activeHoverActionBackground": ui["highlight"],
        "modernEditorTab.activeHoverBackground": ui["element"],
        "modernEditorTab.hoverActionBackground": ui["highlight"],
        "modernEditorTab.hoverBackground": ui["hover"],
        "modernEditorTab.hoverForeground": ui["foreground"],
        "modernEditorTab.inactiveBackground": TRANSPARENT,
        "modernEditorTab.selectedActionBackground": ui["highlight"],
        "modernPanel.border": ui["border"],
        "modernSash.gripForeground": ui["border_strong"],
        "modernTab.activeBackground": ui["element"],
        "modernTab.activeForeground": ui["foreground"],
        "modernTab.hoverBackground": ui["hover"],
        "modernTab.hoverForeground": ui["foreground"],
        "modernUI.inactiveShellBackground": ui["panel"],
        "modernUI.shellBackground": ui["panel"],
        "multiDiffEditor.border": ui["border"],
        "multiDiffEditor.headerBackground": ui["panel"],
        "panel.background": ui["panel"],
        "panel.border": ui["border"],
        "panelInput.border": ui["border"],
        "panelSectionHeader.background": ui["panel"],
        "panelTitle.activeBorder": ui["accent"],
        "panelTitle.activeForeground": ui["foreground"],
        "panelTitle.inactiveForeground": ui["muted"],
        "peekViewEditor.background": ui["panel"],
        "peekViewEditor.matchHighlightBackground": ui["find"],
        "peekViewResult.background": ui["panel"],
        "peekViewResult.fileForeground": ui["foreground"],
        "peekViewResult.lineForeground": ui["muted"],
        "peekViewResult.matchHighlightBackground": ui["find"],
        "peekViewResult.selectionBackground": ui["selection"],
        "peekViewResult.selectionForeground": ui["foreground"],
        "peekViewTitle.background": ui["panel"],
        "peekViewTitleDescription.foreground": ui["muted"],
        "peekViewTitleLabel.foreground": ui["foreground"],
        "pickerGroup.border": ui["border"],
        "pickerGroup.foreground": ui["accent"],
        "problemsErrorIcon.foreground": status["error"],
        "problemsInfoIcon.foreground": status["info"],
        "problemsWarningIcon.foreground": status["warning"],
        "progressBar.background": ui["accent"],
        "quickInput.background": ui["panel"],
        "quickInputTitle.background": ui["element"],
        "scrollbarSlider.activeBackground": hover_thumb,
        "scrollbarSlider.background": thumb,
        "scrollbarSlider.hoverBackground": hover_thumb,
        "selection.background": ui["selection"],
        "settings.headerForeground": ui["foreground"],
        "settings.modifiedItemIndicator": status["modified"],
        "sideBar.background": ui["panel"],
        "sideBar.border": ui["border"],
        "sideBar.foreground": ui["foreground"],
        "sideBarSectionHeader.background": ui["panel"],
        "simpleFindWidget.sashBorder": ui["border"],
        "statusBar.background": ui["panel"],
        "statusBar.border": ui["border"],
        "statusBar.debuggingBackground": status["warning"],
        "statusBar.debuggingForeground": ui["background"],
        "statusBar.foreground": ui["muted"],
        "statusBar.noFolderBackground": ui["panel"],
        "statusBarItem.activeBackground": ui["selection"],
        "statusBarItem.compactHoverBackground": ui["element"],
        "statusBarItem.errorBackground": status["error"],
        "statusBarItem.errorForeground": ui["background"],
        "statusBarItem.hoverBackground": ui["element"],
        "statusBarItem.offlineBackground": status["error"],
        "statusBarItem.prominentBackground": ui["element"],
        "statusBarItem.warningBackground": status["warning"],
        "statusBarItem.warningForeground": ui["background"],
        "strongForeground": ui["foreground"],
        "surface.background": ui["background"],
        "surface.border": ui["border"],
        "surface.foreground": ui["muted"],
        "symbolIcon.classForeground": syntax["type"],
        "symbolIcon.constructorForeground": syntax["function"],
        "symbolIcon.enumeratorForeground": syntax["type"],
        "symbolIcon.enumeratorMemberForeground": syntax["constant"],
        "symbolIcon.eventForeground": syntax["attribute"],
        "symbolIcon.fieldForeground": syntax["variable"],
        "symbolIcon.functionForeground": syntax["function"],
        "symbolIcon.interfaceForeground": syntax["type"],
        "symbolIcon.methodForeground": syntax["function"],
        "symbolIcon.variableForeground": syntax["variable"],
        "tab.activeBackground": ui["background"],
        "tab.activeBorderTop": ui["accent"],
        "tab.activeForeground": ui["foreground"],
        "tab.activeModifiedBorder": status["modified"],
        "tab.border": ui["border"],
        "tab.inactiveBackground": ui["panel"],
        "tab.inactiveForeground": ui["muted"],
        "tab.unfocusedInactiveForeground": ui["quiet"],
        "terminal.background": ui["background"],
        "terminal.findMatchBackground": ui["find_terminal_active"],
        "terminal.findMatchBorder": ui["find_active_border"],
        "terminal.findMatchHighlightBackground": ui["find_terminal"],
        "terminal.findMatchHighlightBorder": ui["find_border"],
        "terminal.foreground": ui["foreground"],
        "terminal.initialHintForeground": status["hint"],
        "terminal.selectionBackground": ui["selection"],
        "terminalCommandDecoration.defaultBackground": ui["quiet"],
        "terminalCommandDecoration.errorBackground": status["error"],
        "terminalCommandDecoration.successBackground": status["info"],
        "terminalCursor.foreground": ui["cursor"],
        "terminalStickyScrollHover.background": ui["hover"],
        "textBlockQuote.background": ui["element"],
        "textBlockQuote.border": ui["indent_active"],
        "textCodeBlock.background": ui["highlight"],
        "textLink.activeForeground": ui["accent"],
        "textLink.foreground": ui["accent_strong"],
        "textPreformat.background": ui["element"],
        "textPreformat.foreground": ui["foreground"],
        "textSeparator.foreground": ui["border"],
        "titleBar.activeBackground": ui["panel"],
        "titleBar.activeForeground": ui["foreground"],
        "titleBar.border": ui["border"],
        "titleBar.inactiveBackground": ui["panel"],
        "titleBar.inactiveForeground": ui["quiet"],
        "toolbar.hoverBackground": ui["element"],
        "tree.indentGuidesStroke": ui["indent"],
        "tree.tableColumnsBorder": ui["border"],
    }
    for index, accent in enumerate(ui["accents"], start=1):
        colours[f"editorBracketHighlight.foreground{index}"] = accent
    for index, name in enumerate(ANSI_NAMES):
        title = name.capitalize()
        colours[f"terminal.ansi{title}"] = ansi["normal"][index]
        colours[f"terminal.ansiBright{title}"] = ansi["bright"][index]
    return dict(sorted(colours.items()))


def vscode_token_settings(colour: str, style: str | None) -> dict[str, str]:
    if style is None:
        return {"foreground": colour}
    return {"foreground": colour, "fontStyle": style}


def vscode_theme(palette: Palette) -> dict[str, Any]:
    if "vscode" in palette["ports"]:
        return port_theme(palette, "vscode") | {"name": palette["name"]}
    syntax, styles = palette["syntax"], palette["syntax_style"]
    # Once a role is styled, a rule with no style inherits a broader scope's, as
    # `string.regexp` would `string`'s; an empty style clears it.
    unstyled = "" if styles else None

    def settings(colour: str, style: str | None) -> dict[str, str]:
        return vscode_token_settings(colour, unstyled if style is None else style)

    token_colours = [
        {
            "scope": scopes,
            "settings": settings(*syntax_look(palette, f"syntax.{role}", style)),
        }
        for scopes, role, style in VSCODE_TOKENS
    ]
    if palette["heading"] is not None:
        colour, style = heading_look(palette)
        # Appended after the token rules to override their bold `markup.heading`; an empty
        # style clears that bold, which an unset one would keep.
        heading = {"foreground": colour, "fontStyle": style or ""}
        token_colours.append({"scope": VSCODE_HEADING_SCOPES, "settings": heading})
    token_colours += [
        {
            "scope": scopes,
            "settings": settings(palette_colour(palette, path), None),
        }
        for scopes, path in VSCODE_DIFF_TOKENS
    ]
    return {
        "name": palette["name"],
        "type": palette["appearance"],
        "semanticHighlighting": True,
        "colors": vscode_colours(palette),
        "tokenColors": token_colours,
        "semanticTokenColors": {
            selector: vscode_token_settings(syntax[role], styles[role])
            if role in styles
            else syntax[role]
            for selector, role in VSCODE_SEMANTIC.items()
        },
    }


def package_description(families: list[Family]) -> str:
    sentences = []
    for family in families:
        names = " and ".join(p["name"] for p in family["palettes"])
        origin = f"{names}, built from the colours of {family['source']}."
        sentences.append(f"{origin} {family['disclaimer']}")
    return " ".join(sentences)


def vscode_manifest(palettes: list[Palette], description: str) -> dict[str, Any]:
    return {
        "name": PACKAGE,
        "displayName": PACKAGE_NAME,
        "description": description,
        "version": "1.0.0",
        "publisher": AUTHOR,
        "license": "MIT AND Apache-2.0",
        "repository": REPOSITORY_URL,
        "engines": {"vscode": "^1.81.0"},
        "categories": ["Themes"],
        "files": ["LICENSE", "themes"],
        "contributes": {
            "themes": [
                {
                    "label": p["name"],
                    "uiTheme": VSCODE_UI_THEMES[p["appearance"]],
                    "path": f"./themes/{slug(p['name'])}.json",
                }
                for p in palettes
            ],
        },
    }


def translucent(colour: str, ground: str, alpha: str) -> str:
    weight = int(alpha, 16) / 255
    channels = []
    for i in (1, 3, 5):
        c, g = int(colour[i : i + 2], 16), int(ground[i : i + 2], 16)
        channel = round(g + (c - g) / weight)
        if not 0 <= channel <= 255:
            raise ValueError(f"{colour} isn't reachable over {ground} at alpha {alpha}")
        channels.append(channel)
    return "#" + "".join(f"{c:02x}" for c in channels) + alpha


def opaque(colour: str, ground: str) -> str:
    if len(colour) == OPAQUE_HEX_LENGTH:
        return colour
    alpha = int(colour[OPAQUE_HEX_LENGTH:], 16) / 255
    channels = (
        round(
            int(colour[i : i + 2], 16) * alpha
            + int(ground[i : i + 2], 16) * (1 - alpha)
        )
        for i in (1, 3, 5)
    )
    return "#" + "".join(f"{c:02x}" for c in channels)


def tint(palette: Palette, colour: str, weight: float = 1) -> str:
    base = palette.get("tint_alpha", TINT_ALPHAS[palette["appearance"]])
    alpha = round(int(base, 16) * weight)
    return opaque(f"{colour}{alpha:02x}", palette["ui"]["background"])


def with_tints(palette: Palette) -> Palette:
    tints = {
        name: tint(palette, palette_colour(palette, path))
        for name, path in TINTS.items()
    }
    return palette | {"tint": tints}


def luminance(hex_colour: str) -> float:
    r, g, b = linear_rgb(hex_colour)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(text: str, ground: str) -> float:
    light, dark = sorted((luminance(text), luminance(ground)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def syntax_grounds(palette: Palette) -> dict[str, str]:
    grounds = {f"ui.{key}": palette["ui"][key] for key in SYNTAX_GROUNDS}
    return grounds | {
        f"tint.{name}": colour for name, colour in palette["tint"].items()
    }


def contrast_failures(palette: Palette) -> list[str]:
    pairs = [
        (f"syntax.{role} on {name}", colour, ground)
        for name, ground in syntax_grounds(palette).items()
        for role, colour in palette["syntax"].items()
    ]
    pairs += [
        (
            f"{text} on {ground}",
            palette_colour(palette, text),
            palette_colour(palette, ground),
        )
        for text, ground in TEXT_PAIRS
    ]
    pairs += [
        (f"{path} on {name}", palette_colour(palette, path), ground)
        for name, ground in syntax_grounds(palette).items()
        for path in SYNTAX_LIKE_PATHS
    ]
    pairs += [
        (f"status.{name} on ui.{ground}", colour, palette["ui"][ground])
        for name, colour in palette["status"].items()
        for ground in STATUS_GROUNDS
    ]
    pairs += [
        (
            f"{path} on ui.background",
            palette_colour(palette, path),
            palette["ui"]["background"],
        )
        for path in ANSI_TEXT_PATHS
    ]
    pairs += claude_code_contrast_pairs(palette)
    pairs += port_contrast_pairs(palette)
    pairs += herdr_app_contrast_pairs(palette)
    failures = []
    for label, text, ground in pairs:
        ratio = contrast(text, ground)
        if ratio >= MINIMUM_CONTRAST:
            continue
        failures.append(f"{palette['name']}: {label} is {ratio:.2f}:1")
    return failures


def port_contrast_pairs(palette: Palette) -> list[tuple[str, str, str]]:
    pairs = []
    for app in palette["ports"]:
        theme = port_theme(palette, app)
        colours = theme["colors"] if app == "vscode" else theme
        background = opaque(colours["editor.background"], palette["ui"]["background"])
        grounds = {"editor.background": background} | {
            key: opaque(colours[key], background) for key in PORT_GROUNDS[app]
        }
        texts = {"editor.foreground": colours["editor.foreground"]}
        if app == "zed":
            selection = theme["players"][0]["selection"]
            grounds["players[0].selection"] = opaque(selection, background)
            texts |= {
                f"syntax.{name}": style["color"]
                for name, style in theme["syntax"].items()
                if "color" in style
            }
        else:
            texts |= {
                str(rule["scope"]): rule["settings"]["foreground"]
                for rule in theme["tokenColors"]
                if "foreground" in rule["settings"]
            }
            texts |= {
                f"semantic {name}": style
                if isinstance(style, str)
                else style["foreground"]
                for name, style in theme.get("semanticTokenColors", {}).items()
                if isinstance(style, str) or "foreground" in style
            }
        pairs += [
            (f"{app} {text} on {name}", opaque(colour, ground), ground)
            for text, colour in texts.items()
            for name, ground in grounds.items()
        ]
        terminal = opaque(colours["terminal.background"], background)
        pairs += [
            (f"{app} {key} on terminal.background", opaque(colour, terminal), terminal)
            for key, colour in colours.items()
            if key.startswith("terminal.ansi") and "black" not in key.lower()
        ]
    return pairs


def xml_text(root: ET.Element) -> str:
    ET.indent(root)
    return ET.tostring(root, encoding="unicode") + "\n"


def scrollbar_thumbs(palette: Palette) -> tuple[str, str]:
    ui = palette["ui"]
    return ui["indent_active"] + SCROLLBAR_ALPHA, ui["muted"] + SCROLLBAR_HOVER_ALPHA


def palette_card(palette: Palette) -> str:
    ui, ansi = palette["ui"], palette["ansi"]
    sections = [
        ("UI", [(key, ui[key]) for key in ("background", "foreground", "accent")]),
        ("Syntax", sorted(palette["syntax"].items())),
        (
            "ANSI",
            [
                (f"{prefix}{name}", colour)
                for shade, prefix in (("normal", ""), ("bright", "bright "))
                for name, colour in zip(ANSI_NAMES, ansi[shade], strict=True)
            ],
        ),
    ]
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg")

    def element(tag: str, text: str | None = None, **attributes: object) -> None:
        ET.SubElement(svg, tag, {k: str(v) for k, v in attributes.items()}).text = text

    element("title", f"{palette['name']} palette")
    element("rect", width="100%", height="100%", rx=12, fill=ui["background"])
    y = CARD_PADDING
    for heading, swatches in sections:
        element(
            "text",
            heading,
            x=CARD_PADDING,
            y=y + CARD_HEADING_BASELINE,
            fill=ui["muted"],
        )
        y += CARD_ROW_HEIGHT
        for index, (role, colour) in enumerate(swatches):
            row, column = divmod(index, CARD_COLUMNS)
            x = CARD_PADDING + column * CARD_CELL_WIDTH
            top = y + row * CARD_ROW_HEIGHT
            label_x = x + CARD_SWATCH + CARD_LABEL_GAP
            element(
                "rect",
                x=x,
                y=top,
                width=CARD_SWATCH,
                height=CARD_SWATCH,
                rx=6,
                fill=colour,
                stroke=ui["border"],
            )
            element(
                "text",
                role,
                x=label_x,
                y=top + CARD_ROLE_BASELINE,
                fill=ui["foreground"],
            )
            element(
                "text", colour, x=label_x, y=top + CARD_HEX_BASELINE, fill=ui["muted"]
            )
        y += math.ceil(len(swatches) / CARD_COLUMNS) * CARD_ROW_HEIGHT
    width = 2 * CARD_PADDING + CARD_COLUMNS * CARD_CELL_WIDTH
    height = y + CARD_PADDING
    svg.attrib |= {
        "width": str(width),
        "height": str(height),
        "viewBox": f"0 0 {width} {height}",
        "style": f"font-family: {CARD_FONT}; font-size: 13px",
    }
    return xml_text(svg)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(path.relative_to(ROOT))


def write_json(path: Path, value: dict[str, Any]) -> None:
    write(path, json.dumps(value, indent=2) + "\n")


def load_family(folder: Path) -> Family:
    family = tomllib.loads((folder / FAMILY_FILE).read_text())
    family["palettes"] = [
        with_ports(with_tints(with_defaults(tomllib.loads(p.read_text()))), folder)
        for p in sorted(folder.glob("*.toml"))
        if p.name != FAMILY_FILE
    ]
    return family


def with_defaults(palette: Palette) -> Palette:
    syntax = dict(palette["syntax"])
    heading = syntax.pop(HEADING, None)
    styles = palette.get("syntax_style", {})
    invalid = [
        f"syntax_style.{role} = {style!r}"
        for role, style in styles.items()
        if role not in syntax or style not in FONT_STYLES
    ]
    if heading is not None and heading not in syntax:
        invalid.append(f"syntax.heading = {heading!r}")
    if invalid:
        raise SystemExit(f"{palette['name']}: invalid {', '.join(invalid)}")
    return palette | {
        "heading": heading,
        "syntax": syntax,
        "syntax_style": styles,
        "ui": {"line_number": palette["ui"]["quiet"]} | palette["ui"],
    }


def with_ports(palette: Palette, folder: Path) -> Palette:
    ports = {}
    for app, port in palette.get("ports", {}).items():
        source = json.loads((folder / port["file"]).read_text())
        if "theme" in port:
            source = next(t for t in source["themes"] if t["name"] == port["theme"])
            source = source["style"]
        licence = (folder / port["file"]).with_name("LICENSE").read_text()
        ports[app] = port | {"licence": licence, "source": source}
    return palette | {"ports": ports}


def main() -> None:
    families = [
        load_family(folder)
        for folder in sorted((ROOT / "palettes").iterdir())
        if folder.is_dir()
    ]
    palettes = [p for family in families for p in family["palettes"]]
    if failures := [f for p in palettes for f in contrast_failures(p)]:
        raise SystemExit("\n".join(failures))
    description = package_description(families)
    write_json(ROOT / "vscode" / "package.json", vscode_manifest(palettes, description))
    port_licences = [
        p["ports"]["vscode"]["licence"] for p in palettes if "vscode" in p["ports"]
    ]
    write(
        ROOT / "vscode" / "LICENSE",
        "\n---\n\n".join([(ROOT / "LICENSE").read_text(), *port_licences]),
    )
    for family in families:
        write_family(family)


def write_family(family: Family) -> None:
    palettes = family["palettes"]
    stem = slug(family["name"])
    write(ROOT / "herdr" / f"{stem}.toml", herdr(palettes))
    bundle = ROOT / "netnewswire" / f"{family['name']}.nnwtheme"
    write(bundle / "Info.plist", netnewswire_info(family))
    write(bundle / "stylesheet.css", netnewswire_stylesheet(palettes))
    write_json(ROOT / "zed" / f"{stem}.json", zed_family(family))
    for palette in palettes:
        name = slug(palette["name"])
        if "zed" in palette["ports"]:
            write(ROOT / "zed" / f"{stem}.LICENSE", palette["ports"]["zed"]["licence"])
        write_json(ROOT / "claude-code" / f"{name}.json", claude_code_theme(palette))
        write(ROOT / "ghostty" / palette["name"], ghostty(palette))
        write_json(ROOT / "herdr-app" / f"{name}.json", herdr_app_theme(palette))
        write(ROOT / "slack" / f"{palette['name']}.txt", slack(palette))
        write_json(ROOT / "vscode" / "themes" / f"{name}.json", vscode_theme(palette))
        write_json(ROOT / "xcode" / f"{name}.json", xcode_recipe(palette))
        write(
            ROOT / "docs" / f"palette-{name}.svg",
            palette_card(palette),
        )


if __name__ == "__main__":
    main()
