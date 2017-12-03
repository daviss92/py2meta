#!/usr/bin/env python

"""
Copyright (C) 2017 Sean Davis

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Sean Davis"
__copyright__ = "Copyright (C) 2017 Sean Davis"
__license__ = "GNU General Public License"
__version__ = "0.1"

import os
import re
import sys
import ntpath
import platform
import subprocess
import datetime
import json

_create_formats = ["DR4", "EXIF", "EXV", "ICC", "ICM", "MIE", "ODI", "ODP",
"ODS", "ODT", "VRD", "XMP"]

_read_formats = ["3FR", "A", "AA", "ACR", "AFM", "ACFM", "AMFM", "AIFF", "AIF",
"AIFC", "APE", "ASF", "AVI", "BMP", "DIB", "BPG", "BTF", "CHM", "COS", "DCM",
"DC3", "DIC", "DICM", "DCR", "DFONT", "DIVX", "DJVU", "DJV", "DOC", "DOT",
"DOCX", "DOCM", "DOTX", "DOTM", "DPX", "DSS", "DS2", "DYLIB", "DV", "EIP",
"EPUB", "EXE", "DLL", "EXR", "FFF", "FLA", "FLAC", "FLV", "FPF", "FPX", "GZ",
"GZIP", "HDR", "HEIC", "HEIF", "HTML", "HTM", "XHTML", "ICS", "ICAL", "IDML",
"INX", "ISO", "ITC", "J2C", "JPC", "JSON", "K25", "KDC", "KEY", "KTH", "LA",
"LFP", "LFR", "LNK", "M2TS", "MTS", "M2T", "TS", "MAX", "MIFF", "MIF", "MKA",
"MKV", "MKS", "MOBI", "AZW", "AZW3", "MODD", "MOI", "MP3", "MPC", "MPEG", "MPG",
"M2V", "MXF", "NMBTEMPLATE", "NUMBERS", "O", "ODB", "ODC", "ODF", "ODG", "ODI",
"ODP", "ODS", "ODT", "OFR", "OGG", "OGV", "OPUS", "OTF", "PAC", "PAGES", "PCD",
"PDB", "PRC", "PFA", "PFB", "PFM", "PGF", "PICT", "PCT", "PLIST", "PMP", "PPT",
"PPS", "POT", "POTX", "POTM", "PPSX", "PPSM", "PPTX", "PPTM", "PSP", "PSPIMAGE",
"RA", "RAM", "RPM", "RAR", "RAW", "RIFF", "RIF", "RM", "RV", "RMVB", "RSRC",
"RTF", "RWZ", "SEQ", "SO", "SRF", "SVG", "SWF", "THMX", "TTF", "TTC", "TORRENT",
"VCF", "VCARD", "VOB", "VSD", "WAV", "WEBM", "WEBP", "WMA", "WMV", "WV", "XCF",
"XLS", "XLT", "XLSX", "XLSM", "XLSB", "XLTX", "XLTM", "ZIP"]

_write_formats = ["3G2", "3GP2", "3GP", "3GPP", "AAX", "AI", "AIT", "ARW",
"CR2", "CRW", "CIFF", "CS1", "DCP", "DNG", "DVB", "EPS", "EPSF", "PS", "ERF",
"F4A", "F4B", "F4P", "F4V", "FFF", "FLIF", "GIF", "HDP", "WDP", "JXR", "IIQ",
"IND", "INDD", "INDT", "JP2", "JPF", "J2K", "JPM", "JPX", "JPEG", "JPG", "JPE",
"M4A", "M4B", "M4P", "M4V", "MEF", "MOS", "MOV", "QT", "MP4", "MPO", "MQV",
"MRW", "NEF", "NRW", "ODI", "ODP", "ODS", "ODT", "ORF", "PDF", "PEF", "PNG", 
"JNG", "MNG", "PPM", "PBM", "PGM", "PSD", "PSB", "PSDT", "QTIF", "QTI", "QIF",
"RAF", "RAW", "RW2", "RWL", "SR2", "SRW", "THM", "TIFF", "TIF", "X3F"]


def __verify_installation( ep ):
	pctype = platform.system()

	if ep is None:
		if ( pctype == "darwin" or "linux" in pctype ):
			cmd = "exiftool"
		else:
			cmd = "exiftool.exe"
	else:
		cmd = ep

	results = _run_command( cmd )

	if ( ( pctype == "darwin" or "linux" in pctype ) and "command not found"
	in results[0] ):
		raise RuntimeError( "Running this requires exiftool installed." )
	elif ( pctype == "win" and "is not recognized" in results[0] ):
		raise RuntimeError( "Running this requires exiftool installed." )


def _verify_file( formats, f ):
	path, filename = ntpath.split( f )
	print filename


def _run_command( cmd ):
	proc = subprocess.Popen( cmd, stdout=subprocess.PIPE )
	output, err = proc.communicate()
	proc.wait()

	return [output, err]


class copy( object ):
	def __init__( self, path=None, overwrite=False ):
		__verify_installation( path )
		self.exiftool = path
		self.overwrite = overwrite

	def all( self ):
		"""exiftool -tagsfromfile file.ext -all:all output.ext"""
		pass

	def all_iptc( self ):
		"""exiftool -tagsfromfile file.ext -iptc:all output.ext"""
		pass

	def all_xmp( self ):
		"""exiftool -tagsfromfile file.ext -xmp:all output.ext"""
		pass

	def custom( self ):
		"""custom arguments"""
		pass


class read( object ):
	def __init__( self, path=None ):
		__verify_installation( path )
		self.exiftool = path

	def all( self ):
		"""exiftool x.ext"""
		pass

	def all_contains( self ):
		"""exiftool "-*resolution*" image.jpg"""
		pass

	def all_duplicates( self ):
		"""exiftool -a -u -g1 a.jpg"""
		pass

	def common( self ):
		"""exiftool -common x.ext"""
		pass

	def custom( self ):
		"""custom arguments"""
		pass


class write( object ):
	def __init__( self, path=None, overwrite=False ):
		__verify_installation()
		self.exiftool = path
		self.overwrite = overwrite

	def keywords( self, data="append" ):
		"""exiftool -iptc:keywords+="""
		pass

	def custom( self ):
		"""custom arguments"""
		pass


def usage():
    print ("""
To use this module, create an instance of either the copy, read, or
write class, passing in the exiftool path (if applicable), and the path
to the image to be handled. You may also pass in whether you want the
program to automatically keep a backup of your original photo
(default=False). If a backup is created, it will be in the same location
as the original, with "_ORIGINAL" appended to the file name. Once you
have an editor instance, you call its methods to get information about
the image, or to modify the image's metadata.""")

if __name__ == "__main__":
    usage()
