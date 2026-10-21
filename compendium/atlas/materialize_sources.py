"""Extract immutable annual archives for a local rebuild (Python standard library)."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parent

def extract_into(root):
    for year in [2023,2024,2025,2026]:
        archive=ROOT/'sources'/f'{year}_Mathematics_Source_Bundle.zip'
        destination=Path(root)/'source_working'/f'{year}_Mathematics_Source_Bundle'
        destination.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(archive) as z:
            for member in z.infolist():
                target=(destination/member.filename).resolve()
                if not target.is_relative_to(destination.resolve()):raise ValueError('Unsafe archive path')
            z.extractall(destination)
if __name__=='__main__':extract_into(ROOT);print('Four annual sources extracted.')
