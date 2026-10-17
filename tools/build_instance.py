"""
친구용 Prism Launcher 인스턴스(.zip)를 만든다.

만들어지는 zip 안에는
  - instance.cfg   : 실행 전 자동 업데이트 명령 + 실행 시 서버 자동 접속
  - mmc-pack.json  : Minecraft / Fabric 버전 (pack.toml 에서 읽음)
  - minecraft/packwiz-installer-bootstrap.jar
이 들어 있고, 친구는 Prism 에서 이 zip 을 '가져오기'만 하면 된다.

사용법:
  python tools/build_instance.py --pack-url https://.../pack.toml \
         --bootstrap packwiz-installer-bootstrap.jar --out UNLEASHED.zip
"""
import argparse
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read_versions():
    text = (ROOT / "pack.toml").read_text(encoding="utf-8")
    section = text.split("[versions]", 1)[1]
    mc = re.search(r'minecraft\s*=\s*"([^"]+)"', section).group(1)
    fabric = re.search(r'fabric\s*=\s*"([^"]+)"', section).group(1)
    return mc, fabric


def ini_escape(value: str) -> str:
    # Qt QSettings(ini) 형식: 따옴표/역슬래시가 들어간 값은 "..." 로 감싸고 이스케이프
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-url", required=True)
    ap.add_argument("--bootstrap", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    cfg = json.loads((ROOT / "tools" / "instance.json").read_text(encoding="utf-8"))
    name = cfg.get("instance_name") or "UNLEASHED"
    server = (cfg.get("server_address") or "").strip()
    mem = int(cfg.get("max_memory_mb") or 0)
    mc, fabric = read_versions()

    pre_launch = f'"$INST_JAVA" -jar packwiz-installer-bootstrap.jar {args.pack_url}'
    lines = [
        "[General]",
        "ConfigVersion=1.2",
        "InstanceType=OneSix",
        f"name={name}",
        "iconKey=default",
        "OverrideCommands=true",
        f"PreLaunchCommand={ini_escape(pre_launch)}",
    ]
    if server:
        lines += ["JoinServerOnLaunch=true", f"JoinServerOnLaunchAddress={server}"]
    if mem > 0:
        lines += ["OverrideMemory=true", f"MaxMemAlloc={mem}", f"MinMemAlloc={min(512, mem)}"]

    mmc_pack = {
        "formatVersion": 1,
        "components": [
            {"uid": "net.minecraft", "version": mc, "important": True},
            {"uid": "net.fabricmc.intermediary", "version": mc, "dependencyOnly": True},
            {"uid": "net.fabricmc.fabric-loader", "version": fabric},
        ],
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("instance.cfg", "\n".join(lines) + "\n")
        z.writestr("mmc-pack.json", json.dumps(mmc_pack, indent=2))
        z.write(args.bootstrap, "minecraft/packwiz-installer-bootstrap.jar")

    print(f"{out} 생성 (MC {mc}, Fabric {fabric}, 서버 자동접속: {server or '없음'})")


if __name__ == "__main__":
    main()
