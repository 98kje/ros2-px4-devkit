#!/usr/bin/env python3
"""두 파라미터 덤프 파일의 차이를 출력한다.

기체 튜닝을 하다 보면 "어제 백업본이랑 뭐가 달라졌지"를 자주 확인하게 된다.
ArduPilot .parm 과 PX4 .params 양쪽 형식을 모두 읽는다.

사용법:
    python3 tools/param_diff.py before.parm after.parm
    python3 tools/param_diff.py before.parm after.parm --tol 1e-6
"""
import argparse
import sys
from pathlib import Path


def load(path: Path) -> dict[str, float]:
    """.parm(공백/콤마 구분) 및 PX4 .params(1 1 NAME VALUE TYPE) 형식을 파싱한다."""
    params: dict[str, float] = {}
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue

        fields = line.replace(",", " ").split()
        if len(fields) >= 5 and fields[0].isdigit() and fields[1].isdigit():
            # PX4 형식: <sysid> <compid> <NAME> <VALUE> <TYPE>
            name, value = fields[2], fields[3]
        elif len(fields) >= 2:
            # ArduPilot 형식: <NAME> <VALUE>
            name, value = fields[0], fields[1]
        else:
            print(f"{path}:{lineno}: 해석 불가, 건너뜀 -> {raw!r}", file=sys.stderr)
            continue

        try:
            params[name] = float(value)
        except ValueError:
            print(f"{path}:{lineno}: 숫자 아님, 건너뜀 -> {value!r}", file=sys.stderr)
    return params


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument(
        "--tol", type=float, default=0.0, help="이 값 이하의 차이는 무시"
    )
    args = parser.parse_args()

    a, b = load(args.before), load(args.after)

    removed = sorted(set(a) - set(b))
    added = sorted(set(b) - set(a))
    changed = sorted(
        name for name in set(a) & set(b) if abs(a[name] - b[name]) > args.tol
    )

    for name in removed:
        print(f"- {name} = {a[name]:g}")
    for name in added:
        print(f"+ {name} = {b[name]:g}")
    for name in changed:
        print(f"~ {name}: {a[name]:g} -> {b[name]:g}")

    total = len(removed) + len(added) + len(changed)
    print(f"\n삭제 {len(removed)} / 추가 {len(added)} / 변경 {len(changed)}", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
