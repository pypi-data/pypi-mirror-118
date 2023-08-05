"""Command line interface for osxphotos """

import code
import csv
import datetime
import json
import os
import os.path
import pathlib
import pprint
import shlex
import subprocess
import sys
import time

import bitmath
import click
import osxmetadata
import photoscript
import rich.traceback
import yaml
from rich import pretty

import osxphotos

from ._constants import (
    _EXIF_TOOL_URL,
    _OSXPHOTOS_NONE_SENTINEL,
    _PHOTOS_4_VERSION,
    _UNKNOWN_PLACE,
    CLI_COLOR_ERROR,
    CLI_COLOR_WARNING,
    DEFAULT_EDITED_SUFFIX,
    DEFAULT_JPEG_QUALITY,
    DEFAULT_ORIGINAL_SUFFIX,
    DEFAULT_PREVIEW_SUFFIX,
    EXTENDED_ATTRIBUTE_NAMES,
    EXTENDED_ATTRIBUTE_NAMES_QUOTED,
    OSXPHOTOS_EXPORT_DB,
    OSXPHOTOS_URL,
    POST_COMMAND_CATEGORIES,
    SIDECAR_EXIFTOOL,
    SIDECAR_JSON,
    SIDECAR_XMP,
)
from ._version import __version__
from .cli_help import ExportCommand, tutorial_help
from .configoptions import (
    ConfigOptions,
    ConfigOptionsInvalidError,
    ConfigOptionsLoadError,
)
from .datetime_formatter import DateTimeFormatter
from .exiftool import get_exiftool_path
from .export_db import ExportDB, ExportDBInMemory
from .fileutil import FileUtil, FileUtilNoOp
from .path_utils import is_valid_filepath, sanitize_filename, sanitize_filepath
from .photoinfo import ExportResults
from .photokit import check_photokit_authorization, request_photokit_authorization
from .photosalbum import PhotosAlbum
from .phototemplate import PhotoTemplate, RenderOptions
from .queryoptions import QueryOptions
from .uti import get_preferred_uti_extension
from .utils import expand_and_validate_filepath, load_function

# global variable to control verbose output
# set via --verbose/-V
VERBOSE = False

rich.traceback.install()


def verbose_(*args, **kwargs):
    """print output if verbose flag set"""
    if VERBOSE:
        styled_args = []
        for arg in args:
            if type(arg) == str:
                if "error" in arg.lower():
                    arg = click.style(arg, fg=CLI_COLOR_ERROR)
                elif "warning" in arg.lower():
                    arg = click.style(arg, fg=CLI_COLOR_WARNING)
            styled_args.append(arg)
        click.echo(*styled_args, **kwargs)


def get_photos_db(*db_options):
    """Return path to photos db, select first non-None db_options
    If no db_options are non-None, try to find library to use in
    the following order:
    - last library opened
    - system library
    - ~/Pictures/Photos Library.photoslibrary
    - failing above, returns None
    """
    if db_options:
        for db in db_options:
            if db is not None:
                return db

    # if get here, no valid database paths passed, so try to figure out which to use
    db = osxphotos.utils.get_last_library_path()
    if db is not None:
        click.echo(f"Using last opened Photos library: {db}", err=True)
        return db

    db = osxphotos.utils.get_system_library_path()
    if db is not None:
        click.echo(f"Using system Photos library: {db}", err=True)
        return db

    db = os.path.expanduser("~/Pictures/Photos Library.photoslibrary")
    if os.path.isdir(db):
        click.echo(f"Using Photos library: {db}", err=True)
        return db
    else:
        return None


class DateTimeISO8601(click.ParamType):

    name = "DATETIME"

    def convert(self, value, param, ctx):
        try:
            return datetime.datetime.fromisoformat(value)
        except Exception:
            self.fail(
                f"Invalid datetime format {value}. "
                "Valid format: YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]"
            )


class BitMathSize(click.ParamType):

    name = "BITMATH"

    def convert(self, value, param, ctx):
        try:
            value = bitmath.parse_string(value)
        except ValueError:
            # no units specified
            try:
                value = int(value)
                value = bitmath.Byte(value)
            except ValueError as e:
                self.fail(
                    f"{value} must be specified as bytes or using SI/NIST units. "
                    + "For example, the following are all valid and equivalent sizes: '1048576' '1.048576MB', '1 MiB'."
                )
        return value


class TimeISO8601(click.ParamType):

    name = "TIME"

    def convert(self, value, param, ctx):
        try:
            return datetime.time.fromisoformat(value).replace(tzinfo=None)
        except Exception:
            self.fail(
                f"Invalid time format {value}. "
                "Valid format: HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]] "
                "however, note that timezone will be ignored."
            )


class FunctionCall(click.ParamType):
    name = "FUNCTION"

    def convert(self, value, param, ctx):
        if "::" not in value:
            self.fail(
                f"Could not parse function name from '{value}'. "
                "Valid format filename.py::function"
            )

        filename, funcname = value.split("::")

        filename_validated = expand_and_validate_filepath(filename)
        if not filename_validated:
            self.fail(f"'{filename}' does not appear to be a file")

        try:
            function = load_function(filename_validated, funcname)
        except Exception as e:
            self.fail(f"Could not load function {funcname} from {filename_validated}")

        return (function, value)


# Click CLI object & context settings
class CLI_Obj:
    def __init__(self, db=None, json=False, debug=False):
        if debug:
            osxphotos._set_debug(True)
        self.db = db
        self.json = json


CTX_SETTINGS = dict(help_option_names=["-h", "--help"])
DB_OPTION = click.option(
    "--db",
    required=False,
    metavar="<Photos database path>",
    default=None,
    help=(
        "Specify Photos database path. "
        "Path to Photos library/database can be specified using either --db "
        "or directly as PHOTOS_LIBRARY positional argument. "
        "If neither --db or PHOTOS_LIBRARY provided, will attempt to find the library "
        "to use in the following order: 1. last opened library, 2. system library, 3. ~/Pictures/Photos Library.photoslibrary"
    ),
    type=click.Path(exists=True),
)

DB_ARGUMENT = click.argument("photos_library", nargs=-1, type=click.Path(exists=True))

JSON_OPTION = click.option(
    "--json",
    "json_",
    required=False,
    is_flag=True,
    default=False,
    help="Print output in JSON format.",
)


def deleted_options(f):
    o = click.option
    options = [
        o(
            "--deleted",
            is_flag=True,
            help="Include photos from the 'Recently Deleted' folder.",
        ),
        o(
            "--deleted-only",
            is_flag=True,
            help="Include only photos from the 'Recently Deleted' folder.",
        ),
    ]
    for o in options[::-1]:
        f = o(f)
    return f


def QUERY_OPTIONS(f):
    o = click.option
    options = [
        o(
            "--keyword",
            metavar="KEYWORD",
            default=None,
            multiple=True,
            help="Search for photos with keyword KEYWORD. "
            'If more than one keyword, treated as "OR", e.g. find photos matching any keyword',
        ),
        o(
            "--person",
            metavar="PERSON",
            default=None,
            multiple=True,
            help="Search for photos with person PERSON. "
            'If more than one person, treated as "OR", e.g. find photos matching any person',
        ),
        o(
            "--album",
            metavar="ALBUM",
            default=None,
            multiple=True,
            help="Search for photos in album ALBUM. "
            'If more than one album, treated as "OR", e.g. find photos matching any album',
        ),
        o(
            "--folder",
            metavar="FOLDER",
            default=None,
            multiple=True,
            help="Search for photos in an album in folder FOLDER. "
            'If more than one folder, treated as "OR", e.g. find photos in any FOLDER.  '
            "Only searches top level folders (e.g. does not look at subfolders)",
        ),
        o(
            "--name",
            metavar="FILENAME",
            default=None,
            multiple=True,
            help="Search for photos with filename matching FILENAME. "
            'If more than one --name options is specified, they are treated as "OR", '
            "e.g. find photos matching any FILENAME. ",
        ),
        o(
            "--uuid",
            metavar="UUID",
            default=None,
            multiple=True,
            help="Search for photos with UUID(s).",
        ),
        o(
            "--uuid-from-file",
            metavar="FILE",
            default=None,
            multiple=False,
            help="Search for photos with UUID(s) loaded from FILE. "
            "Format is a single UUID per line.  Lines preceded with # are ignored.",
            type=click.Path(exists=True),
        ),
        o(
            "--title",
            metavar="TITLE",
            default=None,
            multiple=True,
            help="Search for TITLE in title of photo.",
        ),
        o("--no-title", is_flag=True, help="Search for photos with no title."),
        o(
            "--description",
            metavar="DESC",
            default=None,
            multiple=True,
            help="Search for DESC in description of photo.",
        ),
        o(
            "--no-description",
            is_flag=True,
            help="Search for photos with no description.",
        ),
        o(
            "--place",
            metavar="PLACE",
            default=None,
            multiple=True,
            help="Search for PLACE in photo's reverse geolocation info",
        ),
        o(
            "--no-place",
            is_flag=True,
            help="Search for photos with no associated place name info (no reverse geolocation info)",
        ),
        o(
            "--location",
            is_flag=True,
            help="Search for photos with associated location info (e.g. GPS coordinates)",
        ),
        o(
            "--no-location",
            is_flag=True,
            help="Search for photos with no associated location info (e.g. no GPS coordinates)",
        ),
        o(
            "--label",
            metavar="LABEL",
            multiple=True,
            help="Search for photos with image classification label LABEL (Photos 5 only). "
            'If more than one label, treated as "OR", e.g. find photos matching any label',
        ),
        o(
            "--uti",
            metavar="UTI",
            default=None,
            multiple=False,
            help="Search for photos whose uniform type identifier (UTI) matches UTI",
        ),
        o(
            "-i",
            "--ignore-case",
            is_flag=True,
            help="Case insensitive search for title, description, place, keyword, person, or album.",
        ),
        o("--edited", is_flag=True, help="Search for photos that have been edited."),
        o(
            "--external-edit",
            is_flag=True,
            help="Search for photos edited in external editor.",
        ),
        o("--favorite", is_flag=True, help="Search for photos marked favorite."),
        o(
            "--not-favorite",
            is_flag=True,
            help="Search for photos not marked favorite.",
        ),
        o("--hidden", is_flag=True, help="Search for photos marked hidden."),
        o("--not-hidden", is_flag=True, help="Search for photos not marked hidden."),
        o(
            "--shared",
            is_flag=True,
            help="Search for photos in shared iCloud album (Photos 5 only).",
        ),
        o(
            "--not-shared",
            is_flag=True,
            help="Search for photos not in shared iCloud album (Photos 5 only).",
        ),
        o(
            "--burst",
            is_flag=True,
            help="Search for photos that were taken in a burst.",
        ),
        o(
            "--not-burst",
            is_flag=True,
            help="Search for photos that are not part of a burst.",
        ),
        o("--live", is_flag=True, help="Search for Apple live photos"),
        o(
            "--not-live",
            is_flag=True,
            help="Search for photos that are not Apple live photos.",
        ),
        o("--portrait", is_flag=True, help="Search for Apple portrait mode photos."),
        o(
            "--not-portrait",
            is_flag=True,
            help="Search for photos that are not Apple portrait mode photos.",
        ),
        o("--screenshot", is_flag=True, help="Search for screenshot photos."),
        o(
            "--not-screenshot",
            is_flag=True,
            help="Search for photos that are not screenshot photos.",
        ),
        o("--slow-mo", is_flag=True, help="Search for slow motion videos."),
        o(
            "--not-slow-mo",
            is_flag=True,
            help="Search for photos that are not slow motion videos.",
        ),
        o("--time-lapse", is_flag=True, help="Search for time lapse videos."),
        o(
            "--not-time-lapse",
            is_flag=True,
            help="Search for photos that are not time lapse videos.",
        ),
        o("--hdr", is_flag=True, help="Search for high dynamic range (HDR) photos."),
        o("--not-hdr", is_flag=True, help="Search for photos that are not HDR photos."),
        o(
            "--selfie",
            is_flag=True,
            help="Search for selfies (photos taken with front-facing cameras).",
        ),
        o("--not-selfie", is_flag=True, help="Search for photos that are not selfies."),
        o("--panorama", is_flag=True, help="Search for panorama photos."),
        o(
            "--not-panorama",
            is_flag=True,
            help="Search for photos that are not panoramas.",
        ),
        o(
            "--has-raw",
            is_flag=True,
            help="Search for photos with both a jpeg and raw version",
        ),
        o(
            "--only-movies",
            is_flag=True,
            help="Search only for movies (default searches both images and movies).",
        ),
        o(
            "--only-photos",
            is_flag=True,
            help="Search only for photos/images (default searches both images and movies).",
        ),
        o(
            "--from-date",
            help="Search by item start date, e.g. 2000-01-12T12:00:00, 2001-01-12T12:00:00-07:00, or 2000-12-31 (ISO 8601 with/without timezone).",
            type=DateTimeISO8601(),
        ),
        o(
            "--to-date",
            help="Search by item end date, e.g. 2000-01-12T12:00:00, 2001-01-12T12:00:00-07:00, or 2000-12-31 (ISO 8601 with/without timezone).",
            type=DateTimeISO8601(),
        ),
        o(
            "--from-time",
            help="Search by item start time of day, e.g. 12:00, or 12:00:00.",
            type=TimeISO8601(),
        ),
        o(
            "--to-time",
            help="Search by item end time of day, e.g. 12:00 or 12:00:00.",
            type=TimeISO8601(),
        ),
        o("--has-comment", is_flag=True, help="Search for photos that have comments."),
        o("--no-comment", is_flag=True, help="Search for photos with no comments."),
        o("--has-likes", is_flag=True, help="Search for photos that have likes."),
        o("--no-likes", is_flag=True, help="Search for photos with no likes."),
        o(
            "--is-reference",
            is_flag=True,
            help="Search for photos that were imported as referenced files (not copied into Photos library).",
        ),
        o(
            "--in-album",
            is_flag=True,
            help="Search for photos that are in one or more albums.",
        ),
        o(
            "--not-in-album",
            is_flag=True,
            help="Search for photos that are not in any albums.",
        ),
        o(
            "--duplicate",
            is_flag=True,
            help="Search for photos with possible duplicates. osxphotos will compare signatures of photos, "
            "evaluating date created, size, height, width, and edited status to find *possible* duplicates. "
            "This does not compare images byte-for-byte nor compare hashes but should find photos imported multiple "
            "times or duplicated within Photos.",
        ),
        o(
            "--min-size",
            metavar="SIZE",
            type=BitMathSize(),
            help="Search for photos with size >= SIZE bytes. "
            "The size evaluated is the photo's original size (when imported to Photos). "
            "Size may be specified as integer bytes or using SI or NIST units. "
            "For example, the following are all valid and equivalent sizes: '1048576' '1.048576MB', '1 MiB'.",
        ),
        o(
            "--max-size",
            metavar="SIZE",
            type=BitMathSize(),
            help="Search for photos with size <= SIZE bytes. "
            "The size evaluated is the photo's original size (when imported to Photos). "
            "Size may be specified as integer bytes or using SI or NIST units. "
            "For example, the following are all valid and equivalent sizes: '1048576' '1.048576MB', '1 MiB'.",
        ),
        o(
            "--regex",
            metavar="REGEX TEMPLATE",
            nargs=2,
            multiple=True,
            help="Search for photos where TEMPLATE matches regular expression REGEX. "
            "For example, to find photos in an album that begins with 'Beach': '--regex \"^Beach\" \"{album}\"'. "
            "You may specify more than one regular expression match by repeating '--regex' with different arguments.",
        ),
        o(
            "--selected",
            is_flag=True,
            help="Filter for photos that are currently selected in Photos.",
        ),
        o(
            "--query-eval",
            metavar="CRITERIA",
            multiple=True,
            help="Evaluate CRITERIA to filter photos. "
            "CRITERIA will be evaluated in context of the following python list comprehension: "
            "`photos = [photo for photo in photos if CRITERIA]` "
            "where photo represents a PhotoInfo object. "
            "For example: `--query-eval photo.favorite` returns all photos that have been "
            "favorited and is equivalent to --favorite. "
            "You may specify more than one CRITERIA by using --query-eval multiple times. "
            "CRITERIA must be a valid python expression. "
            "See https://rhettbull.github.io/osxphotos/ for additional documentation on the PhotoInfo class.",
        ),
        o(
            "--query-function",
            metavar="filename.py::function",
            multiple=True,
            type=FunctionCall(),
            help="Run function to filter photos. Use this in format: --query-function filename.py::function where filename.py is a python "
            + "file you've created and function is the name of the function in the python file you want to call. "
            + "Your function will be passed a list of PhotoInfo objects and is expected to return a filtered list of PhotoInfo objects. "
            + "You may use more than one function by repeating the --query-function option with a different value. "
            + "Your query function will be called after all other query options have been evaluated. "
            + "See https://github.com/RhetTbull/osxphotos/blob/master/examples/query_function.py for example of how to use this option.",
        ),
    ]
    for o in options[::-1]:
        f = o(f)
    return f


