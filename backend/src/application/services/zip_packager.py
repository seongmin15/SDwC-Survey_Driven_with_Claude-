"""ZIP Packager: packages generated files into a ZIP archive."""
import io
import zipfile
from pathlib import Path
from uuid import UUID


class ZipPackager:
    def __init__(self, output_dir: str) -> None:
        self._output_dir = Path(output_dir)

    def package(self, project_id: UUID, files: dict[str, str]) -> str:
        """Create a ZIP from files dict and save to output_dir.

        Args:
            project_id: Project UUID for filename.
            files: Mapping of {relative_path: content}.

        Returns:
            The saved zip file path as string.
        """
        self._output_dir.mkdir(parents=True, exist_ok=True)
        zip_path = self._output_dir / f"{project_id}.zip"

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for path, content in sorted(files.items()):
                zf.writestr(path, content)
        buf.seek(0)

        zip_path.write_bytes(buf.getvalue())
        return str(zip_path)
