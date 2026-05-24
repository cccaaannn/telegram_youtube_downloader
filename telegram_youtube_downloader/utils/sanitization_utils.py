import re
import unicodedata
from pathlib import PurePosixPath


class SanitizationUtils:
	__bad_char_replacement = "_"
	__empty_filename_replacement = "unknown"
	__max_filename_bytes = 200
	__bad_path_chars = (".", "..")
	__bad_chars_re = re.compile(r'[\x00-\x1f\x7f<>:"/\\|?*]')
	__reserved_filenames = {
		"CON",
		"PRN",
		"AUX",
		"NUL",
		*(f"COM{i}" for i in range(1, 10)),
		*(f"LPT{i}" for i in range(1, 10)),
	}

	@staticmethod
	def sanitize_filename(filename: str | None) -> str:
		"""
		Sanitize filename for safe use across all systems.
		This could be too aggressive for some cases.
		"""

		# Empty name
		if not filename:
			return SanitizationUtils.__empty_filename_replacement

		# Unicode normalization (Mac uses different normalization form)
		filename = unicodedata.normalize("NFC", filename)

		# Replace bad chars
		filename = SanitizationUtils.__bad_chars_re.sub(
			SanitizationUtils.__bad_char_replacement, filename
		)

		# Strip leading and trailing spaces and dots (Windows does not allow)
		filename = filename.strip(" .")

		# Reject names that became empty or are path-traversal tokens
		if not filename or filename in SanitizationUtils.__bad_path_chars:
			return SanitizationUtils.__empty_filename_replacement

		# Strip Windows reserved names (CON, NUL, COM1, ...)
		path = PurePosixPath(filename)
		stem, suffix = path.stem, path.suffix
		if stem.upper() in SanitizationUtils.__reserved_filenames:
			stem = f"{stem}_"
		filename = f"{stem}{suffix}"

		# Truncate by bytes (filesystem 255 byte limit), without splitting multi-byte characters like emojis
		encoded = filename.encode("utf-8")[: SanitizationUtils.__max_filename_bytes]
		filename = encoded.decode("utf-8", errors="ignore")

		return filename or SanitizationUtils.__empty_filename_replacement
