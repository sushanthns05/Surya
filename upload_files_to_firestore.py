"""
Upload files from a local folder into Firestore documents.

Usage:
  python upload_files_to_firestore.py --folder . --collection project_files

Requirements:
  pip install firebase-admin
  export GOOGLE_APPLICATION_CREDENTIALS="/path/to/serviceAccountKey.json"

If you prefer to use application default credentials, run:
  gcloud auth application-default login

This script is intentionally conservative:
- it uploads file metadata for every file
- it uploads full text content only for text files smaller than 500KB
- it avoids storing raw binary content in Firestore
"""

import argparse
import base64
import hashlib
import mimetypes
import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore

TEXT_FILE_MAX_BYTES = 500_000


def is_text_file(path: Path) -> bool:
    try:
        with open(path, 'rb') as f:
            chunk = f.read(2048)
        if b'\x00' in chunk:
            return False
        chunk.decode('utf-8')
        return True
    except Exception:
        return False


def build_doc_id(relative_path: str) -> str:
    normalized = relative_path.replace('\\', '/').strip('/')
    return hashlib.sha1(normalized.encode('utf-8')).hexdigest()


def load_file_content(path: Path) -> str | None:
    size = path.stat().st_size
    if size > TEXT_FILE_MAX_BYTES:
        return None
    if not is_text_file(path):
        return None
    try:
        return path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return None


def collect_files(folder: Path) -> list[Path]:
    ignored_dirs = {'.git', '.firebase', '.vscode', '__pycache__', 'node_modules', 'public/uploads'}
    files = []
    for root, dirs, filenames in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        for filename in filenames:
            path = Path(root) / filename
            if path.suffix.lower() in {'.pyc', '.pyo', '.exe', '.dll', '.so', '.dylib'}:
                continue
            files.append(path)
    return files


def init_firestore(credential_path: str | None, project_id: str | None):
    if credential_path:
        cred = credentials.Certificate(credential_path)
        firebase_admin.initialize_app(cred, {'projectId': project_id} if project_id else None)
    else:
        firebase_admin.initialize_app(options={'projectId': project_id} if project_id else None)
    return firestore.client()


def upload_folder(folder: Path, collection_name: str, client: firestore.Client):
    files = collect_files(folder)
    print(f"Found {len(files)} files in {folder.resolve()}")
    for path in files:
        rel_path = str(path.relative_to(folder)).replace('\\', '/')
        doc_id = build_doc_id(rel_path)
        size = path.stat().st_size
        mime_type, _ = mimetypes.guess_type(str(path))
        content = load_file_content(path)

        doc = {
            'name': path.name,
            'relative_path': rel_path,
            'size_bytes': size,
            'mime_type': mime_type or 'application/octet-stream',
            'is_text': content is not None,
            'content': content,
            'uploaded_at': firestore.SERVER_TIMESTAMP,
        }

        client.collection(collection_name).document(doc_id).set(doc)
        print(f"Uploaded: {rel_path} -> {collection_name}/{doc_id}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Upload local files into Firestore.')
    parser.add_argument('--folder', default='.', help='Local folder to upload')
    parser.add_argument('--collection', default='project_files', help='Firestore collection name')
    parser.add_argument('--project', default=None, help='Firestore project ID')
    parser.add_argument('--credentials', default=None, help='Path to Firebase service account JSON file')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    folder = Path(args.folder).resolve()

    if not folder.exists() or not folder.is_dir():
        raise SystemExit(f"Folder not found: {folder}")

    print(f"Initializing Firestore client for project: {args.project or '<default>'}")
    client = init_firestore(args.credentials, args.project)
    upload_folder(folder, args.collection, client)


if __name__ == '__main__':
    main()
