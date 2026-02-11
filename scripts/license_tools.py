import argparse
import base64
import json
from datetime import datetime
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    PublicFormat,
    load_pem_private_key,
)


def _canonical_payload(data: dict) -> bytes:
    payload = {
        "name": data.get("name", ""),
        "license_id": data.get("license_id", ""),
        "issued_at": data.get("issued_at", ""),
        "expires_at": data.get("expires_at", ""),
        "product": data.get("product", ""),
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def generate_keys(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )
    public_pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    )

    (out_dir / "tdm_private_key.pem").write_bytes(private_pem)
    (out_dir / "tdm_public_key.pem").write_bytes(public_pem)


def issue_license(
    private_key_path: Path,
    out_path: Path,
    *,
    name: str,
    license_id: str,
    product: str,
    issued_at: str,
    expires_at: str | None,
    public_key_pem: str,
) -> None:
    private_key = load_pem_private_key(private_key_path.read_bytes(), password=None)
    payload = {
        "name": name,
        "license_id": license_id,
        "issued_at": issued_at,
        "expires_at": expires_at or "",
        "product": product,
    }

    signature = private_key.sign(_canonical_payload(payload))
    license_data = {
        **payload,
        "public_key": public_key_pem.strip(),
        "signature": base64.b64encode(signature).decode("ascii"),
    }
    out_path.write_text(json.dumps(license_data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="TDM license key tools")
    sub = parser.add_subparsers(dest="cmd", required=True)

    gen = sub.add_parser("gen-keys", help="Generate Ed25519 key pair")
    gen.add_argument("--out", default="license-keys", help="Output directory")

    issue = sub.add_parser("issue", help="Issue a license.json")
    issue.add_argument("--private-key", required=True, help="Path to private key PEM")
    issue.add_argument("--public-key", required=True, help="Path to public key PEM")
    issue.add_argument("--out", default="license.json", help="Output license file")
    issue.add_argument("--name", required=True)
    issue.add_argument("--license-id", required=True)
    issue.add_argument("--product", default="tdm")
    issue.add_argument("--issued-at", default=datetime.now().isoformat())
    issue.add_argument("--expires-at", default="")

    args = parser.parse_args()

    if args.cmd == "gen-keys":
        generate_keys(Path(args.out))
    elif args.cmd == "issue":
        public_key_pem = Path(args.public_key).read_text(encoding="utf-8")
        issue_license(
            Path(args.private_key),
            Path(args.out),
            name=args.name,
            license_id=args.license_id,
            product=args.product,
            issued_at=args.issued_at,
            expires_at=args.expires_at if args.expires_at else None,
            public_key_pem=public_key_pem,
        )


if __name__ == "__main__":
    main()
