# YAML_Plate

<img src="https://i.imgur.com/hZcl3uS.png" width="160" align="right">

> A fork of <a href="https://github.com/delivrance/plate">Plate</a> (Internationalization library for Python), for YAML

**YAML Plate** (**YAML** **P**ython trans**late**) is an i18n library for Python that gives your application the ability to
speak many languages. It is designed to be simple and straightforward to use for **developers** and easy for
**translators**.

Full credits go to [Dan](https://github.com/delivrance) and other contributors of the original Plate.

## Features

- Translations based on YAML files
- Interpolated translations
- Pluralization
- Emoji

## Installing

``` shell
$ pip3 install YAML-Plate
```

## Setup

Plate is not going to perform any translation; what it does, instead, is simply providing a way to manage
already-translated phrases so that they can be easily accessed from your application code.

These translated phrases are kept in YAML files stored in a folder inside the application working directory and
organized by their respective language codes. The YAML keys are in common to all translations and the values
of each contain the translated phrases.

1. Create a new `locales` folder in your working directory to store translation files.
2. Put files named after their language codes: `en_US.yaml`, `it_IT.yaml`, and so on. All available language codes can
   be found [here](yaml_plate/languages.py).
3. Start adding new phrases and translations. Here's an example for `en_US.yaml` and `it_IT.yaml`
    ``` yaml
    hello: Hello
    morning: Good morning, {name}
    drink: Let's drink :SAKE: together
    apples: No apples | One apple | {count} apples
    ```
    ``` yaml
    hello: Ciao
    morning: Buongiorno, {name}
    drink: Beviamo :SAKE: insieme
    apples: Nessuna mela | Una mela | {count} mele
    ```

## Usage
 
### Instantiation

First of all, create a new `Plate` instance. Plate will automatically look for files inside the `locales` folder
or another custom folder you pass to the *root* parameter. The default and the fallback locale is `en_US`, by default.

``` python
from yaml_plate import Plate

plate = Plate()
```

### Translation

Translate a phrase by simply passing a key and a language code of the destination locale.

``` python
plate("hello", "it_IT")  # Ciao
```

You can also set a new default locale to have all subsequent translations in that language.

``` python
plate.set_locale("it_IT")
plate("hello")  # Ciao
```

Or, get a translator for a given locale instead, so that the default locale will be kept unchanged.

``` python
italian = plate.get_translator("it_IT")
italian("hello")  # Ciao
```

**Note**: The examples below will assume `plate.set_locale("it_IT")` for conciseness.

### Interpolation

Pass named arguments to interpolate your translations.

``` python
plate("morning", name="Dan")  # Buongiorno, Dan
```

### Emoji

Emoji can be added with `:EMOJI_NAME:` inside your sources and are automatically inserted with the actual values.
All available emoji can be found [here](yaml_plate/emojipedia.py). You can search for, visualize them and grab their
names at https://emojipedia.org/.

``` python
plate("drink")  # Beviamo 🍶 insieme
```

### Pluralization

Pluralization is done by keeping all the plural cases separated by a pipe `|` (by default, customizable) and by using the special interpolation
key `{count}`. The following example shows how to translate and pluralize a phrase for count cases of zero, one and more.

``` python
plate("apples", count=0)  # Nessuna mela
plate("apples", count=1)  # Una mela
plate("apples", count=7)  # 7 mele
```

## License

MIT © 2020 [Dan](https://github.com/delivrance)
MIT © 2021 [Gegham Zakaryan](https://github.com/zakaryan2004)
