"""
packwiz `refresh` 대체 스크립트 (packwiz를 설치하지 않아도 됨)

모드팩 폴더를 훑어서 index.toml 을 다시 만들고, pack.toml 안의 index 해시를 갱신한다.
결과물은 packwiz 공식 포맷과 같아서 packwiz-installer 가 그대로 읽는다.

사용법:  python tools/refresh.py [모드팩 폴더]   (기본값: 이 파일의 상위 폴더)
"""
import fnmatch
import hashlib
import re
import sys
from pathlib import Path

ALWAYS_IGNORE = ["pack.toml", "index.toml", ".packwizignore", ".git/"]


def load_ignore(root: Path):
    patterns = list(ALWAYS_IGNORE)
    f = root / ".packwizignore"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def ignored(rel: str, patterns) -> bool:
    name = rel.rsplit("/", 1)[-1]
    for p in patterns:
        if p.endswith("/"):
            d = p.strip("/")
            if rel == d or rel.startswith(d + "/") or ("/" + d + "/") in ("/" + rel):
                return True
        elif fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(name, p):
            return True
    return False


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fp:
        for chunk in iter(lambda: fp.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def toml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    patterns = load_ignore(root)

    files = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if ignored(rel, patterns):
            continue
        files.append((rel, p))

    out = ['hash-format = "sha256"', ""]
    for rel, p in files:
        out.append("[[files]]")
        out.append(f"file = {toml_str(rel)}")
        out.append(f"hash = {toml_str(sha256(p))}")
        if rel.endswith(".pw.toml"):
            out.append("metafile = true")
        out.append("")
    index = root / "index.toml"
    index.write_text("\n".join(out), encoding="utf-8", newline="\n")

    pack = root / "pack.toml"
    text = pack.read_text(encoding="utf-8")
    new_hash = sha256(index)
    text, n = re.subn(r'(\[index\][^\[]*?\nhash\s*=\s*)"[^"]*"', lambda m: m.group(1) + f'"{new_hash}"', text, count=1)
    if n != 1:
        sys.exit("pack.toml 의 [index] hash 줄을 찾지 못했습니다.")
    pack.write_text(text, encoding="utf-8", newline="\n")

    print(f"index.toml 갱신 완료: 파일 {len(files)}개")
    for rel, _ in files:
        print("  -", rel)


if __name__ == "__main__":
    main()