@click.group(context_settings=CTX_SETTINGS)
@DB_OPTION
@JSON_OPTION
@click.option("--debug", required=False, is_flag=True, default=False, hidden=True)
@click.version_option(__version__, "--version", "-v")
@click.pass_context
def cli(ctx, db, json_, debug):
    ctx.obj = CLI_Obj(db=db, json=json_, debug=debug)


@cli.command(cls=ExportCommand)
@DB_OPTION
@click.option("--verbose", "-V", "verbose", is_flag=True, help="Print verbose output.")
@QUERY_OPTIONS
@click.option(
    "--missing",
    is_flag=True,
    help="Export only photos missing from the Photos library; must be used with --download-missing.",
)
@deleted_options
@click.option(
    "--update",
    is_flag=True,
    help="Only export new or updated files. See notes below on export and --update.",
)
@click.option(
    "--ignore-signature",
    is_flag=True,
    help="When used with '--update', ignores file signature when updating files. "
    "This is useful if you have processed or edited exported photos changing the "
    "file signature (size & modification date). In this case, '--update' would normally "
    "re-export the processed files but with '--ignore-signature', files which exist "
    "in the export directory will not be re-exported. "
    "If used with '--sidecar', '--ignore-signature' has the following behavior: "
    "1) if the metadata (in Photos) that went into the sidecar did not change, "
    "the sidecar will not be updated; "
    "2) if the metadata (in Photos) that went into the sidecar did change, "
    "a new sidecar is written but a new image file is not; "
    "3) if a sidecar does not exist for the photo, a sidecar will be written "
    "whether or not the photo file was written or updated.",
)
@click.option(
    "--only-new",
    is_flag=True,
    help="If used with --update, ignores any previously exported files, even if missing from "
    "the export folder and only exports new files that haven't previously been exported.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Dry run (test) the export but don't actually export any files; most useful with --verbose.",
)
@click.option(
    "--export-as-hardlink",
    is_flag=True,
    help="Hardlink files instead of copying them. "
    "Cannot be used with --exiftool which creates copies of the files with embedded EXIF data. "
    "Note: on APFS volumes, files are cloned when exporting giving many of the same "
    "advantages as hardlinks without having to use --export-as-hardlink.",
)
@click.option(
    "--touch-file",
    is_flag=True,
    help="Sets the file's modification time to match photo date.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="Overwrite existing files. "
    "Default behavior is to add (1), (2), etc to filename if file already exists. "
    "Use this with caution as it may create name collisions on export. "
    "(e.g. if two files happen to have the same name)",
)
@click.option(
    "--retry",
    metavar="RETRY",
    type=click.INT,
    help="Automatically retry export up to RETRY times if an error occurs during export.  "
    "This may be useful with network drives that experience intermittent errors.",
)
@click.option(
    "--export-by-date",
    is_flag=True,
    help="Automatically create output folders to organize photos by date created "
    "(e.g. DEST/2019/12/20/photoname.jpg).",
)
@click.option(
    "--skip-edited",
    is_flag=True,
    help="Do not export edited version of photo if an edited version exists.",
)
@click.option(
    "--skip-original-if-edited",
    is_flag=True,
    help="Do not export original if there is an edited version (exports only the edited version).",
)
@click.option(
    "--skip-bursts",
    is_flag=True,
    help="Do not export all associated burst images in the library if a photo is a burst photo.  ",
)
@click.option(
    "--skip-live",
    is_flag=True,
    help="Do not export the associated live video component of a live photo.",
)
@click.option(
    "--skip-raw",
    is_flag=True,
    help="Do not export associated RAW image of a RAW+JPEG pair.  "
    "Note: this does not skip RAW photos if the RAW photo does not have an associated JPEG image "
    "(e.g. the RAW file was imported to Photos without a JPEG preview).",
)
@click.option(
    "--current-name",
    is_flag=True,
    help="Use photo's current filename instead of original filename for export.  "
    "Note: Starting with Photos 5, all photos are renamed upon import.  By default, "
    "photos are exported with the the original name they had before import.",
)
@click.option(
    "--convert-to-jpeg",
    is_flag=True,
    help="Convert all non-JPEG images (e.g. RAW, HEIC, PNG, etc) to JPEG upon export. "
    "Note: does not convert the RAW component of a RAW+JPEG pair as the associated JPEG image "
    "will be exported. You can use --skip-raw to skip exporting the associated RAW image of "
    "a RAW+JPEG pair. See also --jpeg-quality and --jpeg-ext. "
    "Only works if your Mac has a GPU (thus may not work on virtual machines).",
)
@click.option(
    "--jpeg-quality",
    type=click.FloatRange(0.0, 1.0),
    help="Value in range 0.0 to 1.0 to use with --convert-to-jpeg. "
    "A value of 1.0 specifies best quality, "
    "a value of 0.0 specifies maximum compression. "
    f"Defaults to {DEFAULT_JPEG_QUALITY}",
)
@click.option(
    "--preview",
    is_flag=True,
    help="Export preview image generated by Photos. "
    "This is a lower-resolution image used by Photos to quickly preview the image. "
    "See also --preview-suffix and --preview-if-missing.",
)
@click.option(
    "--preview-if-missing",
    is_flag=True,
    help="Export preview image generated by Photos if the actual photo file is missing from the library. "
    "This may be helpful if photos were not copied to the Photos library and the original photo is missing. "
    "See also --preview-suffix and --preview.",
)
@click.option(
    "--preview-suffix",
    metavar="SUFFIX",
    help="Optional suffix template for naming preview photos.  Default name for preview photos is in form "
    f"'photoname{DEFAULT_PREVIEW_SUFFIX}.ext'. For example, with '--preview-suffix _low_res', the preview photo "
    f"would be named 'photoname_low_res.ext'.  The default suffix is '{DEFAULT_PREVIEW_SUFFIX}'. "
    "Multi-value templates (see Templating System) are not permitted with --preview-suffix. "
    "See also --preview and --preview-if-missing.",
)
@click.option(
    "--download-missing",
    is_flag=True,
    help="Attempt to download missing photos from iCloud. The current implementation uses Applescript "
    "to interact with Photos to export the photo which will force Photos to download from iCloud if "
    "the photo does not exist on disk.  This will be slow and will require internet connection. "
    "This obviously only works if the Photos library is synched to iCloud.  "
    "Note: --download-missing does not currently export all burst images; "
    "only the primary photo will be exported--associated burst images will be skipped.",
)
@click.option(
    "--sidecar",
    default=None,
    multiple=True,
    metavar="FORMAT",
    type=click.Choice(["xmp", "json", "exiftool"], case_sensitive=False),
    help="Create sidecar for each photo exported; valid FORMAT values: xmp, json, exiftool; "
    "--sidecar xmp: create XMP sidecar used by Digikam, Adobe Lightroom, etc. "
    "The sidecar file is named in format photoname.ext.xmp "
    "The XMP sidecar exports the following tags: Description, Title, Keywords/Tags, "
    "Subject (set to Keywords + PersonInImage), PersonInImage, CreateDate, ModifyDate, "
    "GPSLongitude, Face Regions (Metadata Working Group and Microsoft Photo)."
    f"\n--sidecar json: create JSON sidecar useable by exiftool ({_EXIF_TOOL_URL}) "
    "The sidecar file can be used to apply metadata to the file with exiftool, for example: "
    '"exiftool -j=photoname.jpg.json photoname.jpg" '
    "The sidecar file is named in format photoname.ext.json; "
    "format includes tag groups (equivalent to running 'exiftool -G -j'). "
    "\n--sidecar exiftool: create JSON sidecar compatible with output of 'exiftool -j'. "
    "Unlike '--sidecar json', '--sidecar exiftool' does not export tag groups. "
    "Sidecar filename is in format photoname.ext.json; "
    "For a list of tags exported in the JSON and exiftool sidecar, see '--exiftool'. "
    "See also '--ignore-signature'.",
)
@click.option(
    "--sidecar-drop-ext",
    is_flag=True,
    help="Drop the photo's extension when naming sidecar files. "
    "By default, sidecar files are named in format 'photo_filename.photo_ext.sidecar_ext', "
    "e.g. 'IMG_1234.JPG.xmp'. Use '--sidecar-drop-ext' to ignore the photo extension. "
    "Resulting sidecar files will have name in format 'IMG_1234.xmp'. "
    "Warning: this may result in sidecar filename collisions if there are files of different "
    "types but the same name in the output directory, e.g. 'IMG_1234.JPG' and 'IMG_1234.MOV'.",
)
@click.option(
    "--exiftool",
    is_flag=True,
    help="Use exiftool to write metadata directly to exported photos. "
    "To use this option, exiftool must be installed and in the path.  "
    "exiftool may be installed from https://exiftool.org/.  "
    "Cannot be used with --export-as-hardlink.  Writes the following metadata: "
    "EXIF:ImageDescription, XMP:Description (see also --description-template); "
    "XMP:Title; XMP:TagsList, IPTC:Keywords, XMP:Subject "
    "(see also --keyword-template, --person-keyword, --album-keyword); "
    "XMP:PersonInImage; EXIF:GPSLatitudeRef; EXIF:GPSLongitudeRef; EXIF:GPSLatitude; EXIF:GPSLongitude; "
    "EXIF:GPSPosition; EXIF:DateTimeOriginal; EXIF:OffsetTimeOriginal; "
    "EXIF:ModifyDate (see --ignore-date-modified); IPTC:DateCreated; IPTC:TimeCreated; "
    "(video files only): QuickTime:CreationDate; QuickTime:CreateDate; QuickTime:ModifyDate (see also --ignore-date-modified); "
    "QuickTime:GPSCoordinates; UserData:GPSCoordinates.",
)
@click.option(
    "--exiftool-path",
    metavar="EXIFTOOL_PATH",
    type=click.Path(exists=True),
    help="Optionally specify path to exiftool; if not provided, will look for exiftool in $PATH.",
)
@click.option(
    "--exiftool-option",
    multiple=True,
    metavar="OPTION",
    help="Optional flag/option to pass to exiftool when using --exiftool. "
    "For example, --exiftool-option '-m' to ignore minor warnings. "
    "Specify these as you would on the exiftool command line. "
    "See exiftool docs at https://exiftool.org/exiftool_pod.html for full list of options. "
    "More than one option may be specified by repeating the option, e.g. "
    "--exiftool-option '-m' --exiftool-option '-F'. ",
)
@click.option(
    "--exiftool-merge-keywords",
    is_flag=True,
    help="Merge any keywords found in the original file with keywords used for '--exiftool' and '--sidecar'.",
)
@click.option(
    "--exiftool-merge-persons",
    is_flag=True,
    help="Merge any persons found in the original file with persons used for '--exiftool' and '--sidecar'.",
)
@click.option(
    "--ignore-date-modified",
    is_flag=True,
    help="If used with --exiftool or --sidecar, will ignore the photo "
    "modification date and set EXIF:ModifyDate to EXIF:DateTimeOriginal; "
    "this is consistent with how Photos handles the EXIF:ModifyDate tag.",
)
@click.option(
    "--person-keyword",
    is_flag=True,
    help="Use person in image as keyword/tag when exporting metadata.",
)
@click.option(
    "--album-keyword",
    is_flag=True,
    help="Use album name as keyword/tag when exporting metadata.",
)
@click.option(
    "--keyword-template",
    metavar="TEMPLATE",
    multiple=True,
    default=None,
    help="For use with --exiftool, --sidecar; specify a template string to use as "
    "keyword in the form '{name,DEFAULT}' "
    "This is the same format as --directory.  For example, if you wanted to add "
    "the full path to the folder and album photo is contained in as a keyword when exporting "
    'you could specify --keyword-template "{folder_album}" '
    'You may specify more than one template, for example --keyword-template "{folder_album}" '
    '--keyword-template "{created.year}". '
    "See '--replace-keywords' and Templating System below.",
)
@click.option(
    "--replace-keywords",
    is_flag=True,
    help="Replace keywords with any values specified with --keyword-template. "
    "By default, --keyword-template will add keywords to any keywords already associated "
    "with the photo.  If --replace-keywords is specified, values from --keyword-template "
    "will replace any existing keywords instead of adding additional keywords.",
)
@click.option(
    "--description-template",
    metavar="TEMPLATE",
    multiple=False,
    default=None,
    help="For use with --exiftool, --sidecar; specify a template string to use as "
    "description in the form '{name,DEFAULT}' "
    "This is the same format as --directory.  For example, if you wanted to append "
    "'exported with osxphotos on [today's date]' to the description, you could specify "
    '--description-template "{descr} exported with osxphotos on {today.date}" '
    "See Templating System below.",
)
@click.option(
    "--finder-tag-template",
    metavar="TEMPLATE",
    multiple=True,
    default=None,
    help="Set MacOS Finder tags to TEMPLATE. These tags can be searched in the Finder or Spotlight with "
    "'tag:tagname' format. For example, '--finder-tag-template \"{label}\"' to set Finder tags to photo labels. "
    "You may specify multiple TEMPLATE values by using '--finder-tag-template' multiple times. "
    "See also '--finder-tag-keywords and Extended Attributes below.'.",
)
@click.option(
    "--finder-tag-keywords",
    is_flag=True,
    help="Set MacOS Finder tags to keywords; any keywords specified via '--keyword-template', '--person-keyword', etc. "
    "will also be used as Finder tags. See also '--finder-tag-template and Extended Attributes below.'.",
)
@click.option(
    "--xattr-template",
    nargs=2,
    metavar="ATTRIBUTE TEMPLATE",
    multiple=True,
    help="Set extended attribute ATTRIBUTE to TEMPLATE value. Valid attributes are: "
    f"{', '.join(EXTENDED_ATTRIBUTE_NAMES_QUOTED)}. "
    "For example, to set Finder comment to the photo's title and description: "
    '\'--xattr-template findercomment "{title}; {descr}" '
    "See Extended Attributes below for additional details on this option.",
)
@click.option(
    "--directory",
    metavar="DIRECTORY",
    default=None,
    help="Optional template for specifying name of output directory in the form '{name,DEFAULT}'. "
    "See below for additional details on templating system.",
)
@click.option(
    "--filename",
    "filename_template",
    metavar="FILENAME",
    default=None,
    help="Optional template for specifying name of output file in the form '{name,DEFAULT}'. "
    "File extension will be added automatically--do not include an extension in the FILENAME template. "
    "See below for additional details on templating system.",
)
@click.option(
    "--jpeg-ext",
    multiple=False,
    metavar="EXTENSION",
    type=click.Choice(["jpeg", "jpg", "JPEG", "JPG"], case_sensitive=True),
    help="Specify file extension for JPEG files. Photos uses .jpeg for edited images but many images "
    "are imported with .jpg or .JPG which can result in multiple different extensions used for JPEG files "
    "upon export.  Use --jpeg-ext to specify a single extension to use for all exported JPEG images. "
    "Valid values are jpeg, jpg, JPEG, JPG; e.g. '--jpeg-ext jpg' to use '.jpg' for all JPEGs.",
)
@click.option(
    "--strip",
    is_flag=True,
    help="Optionally strip leading and trailing whitespace from any rendered templates. "
    'For example, if --filename template is "{title,} {original_name}" and image has no '
    "title, resulting file would have a leading space but if used with --strip, this will "
    "be removed.",
)
@click.option(
    "--edited-suffix",
    metavar="SUFFIX",
    help="Optional suffix template for naming edited photos.  Default name for edited photos is in form "
    "'photoname_edited.ext'. For example, with '--edited-suffix _bearbeiten', the edited photo "
    f"would be named 'photoname_bearbeiten.ext'.  The default suffix is '{DEFAULT_EDITED_SUFFIX}'. "
    "Multi-value templates (see Templating System) are not permitted with --edited-suffix.",
)
@click.option(
    "--original-suffix",
    metavar="SUFFIX",
    help="Optional suffix template for naming original photos.  Default name for original photos is in form "
    "'filename.ext'. For example, with '--original-suffix _original', the original photo "
    "would be named 'filename_original.ext'.  The default suffix is '' (no suffix). "
    "Multi-value templates (see Templating System) are not permitted with --original-suffix.",
)
@click.option(
    "--use-photos-export",
    is_flag=True,
    help="Force the use of AppleScript or PhotoKit to export even if not missing (see also '--download-missing' and '--use-photokit').",
)
@click.option(
    "--use-photokit",
    is_flag=True,
    help="Use with '--download-missing' or '--use-photos-export' to use direct Photos interface instead of AppleScript to export. "
    "Highly experimental alpha feature; does not work with iTerm2 (use with Terminal.app). "
    "This is faster and more reliable than the default AppleScript interface.",
)
@click.option(
    "--report",
    metavar="<path to export report>",
    help="Write a CSV formatted report of all files that were exported.",
    type=click.Path(),
)
@click.option(
    "--cleanup",
    is_flag=True,
    help="Cleanup export directory by deleting any files which were not included in this export set. "
    "For example, photos which had previously been exported and were subsequently deleted in Photos. "
    "WARNING: --cleanup will delete *any* files in the export directory that were not exported by osxphotos, "
    "for example, your own scripts or other files.  Be sure this is what you intend before using "
    "--cleanup.  Use --dry-run with --cleanup first if you're not certain.",
)
@click.option(
    "--add-exported-to-album",
    metavar="ALBUM",
    help="Add all exported photos to album ALBUM in Photos. Album ALBUM will be created "
    "if it doesn't exist.  All exported photos will be added to this album. "
    "This only works if the Photos library being exported is the last-opened (default) library in Photos. "
    "This feature is currently experimental.  I don't know how well it will work on large export sets.",
)
@click.option(
    "--add-skipped-to-album",
    metavar="ALBUM",
    help="Add all skipped photos to album ALBUM in Photos. Album ALBUM will be created "
    "if it doesn't exist.  All skipped photos will be added to this album. "
    "This only works if the Photos library being exported is the last-opened (default) library in Photos. "
    "This feature is currently experimental.  I don't know how well it will work on large export sets.",
)
@click.option(
    "--add-missing-to-album",
    metavar="ALBUM",
    help="Add all missing photos to album ALBUM in Photos. Album ALBUM will be created "
    "if it doesn't exist.  All missing photos will be added to this album. "
    "This only works if the Photos library being exported is the last-opened (default) library in Photos. "
    "This feature is currently experimental.  I don't know how well it will work on large export sets.",
)
@click.option(
    "--post-command",
    metavar="CATEGORY COMMAND",
    nargs=2,
    type=(click.Choice(POST_COMMAND_CATEGORIES, case_sensitive=False), str),
    multiple=True,
    help="Run COMMAND on exported files of category CATEGORY.  CATEGORY can be one of: "
    f"{', '.join(list(POST_COMMAND_CATEGORIES.keys()))}. "
    "COMMAND is an osxphotos template string, for example: '--post-command exported \"echo {filepath|shell_quote} >> {export_dir}/exported.txt\"', "
    "which appends the full path of all exported files to the file 'exported.txt'. "
    "You can run more than one command by repeating the '--post-command' option with different arguments. "
    "See Post Command below.",
)
@click.option(
    "--post-function",
    metavar="filename.py::function",
    nargs=1,
    type=FunctionCall(),
    multiple=True,
    help="Run function on exported files. Use this in format: --post-function filename.py::function where filename.py is a python "
    "file you've created and function is the name of the function in the python file you want to call.  The function will be "
    "passed information about the photo that's been exported and a list of all exported files associated with the photo. "
    "You can run more than one function by repeating the '--post-function' option with different arguments. "
    "See Post Function below.",
)
@click.option(
    "--exportdb",
    metavar="EXPORTDB_FILE",
    default=None,
    help=(
        "Specify alternate name for database file which stores state information for export and --update. "
        f"If --exportdb is not specified, export database will be saved to '{OSXPHOTOS_EXPORT_DB}' "
        "in the export directory.  Must be specified as filename only, not a path, as export database "
        "will be saved in export directory."
    ),
    type=click.Path(),
)
@click.option(
    "--load-config",
    required=False,
    metavar="<config file path>",
    default=None,
    help=(
        "Load options from file as written with --save-config. "
        "This allows you to save a complex export command to file for later reuse. "
        "For example: 'osxphotos export <lots of options here> --save-config osxphotos.toml' then "
        " 'osxphotos export /path/to/export --load-config osxphotos.toml'. "
        "If any other command line options are used in conjunction with --load-config, "
        "they will override the corresponding values in the config file."
    ),
    type=click.Path(exists=True),
)
@click.option(
    "--save-config",
    required=False,
    metavar="<config file path>",
    default=None,
    help=("Save options to file for use with --load-config. File format is TOML."),
    type=click.Path(),
)
@click.option(
    "--beta", is_flag=True, default=False, hidden=True, help="Enable beta options."
)
@DB_ARGUMENT
@click.argument("dest", nargs=1, type=click.Path(exists=True))
@click.pass_obj
@click.pass_context
def export(
    ctx,
    cli_obj,
    db,
    photos_library,
    keyword,
    person,
    album,
    folder,
    uuid,
    name,
    uuid_from_file,
    title,
    no_title,
    description,
    no_description,
    uti,
    ignore_case,
    edited,
    external_edit,
    favorite,
    not_favorite,
    hidden,
    not_hidden,
    shared,
    not_shared,
    from_date,
    to_date,
    from_time,
    to_time,
    verbose,
    missing,
    update,
    ignore_signature,
    only_new,
    dry_run,
    export_as_hardlink,
    touch_file,
    overwrite,
    retry,
    export_by_date,
    skip_edited,
    skip_original_if_edited,
    skip_bursts,
    skip_live,
    skip_raw,
    person_keyword,
    album_keyword,
    keyword_template,
    replace_keywords,
    description_template,
    finder_tag_template,
    finder_tag_keywords,
    xattr_template,
    current_name,
    convert_to_jpeg,
    jpeg_quality,
    sidecar,
    sidecar_drop_ext,
    only_photos,
    only_movies,
    burst,
    not_burst,
    live,
    not_live,
    download_missing,
    dest,
    exiftool,
    exiftool_path,
    exiftool_option,
    exiftool_merge_keywords,
    exiftool_merge_persons,
    ignore_date_modified,
    portrait,
    not_portrait,
    screenshot,
    not_screenshot,
    slow_mo,
    not_slow_mo,
    time_lapse,
    not_time_lapse,
    hdr,
    not_hdr,
    selfie,
    not_selfie,
    panorama,
    not_panorama,
    has_raw,
    directory,
    filename_template,
    jpeg_ext,
    strip,
    edited_suffix,
    original_suffix,
    place,
    no_place,
    location,
    no_location,
    has_comment,
    no_comment,
    has_likes,
    no_likes,
    label,
    deleted,
    deleted_only,
    use_photos_export,
    use_photokit,
    report,
    cleanup,
    add_exported_to_album,
    add_skipped_to_album,
    add_missing_to_album,
    exportdb,
    load_config,
    save_config,
    is_reference,
    beta,
    in_album,
    not_in_album,
    min_size,
    max_size,
    regex,
    selected,
    query_eval,
    query_function,
    duplicate,
    post_command,
    post_function,
    preview,
    preview_suffix,
    preview_if_missing,
):
    """Export photos from the Photos database.
    Export path DEST is required.
    Optionally, query the Photos database using 1 or more search options;
    if more than one option is provided, they are treated as "AND"
    (e.g. search for photos matching all options).
    If no query options are provided, all photos will be exported.
    By default, all versions of all photos will be exported including edited
    versions, live photo movies, burst photos, and associated raw images.
    See --skip-edited, --skip-live, --skip-bursts, and --skip-raw options
    to modify this behavior.
    """

    # NOTE: because of the way ConfigOptions works, Click options must not
    # set defaults which are not None or False. If defaults need to be set
    # do so below after load_config and save_config are handled.
    cfg = ConfigOptions(
        "export",
        locals(),
        ignore=["ctx", "cli_obj", "dest", "load_config", "save_config"],
    )

    global VERBOSE
    VERBOSE = bool(verbose)

    if load_config:
        try:
            cfg.load_from_file(load_config)
        except ConfigOptionsLoadError as e:
            click.echo(
                click.style(
                    f"Error parsing {load_config} config file: {e.message}",
                    fg=CLI_COLOR_ERROR,
                ),
                err=True,
            )
            raise click.Abort()

        # re-set the local vars to the corresponding config value
        # this isn't elegant but avoids having to rewrite this function to use cfg.varname for every parameter
        db = cfg.db
        photos_library = cfg.photos_library
        keyword = cfg.keyword
        person = cfg.person
        album = cfg.album
        folder = cfg.folder
        name = cfg.name
        uuid = cfg.uuid
        uuid_from_file = cfg.uuid_from_file
        title = cfg.title
        no_title = cfg.no_title
        description = cfg.description
        no_description = cfg.no_description
        uti = cfg.uti
        ignore_case = cfg.ignore_case
        edited = cfg.edited
        external_edit = cfg.external_edit
        favorite = cfg.favorite
        not_favorite = cfg.not_favorite
        hidden = cfg.hidden
        not_hidden = cfg.not_hidden
        shared = cfg.shared
        not_shared = cfg.not_shared
        from_date = cfg.from_date
        to_date = cfg.to_date
        from_time = cfg.from_time
        to_time = cfg.to_time
        verbose = cfg.verbose
        missing = cfg.missing
        update = cfg.update
        ignore_signature = cfg.ignore_signature
        dry_run = cfg.dry_run
        export_as_hardlink = cfg.export_as_hardlink
        touch_file = cfg.touch_file
        overwrite = cfg.overwrite
        retry = cfg.retry
        export_by_date = cfg.export_by_date
        skip_edited = cfg.skip_edited
        skip_original_if_edited = cfg.skip_original_if_edited
        skip_bursts = cfg.skip_bursts
        skip_live = cfg.skip_live
        skip_raw = cfg.skip_raw
        person_keyword = cfg.person_keyword
        album_keyword = cfg.album_keyword
        keyword_template = cfg.keyword_template
        replace_keywords = cfg.replace_keywords
        description_template = cfg.description_template
        finder_tag_template = cfg.finder_tag_template
        finder_tag_keywords = cfg.finder_tag_keywords
        xattr_template = cfg.xattr_template
        current_name = cfg.current_name
        convert_to_jpeg = cfg.convert_to_jpeg
        jpeg_quality = cfg.jpeg_quality
        sidecar = cfg.sidecar
        sidecar_drop_ext = cfg.sidecar_drop_ext
        only_photos = cfg.only_photos
        only_movies = cfg.only_movies
        burst = cfg.burst
        not_burst = cfg.not_burst
        live = cfg.live
        not_live = cfg.not_live
        download_missing = cfg.download_missing
        exiftool = cfg.exiftool
        exiftool_path = cfg.exiftool_path
        exiftool_option = cfg.exiftool_option
        exiftool_merge_keywords = cfg.exiftool_merge_keywords
        exiftool_merge_persons = cfg.exiftool_merge_persons
        ignore_date_modified = cfg.ignore_date_modified
        portrait = cfg.portrait
        not_portrait = cfg.not_portrait
        screenshot = cfg.screenshot
        not_screenshot = cfg.not_screenshot
        slow_mo = cfg.slow_mo
        not_slow_mo = cfg.not_slow_mo
        time_lapse = cfg.time_lapse
        not_time_lapse = cfg.not_time_lapse
        hdr = cfg.hdr
        not_hdr = cfg.not_hdr
        selfie = cfg.selfie
        not_selfie = cfg.not_selfie
        panorama = cfg.panorama
        not_panorama = cfg.not_panorama
        has_raw = cfg.has_raw
        directory = cfg.directory
        filename_template = cfg.filename_template
        jpeg_ext = cfg.jpeg_ext
        strip = cfg.strip
        edited_suffix = cfg.edited_suffix
        original_suffix = cfg.original_suffix
        place = cfg.place
        no_place = cfg.no_place
        location = cfg.location
        no_location = cfg.no_location
        has_comment = cfg.has_comment
        no_comment = cfg.no_comment
        has_likes = cfg.has_likes
        no_likes = cfg.no_likes
        label = cfg.label
        deleted = cfg.deleted
        deleted_only = cfg.deleted_only
        use_photos_export = cfg.use_photos_export
        use_photokit = cfg.use_photokit
        report = cfg.report
        cleanup = cfg.cleanup
        add_exported_to_album = cfg.add_exported_to_album
        add_skipped_to_album = cfg.add_skipped_to_album
        add_missing_to_album = cfg.add_missing_to_album
        exportdb = cfg.exportdb
        beta = cfg.beta
        only_new = cfg.only_new
        in_album = cfg.in_album
        not_in_album = cfg.not_in_album
        min_size = cfg.min_size
        max_size = cfg.max_size
        regex = cfg.regex
        selected = cfg.selected
        query_eval = cfg.query_eval
        query_function = cfg.query_function
        duplicate = cfg.duplicate
        post_command = cfg.post_command
        post_function = cfg.post_function
        preview = cfg.preview
        preview_suffix = cfg.preview_suffix
        preview_if_missing = cfg.preview_if_missing

        # config file might have changed verbose
        VERBOSE = bool(verbose)
        verbose_(f"Loaded options from file {load_config}")

    verbose_(f"osxphotos version {__version__}")

    # validate options
    exclusive_options = [
        ("favorite", "not_favorite"),
        ("hidden", "not_hidden"),
        ("title", "no_title"),
        ("description", "no_description"),
        ("only_photos", "only_movies"),
        ("burst", "not_burst"),
        ("live", "not_live"),
        ("portrait", "not_portrait"),
        ("screenshot", "not_screenshot"),
        ("slow_mo", "not_slow_mo"),
        ("time_lapse", "not_time_lapse"),
        ("hdr", "not_hdr"),
        ("selfie", "not_selfie"),
        ("panorama", "not_panorama"),
        ("export_by_date", "directory"),
        ("export_as_hardlink", "exiftool"),
        ("place", "no_place"),
        ("deleted", "deleted_only"),
        ("skip_edited", "skip_original_if_edited"),
        ("export_as_hardlink", "convert_to_jpeg"),
        ("export_as_hardlink", "download_missing"),
        ("shared", "not_shared"),
        ("has_comment", "no_comment"),
        ("has_likes", "no_likes"),
        ("in_album", "not_in_album"),
        ("location", "no_location"),
    ]
    dependent_options = [
        ("missing", ("download_missing", "use_photos_export")),
        ("jpeg_quality", ("convert_to_jpeg")),
        ("ignore_signature", ("update")),
        ("only_new", ("update")),
        ("exiftool_option", ("exiftool")),
        ("exiftool_merge_keywords", ("exiftool", "sidecar")),
        ("exiftool_merge_persons", ("exiftool", "sidecar")),
    ]
    try:
        cfg.validate(exclusive=exclusive_options, dependent=dependent_options, cli=True)
    except ConfigOptionsInvalidError as e:
        click.echo(
            click.style(
                f"Incompatible export options: {e.message}", fg=CLI_COLOR_ERROR
            ),
            err=True,
        )
        raise click.Abort()

    if all(x in [s.lower() for s in sidecar] for x in ["json", "exiftool"]):
        click.echo(
            click.style(
                "Cannot use --sidecar json with --sidecar exiftool due to name collisions",
                fg=CLI_COLOR_ERROR,
            ),
            err=True,
        )
        raise click.Abort()

    if xattr_template:
        for attr, _ in xattr_template:
            if attr not in EXTENDED_ATTRIBUTE_NAMES:
                click.echo(
                    click.style(
                        f"Invalid attribute '{attr}' for --xattr-template; "
                        f"valid values are {', '.join(EXTENDED_ATTRIBUTE_NAMES_QUOTED)}",
                        fg=CLI_COLOR_ERROR,
                    ),
                    err=True,
                )
                raise click.Abort()

    if save_config:
        verbose_(f"Saving options to file {save_config}")
        cfg.write_to_file(save_config)

    # set defaults for options that need them
    jpeg_quality = DEFAULT_JPEG_QUALITY if jpeg_quality is None else jpeg_quality
    edited_suffix = DEFAULT_EDITED_SUFFIX if edited_suffix is None else edited_suffix
    original_suffix = (
        DEFAULT_ORIGINAL_SUFFIX if original_suffix is None else original_suffix
    )
    preview_suffix = (
        DEFAULT_PREVIEW_SUFFIX if preview_suffix is None else preview_suffix
    )
    retry = 0 if not retry else retry

    if not os.path.isdir(dest):
        click.echo(
            click.style(f"DEST {dest} must be valid path", fg=CLI_COLOR_ERROR), err=True
        )
        raise click.Abort()

    dest = str(pathlib.Path(dest).resolve())

    if report and os.path.isdir(report):
        click.echo(
            click.style(
                f"report is a directory, must be file name", fg=CLI_COLOR_ERROR
            ),
            err=True,
        )
        raise click.Abort()

    # if use_photokit and not check_photokit_authorization():
    #     click.echo(
    #         "Requesting access to use your Photos library. Click 'OK' on the dialog box to grant access."
    #     )
    #     request_photokit_authorization()
    #     click.confirm("Have you granted access?")
    #     if not check_photokit_authorization():
    #         click.echo(
    #             "Failed to get access to the Photos library which is needed with `--use-photokit`."
    #         )
    #         return

    # initialize export flags
    # by default, will export all versions of photos unless skip flag is set
    (export_edited, export_bursts, export_live, export_raw) = [
        not x for x in [skip_edited, skip_bursts, skip_live, skip_raw]
    ]

    # verify exiftool installed and in path if path not provided and exiftool will be used
    # NOTE: this won't catch use of {exiftool:} in a template
    # but those will raise error during template eval if exiftool path not set
    if (
        any([exiftool, exiftool_merge_keywords, exiftool_merge_persons])
        and not exiftool_path
    ):
        try:
            exiftool_path = get_exiftool_path()
        except FileNotFoundError:
            click.echo(
                click.style(
                    "Could not find exiftool. Please download and install"
                    " from https://exiftool.org/",
                    fg=CLI_COLOR_ERROR,
                ),
                err=True,
            )
            ctx.exit(2)

    if any([exiftool, exiftool_merge_keywords, exiftool_merge_persons]):
        verbose_(f"exiftool path: {exiftool_path}")

    photos = movies = True  # default searches for everything
    if only_movies:
        photos = False
    if only_photos:
        movies = False

    # load UUIDs if necessary and append to any uuids passed with --uuid
    if uuid_from_file:
        uuid_list = list(uuid)  # Click option is a tuple
        uuid_list.extend(load_uuid_from_file(uuid_from_file))
        uuid = tuple(uuid_list)

    # below needed for to make CliRunner work for testing
    cli_db = cli_obj.db if cli_obj is not None else None
    db = get_photos_db(*photos_library, db, cli_db)
    if db is None:
        click.echo(cli.commands["export"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    # sanity check exportdb
    if exportdb and exportdb != OSXPHOTOS_EXPORT_DB:
        if "/" in exportdb:
            click.echo(
                click.style(
                    f"Error: --exportdb must be specified as filename not path; "
                    + f"export database will saved in export directory '{dest}'.",
                    fg=CLI_COLOR_ERROR,
                )
            )
            raise click.Abort()
        elif pathlib.Path(pathlib.Path(dest) / OSXPHOTOS_EXPORT_DB).exists():
            click.echo(
                click.style(
                    f"Warning: export database is '{exportdb}' but found '{OSXPHOTOS_EXPORT_DB}' in {dest}; using '{exportdb}'",
                    fg=CLI_COLOR_WARNING,
                )
            )

    # open export database and assign copy/link/unlink functions
    export_db_path = os.path.join(dest, exportdb or OSXPHOTOS_EXPORT_DB)

    # check that export isn't in the parent or child of a previously exported library
    other_db_files = find_files_in_branch(dest, OSXPHOTOS_EXPORT_DB)
    if other_db_files:
        click.echo(
            click.style(
                "WARNING: found other export database files in this destination directory branch.  "
                + "This likely means you are attempting to export files into a directory "
                + "that is either the parent or a child directory of a previous export. "
                + "Proceeding may cause your exported files to be overwritten.",
                fg=CLI_COLOR_WARNING,
            ),
            err=True,
        )
        click.echo(
            f"You are exporting to {dest}, found {OSXPHOTOS_EXPORT_DB} files in:"
        )
        for other_db in other_db_files:
            click.echo(f"{other_db}")
        click.confirm("Do you want to continue?", abort=True)

    if dry_run:
        export_db = ExportDBInMemory(export_db_path)
        fileutil = FileUtilNoOp
    else:
        export_db = ExportDB(export_db_path)
        fileutil = FileUtil

    if verbose_:
        if export_db.was_created:
            verbose_(f"Created export database {export_db_path}")
        else:
            verbose_(f"Using export database {export_db_path}")
        upgraded = export_db.was_upgraded
        if upgraded:
            verbose_(
                f"Upgraded export database {export_db_path} from version {upgraded[0]} to {upgraded[1]}"
            )

    photosdb = osxphotos.PhotosDB(dbfile=db, verbose=verbose_, exiftool=exiftool_path)

    # enable beta features if requested
    photosdb._beta = beta

    query_options = QueryOptions(
        keyword=keyword,
        person=person,
        album=album,
        folder=folder,
        uuid=uuid,
        title=title,
        no_title=no_title,
        description=description,
        no_description=no_description,
        ignore_case=ignore_case,
        edited=edited,
        external_edit=external_edit,
        favorite=favorite,
        not_favorite=not_favorite,
        hidden=hidden,
        not_hidden=not_hidden,
        missing=missing,
        not_missing=None,
        shared=shared,
        not_shared=not_shared,
        photos=photos,
        movies=movies,
        uti=uti,
        burst=burst,
        not_burst=not_burst,
        live=live,
        not_live=not_live,
        cloudasset=False,
        not_cloudasset=False,
        incloud=False,
        not_incloud=False,
        from_date=from_date,
        to_date=to_date,
        from_time=from_time,
        to_time=to_time,
        portrait=portrait,
        not_portrait=not_portrait,
        screenshot=screenshot,
        not_screenshot=not_screenshot,
        slow_mo=slow_mo,
        not_slow_mo=not_slow_mo,
        time_lapse=time_lapse,
        not_time_lapse=not_time_lapse,
        hdr=hdr,
        not_hdr=not_hdr,
        selfie=selfie,
        not_selfie=not_selfie,
        panorama=panorama,
        not_panorama=not_panorama,
        has_raw=has_raw,
        place=place,
        no_place=no_place,
        location=location,
        no_location=no_location,
        label=label,
        deleted=deleted,
        deleted_only=deleted_only,
        has_comment=has_comment,
        no_comment=no_comment,
        has_likes=has_likes,
        no_likes=no_likes,
        is_reference=is_reference,
        in_album=in_album,
        not_in_album=not_in_album,
        burst_photos=export_bursts,
        # skip missing bursts if using --download-missing by itself as AppleScript otherwise causes errors
        missing_bursts=(download_missing and use_photokit) or not download_missing,
        name=name,
        min_size=min_size,
        max_size=max_size,
        regex=regex,
        selected=selected,
        query_eval=query_eval,
        function=query_function,
        duplicate=duplicate,
    )

    try:
        photos = photosdb.query(query_options)
    except ValueError as e:
        if "Invalid query_eval CRITERIA:" in str(e):
            msg = str(e).split(":")[1]
            raise click.BadOptionUsage(
                "query_eval", f"Invalid query-eval CRITERIA: {msg}"
            )
        else:
            raise ValueError(e)

    if photos and only_new:
        # ignore previously exported files
        previous_uuids = {uuid: 1 for uuid in export_db.get_previous_uuids()}
        photos = [p for p in photos if p.uuid not in previous_uuids]

    # store results of export
    results = ExportResults()

    if photos:
        num_photos = len(photos)
        # TODO: photos or photo appears several times, pull into a separate function
        photo_str = "photos" if num_photos > 1 else "photo"
        click.echo(f"Exporting {num_photos} {photo_str} to {dest}...")
        start_time = time.perf_counter()
        # though the command line option is current_name, internally all processing
        # logic uses original_name which is the boolean inverse of current_name
        # because the original code used --original-name as an option
        original_name = not current_name

        # set up for --add-export-to-album if needed
        album_export = (
            PhotosAlbum(add_exported_to_album, verbose=verbose_)
            if add_exported_to_album
            else None
        )
        album_skipped = (
            PhotosAlbum(add_skipped_to_album, verbose=verbose_)
            if add_skipped_to_album
            else None
        )
        album_missing = (
            PhotosAlbum(add_missing_to_album, verbose=verbose_)
            if add_missing_to_album
            else None
        )

        # send progress bar output to /dev/null if verbose to hide the progress bar
        fp = open(os.devnull, "w") if verbose else None
        with click.progressbar(photos, file=fp) as bar:
            for p in bar:
                export_results = export_photo(
                    photo=p,
                    dest=dest,
                    verbose=verbose,
                    export_by_date=export_by_date,
                    sidecar=sidecar,
                    sidecar_drop_ext=sidecar_drop_ext,
                    update=update,
                    ignore_signature=ignore_signature,
                    export_as_hardlink=export_as_hardlink,
                    overwrite=overwrite,
                    export_edited=export_edited,
                    skip_original_if_edited=skip_original_if_edited,
                    original_name=original_name,
                    export_live=export_live,
                    download_missing=download_missing,
                    exiftool=exiftool,
                    exiftool_merge_keywords=exiftool_merge_keywords,
                    exiftool_merge_persons=exiftool_merge_persons,
                    directory=directory,
                    filename_template=filename_template,
                    export_raw=export_raw,
                    album_keyword=album_keyword,
                    person_keyword=person_keyword,
                    keyword_template=keyword_template,
                    description_template=description_template,
                    export_db=export_db,
                    fileutil=fileutil,
                    dry_run=dry_run,
                    touch_file=touch_file,
                    edited_suffix=edited_suffix,
                    original_suffix=original_suffix,
                    use_photos_export=use_photos_export,
                    convert_to_jpeg=convert_to_jpeg,
                    jpeg_quality=jpeg_quality,
                    ignore_date_modified=ignore_date_modified,
                    use_photokit=use_photokit,
                    exiftool_option=exiftool_option,
                    strip=strip,
                    jpeg_ext=jpeg_ext,
                    replace_keywords=replace_keywords,
                    retry=retry,
                    export_dir=dest,
                    export_preview=preview,
                    preview_suffix=preview_suffix,
                    preview_if_missing=preview_if_missing,
                )

                if post_function:
                    for function in post_function:
                        # post function is tuple of (function, filename.py::function_name)
                        verbose_(f"Calling post-function {function[1]}")
                        if not dry_run:
                            try:
                                function[0](p, export_results, verbose_)
                            except Exception as e:
                                click.secho(
                                    f"Error running post-function {function[1]}: {e}",
                                    fg=CLI_COLOR_ERROR,
                                    err=True,
                                )

                run_post_command(
                    photo=p,
                    post_command=post_command,
                    export_results=export_results,
                    export_dir=dest,
                    dry_run=dry_run,
                    exiftool_path=exiftool_path,
                    export_db=export_db,
                )

                if album_export and export_results.exported:
                    try:
                        album_export.add(p)
                        export_results.exported_album = [
                            (filename, album_export.name)
                            for filename in export_results.exported
                        ]
                    except Exception as e:
                        click.secho(
                            f"Error adding photo {p.original_filename} ({p.uuid}) to album {album_export.name}: {e}",
                            fg=CLI_COLOR_ERROR,
                            err=True,
                        )

                if album_skipped and export_results.skipped:
                    try:
                        album_skipped.add(p)
                        export_results.skipped_album = [
                            (filename, album_skipped.name)
                            for filename in export_results.skipped
                        ]
                    except Exception as e:
                        click.secho(
                            f"Error adding photo {p.original_filename} ({p.uuid}) to album {album_skipped.name}: {e}",
                            fg=CLI_COLOR_ERROR,
                            err=True,
                        )

                if album_missing and export_results.missing:
                    try:
                        album_missing.add(p)
                        export_results.missing_album = [
                            (filename, album_missing.name)
                            for filename in export_results.missing
                        ]
                    except Exception as e:
                        click.secho(
                            f"Error adding photo {p.original_filename} ({p.uuid}) to album {album_missing.name}: {e}",
                            fg=CLI_COLOR_ERROR,
                            err=True,
                        )

                results += export_results

                # all photo files (not including sidecars) that are part of this export set
                # used below for applying Finder tags, etc.
                photo_files = set(
                    export_results.exported
                    + export_results.new
                    + export_results.updated
                    + export_results.exif_updated
                    + export_results.converted_to_jpeg
                    + export_results.skipped
                )

                if finder_tag_keywords or finder_tag_template:
                    tags_written, tags_skipped = write_finder_tags(
                        p,
                        photo_files,
                        keywords=finder_tag_keywords,
                        keyword_template=keyword_template,
                        album_keyword=album_keyword,
                        person_keyword=person_keyword,
                        exiftool_merge_keywords=exiftool_merge_keywords,
                        finder_tag_template=finder_tag_template,
                        strip=strip,
                        export_dir=dest,
                        export_db=export_db,
                    )
                    results.xattr_written.extend(tags_written)
                    results.xattr_skipped.extend(tags_skipped)

                if xattr_template:
                    xattr_written, xattr_skipped = write_extended_attributes(
                        p,
                        photo_files,
                        xattr_template,
                        strip=strip,
                        export_dir=dest,
                        export_db=export_db,
                    )
                    results.xattr_written.extend(xattr_written)
                    results.xattr_skipped.extend(xattr_skipped)

        if fp is not None:
            fp.close()

        photo_str_total = "photos" if len(photos) != 1 else "photo"
        if update:
            summary = (
                f"Processed: {len(photos)} {photo_str_total}, "
                f"exported: {len(results.new)}, "
                f"updated: {len(results.updated)}, "
                f"skipped: {len(results.skipped)}, "
                f"updated EXIF data: {len(results.exif_updated)}, "
            )
        else:
            summary = (
                f"Processed: {len(photos)} {photo_str_total}, "
                f"exported: {len(results.exported)}, "
            )
        summary += f"missing: {len(results.missing)}, "
        summary += f"error: {len(results.error)}"
        if touch_file:
            summary += f", touched date: {len(results.touched)}"
        click.echo(summary)
        stop_time = time.perf_counter()
        click.echo(f"Elapsed time: {(stop_time-start_time):.3f} seconds")
    else:
        click.echo("Did not find any photos to export")

    # cleanup files and do report if needed
    if cleanup:
        all_files = (
            results.exported
            + results.skipped
            + results.exif_updated
            + results.touched
            + results.converted_to_jpeg
            + results.sidecar_json_written
            + results.sidecar_json_skipped
            + results.sidecar_exiftool_written
            + results.sidecar_exiftool_skipped
            + results.sidecar_xmp_written
            + results.sidecar_xmp_skipped
            # include missing so a file that was already in export directory
            # but was missing on --update doesn't get deleted
            # (better to have old version than none)
            + results.missing
            # include files that have error in case they exist from previous export
            + [r[0] for r in results.error]
            + [str(pathlib.Path(export_db_path).resolve())]
        )
        click.echo(f"Cleaning up {dest}")
        cleaned_files, cleaned_dirs = cleanup_files(dest, all_files, fileutil)
        file_str = "files" if len(cleaned_files) != 1 else "file"
        dir_str = "directories" if len(cleaned_dirs) != 1 else "directory"
        click.echo(
            f"Deleted: {len(cleaned_files)} {file_str}, {len(cleaned_dirs)} {dir_str}"
        )
        results.deleted_files = cleaned_files
        results.deleted_directories = cleaned_dirs

    if report:
        verbose_(f"Writing export report to {report}")
        write_export_report(report, results)

    export_db.close()


@cli.command()
@click.argument("topic", default=None, required=False, nargs=1)
@click.pass_context
def help(ctx, topic, **kw):
    """Print help; for help on commands: help <command>."""
    if topic is None:
        click.echo(ctx.parent.get_help())
    elif topic in cli.commands:
        ctx.info_name = topic
        click.echo_via_pager(cli.commands[topic].get_help(ctx))
    else:
        click.echo(f"Invalid command: {topic}", err=True)
        click.echo(ctx.parent.get_help())


@cli.command()
@DB_OPTION
@JSON_OPTION
@QUERY_OPTIONS
@deleted_options
@click.option("--missing", is_flag=True, help="Search for photos missing from disk.")
@click.option(
    "--not-missing",
    is_flag=True,
    help="Search for photos present on disk (e.g. not missing).",
)
@click.option(
    "--cloudasset",
    is_flag=True,
    help="Search for photos that are part of an iCloud library",
)
@click.option(
    "--not-cloudasset",
    is_flag=True,
    help="Search for photos that are not part of an iCloud library",
)
@click.option(
    "--incloud",
    is_flag=True,
    help="Search for photos that are in iCloud (have been synched)",
)
@click.option(
    "--not-incloud",
    is_flag=True,
    help="Search for photos that are not in iCloud (have not been synched)",
)
@click.option(
    "--add-to-album",
    metavar="ALBUM",
    help="Add all photos from query to album ALBUM in Photos. Album ALBUM will be created "
    "if it doesn't exist.  All photos in the query results will be added to this album. "
    "This only works if the Photos library being queried is the last-opened (default) library in Photos. "
    "This feature is currently experimental.  I don't know how well it will work on large query sets.",
)
@DB_ARGUMENT
@click.pass_obj
@click.pass_context
def query(
    ctx,
    cli_obj,
    db,
    photos_library,
    keyword,
    person,
    album,
    folder,
    name,
    uuid,
    uuid_from_file,
    title,
    no_title,
    description,
    no_description,
    ignore_case,
    json_,
    edited,
    external_edit,
    favorite,
    not_favorite,
    hidden,
    not_hidden,
    missing,
    not_missing,
    shared,
    not_shared,
    only_movies,
    only_photos,
    uti,
    burst,
    not_burst,
    live,
    not_live,
    cloudasset,
    not_cloudasset,
    incloud,
    not_incloud,
    from_date,
    to_date,
    from_time,
    to_time,
    portrait,
    not_portrait,
    screenshot,
    not_screenshot,
    slow_mo,
    not_slow_mo,
    time_lapse,
    not_time_lapse,
    hdr,
    not_hdr,
    selfie,
    not_selfie,
    panorama,
    not_panorama,
    has_raw,
    place,
    no_place,
    location,
    no_location,
    label,
    deleted,
    deleted_only,
    has_comment,
    no_comment,
    has_likes,
    no_likes,
    is_reference,
    in_album,
    not_in_album,
    duplicate,
    min_size,
    max_size,
    regex,
    selected,
    query_eval,
    query_function,
    add_to_album,
):
    """Query the Photos database using 1 or more search options;
    if more than one option is provided, they are treated as "AND"
    (e.g. search for photos matching all options).
    """

    # if no query terms, show help and return
    # sanity check input args
    nonexclusive = [
        keyword,
        person,
        album,
        folder,
        name,
        uuid,
        uuid_from_file,
        edited,
        external_edit,
        uti,
        has_raw,
        from_date,
        to_date,
        from_time,
        to_time,
        label,
        is_reference,
        query_eval,
        query_function,
        min_size,
        max_size,
        regex,
        selected,
        duplicate,
    ]
    exclusive = [
        (favorite, not_favorite),
        (hidden, not_hidden),
        (missing, not_missing),
        (any(title), no_title),
        (any(description), no_description),
        (only_photos, only_movies),
        (burst, not_burst),
        (live, not_live),
        (cloudasset, not_cloudasset),
        (incloud, not_incloud),
        (portrait, not_portrait),
        (screenshot, not_screenshot),
        (slow_mo, not_slow_mo),
        (time_lapse, not_time_lapse),
        (hdr, not_hdr),
        (selfie, not_selfie),
        (panorama, not_panorama),
        (any(place), no_place),
        (deleted, deleted_only),
        (shared, not_shared),
        (has_comment, no_comment),
        (has_likes, no_likes),
        (in_album, not_in_album),
        (location, no_location),
    ]
    # print help if no non-exclusive term or a double exclusive term is given
    if any(all(bb) for bb in exclusive) or not any(
        nonexclusive + [b ^ n for b, n in exclusive]
    ):
        click.echo("Incompatible query options", err=True)
        click.echo(cli.commands["query"].get_help(ctx), err=True)
        return

    # actually have something to query
    photos = movies = True  # default searches for everything
    if only_movies:
        photos = False
    if only_photos:
        movies = False

    # load UUIDs if necessary and append to any uuids passed with --uuid
    if uuid_from_file:
        uuid_list = list(uuid)  # Click option is a tuple
        uuid_list.extend(load_uuid_from_file(uuid_from_file))
        uuid = tuple(uuid_list)

    # below needed for to make CliRunner work for testing
    cli_db = cli_obj.db if cli_obj is not None else None
    db = get_photos_db(*photos_library, db, cli_db)
    if db is None:
        click.echo(cli.commands["query"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    photosdb = osxphotos.PhotosDB(dbfile=db, verbose=verbose_)
    query_options = QueryOptions(
        keyword=keyword,
        person=person,
        album=album,
        folder=folder,
        uuid=uuid,
        title=title,
        no_title=no_title,
        description=description,
        no_description=no_description,
        ignore_case=ignore_case,
        edited=edited,
        external_edit=external_edit,
        favorite=favorite,
        not_favorite=not_favorite,
        hidden=hidden,
        not_hidden=not_hidden,
        missing=missing,
        not_missing=not_missing,
        shared=shared,
        not_shared=not_shared,
        photos=photos,
        movies=movies,
        uti=uti,
        burst=burst,
        not_burst=not_burst,
        live=live,
        not_live=not_live,
        cloudasset=cloudasset,
        not_cloudasset=not_cloudasset,
        incloud=incloud,
        not_incloud=not_incloud,
        from_date=from_date,
        to_date=to_date,
        from_time=from_time,
        to_time=to_time,
        portrait=portrait,
        not_portrait=not_portrait,
        screenshot=screenshot,
        not_screenshot=not_screenshot,
        slow_mo=slow_mo,
        not_slow_mo=not_slow_mo,
        time_lapse=time_lapse,
        not_time_lapse=not_time_lapse,
        hdr=hdr,
        not_hdr=not_hdr,
        selfie=selfie,
        not_selfie=not_selfie,
        panorama=panorama,
        not_panorama=not_panorama,
        has_raw=has_raw,
        place=place,
        no_place=no_place,
        location=location,
        no_location=no_location,
        label=label,
        deleted=deleted,
        deleted_only=deleted_only,
        has_comment=has_comment,
        no_comment=no_comment,
        has_likes=has_likes,
        no_likes=no_likes,
        is_reference=is_reference,
        in_album=in_album,
        not_in_album=not_in_album,
        name=name,
        min_size=min_size,
        max_size=max_size,
        query_eval=query_eval,
        function=query_function,
        regex=regex,
        selected=selected,
        duplicate=duplicate,
    )

    try:
        photos = photosdb.query(query_options)
    except ValueError as e:
        if "Invalid query_eval CRITERIA:" in str(e):
            msg = str(e).split(":")[1]
            raise click.BadOptionUsage(
                "query_eval", f"Invalid query-eval CRITERIA: {msg}"
            )
        else:
            raise ValueError(e)

    # below needed for to make CliRunner work for testing
    cli_json = cli_obj.json if cli_obj is not None else None

    if add_to_album and photos:
        album_query = PhotosAlbum(add_to_album, verbose=None)
        photo_len = len(photos)
        photo_word = "photos" if photo_len > 1 else "photo"
        click.echo(
            f"Adding {photo_len} {photo_word} to album '{album_query.name}'. Note: Photos may prompt you to confirm this action.",
            err=True,
        )
        try:
            album_query.add_list(photos)
        except Exception as e:
            click.secho(
                f"Error adding photos to album {add_to_album}: {e}",
                fg=CLI_COLOR_ERROR,
                err=True,
            )

    print_photo_info(photos, cli_json or json_)


def print_photo_info(photos, json=False):
    dump = []
    if json:
        for p in photos:
            dump.append(p.json())
        click.echo(f"[{', '.join(dump)}]")
    else:
        # dump as CSV
        csv_writer = csv.writer(
            sys.stdout, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        # add headers
        dump.append(
            [
                "uuid",
                "filename",
                "original_filename",
                "date",
                "description",
                "title",
                "keywords",
                "albums",
                "persons",
                "path",
                "ismissing",
                "hasadjustments",
                "external_edit",
                "favorite",
                "hidden",
                "shared",
                "latitude",
                "longitude",
                "path_edited",
                "isphoto",
                "ismovie",
                "uti",
                "burst",
                "live_photo",
                "path_live_photo",
                "iscloudasset",
                "incloud",
                "date_modified",
                "portrait",
                "screenshot",
                "slow_mo",
                "time_lapse",
                "hdr",
                "selfie",
                "panorama",
                "has_raw",
                "uti_raw",
                "path_raw",
                "intrash",
            ]
        )
        for p in photos:
            date_modified_iso = p.date_modified.isoformat() if p.date_modified else None
            dump.append(
                [
                    p.uuid,
                    p.filename,
                    p.original_filename,
                    p.date.isoformat(),
                    p.description,
                    p.title,
                    ", ".join(p.keywords),
                    ", ".join(p.albums),
                    ", ".join(p.persons),
                    p.path,
                    p.ismissing,
                    p.hasadjustments,
                    p.external_edit,
                    p.favorite,
                    p.hidden,
                    p.shared,
                    p._latitude,
                    p._longitude,
                    p.path_edited,
                    p.isphoto,
                    p.ismovie,
                    p.uti,
                    p.burst,
                    p.live_photo,
                    p.path_live_photo,
                    p.iscloudasset,
                    p.incloud,
                    date_modified_iso,
                    p.portrait,
                    p.screenshot,
                    p.slow_mo,
                    p.time_lapse,
                    p.hdr,
                    p.selfie,
                    p.panorama,
                    p.has_raw,
                    p.uti_raw,
                    p.path_raw,
                    p.intrash,
                ]
            )
        for row in dump:
            csv_writer.writerow(row)


def export_photo(
    photo=None,
    dest=None,
    verbose=None,
    export_by_date=None,
    sidecar=None,
    sidecar_drop_ext=False,
    update=None,
    ignore_signature=None,
    export_as_hardlink=None,
    overwrite=None,
    export_edited=None,
    skip_original_if_edited=None,
    original_name=None,
    export_live=None,
    download_missing=None,
    exiftool=None,
    exiftool_merge_keywords=False,
    exiftool_merge_persons=False,
    directory=None,
    filename_template=None,
    export_raw=None,
    album_keyword=None,
    person_keyword=None,
    keyword_template=None,
    description_template=None,
    export_db=None,
    fileutil=FileUtil,
    dry_run=None,
    touch_file=None,
    edited_suffix="_edited",
    original_suffix="",
    use_photos_export=False,
    convert_to_jpeg=False,
    jpeg_quality=1.0,
    ignore_date_modified=False,
    use_photokit=False,
    exiftool_option=None,
    strip=False,
    jpeg_ext=None,
    replace_keywords=False,
    retry=0,
    export_dir=None,
    export_preview=False,
    preview_suffix=None,
    preview_if_missing=False,
):
    """Helper function for export that does the actual export

    Args:
        photo: PhotoInfo object
        dest: destination path as string
        verbose: boolean; print verbose output
        export_by_date: boolean; create export folder in form dest/YYYY/MM/DD
        sidecar: list zero, 1 or 2 of ["json","xmp"] of sidecar variety to export
        sidecar_drop_ext: boolean; if True, drops photo extension from sidecar name
        export_as_hardlink: boolean; hardlink files instead of copying them
        overwrite: boolean; overwrite dest file if it already exists
        original_name: boolean; use original filename instead of current filename
        export_live: boolean; also export live video component if photo is a live photo
                     live video will have same name as photo but with .mov extension
        download_missing: attempt download of missing iCloud photos
        exiftool: use exiftool to write EXIF metadata directly to exported photo
        directory: template used to determine output directory
        filename_template: template use to determine output file
        export_raw: boolean; if True exports raw image associate with the photo
        export_edited: boolean; if True exports edited version of photo if there is one
        skip_original_if_edited: boolean; if True does not export original if photo has been edited
        album_keyword: boolean; if True, exports album names as keywords in metadata
        person_keyword: boolean; if True, exports person names as keywords in metadata
        keyword_template: list of strings; if provided use rendered template strings as keywords
        description_template: string; optional template string that will be rendered for use as photo description
        export_db: export database instance compatible with ExportDB_ABC
        fileutil: file util class compatible with FileUtilABC
        dry_run: boolean; if True, doesn't actually export or update any files
        touch_file: boolean; sets file's modification time to match photo date
        use_photos_export: boolean; if True forces the use of AppleScript to export even if photo not missing
        convert_to_jpeg: boolean; if True, converts non-jpeg images to jpeg
        jpeg_quality: float in range 0.0 <= jpeg_quality <= 1.0.  A value of 1.0 specifies use best quality, a value of 0.0 specifies use maximum compression.
        ignore_date_modified: if True, sets EXIF:ModifyDate to EXIF:DateTimeOriginal even if date_modified is set
        exiftool_option: optional list flags (e.g. ["-m", "-F"]) to pass to exiftool
        exiftool_merge_keywords: boolean; if True, merged keywords found in file's exif data (requires exiftool)
        exiftool_merge_persons: boolean; if True, merged persons found in file's exif data (requires exiftool)
        jpeg_ext: if not None, specify the extension to use for all JPEG images on export
        replace_keywords: if True, --keyword-template replaces keywords instead of adding keywords
        retry: retry up to retry # of times if there's an error
        export_dir: top-level export directory for {export_dir} template
        export_preview: export the preview image generated by Photos
        preview_suffix: str, template to use as suffix for preview images
        preview_if_missing: bool, export preview if original is missing

    Returns:
        list of path(s) of exported photo or None if photo was missing

    Raises:
        ValueError on invalid filename_template
    """
    global VERBOSE
    VERBOSE = bool(verbose)

    export_original = not (skip_original_if_edited and photo.hasadjustments)

    # can't export edited if photo doesn't have edited versions
    export_edited = export_edited if photo.hasadjustments else False

    # slow_mo photos will always have hasadjustments=True even if not edited
    if photo.hasadjustments and photo.path_edited is None:
        if photo.slow_mo:
            export_original = True
            export_edited = False
        elif not download_missing:
            # requested edited version but it's missing, download original
            export_original = True
            export_edited = False
            verbose_(
                f"Edited file for {photo.original_filename} is missing, exporting original"
            )

    # check for missing photos before downloading
    missing_original = False
    missing_edited = False
    if download_missing:
        if (
            (photo.ismissing or photo.path is None)
            and not photo.iscloudasset
            and not photo.incloud
        ):
            missing_original = True
        if (
            photo.hasadjustments
            and photo.path_edited is None
            and not photo.iscloudasset
            and not photo.incloud
        ):
            missing_edited = True
    else:
        if photo.ismissing or photo.path is None:
            missing_original = True
        if photo.hasadjustments and photo.path_edited is None:
            missing_edited = True

    sidecar = [s.lower() for s in sidecar]
    sidecar_flags = 0
    if "json" in sidecar:
        sidecar_flags |= SIDECAR_JSON
    if "xmp" in sidecar:
        sidecar_flags |= SIDECAR_XMP
    if "exiftool" in sidecar:
        sidecar_flags |= SIDECAR_EXIFTOOL

    rendered_suffix = _render_suffix_template(
        original_suffix,
        "original_suffix",
        "--original-suffix",
        strip,
        dest,
        photo,
        export_db,
    )
    rendered_preview_suffix = _render_suffix_template(
        preview_suffix,
        "preview_suffix",
        "--preview-suffix",
        strip,
        dest,
        photo,
        export_db,
    )

    # if download_missing and the photo is missing or path doesn't exist,
    # try to download with Photos
    use_photos_export = use_photos_export or (
        download_missing
        and (
            photo.ismissing
            or photo.path is None
            or (export_edited and photo.path_edited is None)
        )
    )

    results = ExportResults()
    dest_paths = get_dirnames_from_template(
        photo,
        directory,
        export_by_date,
        dest,
        dry_run,
        strip=strip,
        edited=False,
        export_db=export_db,
    )
    for dest_path in dest_paths:
        filenames = get_filenames_from_template(
            photo,
            filename_template,
            dest,
            dest_path,
            original_name,
            strip=strip,
            export_db=export_db,
        )

        for filename in filenames:
            original_filename = pathlib.Path(filename)
            file_ext = original_filename.suffix
            if photo.isphoto and (jpeg_ext or convert_to_jpeg):
                # change the file extension to correct jpeg extension if needed
                file_ext = (
                    "." + jpeg_ext
                    if jpeg_ext
                    and (photo.uti_original == "public.jpeg" or convert_to_jpeg)
                    else ".jpeg"
                    if convert_to_jpeg and photo.uti_original != "public.jpeg"
                    else original_filename.suffix
                )
            original_filename = (
                original_filename.parent
                / f"{original_filename.stem}{rendered_suffix}{file_ext}"
            )
            original_filename = str(original_filename)

            verbose_(
                f"Exporting {photo.original_filename} ({photo.filename}) as {original_filename}"
            )

            results += export_photo_to_directory(
                photo=photo,
                filename=original_filename,
                dest_path=dest_path,
                edited=False,
                use_photos_export=use_photos_export,
                dest=dest,
                dry_run=dry_run,
                export_original=export_original,
                missing=missing_original,
                verbose=verbose,
                sidecar_flags=sidecar_flags,
                sidecar_drop_ext=sidecar_drop_ext,
                export_live=export_live,
                export_raw=export_raw,
                export_as_hardlink=export_as_hardlink,
                overwrite=overwrite,
                exiftool=exiftool,
                exiftool_merge_keywords=exiftool_merge_keywords,
                exiftool_merge_persons=exiftool_merge_persons,
                album_keyword=album_keyword,
                person_keyword=person_keyword,
                keyword_template=keyword_template,
                description_template=description_template,
                update=update,
                ignore_signature=ignore_signature,
                export_db=export_db,
                fileutil=fileutil,
                touch_file=touch_file,
                convert_to_jpeg=convert_to_jpeg,
                jpeg_quality=jpeg_quality,
                ignore_date_modified=ignore_date_modified,
                use_photokit=use_photokit,
                exiftool_option=exiftool_option,
                jpeg_ext=jpeg_ext,
                replace_keywords=replace_keywords,
                retry=retry,
                export_dir=export_dir,
                export_preview=export_preview,
                preview_suffix=rendered_preview_suffix,
                preview_if_missing=preview_if_missing,
            )

    if export_edited and photo.hasadjustments:
        dest_paths = get_dirnames_from_template(
            photo,
            directory,
            export_by_date,
            dest,
            dry_run,
            strip=strip,
            edited=True,
            export_db=export_db,
        )
        for dest_path in dest_paths:
            # if export-edited, also export the edited version
            edited_filenames = get_filenames_from_template(
                photo,
                filename_template,
                dest,
                dest_path,
                original_name,
                strip=strip,
                edited=True,
                export_db=export_db,
            )
            for edited_filename in edited_filenames:
                edited_filename = pathlib.Path(edited_filename)
                # verify the photo has adjustments and valid path to avoid raising an exception
                edited_ext = (
                    # rare cases on Photos <= 4 that uti_edited is None
                    "." + get_preferred_uti_extension(photo.uti_edited)
                    if photo.uti_edited
                    else pathlib.Path(photo.path_edited).suffix
                    if photo.path_edited
                    else pathlib.Path(photo.filename).suffix
                )

                if (
                    photo.isphoto
                    and jpeg_ext
                    and edited_ext.lower() in [".jpg", ".jpeg"]
                ):
                    edited_ext = "." + jpeg_ext

                # Big Sur uses .heic for some edited photos so need to check
                # if extension isn't jpeg/jpg and using --convert-to-jpeg
                if (
                    photo.isphoto
                    and convert_to_jpeg
                    and edited_ext.lower() not in [".jpg", ".jpeg"]
                ):
                    edited_ext = "." + jpeg_ext if jpeg_ext else ".jpeg"

                rendered_edited_suffix = _render_suffix_template(
                    edited_suffix,
                    "edited_suffix",
                    "--edited-suffix",
                    strip,
                    dest,
                    photo,
                    export_db,
                )
                edited_filename = (
                    f"{edited_filename.stem}{rendered_edited_suffix}{edited_ext}"
                )

                verbose_(
                    f"Exporting edited version of {photo.original_filename} ({photo.filename}) as {edited_filename}"
                )

                results += export_photo_to_directory(
                    photo=photo,
                    filename=edited_filename,
                    dest_path=dest_path,
                    edited=True,
                    use_photos_export=use_photos_export,
                    dest=dest,
                    dry_run=dry_run,
                    export_original=False,
                    missing=missing_edited,
                    verbose=verbose,
                    sidecar_flags=sidecar_flags if not export_original else 0,
                    sidecar_drop_ext=sidecar_drop_ext,
                    export_live=export_live,
                    export_raw=not export_original and export_raw,
                    export_as_hardlink=export_as_hardlink,
                    overwrite=overwrite,
                    exiftool=exiftool,
                    exiftool_merge_keywords=exiftool_merge_keywords,
                    exiftool_merge_persons=exiftool_merge_persons,
                    album_keyword=album_keyword,
                    person_keyword=person_keyword,
                    keyword_template=keyword_template,
                    description_template=description_template,
                    update=update,
                    ignore_signature=ignore_signature,
                    export_db=export_db,
                    fileutil=fileutil,
                    touch_file=touch_file,
                    convert_to_jpeg=convert_to_jpeg,
                    jpeg_quality=jpeg_quality,
                    ignore_date_modified=ignore_date_modified,
                    use_photokit=use_photokit,
                    exiftool_option=exiftool_option,
                    jpeg_ext=jpeg_ext,
                    replace_keywords=replace_keywords,
                    retry=retry,
                    export_dir=export_dir,
                    export_preview=not export_original and export_preview,
                    preview_suffix=rendered_preview_suffix,
                    preview_if_missing=preview_if_missing,
                )

    return results


def _render_suffix_template(
    suffix_template, var_name, option_name, strip, dest, photo, export_db
):
    """render suffix template

    Returns:
        rendered template
    """
    if not suffix_template:
        return ""

    try:
        options = RenderOptions(filename=True, export_dir=dest, exportdb=export_db)
        rendered_suffix, unmatched = photo.render_template(suffix_template, options)
    except ValueError as e:
        raise click.BadOptionUsage(
            var_name,
            f"Invalid template for {option_name} '{suffix_template}': {e}",
        )
    if not rendered_suffix or unmatched:
        raise click.BadOptionUsage(
            var_name,
            f"Invalid template for {option_name} '{suffix_template}': results={rendered_suffix} unknown field={unmatched}",
        )
    if len(rendered_suffix) > 1:
        raise click.BadOptionUsage(
            var_name,
            f"Invalid template for {option_name}: may not use multi-valued templates: '{suffix_template}': results={rendered_suffix}",
        )

    if strip:
        rendered_suffix[0] = rendered_suffix[0].strip()

    return rendered_suffix[0]


def export_photo_to_directory(
    photo,
    filename,
    dest_path,
    edited,
    use_photos_export,
    dest,
    dry_run,
    export_original,
    missing,
    verbose,
    sidecar_flags,
    sidecar_drop_ext,
    export_live,
    export_raw,
    export_as_hardlink,
    overwrite,
    exiftool,
    exiftool_merge_keywords,
    exiftool_merge_persons,
    album_keyword,
    person_keyword,
    keyword_template,
    description_template,
    update,
    ignore_signature,
    export_db,
    fileutil,
    touch_file,
    convert_to_jpeg,
    jpeg_quality,
    ignore_date_modified,
    use_photokit,
    exiftool_option,
    jpeg_ext,
    replace_keywords,
    retry,
    export_dir,
    export_preview,
    preview_suffix,
    preview_if_missing,
):
    """Export photo to directory dest_path"""

    results = ExportResults()
    if export_original:
        if missing and not preview_if_missing:
            space = " " if not verbose else ""
            verbose_(
                f"{space}Skipping missing photo {photo.original_filename} ({photo.uuid})"
            )
            results.missing.append(str(pathlib.Path(dest_path) / filename))
        elif (
            photo.intrash
            and (not photo.path or use_photos_export)
            and not preview_if_missing
        ):
            # skip deleted files if they're missing or using use_photos_export
            # as AppleScript/PhotoKit cannot export deleted photos
            space = " " if not verbose else ""
            verbose_(
                f"{space}Skipping missing deleted photo {photo.original_filename} ({photo.uuid})"
            )
            results.missing.append(str(pathlib.Path(dest_path) / filename))
            return results
    elif not edited:
        verbose_(f"Skipping original version of {photo.original_filename}")
        return results
    else:
        # exporting the edited version
        if missing and not preview_if_missing:
            space = " " if not verbose else ""
            verbose_(f"{space}Skipping missing edited photo for {filename}")
            results.missing.append(str(pathlib.Path(dest_path) / filename))
            return results
        elif (
            photo.intrash
            and (not photo.path_edited or use_photos_export)
            and not preview_if_missing
        ):
            # skip deleted files if they're missing or using use_photos_export
            # as AppleScript/PhotoKit cannot export deleted photos
            space = " " if not verbose else ""
            verbose_(
                f"{space}Skipping missing deleted photo {photo.original_filename} ({photo.uuid})"
            )
            results.missing.append(str(pathlib.Path(dest_path) / filename))
            return results

    render_options = RenderOptions(
        export_dir=export_dir, dest_path=dest_path, exportdb=export_db
    )

    tries = 0
    while tries <= retry:
        tries += 1
        error = 0
        try:
            export_results = photo.export2(
                dest_path,
                original_filename=filename,
                edited=edited,
                original=export_original,
                edited_filename=filename,
                sidecar=sidecar_flags,
                sidecar_drop_ext=sidecar_drop_ext,
                live_photo=export_live,
                raw_photo=export_raw,
                export_as_hardlink=export_as_hardlink,
                overwrite=overwrite,
                use_photos_export=use_photos_export,
                exiftool=exiftool,
                merge_exif_keywords=exiftool_merge_keywords,
                merge_exif_persons=exiftool_merge_persons,
                use_albums_as_keywords=album_keyword,
                use_persons_as_keywords=person_keyword,
                keyword_template=keyword_template,
                description_template=description_template,
                update=update,
                ignore_signature=ignore_signature,
                export_db=export_db,
                fileutil=fileutil,
                dry_run=dry_run,
                touch_file=touch_file,
                convert_to_jpeg=convert_to_jpeg,
                jpeg_quality=jpeg_quality,
                ignore_date_modified=ignore_date_modified,
                use_photokit=use_photokit,
                verbose=verbose_,
                exiftool_flags=exiftool_option,
                jpeg_ext=jpeg_ext,
                replace_keywords=replace_keywords,
                render_options=render_options,
                preview=export_preview or (missing and preview_if_missing),
                preview_suffix=preview_suffix,
            )
            for warning_ in export_results.exiftool_warning:
                verbose_(f"exiftool warning for file {warning_[0]}: {warning_[1]}")
            for error_ in export_results.exiftool_error:
                click.echo(
                    click.style(
                        f"exiftool error for file {error_[0]}: {error_[1]}",
                        fg=CLI_COLOR_ERROR,
                    ),
                    err=True,
                )
            for error_ in export_results.error:
                click.echo(
                    click.style(
                        f"Error exporting photo ({photo.uuid}: {photo.original_filename}) as {error_[0]}: {error_[1]}",
                        fg=CLI_COLOR_ERROR,
                    ),
                    err=True,
                )
                error += 1
            if not error or tries > retry:
                results += export_results
                break
            else:
                click.echo(
                    "Retrying export for photo ({photo.uuid}: {photo.original_filename})"
                )
        except Exception as e:
            click.echo(
                click.style(
                    f"Error exporting photo ({photo.uuid}: {photo.original_filename}) as {filename}: {e}",
                    fg=CLI_COLOR_ERROR,
                ),
                err=True,
            )
            if tries > retry:
                results.error.append((str(pathlib.Path(dest) / filename), e))
                break
            else:
                click.echo(
                    f"Retrying export for photo ({photo.uuid}: {photo.original_filename})"
                )

    if verbose:
        if update:
            for new in results.new:
                verbose_(f"Exported new file {new}")
            for updated in results.updated:
                verbose_(f"Exported updated file {updated}")
            for skipped in results.skipped:
                verbose_(f"Skipped up to date file {skipped}")
        else:
            for exported in results.exported:
                verbose_(f"Exported {exported}")
        for touched in results.touched:
            verbose_(f"Touched date on file {touched}")

    return results


def get_filenames_from_template(
    photo,
    filename_template,
    export_dir,
    dest_path,
    original_name,
    strip=False,
    edited=False,
    export_db=None,
):
    """get list of export filenames for a photo

    Args:
        photo: a PhotoInfo instance
        filename_template: a PhotoTemplate template string, may be None
        original_name: boolean; if True, use photo's original filename instead of current filename
        dest_path: the path the photo will be exported to
        strip: if True, strips leading/trailing white space from resulting template
        edited: if True, sets {edited_version} field to True, otherwise it gets set to False; set if you want template evaluated for edited version

    Returns:
        list of filenames

    Raises:
        click.BadOptionUsage if template is invalid
    """
    if filename_template:
        photo_ext = pathlib.Path(photo.original_filename).suffix
        try:
            options = RenderOptions(
                path_sep="_",
                filename=True,
                edited_version=edited,
                export_dir=export_dir,
                dest_path=dest_path,
                exportdb=export_db,
            )
            filenames, unmatched = photo.render_template(filename_template, options)
        except ValueError as e:
            raise click.BadOptionUsage(
                "filename_template", f"Invalid template '{filename_template}': {e}"
            )
        if not filenames or unmatched:
            raise click.BadOptionUsage(
                "filename_template",
                f"Invalid template '{filename_template}': unknown field={unmatched}",
            )
        filenames = [f"{file_}{photo_ext}" for file_ in filenames]
    else:
        filenames = (
            [photo.original_filename]
            if (original_name and (photo.original_filename is not None))
            else [photo.filename]
        )

    if strip:
        filenames = [filename.strip() for filename in filenames]
    filenames = [sanitize_filename(filename) for filename in filenames]

    return filenames


def get_dirnames_from_template(
    photo,
    directory,
    export_by_date,
    dest,
    dry_run,
    strip=False,
    edited=False,
    export_db=None,
):
    """get list of directories to export a photo into, creates directories if they don't exist

    Args:
        photo: a PhotoInstance object
        directory: a PhotoTemplate template string, may be None
        export_by_date: boolean; if True, creates output directories in form YYYY-MM-DD
        dest: top-level destination directory
        dry_run: boolean; if True, runs in dry-run mode and does not create output directories
        strip: if True, strips leading/trailing white space from resulting template
        edited: if True, sets {edited_version} field to True, otherwise it gets set to False; set if you want template evaluated for edited version

    Returns:
        list of export directories

    Raises:
        click.BadOptionUsage if template is invalid
    """

    if export_by_date:
        date_created = DateTimeFormatter(photo.date)
        dest_path = os.path.join(
            dest, date_created.year, date_created.mm, date_created.dd
        )
        if not (dry_run or os.path.isdir(dest_path)):
            os.makedirs(dest_path)
        dest_paths = [dest_path]
    elif directory:
        # got a directory template, render it and check results are valid
        try:
            options = RenderOptions(
                dirname=True, edited_version=edited, exportdb=export_db
            )
            dirnames, unmatched = photo.render_template(directory, options)
        except ValueError as e:
            raise click.BadOptionUsage(
                "directory", f"Invalid template '{directory}': {e}"
            )
        if not dirnames or unmatched:
            raise click.BadOptionUsage(
                "directory",
                f"Invalid template '{directory}': unknown field={unmatched}",
            )

        dest_paths = []
        for dirname in dirnames:
            if strip:
                dirname = dirname.strip()
            dirname = sanitize_filepath(dirname)
            dest_path = os.path.join(dest, dirname)
            if not is_valid_filepath(dest_path):
                raise ValueError(f"Invalid file path: '{dest_path}'")
            if not dry_run and not os.path.isdir(dest_path):
                os.makedirs(dest_path)
            dest_paths.append(dest_path)
    else:
        dest_paths = [dest]
    return dest_paths


def find_files_in_branch(pathname, filename):
    """Search a directory branch to find file(s) named filename
        The branch searched includes all folders below pathname and
        the parent tree of pathname but not pathname itself.

        e.g. find filename in children folders and parent folders

    Args:
        pathname: str, full path of directory to search
        filename: str, filename to search for

    Returns: list of full paths to any matching files
    """

    pathname = pathlib.Path(pathname).resolve()
    files = []

    # walk down the tree
    for root, _, filenames in os.walk(pathname):
        # for directory in directories:
        # print(os.path.join(root, directory))
        for fname in filenames:
            if fname == filename and pathlib.Path(root) != pathname:
                files.append(os.path.join(root, fname))

    # walk up the tree
    path = pathlib.Path(pathname)
    for root in path.parents:
        filenames = os.listdir(root)
        for fname in filenames:
            filepath = os.path.join(root, fname)
            if fname == filename and os.path.isfile(filepath):
                files.append(os.path.join(root, fname))

    return files


def load_uuid_from_file(filename):
    """Load UUIDs from file.  Does not validate UUIDs.
        Format is 1 UUID per line, any line beginning with # is ignored.
        Whitespace is stripped.

    Arguments:
        filename: file name of the file containing UUIDs

    Returns:
        list of UUIDs or empty list of no UUIDs in file

    Raises:
        FileNotFoundError if file does not exist
    """

    if not pathlib.Path(filename).is_file():
        raise FileNotFoundError(f"Could not find file {filename}")

    uuid = []
    with open(filename, "r") as uuid_file:
        for line in uuid_file:
            line = line.strip()
            if len(line) and line[0] != "#":
                uuid.append(line)
    return uuid


def write_export_report(report_file, results):

    """write CSV report with results from export

    Args:
        report_file: path to report file
        results: ExportResults object
    """

    # Collect results for reporting
    all_results = {
        result: {
            "filename": result,
            "exported": 0,
            "new": 0,
            "updated": 0,
            "skipped": 0,
            "exif_updated": 0,
            "touched": 0,
            "converted_to_jpeg": 0,
            "sidecar_xmp": 0,
            "sidecar_json": 0,
            "sidecar_exiftool": 0,
            "missing": 0,
            "error": "",
            "exiftool_warning": "",
            "exiftool_error": "",
            "extended_attributes_written": 0,
            "extended_attributes_skipped": 0,
            "cleanup_deleted_file": 0,
            "cleanup_deleted_directory": 0,
            "exported_album": "",
        }
        for result in results.all_files()
        + results.deleted_files
        + results.deleted_directories
    }

    for result in results.exported:
        all_results[result]["exported"] = 1

    for result in results.new:
        all_results[result]["new"] = 1

    for result in results.updated:
        all_results[result]["updated"] = 1

    for result in results.skipped:
        all_results[result]["skipped"] = 1

    for result in results.exif_updated:
        all_results[result]["exif_updated"] = 1

    for result in results.touched:
        all_results[result]["touched"] = 1

    for result in results.converted_to_jpeg:
        all_results[result]["converted_to_jpeg"] = 1

    for result in results.sidecar_xmp_written:
        all_results[result]["sidecar_xmp"] = 1
        all_results[result]["exported"] = 1

    for result in results.sidecar_xmp_skipped:
        all_results[result]["sidecar_xmp"] = 1
        all_results[result]["skipped"] = 1

    for result in results.sidecar_json_written:
        all_results[result]["sidecar_json"] = 1
        all_results[result]["exported"] = 1

    for result in results.sidecar_json_skipped:
        all_results[result]["sidecar_json"] = 1
        all_results[result]["skipped"] = 1

    for result in results.sidecar_exiftool_written:
        all_results[result]["sidecar_exiftool"] = 1
        all_results[result]["exported"] = 1

    for result in results.sidecar_exiftool_skipped:
        all_results[result]["sidecar_exiftool"] = 1
        all_results[result]["skipped"] = 1

    for result in results.missing:
        all_results[result]["missing"] = 1

    for result in results.error:
        all_results[result[0]]["error"] = result[1]

    for result in results.exiftool_warning:
        all_results[result[0]]["exiftool_warning"] = result[1]

    for result in results.exiftool_error:
        all_results[result[0]]["exiftool_error"] = result[1]

    for result in results.xattr_written:
        all_results[result]["extended_attributes_written"] = 1

    for result in results.xattr_skipped:
        all_results[result]["extended_attributes_skipped"] = 1

    for result in results.deleted_files:
        all_results[result]["cleanup_deleted_file"] = 1

    for result in results.deleted_directories:
        all_results[result]["cleanup_deleted_directory"] = 1

    for result, album in results.exported_album:
        all_results[result]["exported_album"] = album

    report_columns = [
        "filename",
        "exported",
        "new",
        "updated",
        "skipped",
        "exif_updated",
        "touched",
        "converted_to_jpeg",
        "sidecar_xmp",
        "sidecar_json",
        "sidecar_exiftool",
        "missing",
        "error",
        "exiftool_warning",
        "exiftool_error",
        "extended_attributes_written",
        "extended_attributes_skipped",
        "cleanup_deleted_file",
        "cleanup_deleted_directory",
        "exported_album",
    ]

    try:
        with open(report_file, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=report_columns)
            writer.writeheader()
            for data in [result for result in all_results.values()]:
                writer.writerow(data)
    except IOError:
        click.echo(
            click.style("Could not open output file for writing", fg=CLI_COLOR_ERROR),
            err=True,
        )
        raise click.Abort()


def cleanup_files(dest_path, files_to_keep, fileutil):
    """cleanup dest_path by deleting and files and empty directories
        not in files_to_keep

    Args:
        dest_path: path to directory to clean
        files_to_keep: list of full file paths to keep (not delete)
        fileutile: FileUtil object

    Returns:
        tuple of (list of files deleted, list of directories deleted)
    """
    keepers = {str(filename).lower(): 1 for filename in files_to_keep}

    deleted_files = []
    for p in pathlib.Path(dest_path).rglob("*"):
        path = str(p).lower()
        if p.is_file() and path not in keepers:
            verbose_(f"Deleting {p}")
            fileutil.unlink(p)
            deleted_files.append(str(p))

    # delete empty directories
    deleted_dirs = []
    # walk directory tree bottom up and verify contents are empty
    for dirpath, _, _ in os.walk(dest_path, topdown=False):
        if not list(pathlib.Path(dirpath).glob("*")):
            # directory and directory is empty
            verbose_(f"Deleting empty directory {dirpath}")
            fileutil.rmdir(dirpath)
            deleted_dirs.append(str(dirpath))

    return (deleted_files, deleted_dirs)


def write_finder_tags(
    photo,
    files,
    keywords=False,
    keyword_template=None,
    album_keyword=None,
    person_keyword=None,
    exiftool_merge_keywords=None,
    finder_tag_template=None,
    strip=False,
    export_dir=None,
    export_db=None,
):
    """Write Finder tags (extended attributes) to files; only writes attributes if attributes on file differ from what would be written

    Args:
        photo: a PhotoInfo object
        files: list of file paths to write Finder tags to
        keywords: if True, sets Finder tags to all keywords including any evaluated from keyword_template, album_keyword, person_keyword, exiftool_merge_keywords
        keyword_template: list of keyword templates to evaluate for determining keywords
        album_keyword: if True, use album names as keywords
        person_keyword: if True, use person in image as keywords
        exiftool_merge_keywords: if True, include any keywords in the exif data of the source image as keywords
        finder_tag_template: list of templates to evaluate for determining Finder tags
        export_dir: value to use for {export_dir} template
        export_db: an ExportDB object

    Returns:
        (list of file paths that were updated with new Finder tags, list of file paths skipped because Finder tags didn't need updating)
    """

    tags = []
    written = []
    skipped = []
    if keywords:
        # match whatever keywords would've been used in --exiftool or --sidecar
        exif = photo._exiftool_dict(
            use_albums_as_keywords=album_keyword,
            use_persons_as_keywords=person_keyword,
            keyword_template=keyword_template,
            merge_exif_keywords=exiftool_merge_keywords,
        )
        try:
            if exif["IPTC:Keywords"]:
                tags.extend(exif["IPTC:Keywords"])
        except KeyError:
            pass

    if finder_tag_template:
        rendered_tags = []
        for template_str in finder_tag_template:
            try:
                options = RenderOptions(
                    none_str=_OSXPHOTOS_NONE_SENTINEL,
                    path_sep="/",
                    export_dir=export_dir,
                    exportdb=export_db,
                )
                rendered, unmatched = photo.render_template(template_str, options)
            except ValueError as e:
                raise click.BadOptionUsage(
                    "finder_tag_template",
                    f"Invalid template for --finder-tag-template '{template_str}': {e}",
                )

            if unmatched:
                click.echo(
                    click.style(
                        f"Warning: unknown field for template: {template_str} unknown field = {unmatched}",
                        fg=CLI_COLOR_WARNING,
                    ),
                    err=True,
                )
            rendered_tags.extend(rendered)

        # filter out any template values that didn't match by looking for sentinel
        if strip:
            rendered_tags = [value.strip() for value in rendered_tags]

        rendered_tags = [
            value.replace(_OSXPHOTOS_NONE_SENTINEL, "") for value in rendered_tags
        ]
        tags.extend(rendered_tags)

    tags = [osxmetadata.Tag(tag) for tag in set(tags)]
    for f in files:
        md = osxmetadata.OSXMetaData(f)
        if sorted(md.tags) != sorted(tags):
            verbose_(f"Writing Finder tags to {f}")
            md.tags = tags
            written.append(f)
        else:
            verbose_(f"Skipping Finder tags for {f}: nothing to do")
            skipped.append(f)

    return (written, skipped)


def write_extended_attributes(
    photo,
    files,
    xattr_template,
    strip=False,
    export_dir=None,
    export_db=None,
):
    """Writes extended attributes to exported files

    Args:
        photo: a PhotoInfo object
        strip:   xattr_template: list of tuples: (attribute name, attribute template)
        export_dir: value to use for {export_dir} template
        exportdb: an ExportDB object

    Returns:
        tuple(list of file paths that were updated with new attributes, list of file paths skipped because attributes didn't need updating)
    """

    attributes = {}
    for xattr, template_str in xattr_template:
        try:
            options = RenderOptions(
                none_str=_OSXPHOTOS_NONE_SENTINEL,
                path_sep="/",
                export_dir=export_dir,
                exportdb=export_db,
            )
            rendered, unmatched = photo.render_template(template_str, options)
        except ValueError as e:
            raise click.BadOptionUsage(
                "xattr_template",
                f"Invalid template for --xattr-template '{template_str}': {e}",
            )
        if unmatched:
            click.echo(
                click.style(
                    f"Warning: unmatched template substitution for template: {template_str} unknown field={unmatched}",
                    fg=CLI_COLOR_WARNING,
                ),
                err=True,
            )

        # filter out any template values that didn't match by looking for sentinel
        if strip:
            rendered = [value.strip() for value in rendered]

        rendered = [value.replace(_OSXPHOTOS_NONE_SENTINEL, "") for value in rendered]

        try:
            attributes[xattr].extend(rendered)
        except KeyError:
            attributes[xattr] = rendered

    written = set()
    skipped = set()
    for f in files:
        md = osxmetadata.OSXMetaData(f)
        for attr, value in attributes.items():
            islist = osxmetadata.ATTRIBUTES[attr].list
            if value:
                value = ", ".join(value) if not islist else sorted(value)
            file_value = md.get_attribute(attr)

            if file_value and islist:
                file_value = sorted(file_value)

            if (not file_value and not value) or file_value == value:
                # if both not set or both equal, nothing to do
                # get_attribute returns None if not set and value will be [] if not set so can't directly compare
                verbose_(f"Skipping extended attribute {attr} for {f}: nothing to do")
                skipped.add(f)
            else:
                verbose_(f"Writing extended attribute {attr} to {f}")
                md.set_attribute(attr, value)
                written.add(f)

    return list(written), [f for f in skipped if f not in written]


def run_post_command(
    photo, post_command, export_results, export_dir, dry_run, exiftool_path, export_db
):
    # todo: pass in RenderOptions from export? (e.g. so it contains strip, etc?)
    # todo: need a shell_quote template type:
    # {shell_quote,{filepath}/foo/bar}
    # that quotes everything in the default value
    for category, command_template in post_command:
        files = getattr(export_results, category)
        for f in files:
            # some categories, like error, return a tuple of (file, error str)
            if isinstance(f, tuple):
                f = f[0]
            render_options = RenderOptions(
                export_dir=export_dir, filepath=f, exportdb=export_db
            )
            template = PhotoTemplate(photo, exiftool_path=exiftool_path)
            command, _ = template.render(command_template, options=render_options)
            command = command[0] if command else None
            if command:
                verbose_(f'Running command: "{command}"')
                if not dry_run:
                    args = shlex.split(command)
                    cwd = pathlib.Path(f).parent
                    run_error = None
                    run_results = None
                    try:
                        run_results = subprocess.run(command, shell=True, cwd=cwd)
                    except Exception as e:
                        run_error = e
                    finally:
                        run_error = run_error or run_results.returncode
                        if run_error:
                            click.echo(
                                click.style(
                                    f'Error running command "{command}": {run_error}',
                                    fg=CLI_COLOR_ERROR,
                                ),
                                err=True,
                            )


@cli.command(hidden=True)
@DB_OPTION
@DB_ARGUMENT
@click.option(
    "--dump",
    metavar="ATTR",
    help="Name of PhotosDB attribute to print; "
    + "can also use albums, persons, keywords, photos to dump related attributes.",
    multiple=True,
)
@click.option(
    "--uuid",
    metavar="UUID",
    help="Use with '--dump photos' to dump only certain UUIDs",
    multiple=True,
)
@click.option("--verbose", "-V", "verbose", is_flag=True, help="Print verbose output.")
@click.pass_obj
@click.pass_context
def debug_dump(ctx, cli_obj, db, photos_library, dump, uuid, verbose):
    """Print out debug info"""

    global VERBOSE
    VERBOSE = bool(verbose)

    db = get_photos_db(*photos_library, db, cli_obj.db)
    if db is None:
        click.echo(cli.commands["debug-dump"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    start_t = time.perf_counter()
    print(f"Opening database: {db}")
    photosdb = osxphotos.PhotosDB(dbfile=db, verbose=verbose_)
    stop_t = time.perf_counter()
    print(f"Done; took {(stop_t-start_t):.2f} seconds")

    for attr in dump:
        if attr == "albums":
            print("_dbalbums_album:")
            pprint.pprint(photosdb._dbalbums_album)
            print("_dbalbums_uuid:")
            pprint.pprint(photosdb._dbalbums_uuid)
            print("_dbalbum_details:")
            pprint.pprint(photosdb._dbalbum_details)
            print("_dbalbum_folders:")
            pprint.pprint(photosdb._dbalbum_folders)
            print("_dbfolder_details:")
            pprint.pprint(photosdb._dbfolder_details)
        elif attr == "keywords":
            print("_dbkeywords_keyword:")
            pprint.pprint(photosdb._dbkeywords_keyword)
            print("_dbkeywords_uuid:")
            pprint.pprint(photosdb._dbkeywords_uuid)
        elif attr == "persons":
            print("_dbfaces_uuid:")
            pprint.pprint(photosdb._dbfaces_uuid)
            print("_dbfaces_pk:")
            pprint.pprint(photosdb._dbfaces_pk)
            print("_dbpersons_pk:")
            pprint.pprint(photosdb._dbpersons_pk)
            print("_dbpersons_fullname:")
            pprint.pprint(photosdb._dbpersons_fullname)
        elif attr == "photos":
            if uuid:
                for uuid_ in uuid:
                    print(f"_dbphotos['{uuid_}']:")
                    try:
                        pprint.pprint(photosdb._dbphotos[uuid_])
                    except KeyError:
                        print(f"Did not find uuid {uuid_} in _dbphotos")
            else:
                print("_dbphotos:")
                pprint.pprint(photosdb._dbphotos)
        else:
            try:
                val = getattr(photosdb, attr)
                print(f"{attr}:")
                pprint.pprint(val)
            except Exception:
                print(f"Did not find attribute {attr} in PhotosDB")


@cli.command()
@DB_OPTION
@JSON_OPTION
@DB_ARGUMENT
@click.pass_obj
@click.pass_context
def keywords(ctx, cli_obj, db, json_, photos_library):
    """Print out keywords found in the Photos library."""

    # below needed for to make CliRunner work for testing
    cli_db = cli_obj.db if cli_obj is not None else None
    db = get_photos_db(*photos_library, db, cli_db)
    if db is None:
        click.echo(cli.commands["keywords"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    photosdb = osxphotos.PhotosDB(dbfile=db)
    keywords = {"keywords": photosdb.keywords_as_dict}
    if json_ or cli_obj.json:
        click.echo(json.dumps(keywords, ensure_ascii=False))
    else:
        click.echo(yaml.dump(keywords, sort_keys=False, allow_unicode=True))


@cli.command()
@DB_OPTION
@JSON_OPTION
@DB_ARGUMENT
@click.pass_obj
@click.pass_context
def albums(ctx, cli_obj, db, json_, photos_library):
    """Print out albums found in the Photos library."""

    # below needed for to make CliRunner work for testing
    cli_db = cli_obj.db if cli_obj is not None else None
    db = get_photos_db(*photos_library, db, cli_db)
    if db is None:
        click.echo(cli.commands["albums"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    photosdb = osxphotos.PhotosDB(dbfile=db)
    albums = {"albums": photosdb.albums_as_dict}
    if photosdb.db_version > _PHOTOS_4_VERSION:
        albums["shared albums"] = photosdb.albums_shared_as_dict

    if json_ or cli_obj.json:
        click.echo(json.dumps(albums, ensure_ascii=False))
    else:
        click.echo(yaml.dump(albums, sort_keys=False, allow_unicode=True))


@cli.command()
@DB_OPTION
@JSON_OPTION
@DB_ARGUMENT
@click.pass_obj
@click.pass_context
def persons(ctx, cli_obj, db, json_, photos_library):
    """Print out persons (faces) found in the Photos library."""

    # below needed for to make CliRunner work for testing
    cli_db = cli_obj.db if cli_obj is not None else None
    db = get_photos_db(*photos_library, db, cli_db)
    if db is None:
        click.echo(cli.commands["persons"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    photosdb = osxphotos.PhotosDB(dbfile=db)
    persons = {"persons": photosdb.persons_as_dict}
    if json_ or cli_obj.json:
        click.echo(json.dumps(persons, ensure_ascii=False))
    else:
        click.echo(yaml.dump(persons, sort_keys=False, allow_unicode=True))


@cli.command()
@DB_OPTION
@JSON_OPTION
@DB_ARGUMENT
@click.pass_obj
@click.pass_context
def labels(ctx, cli_obj, db, json_, photos_library):
    """Print out image classification labels found in the Photos library."""

    # below needed for to make CliRunner work for testing
    cli_db = cli_obj.db if cli_obj is not None else None
    db = get_photos_db(*photos_library, db, cli_db)
    if db is None:
        click.echo(cli.commands["labels"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    photosdb = osxphotos.PhotosDB(dbfile=db)
    labels = {"labels": photosdb.labels_as_dict}
    if json_ or cli_obj.json:
        click.echo(json.dumps(labels, ensure_ascii=False))
    else:
        click.echo(yaml.dump(labels, sort_keys=False, allow_unicode=True))


@cli.command()
@DB_OPTION
@JSON_OPTION
@DB_ARGUMENT
@click.pass_obj
@click.pass_context
def info(ctx, cli_obj, db, json_, photos_library):
    """Print out descriptive info of the Photos library database."""

    db = get_photos_db(*photos_library, db, cli_obj.db)
    if db is None:
        click.echo(cli.commands["info"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    photosdb = osxphotos.PhotosDB(dbfile=db)
    info = {"database_path": photosdb.db_path, "database_version": photosdb.db_version}
    photos = photosdb.photos(movies=False)
    not_shared_photos = [p for p in photos if not p.shared]
    info["photo_count"] = len(not_shared_photos)

    hidden = [p for p in photos if p.hidden]
    info["hidden_photo_count"] = len(hidden)

    movies = photosdb.photos(images=False, movies=True)
    not_shared_movies = [p for p in movies if not p.shared]
    info["movie_count"] = len(not_shared_movies)

    if photosdb.db_version > _PHOTOS_4_VERSION:
        shared_photos = [p for p in photos if p.shared]
        info["shared_photo_count"] = len(shared_photos)

        shared_movies = [p for p in movies if p.shared]
        info["shared_movie_count"] = len(shared_movies)

    keywords = photosdb.keywords_as_dict
    info["keywords_count"] = len(keywords)
    info["keywords"] = keywords

    albums = photosdb.albums_as_dict
    info["albums_count"] = len(albums)
    info["albums"] = albums

    if photosdb.db_version > _PHOTOS_4_VERSION:
        albums_shared = photosdb.albums_shared_as_dict
        info["shared_albums_count"] = len(albums_shared)
        info["shared_albums"] = albums_shared

    persons = photosdb.persons_as_dict

    info["persons_count"] = len(persons)
    info["persons"] = persons

    if cli_obj.json or json_:
        click.echo(json.dumps(info, ensure_ascii=False))
    else:
        click.echo(yaml.dump(info, sort_keys=False, allow_unicode=True))


@cli.command()
@DB_OPTION
@JSON_OPTION
@DB_ARGUMENT
@click.pass_obj
@click.pass_context
def places(ctx, cli_obj, db, json_, photos_library):
    """Print out places found in the Photos library."""

    # below needed for to make CliRunner work for testing
    cli_db = cli_obj.db if cli_obj is not None else None
    db = get_photos_db(*photos_library, db, cli_db)
    if db is None:
        click.echo(cli.commands["places"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    photosdb = osxphotos.PhotosDB(dbfile=db)
    place_names = {}
    for photo in photosdb.photos(movies=True):
        if photo.place:
            try:
                place_names[photo.place.name] += 1
            except Exception:
                place_names[photo.place.name] = 1
        else:
            try:
                place_names[_UNKNOWN_PLACE] += 1
            except Exception:
                place_names[_UNKNOWN_PLACE] = 1

    # sort by place count
    places = {
        "places": {
            name: place_names[name]
            for name in sorted(
                place_names.keys(), key=lambda key: place_names[key], reverse=True
            )
        }
    }

    # below needed for to make CliRunner work for testing
    cli_json = cli_obj.json if cli_obj is not None else None
    if json_ or cli_json:
        click.echo(json.dumps(places, ensure_ascii=False))
    else:
        click.echo(yaml.dump(places, sort_keys=False, allow_unicode=True))


@cli.command()
@DB_OPTION
@JSON_OPTION
@deleted_options
@DB_ARGUMENT
@click.pass_obj
@click.pass_context
def dump(ctx, cli_obj, db, json_, deleted, deleted_only, photos_library):
    """Print list of all photos & associated info from the Photos library."""

    db = get_photos_db(*photos_library, db, cli_obj.db)
    if db is None:
        click.echo(cli.commands["dump"].get_help(ctx), err=True)
        click.echo("\n\nLocated the following Photos library databases: ", err=True)
        _list_libraries()
        return

    # check exclusive options
    if deleted and deleted_only:
        click.echo("Incompatible dump options", err=True)
        click.echo(cli.commands["dump"].get_help(ctx), err=True)
        return

    photosdb = osxphotos.PhotosDB(dbfile=db)
    if deleted or deleted_only:
        photos = photosdb.photos(movies=True, intrash=True)
    else:
        photos = []
    if not deleted_only:
        photos += photosdb.photos(movies=True)

    print_photo_info(photos, json_ or cli_obj.json)


@cli.command(name="list")
@JSON_OPTION
@click.pass_obj
@click.pass_context
def list_libraries(ctx, cli_obj, json_):
    """Print list of Photos libraries found on the system."""

    # implemented in _list_libraries so it can be called by other CLI functions
    # without errors due to passing ctx and cli_obj
    _list_libraries(json_=json_ or cli_obj.json, error=False)


def _list_libraries(json_=False, error=True):
    """Print list of Photos libraries found on the system.
    If json_ == True, print output as JSON (default = False)"""

    photo_libs = osxphotos.utils.list_photo_libraries()
    sys_lib = osxphotos.utils.get_system_library_path()
    last_lib = osxphotos.utils.get_last_library_path()

    if json_:
        libs = {
            "photo_libraries": photo_libs,
            "system_library": sys_lib,
            "last_library": last_lib,
        }
        click.echo(json.dumps(libs, ensure_ascii=False))
    else:
        last_lib_flag = sys_lib_flag = False

        for lib in photo_libs:
            if lib == sys_lib:
                click.echo(f"(*)\t{lib}", err=error)
                sys_lib_flag = True
            elif lib == last_lib:
                click.echo(f"(#)\t{lib}", err=error)
                last_lib_flag = True
            else:
                click.echo(f"\t{lib}", err=error)

        if sys_lib_flag or last_lib_flag:
            click.echo("\n", err=error)
        if sys_lib_flag:
            click.echo("(*)\tSystem Photos Library", err=error)
        if last_lib_flag:
            click.echo("(#)\tLast opened Photos Library", err=error)


@cli.command(name="about")
@click.pass_obj
@click.pass_context
def about(ctx, cli_obj):
    """Print information about osxphotos including license."""
    license = """
MIT License

Copyright (c) 2019-2021 Rhet Turnbull

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    click.echo(f"osxphotos, version {__version__}")
    click.echo("")
    click.echo(f"Source code available at: {OSXPHOTOS_URL}")
    click.echo(license)


@cli.command(name="tutorial")
@click.argument(
    "WIDTH",
    nargs=-1,
    type=click.INT,
)
@click.pass_obj
@click.pass_context
def tutorial(ctx, cli_obj, width):
    """Display osxphotos tutorial."""
    width = width[0] if width else 100
    click.echo_via_pager(tutorial_help(width=width))


def _show_photo(photo):
    """open image with default image viewer

    Note: This is for debugging only -- it will actually open any filetype which could
    be very, very bad.

    Args:
        photo: PhotoInfo object or a path to a photo on disk
    """
    photopath = photo.path if isinstance(photo, osxphotos.PhotoInfo) else photo

    if not os.path.isfile(photopath):
        return f"'{photopath}' does not appear to be a valid photo path"

    os.system(f"open '{photopath}'")


def _load_photos_db(dbpath):
    print("Loading database")
    tic = time.perf_counter()
    photosdb = osxphotos.PhotosDB(dbfile=dbpath, verbose=print)
    toc = time.perf_counter()
    tictoc = toc - tic
    print(f"Done: took {tictoc:0.2f} seconds")
    return photosdb


def _get_photos(photosdb):
    """get list of all photos in photosdb"""
    photos = photosdb.photos(images=True, movies=True)
    photos.extend(photosdb.photos(images=True, movies=True, intrash=True))
    return photos


def _get_selected(photosdb):
    """get list of PhotoInfo objects for photos selected in Photos"""

    def get_selected():
        selected = photoscript.PhotosLibrary().selection
        if not selected:
            return []
        return photosdb.photos(uuid=[p.uuid for p in selected])

    return get_selected


@cli.command()
@DB_OPTION
@click.pass_obj
@click.pass_context
def repl(ctx, cli_obj, db):
    """Run interactive osxphotos shell"""

    from osxphotos import PhotosDB, PhotoInfo, ExifTool
    from rich import inspect as _inspect

    pretty.install()
    print(f"python version: {sys.version}")
    print(f"osxphotos version: {osxphotos._version.__version__}")
    db = db or get_photos_db()
    photosdb = _load_photos_db(db)
    print("Getting photos")
    tic = time.perf_counter()
    photos = _get_photos(photosdb)
    toc = time.perf_counter()
    tictoc = toc - tic

    # shortcut for helper functions
    get_photo = photosdb.get_photo
    show = _show_photo
    get_selected = _get_selected(photosdb)
    selected = get_selected()

    def inspect(obj):
        """inspect object"""
        return _inspect(obj, methods=True)

    class ReprQuit:
        def __repr__(self):
            sys.exit(0)

        def __call__(self):
            sys.exit(0)

    quit = ReprQuit()
    q = ReprQuit()

    print(f"Found {len(photos)} photos in {tictoc:0.2f} seconds")
    print("The following variables are defined:")
    print(f"- photosdb: PhotosDB() instance for {photosdb.library_path}")
    print(
        f"- photos: list of PhotoInfo objects for all photos in photosdb, including those in the trash (len={len(photos)})"
    )
    print(
        f"- selected: list of PhotoInfo objects for any photos selected in Photos (len={len(selected)})"
    )
    print(f"\nThe following functions may be helpful:")
    print(f"- get_photo(uuid): return a PhotoInfo object for photo with uuid")
    print(
        f"- get_selected(): return list of PhotoInfo objects for photos selected in Photos"
    )
    print(f"- show(photo): open a photo object in the default viewer")
    print(
        f"- help(object): print help text including list of methods for object; for example, help(PhotosDB)"
    )
    print(
        f"- inspect(object): print information about an object; for example inspect(photosdb)"
    )
    print(f"- q, quit, or quit(): exit this interactive shell\n")
    code.interact(banner="", local=locals())
