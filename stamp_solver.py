import time
from collections import namedtuple

import numpy as np

StampSet = namedtuple("StampSet", ["residual", "stamps"])


def solve_stamps(
    target_price: int, stamps: list[int], recursion: int = 0
) -> list[StampSet]:
    """
    手持ちの切手で目標の郵便料金を超える最小金額の組み合わせを算出する

    param:
        target_price
            目標金額
        stamps
            手持ちの切手の金額リスト
        recursion
            再帰の段数（初段のみ切手リストをソートするのに利用する）
    """
    if recursion == 0:
        # 初回のみ昇順ソートする
        stamps.sort()
    result = []
    min_residual = np.inf
    for idx, stamp in enumerate(stamps):
        if target_price <= stamp:
            # 予定金額に到達したら
            residual = stamp - target_price
            if residual < min_residual:
                # 最小値更新
                min_residual = residual
                ss = StampSet(residual, [stamp])
                result = [ss]
            elif residual == min_residual:
                # 最小値と同値
                ss = StampSet(residual, [stamp])
                result.append(ss)
        else:
            # 予定金額に到達しなかったら
            residual = target_price - stamp
            if len(stamps) == 1:
                continue
            remaining_stamps = stamps[idx + 1 :].copy()
            ss_list = solve_stamps(residual, remaining_stamps, recursion + 1)
            if ss_list:
                residual = ss_list[0].residual
                if residual < min_residual:
                    # 最小値更新
                    min_residual = residual
                    result = []
                    for ss in ss_list:
                        ss.stamps.append(stamp)
                        result.append(ss)
                elif residual == min_residual:
                    # 最小値と同値
                    for ss in ss_list:
                        ss.stamps.append(stamp)
                        result.append(ss)
            else:
                break

    # 重複除去
    prev_stamps = None
    for result_stamps in reversed(result):
        if prev_stamps is None:
            prev_stamps = result_stamps
            continue
        else:
            if prev_stamps == result_stamps:
                result.remove(result_stamps)
            else:
                prev_stamps = result_stamps
    return result


def print_result(result: list[StampSet]):
    residual = None
    for stamp_set in result:
        if residual is None:
            residual = stamp_set.residual
            print(f"residual: {residual}")
            assert residual >= 0, f"residual ({residual}) is less than 0"

        print("stamp set:", stamp_set.stamps)


if __name__ == "__main__":
    start = time.perf_counter()
    result = solve_stamps(400, [40, 41, 50, 52, 62, 63, 85, 60, 62, 80, 82, 84, 110])
    end = time.perf_counter()
    elapsed = end - start
    print_result(result)
    print(f"elapsed time:{elapsed * 1000 * 1000} usec")
