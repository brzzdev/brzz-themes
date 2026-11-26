# Inherited colours

Every app fills each colour key a theme leaves unset from its own base theme, so a key a theme doesn't set shows the base theme's colour. Every family goes through the same `build.py` mappings, so where an entry says Geist, it holds for Ayu Dark Contrast too. This record lists, for each target, every key still left to the base theme and why. It comes from an audit of each app's own defaults (#39), not from `build.py`, so it needs a fresh audit when an app adds keys.

The reasons:

- **Derived**: the app computes it from a key we set.
- **Matches**: the base value is already Geist's, is transparent, or is a neutral shadow.
- **No colour**: the key sets only a font style, or is null.
- **No reader**: nothing in the app reads the key.
- **Not targeted**: it belongs to a feature the themes don't cover.
- **Fixed**: the app computes it, and no theme key reaches it.

## Claude Code

Audited against the keys of Claude Code 2.1.332's built-in themes, which add nine undocumented keys to the 63 in its [colour token reference](https://code.claude.com/docs/en/terminal-config#create-a-custom-theme). Each theme starts from the built-in `dark` or `light` preset. Geist sets all 63 documented tokens and five undocumented ones it can read in the binary: `autoAcceptShimmer`, which pairs with `autoAccept`, and the text colours `background` (background agent and task labels), `chromeYellow` (`/chrome`), `professionalBlue` (the data privacy and consumer terms dialogs), and `skill` (skill labels).

| Reason | Keys |
| --- | --- |
| **Fixed**: diff code takes Claude Code's own highlighter, Monokai Extended over `dark` or GitHub over `light` (see ADR 0003) | syntax colours |
| **Not targeted**: the Clawd mascot | `clawd_background`, `clawd_body` |
| **Not targeted**: the system spinner | `claudeBlue_FOR_SYSTEM_SPINNER`, `claudeBlueShimmer_FOR_SYSTEM_SPINNER` |

## Ghostty

Audited against Ghostty 1.4.0's `+show-config --default --docs`. Ghostty fills unset options from its built-in defaults.

| Reason | Keys |
| --- | --- |
| **Derived**: unset, Ghostty uses the background | `unfocused-split-fill`, `window-padding-color` |
| **Matches**: unset, bold text keeps its cell's colour | `bold-color` |
| **No colour**: a ratio or an image, not a colour | `background-image`, `minimum-contrast` |
| **Not targeted**: the 256-colour cube and grey ramp, which programs pick by index for fixed colours | `palette` 16–255 |
| **Not targeted**: the GTK title bar | `window-titlebar-background`, `window-titlebar-foreground` |
| **Not targeted**: the app icon | `macos-icon-ghost-color`, `macos-icon-screen-color` |

## herdr

Audited against herdr 0.9.5. A `[theme.custom]` table accepts 19 tokens, and Geist sets all of them. Pane contents take the host terminal's colours.

## Herdr desktop app

Audited against Herdr 0.1.15's `themes()`, declared in `~/.config/herdr-app/herdr.d.ts`. A theme file sets the terminal colours, and its `colors` table overrides the panel colours Herdr derives from them. Geist sets every colour `themes()` reports, including `terminal_foreground`, which Herdr takes from the top-level `foreground`.

## NetNewsWire

Audited against NetNewsWire 7.2.1. A theme's stylesheet replaces the default one rather than layering on it. Only `core.css` is always added, and it sets no colours, so whatever Geist's stylesheet doesn't style falls back to WebKit's defaults.

| Reason | Keys |
| --- | --- |
| **Derived**: `currentColor` or inherited text, so they follow `--foreground` or `--link` | `.twemoji svg`, `::marker`, `a:active`, `a:visited`, `abbr`, `caption`, `cite`, `dd`, `del`, `dfn`, `dt`, `iframe` border, `ins`, iOS `sup a`, `kbd`, `q`, `s`, `samp`, `small`, `summary`, `tt`, `u`, `var` |
| **Not targeted**: the default theme's filled link hover and Feedbin wrapper border, left out on purpose | `.articleBody a:hover` background, `.feedbin--article-wrap` border |
| **Not targeted**: system controls, which follow `color-scheme` | `audio` and `video` controls, the focus ring, form controls, iOS tap highlight, scrollbars, WebKit's find highlight |
| **Not targeted**: colours a feed sets in its own markup | `<font color>`, `bgcolor`, inline `border-color` |

## Rex

Audited against Rex 0.1.0 (build 1925). Rex imports the Ghostty files and keeps the background, text, cursor, cursor text, selection, selected text, and the 16 ANSI colours. It drops the search and split-divider colours.

| Reason | Keys |
| --- | --- |
| **Derived**: with **Tint with theme** on, Rex shades it from the theme | the sidebar |
| **Fixed**: with **Tint with theme** off, Rex uses macOS's own shade | the sidebar |
| **Fixed**: a Rex theme has no key for them | search matches, split dividers |
| **Not targeted**: the extended palette, which Rex fills with xterm's defaults on import | `palette` 16–255 |

## Slack

Audited against Slack's desktop app in November 2026. A custom theme takes four colours, and Geist sets all of them: system navigation, selected items, presence indication, and notifications.

| Reason | Keys |
| --- | --- |
| **Fixed**: Slack computes them from the system navigation colour and the colour mode, and nudges the sidebar off pure black and white | the message pane, text, and borders |
| **Not targeted**: blends the background with the selected items colour | Window gradient |

## VS Code

Audited against VS Code 1.144.1: every colour registered with `registerColor`, plus the colours the bundled Git extension contributes, 998 keys in all, of which Geist sets 317. VS Code fills unset keys from the defaults for `vs-dark` and `vs`, many of which are expressions over other keys.

