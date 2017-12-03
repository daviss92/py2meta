#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import pathlib
import platform
import subprocess

_create_formats = ["DR4", "EXIF", "EXV", "ICC", "ICM", "MIE", "ODI", "ODP",
"ODS", "ODT", "VRD", "XMP"]

_read_formats = ["3FR", "3G2", "3GP2", "3GP", "3GPP", "A", "AA", "AAX", "ACR",
"AFM", "ACFM", "AMFM", "AI", "AIT", "AIFF", "AIF", "AIFC", "APE", "ARW", "ASF",
"AVI", "BMP", "DIB", "BPG", "BTF", "CHM", "COS", "CR2", "CRW", "CIFF", "CS1",
"DCM", "DC3", "DIC", "DICM", "DCP", "DCR", "DFONT", "DIVX", "DJVU", "DJV",
"DNG", "DOC", "DOT", "DOCX", "DOCM", "DOTX", "DOTM", "DPX", "DR4", "DSS", "DS2",
"DYLIB", "DV", "DVB", "EIP", "EPS", "EPSF", "PS", "EPUB", "ERF", "EXE", "DLL",
"EXIF", "EXR", "EXV", "F4A", "F4B", "F4P", "F4V", "FFF", "FFF", "FLA", "FLAC",
"FLIF", "FLV", "FPF", "FPX", "GIF", "GZ", "GZIP", "HDP", "WDP", "JXR", "HDR",
"HEIC", "HEIF", "HTML", "HTM", "XHTML", "ICC", "ICM", "ICS", "ICAL", "IDML",
"IIQ", "IND", "INDD", "INDT", "INX", "ISO", "ITC", "J2C", "JPC", "JP2", "JPF",
"J2K", "JPM", "JPX", "JPEG", "JPG", "JPE", "JSON", "K25", "KDC", "KEY", "KTH",
"LA", "LFP", "LFR", "LNK", "M2TS", "MTS", "M2T", "TS", "M4A", "M4B", "M4P",
"M4V", "MAX", "MEF", "MIE", "MIFF", "MIF", "MKA", "MKV", "MKS", "MOBI", "AZW",
"AZW3", "MODD", "MOI", "MOS", "MOV", "QT", "MP3", "MP4", "MPC", "MPEG", "MPG",
"M2V", "MPO", "MQV", "MRW", "MXF", "NEF", "NMBTEMPLATE", "NRW", "NUMBERS", "O",
"ODB", "ODC", "ODF", "ODG,", "ODI", "ODP", "ODS", "ODT", "OFR", "OGG", "OGV",
"OPUS", "ORF", "OTF", "PAC", "PAGES", "PCD", "PDB", "PRC", "PDF", "PEF", "PFA",
"PFB", "PFM", "PGF", "PICT", "PCT", "PLIST", "PMP", "PNG, JNG", "MNG", "PPM",
"PBM", "PGM", "PPT", "PPS", "POT", "POTX", "POTM", "PPSX", "PPSM", "PPTX",
"PPTM", "PSD", "PSB", "PSDT", "PSP", "PSPIMAGE", "QTIF", "QTI", "QIF", "RA",
"RAF", "RAM", "RPM", "RAR", "RAW", "RAW", "RIFF", "RIF", "RM", "RV", "RMVB",
"RSRC", "RTF", "RW2", "RWL", "RWZ", "SEQ", "SO", "SR2", "SRF", "SRW", "SVG",
"SWF", "THM", "THMX", "TIFF", "TIF", "TTF", "TTC", "TORRENT", "VCF", "VCARD",
"VOB", "VRD", "VSD", "WAV", "WEBM", "WEBP", "WMA", "WMV", "WV", "X3F", "XCF",
"XLS", "XLT", "XLSX", "XLSM", "XLSB", "XLTX", "XLTM", "XMP", "ZIP"]

_write_formats = ["3G2", "3GP2", "3GP", "3GPP", "AAX", "AI", "AIT", "ARW",
"CR2", "CRW", "CIFF", "CS1", "DCP", "DNG", "DVB", "EPS", "EPSF", "PS", "ERF",
"F4A", "F4B", "F4P", "F4V", "FFF", "FLIF", "GIF", "HDP", "WDP", "JXR", "IIQ",
"IND", "INDD", "INDT", "JP2", "JPF", "J2K", "JPM", "JPX", "JPEG", "JPG", "JPE",
"M4A", "M4B", "M4P", "M4V", "MEF", "MOS", "MOV", "QT", "MP4", "MPO", "MQV",
"MRW", "NEF", "NRW", "ODI", "ODP", "ODS", "ODT", "ORF", "PDF", "PEF", "PNG",
"JNG", "MNG", "PPM", "PBM", "PGM", "PSD", "PSB", "PSDT", "QTIF", "QTI", "QIF",
"RAF", "RAW", "RW2", "RWL", "SR2", "SRW", "THM", "TIFF", "TIF", "X3F"]


