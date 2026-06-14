import filetype

from core.constants import COMPRESSED_EXTENSIONS, COMPRESSED_MIMES


class FileValidator:

    @staticmethod
    def validate_is_compressed(archivo: bytes) -> None:
        kind = filetype.guess(archivo)
        if kind is None or kind.mime not in COMPRESSED_MIMES:
            raise ValueError(
                f"El archivo debe ser un archivo comprimido ({COMPRESSED_EXTENSIONS})"
            )