| Reason | Keys |
| --- | --- |
| **Derived**: follows `activityBar.foreground` | `activityBar.activeBorder`, `activityBar.dropBorder` |
| **Derived**: follows `activityBarBadge.background` | `agentsBadge.background`, `agentsUnreadBadge.background`, `extensionBadge.remoteBackground`, `panelTitleBadge.background`, `statusBarItem.remoteBackground` |
| **Derived**: follows `activityBarBadge.foreground` | `agentsBadge.foreground`, `agentsUnreadBadge.foreground`, `extensionBadge.remoteForeground`, `panelTitleBadge.foreground`, `statusBarItem.remoteForeground` |
| **Derived**: follows `activityBarTop.foreground` | `activityBarTop.activeBorder`, `activityBarTop.dropBorder` |
| **Derived**: follows `agents.background` | `inactiveSessionView.background` |
| **Derived**: follows `agentsPanel.background` | `activeSessionView.background` |
| **Derived**: follows `agentsPanel.border` | `agentsBottomPanel.border`, `agentsCard.border` |
| **Derived**: follows `agentsPanel.foreground` | `activeSessionView.foreground`, `inactiveSessionView.foreground` |
| **Derived**: follows `agentsVoice.speakingForeground` | `agentsVoice.speakingBackground` |
| **Derived**: follows `badge.background` | `scmGraph.historyItemHoverDefaultLabelBackground`, `testing.coverCountBadgeBackground` |
| **Derived**: follows `badge.foreground` | `testing.coverCountBadgeForeground` |
| **Derived**: follows `button.background` | `agentsGradient.tintColor`, `agentsUpdateButton.downloadedBackground`, `agentsUpdateButton.downloadingBackground`, `chat.inputWorkingBorderColor1`, `chat.inputWorkingBorderColor2`, `chat.inputWorkingBorderColor3`, `extensionButton.prominentBackground`, `inlineEdit.gutterIndicator.primaryBorder`, `inlineEdit.gutterIndicator.successfulBorder` |
| **Derived**: follows `button.foreground` | `button.separator`, `extensionButton.prominentForeground`, `inlineEdit.gutterIndicator.primaryForeground`, `inlineEdit.gutterIndicator.successfulForeground` |
| **Derived**: follows `button.hoverBackground` | `extensionButton.prominentHoverBackground` |
| **Derived**: follows `button.secondaryBackground` | `extensionButton.background` |
| **Derived**: follows `button.secondaryBorder` | `agentsNewSessionButton.border`, `extensionButton.border` |
| **Derived**: follows `button.secondaryForeground` | `extensionButton.foreground` |
| **Derived**: follows `button.secondaryHoverBackground` | `extensionButton.hoverBackground` |
| **Derived**: follows `button.separator` | `extensionButton.separator` |
| **Derived**: follows `charts.blue` | `agentsVoice.speakingForeground`, `scmGraph.historyItemRefColor` |
| **Derived**: follows `charts.yellow` | `chat.sessionStateIndicator.inProgressBorder` |
| **Derived**: follows `chat.findMatchHighlightBackground` | `chat.findMatchBackground` |
| **Derived**: follows `chat.voiceGlowBaseColor` | `chat.dictationActiveMicGlow` |
| **Derived**: follows `checkbox.background` | `checkbox.disabled.background`, `settings.checkboxBackground` |
| **Derived**: follows `checkbox.border` | `settings.checkboxBorder` |
| **Derived**: follows `checkbox.foreground` | `checkbox.disabled.foreground`, `settings.checkboxForeground` |
| **Derived**: follows `commandCenter.background` | `agentStatusIndicator.background` |
| **Derived**: follows `commentsView.resolvedIcon` | `editorCommentsWidget.resolvedBorder` |
| **Derived**: follows `commentsView.unresolvedIcon` | `editorCommentsWidget.unresolvedBorder` |
| **Derived**: follows `disabledForeground` | `commentsView.resolvedIcon` |
| **Derived**: follows `dropdown.background` | `checkbox.background`, `settings.dropdownBackground` |
| **Derived**: follows `dropdown.border` | `checkbox.border`, `settings.dropdownBorder` |
| **Derived**: follows `dropdown.foreground` | `checkbox.foreground`, `menu.foreground`, `settings.dropdownForeground` |
| **Derived**: follows `editor.background` | `agents.background`, `agentsDetail.background`, `breadcrumb.background`, `chat.requestBackground`, `editorGroupHeader.noTabsBackground`, `editorMarkerNavigation.background`, `editorPane.background`, `editorStickyScroll.background`, `editorStickyScrollGutter.background`, `minimap.chatEditHighlight`, `multiDiffEditor.background` |
| **Derived**: follows `editor.findMatchHighlightBackground` | `chat.findMatchHighlightBackground`, `editor.symbolHighlightBackground`, `list.filterMatchBackground`, `minimap.findMatchHighlight`, `searchEditor.findMatchBackground` |
| **Derived**: follows `editor.findMatchHighlightBorder` | `list.filterMatchBorder`, `searchEditor.findMatchBorder` |
| **Derived**: follows `editor.foreground` | `editorGutter.commentGlyphForeground`, `editorGutter.itemGlyphForeground`, `editorSuggestWidget.foreground`, `testing.message.info.decorationForeground` |
| **Derived**: follows `editor.hoverHighlightBackground` | `terminal.hoverHighlightBackground` |
| **Derived**: follows `editor.lineHighlightBackground` | `editor.inactiveLineHighlightBackground` |
| **Derived**: follows `editor.selectionBackground` | `chat.requestBubbleBackground`, `chat.requestBubbleHoverBackground`, `editor.foldBackground`, `editor.inactiveSelectionBackground`, `editor.selectionHighlightBackground`, `minimap.selectionHighlight` |
| **Derived**: follows `editor.selectionHighlightBackground` | `minimap.selectionOccurrenceHighlight` |
| **Derived**: follows `editor.wordHighlightBackground` | `editor.wordHighlightTextBackground` |
| **Derived**: follows `editorCommentsWidget.unresolvedBorder` | `editorCommentsWidget.rangeActiveBackground`, `editorCommentsWidget.rangeBackground` |
| **Derived**: follows `editorCursor.foreground` | `editorMultiCursor.primary.foreground`, `editorMultiCursor.secondary.foreground` |
| **Derived**: follows `editorError.foreground` | `charts.red`, `editorMarkerNavigationError.background`, `markdownAlert.caution.foreground`, `notificationsErrorIcon.foreground`, `testing.peekBorder`, `testing.peekHeaderBackground` |
| **Derived**: follows `editorGhostText.foreground` | `editor.placeholder.foreground` |
| **Derived**: follows `editorGroup.border` | `sideBySideEditor.horizontalBorder`, `sideBySideEditor.verticalBorder` |
| **Derived**: follows `editorGroup.dropBackground` | `panelSection.dropBackground`, `sideBar.dropBackground`, `terminal.dropBackground` |
| **Derived**: follows `editorGroupHeader.tabsBackground` | `editorGroupHeader.connectedTabsBackground` |
| **Derived**: follows `editorGutter.addedBackground` | `editorGutter.addedSecondaryBackground`, `editorOverviewRuler.addedForeground`, `minimapGutter.addedBackground` |
| **Derived**: follows `editorGutter.commentGlyphForeground` | `editorGutter.commentDraftGlyphForeground`, `editorGutter.commentUnresolvedGlyphForeground` |
| **Derived**: follows `editorGutter.commentRangeForeground` | `editorOverviewRuler.commentForeground` |
| **Derived**: follows `editorGutter.deletedBackground` | `editorGutter.deletedSecondaryBackground`, `editorOverviewRuler.deletedForeground`, `minimapGutter.deletedBackground` |
| **Derived**: follows `editorGutter.modifiedBackground` | `editorGutter.modifiedSecondaryBackground`, `editorOverviewRuler.modifiedForeground`, `minimapGutter.modifiedBackground` |
| **Derived**: follows `editorHoverWidget.background` | `editorHoverWidget.statusBarBackground`, `inlineEdit.gutterIndicator.secondaryBackground` |
| **Derived**: follows `editorHoverWidget.border` | `inlineEdit.gutterIndicator.secondaryBorder` |
| **Derived**: follows `editorHoverWidget.foreground` | `inlineEdit.gutterIndicator.secondaryForeground` |
| **Derived**: follows `editorInfo.foreground` | `banner.iconForeground`, `charts.blue`, `debugConsole.infoForeground`, `editorMarkerNavigationInfo.background`, `editorOverviewRuler.infoForeground`, `markdownAlert.note.foreground`, `minimap.infoHighlight`, `notificationsInfoIcon.foreground`, `peekView.border`, `testing.messagePeekBorder`, `testing.messagePeekHeaderBackground` |
| **Derived**: follows `editorInlayHint.background` | `editorInlayHint.parameterBackground`, `editorInlayHint.typeBackground` |
| **Derived**: follows `editorInlayHint.foreground` | `editorInlayHint.parameterForeground`, `editorInlayHint.typeForeground`, `git.blame.editorDecorationForeground` |
| **Derived**: follows `editorMarkerNavigationError.background` | `editorMarkerNavigationError.headerBackground` |
| **Derived**: follows `editorMarkerNavigationInfo.background` | `editorMarkerNavigationInfo.headerBackground` |
| **Derived**: follows `editorMarkerNavigationWarning.background` | `editorMarkerNavigationWarning.headerBackground` |
| **Derived**: follows `editorOverviewRuler.border` | `terminalOverviewRuler.border` |
| **Derived**: follows `editorOverviewRuler.commentForeground` | `editorOverviewRuler.commentUnresolvedForeground` |
| **Derived**: follows `editorOverviewRuler.commentUnresolvedForeground` | `editorOverviewRuler.commentDraftForeground` |
| **Derived**: follows `editorOverviewRuler.findMatchForeground` | `terminalOverviewRuler.findMatchForeground` |
| **Derived**: follows `editorPane.background` | `notebook.editorBackground` |
| **Derived**: follows `editorWarning.foreground` | `charts.yellow`, `debugConsole.warningForeground`, `editorMarkerNavigationWarning.background`, `editorOverviewRuler.warningForeground`, `editorUnicodeHighlight.border`, `markdownAlert.warning.foreground`, `minimap.warningHighlight`, `notificationsWarningIcon.foreground` |
| **Derived**: follows `editorWhitespace.foreground` | `editorIndentGuide.activeBackground`, `editorIndentGuide.background`, `editorWordWrapIndicator.foreground` |
| **Derived**: follows `editorWidget.background` | `agentFeedbackEditorWidget.background`, `breadcrumbPicker.background`, `checkbox.selectBackground`, `editorActionList.background`, `editorGroup.dropIntoPromptBackground`, `editorHoverWidget.background`, `editorSuggestWidget.background`, `inlineChat.background`, `listFilterWidget.background`, `notifications.background`, `welcomePage.tileBackground`, `welcomePage.tileHoverBackground` |
| **Derived**: follows `editorWidget.border` | `agentFeedbackInputWidget.border`, `editorHoverWidget.border`, `editorSuggestWidget.border`, `inlineChat.border`, `inlineChatInput.border`, `settings.dropdownListBorder` |
| **Derived**: follows `editorWidget.foreground` | `editorActionList.foreground`, `editorGroup.dropIntoPromptForeground`, `editorHoverWidget.foreground`, `inlineChat.foreground`, `notifications.foreground`, `quickInput.foreground` |
| **Derived**: follows `errorForeground` | `debugConsole.errorForeground` |
| **Derived**: follows `focusBorder` | `agentsChatInput.focusBorder`, `chat.voiceGlowBaseColor`, `inlineChatInput.focusBorder`, `inputOption.activeBackground`, `notebook.cellInsertionIndicator`, `notebook.focusedCellBorder`, `notebook.focusedEditorBorder`, `sash.hoverBorder`, `settings.focusedRowBorder`, `tab.selectedBorderTop` |
| **Derived**: follows `foreground` | `agentFeedbackEditorWidget.border`, `agentSessionReadIndicator.foreground`, `agentSessionSelectedUnfocusedBadge.border`, `agentsPanel.border`, `breadcrumb.activeSelectionForeground`, `breadcrumb.focusForeground`, `breadcrumb.foreground`, `button.secondaryBorder`, `button.secondaryForeground`, `charts.foreground`, `charts.lines`, `chat.avatarForeground`, `chat.statusBackground`, `debugConsole.sourceForeground`, `debugConsoleInputIcon.foreground`, `debugView.stateLabelForeground`, `diffEditor.unchangedRegionForeground`, `editorWidget.foreground`, `input.foreground`, `menu.separatorBackground`, `notebookStatusRunningIcon.foreground`, `scmGraph.historyItemHoverDefaultLabelForeground`, `search.resultsInfoForeground`, `symbolIcon.arrayForeground`, `symbolIcon.booleanForeground`, `symbolIcon.colorForeground`, `symbolIcon.constantForeground`, `symbolIcon.fileForeground`, `symbolIcon.folderForeground`, `symbolIcon.keyForeground`, `symbolIcon.keywordForeground`, `symbolIcon.moduleForeground`, `symbolIcon.namespaceForeground`, `symbolIcon.nullForeground`, `symbolIcon.numberForeground`, `symbolIcon.objectForeground`, `symbolIcon.operatorForeground`, `symbolIcon.packageForeground`, `symbolIcon.propertyForeground`, `symbolIcon.referenceForeground`, `symbolIcon.snippetForeground`, `symbolIcon.stringForeground`, `symbolIcon.structForeground`, `symbolIcon.textForeground`, `symbolIcon.typeParameterForeground`, `symbolIcon.unitForeground`, `tree.tableOddRowsBackground` |
| **Derived**: follows `icon.foreground` | `checkbox.selectBorder`, `editorGutter.foldingControlForeground`, `list.dropBetweenBackground` |
| **Derived**: follows `ifDefined` | `interactive.inactiveCodeBorder` |
| **Derived**: follows `inlineEdit.gutterIndicator.primaryBorder` | `inlineEdit.gutterIndicator.primaryBackground` |
| **Derived**: follows `inlineEdit.gutterIndicator.successfulBorder` | `inlineEdit.gutterIndicator.successfulBackground` |
| **Derived**: follows `input.background` | `agentsChatInput.background`, `inlineChatInput.background`, `settings.numberInputBackground`, `settings.textInputBackground`, `welcomePage.progress.background` |
| **Derived**: follows `input.border` | `agentsChatInput.border`, `searchEditor.textInputBorder`, `settings.numberInputBorder`, `settings.textInputBorder` |
| **Derived**: follows `input.foreground` | `agentsChatInput.foreground`, `settings.numberInputForeground`, `settings.textInputForeground` |
| **Derived**: follows `input.placeholderForeground` | `agentsChatInput.placeholderForeground`, `inlineChatInput.placeholderForeground` |
| **Derived**: follows `inputOption.activeBackground` | `actionBar.toggledBackground`, `radio.activeBackground` |
| **Derived**: follows `inputOption.activeBorder` | `radio.activeBorder` |
| **Derived**: follows `inputOption.activeForeground` | `radio.activeForeground` |
| **Derived**: follows `inputOption.hoverBackground` | `radio.inactiveHoverBackground` |
| **Derived**: follows `list.activeSelectionBackground` | `banner.background`, `editorActionList.focusBackground`, `menu.selectionBackground` |
| **Derived**: follows `list.activeSelectionForeground` | `agentSessionSelectedBadge.border`, `banner.foreground`, `editorActionList.focusForeground`, `menu.selectionForeground`, `quickInputList.focusForeground` |
| **Derived**: follows `list.errorForeground` | `testing.iconErrored`, `testing.iconFailed` |
| **Derived**: follows `list.focusHighlightForeground` | `editorSuggestWidget.focusHighlightForeground`, `quickInputList.focusHighlightForeground` |
| **Derived**: follows `list.focusOutline` | `commentsView.unresolvedIcon` |
| **Derived**: follows `list.highlightForeground` | `editorHoverWidget.highlightForeground`, `editorSuggestWidget.highlightForeground`, `list.focusHighlightForeground` |
| **Derived**: follows `list.hoverBackground` | `button.secondaryBackground`, `button.secondaryHoverBackground`, `settings.focusedRowBackground`, `settings.rowHoverBackground` |
| **Derived**: follows `list.inactiveSelectionBackground` | `editorGutter.commentRangeForeground`, `editorGutter.itemBackground`, `notebook.cellBorderColor`, `notebook.selectedCellBackground`, `tab.selectedBackground`, `terminalCommandGuide.foreground` |
| **Derived**: follows `list.warningForeground` | `testing.iconQueued` |
| **Derived**: follows `menubar.selectionForeground` | `commandCenter.activeForeground` |
| **Derived**: follows `notebook.cellBorderColor` | `notebook.inactiveFocusedCellBorder`, `notebook.selectedCellBorder` |
| **Derived**: follows `notificationCenterHeader.background` | `notifications.border` |
| **Derived**: follows `notifications.background` | `notificationCenterHeader.background` |
| **Derived**: follows `panel.background` | `panelStickyScroll.background`, `scmGraph.historyItemHoverLabelForeground` |
| **Derived**: follows `panel.border` | `panelSection.border`, `profiles.sashBorder`, `settings.headerBorder`, `settings.sashBorder`, `terminal.border` |
| **Derived**: follows `panelTitle.activeForeground` | `panel.dropBorder` |
| **Derived**: follows `peekViewEditor.background` | `peekViewEditorGutter.background`, `peekViewEditorStickyScroll.background`, `peekViewEditorStickyScrollGutter.background` |
| **Derived**: follows `quickInput.list.focusBackground` | `quickInputList.focusBackground` |
| **Derived**: follows `quickInputList.focusBackground` | `editorSuggestWidget.selectedBackground` |
| **Derived**: follows `quickInputList.focusForeground` | `editorSuggestWidget.selectedForeground` |
| **Derived**: follows `radio.activeForeground` | `radio.inactiveBorder` |
| **Derived**: follows `scrollbarSlider.activeBackground` | `minimapSlider.activeBackground`, `notebookScrollbarSlider.activeBackground` |
| **Derived**: follows `scrollbarSlider.background` | `minimapSlider.background`, `notebookScrollbarSlider.background` |
| **Derived**: follows `scrollbarSlider.hoverBackground` | `minimapSlider.hoverBackground`, `notebookScrollbarSlider.hoverBackground` |
| **Derived**: follows `settings.headerForeground` | `settings.settingsHeaderHoverForeground` |
| **Derived**: follows `sideBar.background` | `agentsPanel.background`, `diffEditor.unchangedRegionBackground`, `notebook.cellEditorBackground`, `sideBarStickyScroll.background`, `sideBarTitle.background` |
| **Derived**: follows `sideBar.foreground` | `agentsNewSessionButton.foreground`, `agentsPanel.foreground`, `sideBarSectionHeader.foreground`, `sideBarTitle.foreground` |
| **Derived**: follows `statusBar.border` | `statusBar.debuggingBorder`, `statusBar.noFolderBorder` |
| **Derived**: follows `statusBar.debuggingBackground` | `commandCenter.debuggingBackground` |
| **Derived**: follows `statusBar.foreground` | `statusBar.focusBorder`, `statusBar.noFolderForeground`, `statusBarItem.focusBorder`, `statusBarItem.hoverForeground`, `statusBarItem.prominentForeground` |
| **Derived**: follows `statusBarItem.hoverBackground` | `statusBarItem.errorHoverBackground`, `statusBarItem.offlineHoverBackground`, `statusBarItem.prominentHoverBackground`, `statusBarItem.remoteHoverBackground`, `statusBarItem.warningHoverBackground` |
| **Derived**: follows `statusBarItem.hoverForeground` | `statusBarItem.errorHoverForeground`, `statusBarItem.offlineHoverForeground`, `statusBarItem.prominentHoverForeground`, `statusBarItem.remoteHoverForeground`, `statusBarItem.warningHoverForeground` |
| **Derived**: follows `statusBarItem.remoteBackground` | `ports.iconRunningProcessForeground` |
| **Derived**: follows `statusBarItem.remoteForeground` | `statusBarItem.offlineForeground` |
| **Derived**: follows `surface.border` | `editor.border` |
| **Derived**: follows `symbolIcon.fileForeground` | `terminalSymbolIcon.branchForeground`, `terminalSymbolIcon.commitForeground`, `terminalSymbolIcon.fileForeground`, `terminalSymbolIcon.pullRequestDoneForeground`, `terminalSymbolIcon.pullRequestForeground`, `terminalSymbolIcon.remoteForeground`, `terminalSymbolIcon.stashForeground`, `terminalSymbolIcon.symbolicLinkFileForeground`, `terminalSymbolIcon.symbolText`, `terminalSymbolIcon.tagForeground` |
| **Derived**: follows `symbolIcon.folderForeground` | `terminalSymbolIcon.folderForeground`, `terminalSymbolIcon.symbolicLinkFolderForeground` |
| **Derived**: follows `tab.activeBackground` | `tab.unfocusedActiveBackground` |
| **Derived**: follows `tab.activeBorderTop` | `tab.unfocusedActiveBorderTop` |
| **Derived**: follows `tab.activeForeground` | `tab.dragAndDropBorder`, `tab.selectedForeground`, `tab.unfocusedActiveForeground` |
| **Derived**: follows `tab.activeModifiedBorder` | `tab.inactiveModifiedBorder`, `tab.unfocusedActiveModifiedBorder` |
| **Derived**: follows `tab.border` | `browser.border`, `tab.divider` |
| **Derived**: follows `tab.inactiveBackground` | `tab.unfocusedInactiveBackground` |
| **Derived**: follows `tab.inactiveModifiedBorder` | `tab.unfocusedInactiveModifiedBorder` |
| **Derived**: follows `terminal.selectionBackground` | `terminal.inactiveSelectionBackground` |
| **Derived**: follows `testing.iconErrored` | `testing.iconErrored.retired` |
| **Derived**: follows `testing.iconFailed` | `testing.iconFailed.retired` |
| **Derived**: follows `testing.iconQueued` | `testing.iconQueued.retired` |
| **Derived**: follows `textLink.foreground` | `extensionIcon.verifiedForeground`, `notificationLink.foreground`, `welcomePage.progress.foreground` |
| **Derived**: follows `titleBar.activeForeground` | `commandCenter.activeBorder`, `commandCenter.border`, `commandCenter.foreground`, `menubar.selectionForeground` |
| **Derived**: follows `titleBar.inactiveForeground` | `commandCenter.inactiveBorder`, `commandCenter.inactiveForeground` |
| **Derived**: follows `toolbar.hoverBackground` | `menubar.selectionBackground`, `toolbar.activeBackground` |
| **Derived**: follows `tree.indentGuidesStroke` | `tab.lastPinnedBorder`, `tree.inactiveIndentGuidesStroke` |
| **Derived**: follows `tree.tableOddRowsBackground` | `keybindingTable.headerBackground`, `keybindingTable.rowsBackground` |
| **Derived**: transparent by default, so VS Code draws the level-1 guide or bracket colour we set | `editorBracketPairGuide.activeBackground1`, `editorBracketPairGuide.activeBackground2`, `editorBracketPairGuide.activeBackground3`, `editorBracketPairGuide.activeBackground4`, `editorBracketPairGuide.activeBackground5`, `editorBracketPairGuide.activeBackground6`, `editorBracketPairGuide.background1`, `editorBracketPairGuide.background2`, `editorBracketPairGuide.background3`, `editorBracketPairGuide.background4`, `editorBracketPairGuide.background5`, `editorBracketPairGuide.background6`, `editorIndentGuide.activeBackground2`, `editorIndentGuide.activeBackground3`, `editorIndentGuide.activeBackground4`, `editorIndentGuide.activeBackground5`, `editorIndentGuide.activeBackground6`, `editorIndentGuide.background2`, `editorIndentGuide.background3`, `editorIndentGuide.background4`, `editorIndentGuide.background5`, `editorIndentGuide.background6` |
| **Matches**: `#a0a0a0`, Dark's `ui.muted` and close to Light's `ui.indent_active` | `editorOverviewRuler.bracketMatchForeground`, `editorOverviewRuler.selectionHighlightForeground`, `editorOverviewRuler.wordHighlightForeground`, `editorOverviewRuler.wordHighlightTextForeground`, `terminalOverviewRuler.cursorForeground` |
| **Matches**: a neutral shadow, so it suits Geist too | `diffEditor.unchangedRegionShadow`, `editorStickyScroll.shadow`, `listFilterWidget.shadow`, `panelStickyScroll.shadow`, `scrollbar.shadow`, `sideBarStickyScroll.shadow`, `widget.shadow` |
| **Matches**: a translucent neutral grey, close to `ui.quiet` | `diffEditor.move.border` |
| **Matches**: an alpha that dims unused code, not a colour | `editorUnnecessaryCode.opacity` |
| **Matches**: an alpha, not a colour | `minimap.foregroundOpacity` |
| **Matches**: composites to `#131313` and `#f0f0f0`, indistinguishable from `ui.hover` | `diffEditor.unchangedCodeBackground` |
| **Matches**: the input-method underline in white or black, as `ui.foreground` | `editor.compositionBorder` |
| **Matches**: transparent, so it paints nothing | `listFilterWidget.outline` |
| **No colour**: null in both themes, so VS Code paints nothing | `activityBar.activeBackground`, `activityBar.activeFocusBorder`, `activityBarTop.activeBackground`, `activityBarTop.background`, `button.border`, `debugToolBar.border`, `diffEditor.border`, `diffEditor.insertedTextBorder`, `diffEditor.removedTextBorder`, `diffEditorGutter.insertedLineBackground`, `diffEditorGutter.removedLineBackground`, `diffEditorOverview.insertedForeground`, `diffEditorOverview.removedForeground`, `dropdown.listBackground`, `editor.findMatchForeground`, `editor.findMatchHighlightForeground`, `editor.findRangeHighlightBorder`, `editor.rangeHighlightBorder`, `editor.selectionForeground`, `editor.selectionHighlightBorder`, `editor.snippetFinalTabstopHighlightBackground`, `editor.snippetTabstopHighlightBorder`, `editor.symbolHighlightBorder`, `editor.wordHighlightBorder`, `editor.wordHighlightStrongBorder`, `editor.wordHighlightTextBorder`, `editorBracketMatch.foreground`, `editorCursor.background`, `editorError.background`, `editorError.border`, `editorGhostText.background`, `editorGhostText.border`, `editorGroup.dropIntoPromptBorder`, `editorGroup.emptyBackground`, `editorGroup.focusedEmptyBorder`, `editorGroupHeader.border`, `editorGroupHeader.tabsBorder`, `editorHint.border`, `editorInfo.background`, `editorInfo.border`, `editorLineNumber.dimmedForeground`, `editorMultiCursor.primary.background`, `editorMultiCursor.secondary.background`, `editorOverviewRuler.background`, `editorStickyScroll.border`, `editorSuggestWidget.focusOutline`, `editorSuggestWidget.selectedIconForeground`, `editorUnicodeHighlight.background`, `editorUnnecessaryCode.border`, `editorWarning.background`, `editorWarning.border`, `editorWidget.resizeBorder`, `inputValidation.errorForeground`, `inputValidation.infoForeground`, `inputValidation.warningForeground`, `list.activeSelectionIconForeground`, `list.focusAndSelectionOutline`, `list.focusBackground`, `list.focusForeground`, `list.hoverForeground`, `list.inactiveFocusBackground`, `list.inactiveFocusOutline`, `list.inactiveSelectionForeground`, `list.inactiveSelectionIconForeground`, `menu.selectionBorder`, `menubar.selectionBorder`, `minimap.background`, `notificationCenter.border`, `notificationCenterHeader.foreground`, `notificationToast.border`, `outputView.background`, `outputViewStickyScroll.background`, `panelSectionHeader.border`, `panelSectionHeader.foreground`, `panelStickyScroll.border`, `panelTitle.border`, `peekViewEditor.matchHighlightBorder`, `quickInputList.focusIconForeground`, `radio.inactiveBackground`, `radio.inactiveForeground`, `scrollbar.background`, `sideBarActivityBarTop.border`, `sideBarSectionHeader.border`, `sideBarStickyScroll.border`, `sideBarTitle.border`, `statusBar.inactiveBackground`, `tab.activeBorder`, `tab.hoverBackground`, `tab.hoverBorder`, `tab.hoverForeground`, `tab.unfocusedActiveBorder`, `tab.unfocusedHoverBackground`, `tab.unfocusedHoverBorder`, `tab.unfocusedHoverForeground`, `terminal.selectionForeground`, `terminal.tab.activeBorder`, `terminalCursor.background`, `terminalStickyScroll.background`, `terminalStickyScroll.border`, `textPreformat.border`, `toolbar.hoverOutline`, `widget.border`, `window.activeBorder`, `window.inactiveBorder` |
| **Not targeted**: AI: chat, inline chat, agents, inline edits, MCP | `agentsNewSessionButton.background`, `agentsNewSessionButton.hoverBackground`, `agentsWindowGraphic.orange`, `chat.avatarBackground`, `chat.checkpointSeparator`, `chat.editedFileForeground`, `chat.fusionBadgeForeground`, `chat.fusionBadgeGradientEnd`, `chat.fusionBadgeGradientStart`, `chat.linesAddedForeground`, `chat.linesRemovedForeground`, `chat.mcpCompatibilityWarningForeground`, `chat.requestBorder`, `chat.requestCodeBorder`, `chat.sessionStateIndicator.needsInputBorder`, `chat.sessionStateIndicator.unvisitedBorder`, `chat.slashCommandBackground`, `chat.slashCommandForeground`, `chat.thinkingShimmer`, `chat.voiceListeningGlow`, `chat.voiceSpeakingGlow`, `chat.workingProgressInsidersIconForeground`, `chat.workingProgressStableIconForeground`, `editorLightBulbAi.foreground`, `editorMinimap.inlineChatInserted`, `editorOverviewRuler.inlineChatInserted`, `editorOverviewRuler.inlineChatRemoved`, `inlineChat.shadow`, `inlineChatDiff.inserted`, `inlineChatDiff.removed`, `inlineEdit.gutterIndicator.background`, `inlineEdit.modifiedBackground`, `inlineEdit.modifiedBorder`, `inlineEdit.modifiedChangedLineBackground`, `inlineEdit.modifiedChangedTextBackground`, `inlineEdit.originalBackground`, `inlineEdit.originalBorder`, `inlineEdit.originalChangedLineBackground`, `inlineEdit.originalChangedTextBackground`, `inlineEdit.tabWillAcceptModifiedBorder`, `inlineEdit.tabWillAcceptOriginalBorder`, `interactive.activeCodeBorder`, `mcpIcon.starForeground` |
| **Not targeted**: Charts | `chart.axis`, `chart.guide`, `chart.line`, `charts.green`, `charts.orange`, `charts.purple` |
| **Not targeted**: Comments | `editorCommentsWidget.replyInputBackground` |
| **Not targeted**: Deprecated | `editorActiveLineNumber.foreground`, `modernActivityBar.activeBackground`, `modernActivityBar.activeForeground`, `modernActivityBar.hoverBackground`, `modernActivityBar.hoverForeground`, `quickInput.list.focusBackground` |
| **Not targeted**: Extensions view and marketplace | `extensionIcon.preReleaseForeground`, `extensionIcon.privateForeground`, `extensionIcon.sponsorForeground`, `extensionIcon.starForeground` |
| **Not targeted**: High contrast only | `contrastActiveBorder`, `contrastBorder` |
| **Not targeted**: Merge conflicts and merge editor | `editorOverviewRuler.commonContentForeground`, `editorOverviewRuler.currentContentForeground`, `editorOverviewRuler.incomingContentForeground`, `merge.border`, `merge.commonContentBackground`, `merge.commonHeaderBackground`, `merge.currentContentBackground`, `merge.currentHeaderBackground`, `merge.incomingContentBackground`, `merge.incomingHeaderBackground`, `mergeEditor.change.background`, `mergeEditor.change.word.background`, `mergeEditor.changeBase.background`, `mergeEditor.changeBase.word.background`, `mergeEditor.conflict.handled.minimapOverViewRuler`, `mergeEditor.conflict.handledFocused.border`, `mergeEditor.conflict.handledUnfocused.border`, `mergeEditor.conflict.input1.background`, `mergeEditor.conflict.input2.background`, `mergeEditor.conflict.unhandled.minimapOverViewRuler`, `mergeEditor.conflict.unhandledFocused.border`, `mergeEditor.conflict.unhandledUnfocused.border`, `mergeEditor.conflictingLines.background` |
| **Not targeted**: Notebooks | `notebook.cellHoverBackground`, `notebook.cellStatusBarItemHoverBackground`, `notebook.cellToolbarSeparator`, `notebook.focusedCellBackground`, `notebook.inactiveSelectedCellBorder`, `notebook.outputContainerBackgroundColor`, `notebook.outputContainerBorderColor`, `notebook.symbolHighlightBackground`, `notebookEditorOverviewRuler.runningCellForeground`, `notebookStatusErrorIcon.foreground`, `notebookStatusSuccessIcon.foreground` |
| **Not targeted**: Profiles | `profileBadge.background`, `profileBadge.foreground` |
| **Not targeted**: SCM graph | `scmGraph.foreground1`, `scmGraph.foreground2`, `scmGraph.foreground3`, `scmGraph.foreground4`, `scmGraph.foreground5`, `scmGraph.historyItemBaseRefColor`, `scmGraph.historyItemHoverAdditionsForeground`, `scmGraph.historyItemHoverDeletionsForeground`, `scmGraph.historyItemRemoteRefColor` |
| **Not targeted**: Terminal suggest | `terminalSymbolIcon.aliasForeground`, `terminalSymbolIcon.argumentForeground`, `terminalSymbolIcon.flagForeground`, `terminalSymbolIcon.inlineSuggestionForeground`, `terminalSymbolIcon.methodForeground`, `terminalSymbolIcon.optionForeground`, `terminalSymbolIcon.optionValueForeground` |
| **Not targeted**: Testing | `testing.coveredBackground`, `testing.coveredBorder`, `testing.coveredGutterBackground`, `testing.coveredMinimapBackground`, `testing.iconPassed`, `testing.iconPassed.retired`, `testing.iconSkipped`, `testing.iconSkipped.retired`, `testing.iconUnset`, `testing.iconUnset.retired`, `testing.message.error.badgeBackground`, `testing.message.error.badgeBorder`, `testing.message.error.badgeForeground`, `testing.message.error.lineBackground`, `testing.message.info.lineBackground`, `testing.runAction`, `testing.uncoveredBackground`, `testing.uncoveredBorder`, `testing.uncoveredBranchBackground`, `testing.uncoveredGutterBackground`, `testing.uncoveredMinimapBackground` |
| **Not targeted**: Welcome page and walkthroughs | `walkThrough.embeddedEditorBackground`, `walkthrough.stepTitle.foreground`, `welcomePage.background`, `welcomePage.tileBorder` |