def _cleanup_data( data, datatype ):
	if datatype == "string":
		x = str( data )
	elif datatype == "list":
		x = list( filter(
		None, [ re.sub( r"\s+", " ", s ) for s in data.split("\n") ] ) )
	elif datatype == "dict":
		y = list( filter(
		None, [ re.sub( r"\s+", " ", s ) for s in data.split("\n") ] ) )
		x = { k:v for k,v in ( i.split(' : ') for i in y ) }

	return x


def _run_command( cmd ):
	proc = subprocess.Popen( cmd, stdout=subprocess.PIPE, shell=True )
	output, err = proc.communicate()
	proc.wait()

	return output.decode('utf-8')


def _verify_file( c, f ):
	if c == "create":
		formats = _create_formats
	elif c == "read":
		formats = _read_formats
	else:
		formats = _write_formats

	extension = pathlib.Path( f ).suffix[1:]

	if not any( extension.upper() in x for x in formats ):
		raise RuntimeError( ("{} is not a valid file type to {}.").format( f, c ) )

	try:
		fp = open( f )
	except IOError as e:
		print(e)
		raise RuntimeError(
			("You do not have permissions to {} the file {}." ).format( c, f ))
	else:
		fp.close()

	return


def _verify_installation( x ):
	pctype = platform.system()

	if x is None:
		if ( pctype.lower() == "darwin" or "linux" in pctype.lower() ):
			cmd = "exiftool"
		else:
			cmd = "exiftool.exe"
	else:
		if ( pctype.lower() == "darwin" or "linux" in pctype.lower() ):
			if ( pathlib.Path( x ).is_file() or x == "exiftool" ):
				cmd = x
			else:
				cmd = "exiftool"
		else:
			if ( pathlib.Path( x ).is_file() or "exiftool.exe" in x ):
				cmd = x
			else:
				cmd = "exiftool.exe"

	try:
		results = _run_command( cmd )
	except Exception as e:
		print ( e )
		raise RuntimeError( "Running this requires exiftool installed." )
	else:
		if any( a in str( results[0] ) for a in ["command not found",
		"is not recognized"] ):
			raise RuntimeError( "Running this requires exiftool installed." )

	return cmd


class py3exifcopy( object ):
	def __init__( self, path=None, overwrite=False ):
		self.exiftool = _verify_installation( path )
		self.overwrite = overwrite

	def _check_sidecar( self, sidecar ):
		if sidecar is None:
			result = False
		else:
			if pathlib.Path( sidecar ).is_file():
				result = sidecar
			else:
				raise RuntimeError( "Not a valid sidecar file." )

		return result

	def all( self, args, sidecar=None ):
		"""exiftool -tagsfromfile file.ext -all:all output.ext"""
		pass

	def all_iptc( self, args, sidecar=None ):
		"""exiftool -tagsfromfile file.ext -iptc:all output.ext"""
		pass

	def all_xmp( self, args, sidecar=None ):
		"""exiftool -tagsfromfile file.ext -xmp:all output.ext"""
		pass

	def custom( self, args ):
		"""custom arguments"""
		pass


class py3exifread( object ):
	def __init__( self, path=None ):
		self.exiftool = _verify_installation( path )

	def all( self, filepath ):
		"""exiftool x.ext"""
		pass

	def all_contains( self, terms, filepath ):
		"""exiftool "-*resolution*" image.jpg"""
		pass

	def all_duplicates( self, filepath ):
		"""exiftool -a -u -g1 a.jpg"""
		pass

	def common( self, filepath, datatype ):
		_verify_file( "read", filepath )

		cmd = '"{}" -common "{}"'.format( self.exiftool, filepath )
		results = _run_command( cmd )
		data = _cleanup_data( results, datatype )

		return data

	def custom( self, args, filepath ):
		"""custom arguments"""
		pass


class py3exifwrite( object ):
	def __init__( self, path=None, overwrite=False ):
		self.exiftool = _verify_installation( path )
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
