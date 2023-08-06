import gzip
import json

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2007, The Cogent Project"
__credits__ = ["Noé Cruz", "Zurck'z", "Jesus Salazar"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"

##  Class GZip
#   Zipper class contains compress/decompress gzip methods
#
class GZip():
    """
    Helper compress/decompress gzip
    """

    @staticmethod
    def unzip_json( json_data_compressed) -> dict:
        """Decompress json compressed provided

        Parameters
        ----------
        data : bytes | str
            JSON data to descompress

        Returns
        -------
        dict
            JSON descompressed
        """
        return json.loads(GZip.decompress(json_data_compressed))

    @staticmethod
    def gzip_json( json_data: dict) -> bytes:
        """Compress JSON with gzip

        Parameters
        ----------
        data : str
            JSON data to compress
        enc : str, optional
            charset encoding (default is
            utf-8)

        Returns
        -------
        bytes
            Data compressed
        """
        return GZip.compress(json.dumps(json_data))

    @staticmethod
    def compress( data: str, enc = 'utf-8') -> bytes:
        """Decompress data provided

        Parameters
        ----------
        data : str
            Data to compress
        enc : str, optional
            charset encoding (default is
            utf-8)

        Returns
        -------
        bytes
            Data compressed
        """
        return gzip.compress(bytes(data,enc))

    @staticmethod
    def decompress(data: bytes, enc = 'utf-8') -> str:
        """Decompress data provided

        Parameters
        ----------
        data : str
            Gzip compressed data
        enc : str, optional
            charset encoding (default is
            utf-8)

        Returns
        -------
        str
            Data descompressed in string format
        """
        return gzip.decompress(data).decode(enc)