## Xcode 27

Audited against Xcode 27.2. A recipe accepts 41 override tokens, and Geist sets all of them. Xcode computes everything else from the recipe's palette.

| Reason | Keys |
| --- | --- |
| **Derived**: they scale the chroma of colours computed from `primary` and `secondary`, and every text colour and editor fill is overridden | `palette.primaryIntensity`, `palette.secondaryIntensity` |
| **Derived**: hue-only tints mirroring override tokens Geist sets, or neutrals from `palette.secondary` | `tintHueOverrides` `background`, `foreground`, `secondaryBackground`, `secondaryForeground`, `tertiaryBackground`, `tertiaryForeground`, and the 20 mirrored tokens |
| **Matches**: system hues from the same families as Geist's status colours | `tintHueOverrides` `analyzer`, `error`, `runtimeIssue`, `success`, `warning` |
| **No reader**: no binary in Xcode 27.2 contains the key | `palette.colorGranularity` |
| **Not targeted**: Geist ships one recipe per appearance | `darkPalette`, `lightPalette`, `showsInAllColorSchemes` |
| **Not targeted**: presets in the editor's hue picker, not surfaces | `tintHueOverrides` `accent`, `blue`, `brown`, `cyan`, `darkBlue`, `golden`, `green`, `indigo`, `magenta`, `mint`, `orange`, `pink`, `red`, `steel`, `swift`, `systemPurple`, `teal`, `xcodePurple`, `yellow` |
| **Fixed**: below 4.5:1, see ADR 0004 | line numbers (`sourceTextSidebarNumbersColor`) |
| **Fixed**: behind syntax text, which in Geist Light falls below 4.5:1 for comments and types, see ADR 0004 | inactive selection and symbol highlight (`sourceTextInactiveSelectionColor`) |
| **Fixed**: they measure as `ui.background` and `ui.foreground` | caret-row line number, gutter (`sourceTextSidebarBackgroundColor`) |
| **Fixed**: not yet measured, see ADR 0004 | accent, dividers, gutter edge, inline code in Markdown, quaternary and quinary fills |

