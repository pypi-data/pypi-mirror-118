# Next Stroke Suggestions for Plover
[![PyPI](https://img.shields.io/pypi/v/plover-next-stroke)](https://pypi.org/project/plover-next-stroke/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/plover-next-stroke)
![GitHub](https://img.shields.io/github/license/Kaoffie/plover_next_stroke)

This is a plugin that displays the possible options for the next few strokes.

![](https://user-images.githubusercontent.com/30435273/130559245-0290a428-57cf-4ffe-b88f-906811557d70.png)

## Installation

This plugin can't be installed from the Plover Plugin Manager yet. Use the following command to install the plugin:

```
plover -s plover_plugins install plover-next-stroke
```


## Usage Notes

### Macro Strokes & Shortcuts

To make full use of the plugin, you'll have to define a few additional entries in your dictionary to navigate the menu (They won't be added automatically!). The recommended strokes are just what I use personally, so it's okay if you'd like to use something else.

| Action             | Dictionary Definition | Recommended Stroke |
|--------------------|-----------------------|--------------------|
| Next Page          | `=ns_next_page`       | `#WR`              |
| Previous Page      | `=ns_prev_page`       | `1K`               |
| Reload Suggestions | `=ns_reload`          | `1KWR`             |

Since the plugin keeps an internal copy of your dictionaries to load suggestions quicker, you'll have to manually reload this internal copy with a reload stroke whenever you add or delete entries to/from any of your dictionaries. You don't need to trigger a manual update if you're switching languages or activating/deactivating dictionaries.

### Display Order Types

| Display Order | Explanation |
|---|---|
| Frequency | Order by lowest stroke count first, then when stroke counts are equal, order by most frequent first based on system orthography list (if available) |
| Frequency (Prioritize Numbers) | Same as Frequency, but strokes containing numbers are prioritized and ordered by numeric value. |
| Frequency (Prioritize Non-numberic) | Same as Frequency, but strokes containing numbers are pushed to the back. |
| Stroke Count | Order by lowest stroke count first, preserving original dictionary order. |
| Alphabetical | Order by translation alphabetically. |
| System Defined | Order defined by the system. The default English stenotype system doesn't have a defined display order. Defaults to Frequency. |

### System-defined functions

If you're designing a language system for Plover and you'd like to customize the display order and format (for instance, converting certain strokes to numbers), you may do so by including these functions in your system file:

```py
def NS_STROKE_FORMATTER(stroke: str) -> str:
    """Formats single strokes, such as STROEBG"""
    return ...

def NS_TRANSLATION_FORMATTER(translation: str) -> str:
    """Formats the translated string, such as 'stroke'"""
    return ...

def NS_SORTER(entry: Tuple[Tuple[str], str]) -> int:
    """
    Scores outline-translation pairs, such as (("TRAPBS", "HRAEUT"), "translate")

    Pairs are ordered from smallest to biggest;
    it need not be an int - anything that can be compared
    works, including strings or tuples of ints.
    """
    outline, translation = entry
    return ...
```

All next stroke suggestions will be run through the two formatters (if available) before being sorted. The sorter will only be used if the user changes their display order to "System Defined".

## License & Credits

This plugin is licensed under the MIT license.

The icons used in this plugin are taken from [Icons8 Flat Color Icons](https://github.com/icons8/flat-color-icons).