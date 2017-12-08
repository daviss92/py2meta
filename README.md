# py3meta
A python 3 wrapper for Phil Harvey's Exiftool.

## Prerequisites

What things you need to utilize py3meta:

[Exiftool](https://www.sno.phy.queensu.ca/~phil/exiftool/) - ExifTool is a platform-independent Perl library plus a command-line application for reading, writing and editing meta information in a wide variety of files.

## py3exifcopy

Currently under construction

## py3exifread

All read functions require a return type. Specify 'string', 'list', or 'dict'. If left out, default is 'string'.

### all_contains

`all_contains()` allows you to output all metadata within a given file that contains a particular string.

### all_data

`all_data()` allows you to output all metadata within a given file.

### all_duplicates

`all_duplicates()` outputs all metadata, including any duplicate tags.

### common

`common()` allows you to output all common metadata information.

### keywords

`keywords()` outputs keywords within a given file.

### custom

`all_contains()` allows you to read any metadata specified by custom arguments input by the user.

To use this, visit [Exiftool's Official Website](https://www.sno.phy.queensu.ca/~phil/exiftool/) for examples and a full list of available tag names and resources.

Arguments entered must be entered as a string. E.g. '-b -PreviewImage -w \_preview.jpg -ext cr2 -r'

## py3exifwrite

Currently under construction

## License

This project is licensed under the GNU General Public License - see the [LICENSE.md](LICENSE.md) file for details.
