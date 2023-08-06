#!/usr/bin/env python3

"""PIE-Office: (Proto-)Indo-European Office

A terminal based script converter for ancient (Proto-)Indo-European languages.

Usage:
    pieoffice convert <language> <text> [--type TYPE]
    pieoffice rules <language>
    pieoffice list
    pieoffice --help

Languages:
    pie                             Proto-Indo-European
    greek                           Polytonic Greek
    linearb                         Mycenaean Libear B
    cypriot                         Cypriot Greek Script
    luwian                          Hieroglyphic Luwian
    lycian                          Lycian
    lydian                          Lydian
    carian                          Carian
    gothic                          Gothic
    armenian                        Armenian
    vedic / sanskrit                Vedic / Sanskrit (entry with Harvard-Kyoto)
    avestan                         Avestan
    oldpersian                      Old Persian Cuneiform
    ogham                           Ogham Script
    oscan                           Oscan (Old Italic Script)

Options:
    -t --type           Type of transliteration
    -h --help           Show this screen.

"""

from docopt import docopt

def main():
    arguments = docopt(__doc__)

    rules = False

    if arguments["convert"]:
        language = arguments["<language>"]
        # print(arguments["--type"])
        if language == "pie":
            from pieoffice.pie import alpha_to_pie as conv
        if language == "greek":
            from pieoffice.greek import alpha_to_greek as conv
        if language == "linearb":
            from pieoffice.linearb import alpha_to_linearb as conv
        elif language == "luwian":
            from pieoffice.luwian import alpha_to_luwian as conv
        elif language == "lycian":
            from pieoffice.lycian import alpha_to_lycian as conv
        elif language == "lydian":
            from pieoffice.lydian import alpha_to_lydian as conv
        elif language == "carian":
            from pieoffice.carian import alpha_to_carian as conv
        elif language == "gothic":
            from pieoffice.gothic import alpha_to_gothic as conv
        elif language == "armenian":
            from pieoffice.armenian import AsciiConverter
            if arguments["TYPE"] == "iso":
                ascii_conv = AsciiConverter("iso")
            elif arguments["TYPE"] == "classical":
                ascii_conv = AsciiConverter("classical")
            elif arguments["TYPE"] == "maiscules":
                ascii_conv = AsciiConverter("armenian_maiscules")
            else:
                ascii_conv = AsciiConverter()
            conv = ascii_conv.converter
        elif language == "vedic" or language == "sanskrit":
            from pieoffice.vedic import AsciiConverter
            if arguments["TYPE"] == "iso":
                ascii_conv = AsciiConverter("hk_to_iso")
            elif arguments["TYPE"] == "iast":
                ascii_conv = AsciiConverter("hk_to_iast")
            else:
                ascii_conv = AsciiConverter()
            conv = ascii_conv.converter
        elif language == "avestan":
            from pieoffice.avestan import AsciiConverter
            if arguments["TYPE"] == "translit":
                ascii_conv = AsciiConverter("roman-hoffman")
            else:
                ascii_conv = AsciiConverter("script")
            conv = ascii_conv.converter
        elif language == "oldpersian":
            from pieoffice.oldpersian import alpha_to_oldpersian as conv
        elif language == "ogham":
            from pieoffice.ogham import alpha_to_ogham as conv
        elif language == "oscan":
            from pieoffice.oscan import alpha_to_oscan as conv
        elif language == "cypriot":
            from pieoffice.cypriot import alpha_to_cypriot as conv


        if arguments['<text>']:
            print(conv(arguments['<text>']))
        else:
            print("Insert a text.")
            rules = True


    if arguments['rules'] or rules:
        language = arguments["<language>"]
        if language == "pie":
            from pieoffice.pie import __doc__ as doc
        if language == "greek":
            from pieoffice.greek import __doc__ as doc
        if language == "linearb":
            from pieoffice.linearb import __doc__ as doc
        elif language == "luwian":
            from pieoffice.luwian import __doc__ as doc
        elif language == "lycian":
            from pieoffice.lycian import __doc__ as doc
        elif language == "lydian":
            from pieoffice.lydian import __doc__ as doc
        elif language == "carian":
            from pieoffice.carian import __doc__ as doc
        elif language == "gothic":
            from pieoffice.gothic import __doc__ as doc
        elif language == "armenian":
            from pieoffice.armenian import __doc__ as doc
        elif language == "avestan" or language == "avestantranslit":
            from pieoffice.avestan import __doc__ as doc
        elif language in ["vedic", "vedictranslit", "sanskrit", "sanskrithk"]:
            from pieoffice.vedic import __doc__ as doc
        elif language == "oldpersian":
            from pieoffice.oldpersian import __doc__ as doc
        elif language == "ogham":
            from pieoffice.ogham import __doc__ as doc
        elif language == "oscan":
            from pieoffice.oscan import __doc__ as doc
        elif language == "cypriot":
            from pieoffice.cypriot import __doc__ as doc
        print(doc)

    if arguments['list']:
        print("""Languages:
            pie                             Proto-Indo-European
            greek                           Polytonic Greek
            linearb                         Mycenaean Libear B
            cypriot                         Cypriot Greek Script
            luwian                          Hieroglyphic Luwian
            lycian                          Lycian
            lydian                          Lydian
            carian                          Carian
            gothic                          Gothic
            armenian                        Armenian
            vedic / sanskrit                Vedic / Sanskrit (HK>Devanagari)
            vedictranslit /sanskrithk       Vedic / Sanskrit (HK>IAST)
            avestan                         Avestan (script)
            avestantranslit                 Avestan (romanized)
            oldpersian                      Old Persian Cuneiform
            ogham                           Ogham Script
            oscan                           Oscan (Old Italic Script)
            """
            )


if __name__ == "__main__":
    main()