## Zed

Audited against Zed 1.27.0. Zed refines a theme over its built-in default colours (`crates/theme/src/default_colors.rs`), not over One Dark or One Light. Syntax isn't merged with any base: a capture Geist doesn't cover takes the longest prefix Geist does, or else `editor.foreground`.

| Reason | Keys |
| --- | --- |
| **Derived**: `panel.background` blended with `element.hover` | `panel.overlay_hover` |
| **Derived**: `panel.background`, made opaque | `panel.overlay_background` |
| **Derived**: follows `editor.document_highlight.read_background` | `vim.yank.background` |
| **Derived**: follows `error` | `vim.helix_jump_label.foreground` |
| **Derived**: follows `modified`, which equals `renamed` in Geist | `version_control.renamed` |
| **Derived**: follows the matching status colour | `version_control.added`, `version_control.deleted`, `version_control.ignored`, `version_control.modified` |
| **Derived**: inlay hints fall back to `hint` and `hint.background` | `syntax.hint` |
| **Derived**: the first player's selection, `ui.selection_overlay` | `element.selection_background` |
| **Derived**: the scrollbar thumb colours, capped at 70% alpha | `minimap.thumb.active_background`, `minimap.thumb.background`, `minimap.thumb.hover_background` |
| **Derived**: the status colour at 36% (Dark) or 48% (Light), a border with no text on it | `editor.diff_hunk.added.hollow_border`, `editor.diff_hunk.deleted.hollow_border` |
| **Derived**: the status colour at 6% (Dark) or 8% (Light), fainter than the tint | `editor.diff_hunk.added.hollow_background`, `editor.diff_hunk.deleted.hollow_background` |
| **Derived**: Zed draws code lenses in `text.muted` | `editor.code_lens.foreground` |
| **Derived**: Zed matches the longest prefix Geist sets, `attribute` | `syntax.attribute.builtin`, `syntax.attribute.jsx`, `syntax.attribute.special` |
| **Derived**: Zed matches the longest prefix Geist sets, `constant` | `syntax.constant.builtin` |
| **Derived**: Zed matches the longest prefix Geist sets, `diff.delta` | `syntax.diff.delta.moved` |
| **Derived**: Zed matches the longest prefix Geist sets, `emphasis.strong` | `syntax.emphasis.strong.markup` |
| **Derived**: Zed matches the longest prefix Geist sets, `emphasis` | `syntax.emphasis.markup` |
| **Derived**: Zed matches the longest prefix Geist sets, `function` | `syntax.function.call`, `syntax.function.decorator`, `syntax.function.decorator.call`, `syntax.function.definition`, `syntax.function.kwargs`, `syntax.function.method`, `syntax.function.method.call`, `syntax.function.method.constructor`, `syntax.function.special`, `syntax.function.special.definition` |
| **Derived**: Zed matches the longest prefix Geist sets, `keyword` | `syntax.keyword.control`, `syntax.keyword.declaration`, `syntax.keyword.definition`, `syntax.keyword.directive`, `syntax.keyword.import`, `syntax.keyword.jsdoc`, `syntax.keyword.operator`, `syntax.keyword.operator.regex`, `syntax.keyword.preproc` |
| **Derived**: Zed matches the longest prefix Geist sets, `label` | `syntax.label.regex` |
| **Derived**: Zed matches the longest prefix Geist sets, `link_text` | `syntax.link_text.markup` |
| **Derived**: Zed matches the longest prefix Geist sets, `link_uri` | `syntax.link_uri.markup` |
| **Derived**: Zed matches the longest prefix Geist sets, `number` | `syntax.number.quantifier.regex` |
| **Derived**: Zed matches the longest prefix Geist sets, `operator` | `syntax.operator.regex`, `syntax.operator.spaceship` |
| **Derived**: Zed matches the longest prefix Geist sets, `property` | `syntax.property.json_key`, `syntax.property.name` |
| **Derived**: Zed matches the longest prefix Geist sets, `punctuation` | `syntax.punctuation.bracket`, `syntax.punctuation.bracket.jsx`, `syntax.punctuation.bracket.regex`, `syntax.punctuation.delimiter`, `syntax.punctuation.delimiter.jsx`, `syntax.punctuation.delimiter.regex`, `syntax.punctuation.embedded.markup`, `syntax.punctuation.list_marker`, `syntax.punctuation.list_marker.markup`, `syntax.punctuation.markup`, `syntax.punctuation.special` |
| **Derived**: Zed matches the longest prefix Geist sets, `selector` | `syntax.selector.class`, `syntax.selector.id`, `syntax.selector.pseudo` |
| **Derived**: Zed matches the longest prefix Geist sets, `string.escape` | `syntax.string.escape.regex` |
| **Derived**: Zed matches the longest prefix Geist sets, `string.special` | `syntax.string.special.path` |
| **Derived**: Zed matches the longest prefix Geist sets, `string` | `syntax.string.doc` |
| **Derived**: Zed matches the longest prefix Geist sets, `tag` | `syntax.tag.component.jsx`, `syntax.tag.jsx` |
| **Derived**: Zed matches the longest prefix Geist sets, `text.literal` | `syntax.text.literal.markup` |
| **Derived**: Zed matches the longest prefix Geist sets, `title` | `syntax.title.markup` |
| **Derived**: Zed matches the longest prefix Geist sets, `type` | `syntax.type.class`, `syntax.type.class.builtin`, `syntax.type.class.call`, `syntax.type.class.definition`, `syntax.type.class.inheritance`, `syntax.type.definition`, `syntax.type.interface`, `syntax.type.jsdoc`, `syntax.type.name`, `syntax.type.unit` |
| **Derived**: Zed matches the longest prefix Geist sets, `variable` | `syntax.variable.jsdoc`, `syntax.variable.other.member` |
| **Matches**: deliberately unstyled, so it takes `editor.foreground` | `syntax.none` |
| **Matches**: transparent, so it paints nothing | `minimap.thumb.border`, `scrollbar.thumb.border` |
| **Matches**: unstyled, so it takes `editor.foreground` | `syntax.embedded`, `syntax.markup.link.url`, `syntax.strikethrough.markup`, `syntax.text`, `syntax.text.jsx` |
| **No reader**: edit predictions use `predictive` | `syntax.predictive` |
| **No reader**: no capture or code uses it | `syntax.primary` |
| **Not targeted**: Vim and Helix mode indicators, transparent by default | `vim.helix_normal.background`, `vim.helix_normal.foreground`, `vim.helix_select.background`, `vim.helix_select.foreground`, `vim.insert.background`, `vim.insert.foreground`, `vim.normal.background`, `vim.normal.foreground`, `vim.replace.background`, `vim.replace.foreground`, `vim.visual.background`, `vim.visual.foreground`, `vim.visual_block.background`, `vim.visual_block.foreground`, `vim.visual_line.background`, `vim.visual_line.foreground` |
| **Not targeted**: window blur and transparency; the default is opaque | `background.appearance` |
