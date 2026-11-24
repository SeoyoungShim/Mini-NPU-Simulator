
import time
import json
import math


# ==========================================
# 1. 기본 설정 및 MAC 연산
# ==========================================

EPSILON = 1e-9
REPETITIONS = 100
FLAT_BENCHMARK_REPETITIONS = 100


def mac(input_matrix, filter_matrix):
    """2차원 배열을 이용해 MAC 연산을 수행한다."""

    if len(input_matrix) != len(filter_matrix):
        raise ValueError("두 행렬의 행 개수가 다릅니다.")

    total = 0.0

    for row in range(len(input_matrix)):
        if len(input_matrix[row]) != len(filter_matrix[row]):
            raise ValueError("두 행렬의 열 개수가 다릅니다.")

        for col in range(len(input_matrix[row])):
            total += input_matrix[row][col] * filter_matrix[row][col]

    return total


def flatten_matrix(matrix):
    """2차원 배열을 행 우선 순서의 1차원 배열로 변환한다."""

    return [value for row in matrix for value in row]


def mac_flat(input_flat, filter_flat):
    """1차원 배열을 순회하며 MAC 연산을 수행한다."""

    if len(input_flat) != len(filter_flat):
        raise ValueError("두 1차원 배열의 길이가 다릅니다.")

    total = 0.0

    for index in range(len(input_flat)):
        total += input_flat[index] * filter_flat[index]

    return total


# ==========================================
# 2. 패턴 생성기
# ==========================================

def create_cross_pattern(size):
    """N×N 십자가 패턴을 생성한다."""

    if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
        raise ValueError("패턴 크기는 양의 정수여야 합니다.")

    center = size // 2

    return [
        [
            1 if row == center or col == center else 0
            for col in range(size)
        ]
        for row in range(size)
    ]


def create_x_pattern(size):
    """N×N X 패턴을 생성한다."""

    if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
        raise ValueError("패턴 크기는 양의 정수여야 합니다.")

    return [
        [
            1 if row == col or row + col == size - 1 else 0
            for col in range(size)
        ]
        for row in range(size)
    ]


def print_matrix(matrix):
    """행렬을 보기 좋은 형태로 출력한다."""

    for row in matrix:
        print(" ".join(str(value) for value in row))


def run_pattern_generator():
    """사용자가 입력한 크기의 Cross와 X 패턴을 생성해 출력한다."""

    print("\n===== 패턴 생성기 =====")

    while True:
        try:
            size = int(input("패턴 크기 N을 입력하세요: "))

            if size <= 0:
                print("1 이상의 정수를 입력해 주세요.")
                continue

            break

        except ValueError:
            print("숫자로 된 정수를 입력해 주세요.")

    cross_pattern = create_cross_pattern(size)
    x_pattern = create_x_pattern(size)

    print(f"\n===== {size}x{size} Cross 패턴 =====")
    print_matrix(cross_pattern)

    print(f"\n===== {size}x{size} X 패턴 =====")
    print_matrix(x_pattern)


# ==========================================
# 3. 판정 및 라벨 정규화
# ==========================================

def decide(score_a, score_b):
    """두 점수를 비교하여 A, B 또는 UNDECIDED를 반환한다."""

    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"

    if score_a > score_b:
        return "A"

    return "B"


def normalize_label(label):
    """서로 다른 라벨 표현을 Cross 또는 X로 통일한다."""

    if not isinstance(label, str):
        raise ValueError(f"라벨 형식이 올바르지 않습니다: {label}")

    if label in ["+", "cross", "Cross"]:
        return "Cross"

    if label in ["x", "X"]:
        return "X"

    raise ValueError(f"알 수 없는 라벨입니다: {label}")


def normalize_filters(filters):
    """필터 키를 표준 라벨 Cross와 X로 통일한다."""

    if not isinstance(filters, dict):
        raise ValueError("필터 데이터 형식이 올바르지 않습니다.")

    normalized = {}

    for key, value in filters.items():
        label = normalize_label(key)
        normalized[label] = value

    if "Cross" not in normalized or "X" not in normalized:
        raise ValueError("Cross 또는 X 필터가 누락되었습니다.")

    return normalized


# ==========================================
# 4. 사용자 입력 및 행렬 검증
# ==========================================

def read_matrix(size, name):
    """사용자가 입력한 행렬을 읽고 형식을 검사한다."""

    matrix = []

    print(f"\n{name} 입력 ({size}행, 각 행에 숫자 {size}개)")

    for row in range(size):

        while True:
            user_input = input(f"{row + 1}번째 행: ")

            try:
                numbers = [float(value) for value in user_input.split()]

                if len(numbers) != size:
                    print(
                        f"입력 형식 오류: 각 줄에 {size}개의 숫자를 "
                        "공백으로 구분해 입력하세요."
                    )
                    continue

                if not all(math.isfinite(value) for value in numbers):
                    print("유효한 숫자를 입력해 주세요.")
                    continue

                matrix.append(numbers)
                break

            except ValueError:
                print("숫자 파싱 오류: 숫자만 입력해 주세요.")

    return matrix


def read_mode1_pattern(size):
    """Mode 1에서 직접 입력하거나 자동 생성한 패턴을 선택한다."""

    print("\n입력 패턴 방식을 선택하세요.")
    print("1. 직접 입력")
    print("2. Cross 패턴 자동 생성")
    print("3. X 패턴 자동 생성")

    while True:
        choice = input("선택: ").strip()

        if choice == "1":
            return read_matrix(size, "입력 패턴")

        if choice == "2":
            pattern = create_cross_pattern(size)
            print("\n생성된 Cross 패턴:")
            print_matrix(pattern)
            return pattern

        if choice == "3":
            pattern = create_x_pattern(size)
            print("\n생성된 X 패턴:")
            print_matrix(pattern)
            return pattern

        print("1, 2, 3 중에서 선택해 주세요.")


def validate_matrix(matrix, size, name):
    """행렬의 형식, 크기, 숫자 여부를 검사한다."""

    if not isinstance(matrix, list):
        raise ValueError(f"{name}: 행렬 형식이 아닙니다.")

    if len(matrix) != size:
        raise ValueError(f"{name}: 행 개수가 맞지 않습니다.")

    for row in matrix:

        if not isinstance(row, list):
            raise ValueError(f"{name}: 행 형식이 잘못되었습니다.")

        if len(row) != size:
            raise ValueError(f"{name}: 열 개수가 맞지 않습니다.")

        for value in row:

            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
            ):
                raise ValueError(f"{name}: 유효하지 않은 숫자가 있습니다.")


# ==========================================
# 5. JSON 파일 처리
# ==========================================

def load_data():
    """data.json 파일을 읽는다."""

    with open("data.json", "r", encoding="utf-8") as file:
        return json.load(file)


def get_pattern_size(pattern_key):
    """패턴 이름 size_N_idx에서 행렬 크기 N을 추출한다."""

    if not isinstance(pattern_key, str):
        raise ValueError("패턴 이름은 문자열이어야 합니다.")

    parts = pattern_key.split("_")

    if len(parts) != 3 or parts[0] != "size":
        raise ValueError("패턴 이름 형식이 올바르지 않습니다.")

    try:
        size = int(parts[1])

    except ValueError:
        raise ValueError("패턴 크기를 숫자로 읽을 수 없습니다.")

    if size <= 0:
        raise ValueError("행렬 크기는 양수여야 합니다.")

    return size


# ==========================================
# 6. MAC 연산 시간 측정
# ==========================================

def measure_mac(input_matrix, filter_matrix, repetitions=REPETITIONS):
    """2차원 MAC 연산을 반복하고 평균 실행 시간을 측정한다."""

    if repetitions <= 0:
        raise ValueError("반복 횟수는 양수여야 합니다.")

    total_time = 0.0
    score = 0.0

    for _ in range(repetitions):

        start = time.perf_counter()
        score = mac(input_matrix, filter_matrix)
        end = time.perf_counter()

        total_time += end - start

    average_ms = (total_time / repetitions) * 1000

    return score, average_ms


def measure_mac_flat(
    input_flat,
    filter_flat,
    repetitions=FLAT_BENCHMARK_REPETITIONS
):
    """1차원 MAC 연산을 반복하고 평균 실행 시간을 측정한다."""

    if repetitions <= 0:
        raise ValueError("반복 횟수는 양수여야 합니다.")

    total_time = 0.0
    score = 0.0

    for _ in range(repetitions):

        start = time.perf_counter()
        score = mac_flat(input_flat, filter_flat)
        end = time.perf_counter()

        total_time += end - start

    average_ms = (total_time / repetitions) * 1000

    return score, average_ms


# ==========================================
# 7. 성능 분석 및 2D/1D 비교
# ==========================================

def run_performance_test(sizes):
    """생성한 Cross/X 패턴을 사용해 크기별 MAC 연산 시간을 측정한다."""

    print("\n===== 성능 측정 결과 =====")
    print(f"측정 방식: 2차원 MAC 연산 {REPETITIONS}회 반복 평균")
    print("크기\t평균 연산 시간(ms)\t연산 횟수(N²)")

    for size in sizes:

        input_matrix = create_cross_pattern(size)
        filter_matrix = create_x_pattern(size)

        _, average_ms = measure_mac(
            input_matrix,
            filter_matrix,
            REPETITIONS
        )

        operation_count = size ** 2

        print(
            f"{size}x{size}\t"
            f"{average_ms:.6f}\t\t"
            f"{operation_count}"
        )


def run_memory_optimization_test(sizes=None):
    """동일한 데이터와 반복 횟수로 2차원/1차원 MAC 성능을 비교한다."""

    if sizes is None:
        sizes = [3, 5, 13, 25, 100, 250]

    print("\n===== 보너스 1: 2차원 / 1차원 MAC 성능 비교 =====")
    print(f"측정 반복 횟수: 각 방식 {FLAT_BENCHMARK_REPETITIONS}회")
    print("배열 변환 시간은 측정에서 제외하고 MAC 연산 시간만 비교합니다.")

    print(
        "크기\t2차원(ms)\t1차원(ms)\t"
        "점수 일치\t1차원 속도 비교"
    )

    for size in sizes:

        input_matrix = create_cross_pattern(size)
        filter_matrix = create_x_pattern(size)

        # 변환은 측정 시작 전에 수행한다.
        input_flat = flatten_matrix(input_matrix)
        filter_flat = flatten_matrix(filter_matrix)

        score_2d, time_2d = measure_mac(
            input_matrix,
            filter_matrix,
            FLAT_BENCHMARK_REPETITIONS
        )

        score_1d, time_1d = measure_mac_flat(
            input_flat,
            filter_flat,
            FLAT_BENCHMARK_REPETITIONS
        )

        scores_match = math.isclose(
            score_2d,
            score_1d,
            rel_tol=0.0,
            abs_tol=EPSILON
        )

        if time_1d < time_2d:
            comparison = "빠름"

        elif time_1d > time_2d:
            comparison = "느림"

        else:
            comparison = "비슷함"

        print(
            f"{size}x{size}\t"
            f"{time_2d:.6f}\t"
            f"{time_1d:.6f}\t"
            f"{'일치' if scores_match else '불일치'}\t"
            f"{comparison}"
        )


# ==========================================
# 8. Mode 1 - 사용자 입력 방식
# ==========================================

def run_mode1():

    print("\n===== Mode 1: 사용자 입력 방식 =====")

    filter_a = read_matrix(3, "필터 A")
    filter_b = read_matrix(3, "필터 B")

    print("\n===== 입력 확인 =====")
    print("필터 A와 필터 B 입력이 완료되었습니다.")

    input_pattern = read_mode1_pattern(3)

    score_a, time_a = measure_mac(input_pattern, filter_a)
    score_b, time_b = measure_mac(input_pattern, filter_b)

    result = decide(score_a, score_b)

    print("\n===== Mode 1 결과 =====")
    print(f"A 점수: {score_a:.6f}")
    print(f"B 점수: {score_b:.6f}")
    print(f"A 평균 연산 시간: {time_a:.6f} ms")
    print(f"B 평균 연산 시간: {time_b:.6f} ms")

    if result == "UNDECIDED":
        print("최종 판정: 판정 불가")

    else:
        print(f"최종 판정: {result}")

    run_performance_test([3])


# ==========================================
# 9. Mode 2 - JSON 데이터 방식
# ==========================================

def run_mode2():

    print("\n===== Mode 2: JSON 데이터 방식 =====")

    try:
        data = load_data()

    except FileNotFoundError:
        print("오류: data.json 파일을 찾을 수 없습니다.")
        return

    except json.JSONDecodeError as error:
        print(f"오류: JSON 파일 형식이 잘못되었습니다. {error}")
        return

    if not isinstance(data, dict):
        print("오류: JSON 최상위 구조가 올바르지 않습니다.")
        return

    if not isinstance(data.get("filters"), dict):
        print("오류: filters 데이터가 올바르지 않습니다.")
        return

    if not isinstance(data.get("patterns"), dict):
        print("오류: patterns 데이터가 올바르지 않습니다.")
        return

    total_count = 0
    pass_count = 0
    fail_count = 0
    failures = []

    for pattern_key, pattern_data in data["patterns"].items():

        total_count += 1

        print(f"\n[테스트: {pattern_key}]")

        try:

            size = get_pattern_size(pattern_key)
            filter_key = f"size_{size}"

            if filter_key not in data["filters"]:
                raise ValueError(f"{filter_key} 필터 데이터가 없습니다.")

            filters = normalize_filters(data["filters"][filter_key])

            if not isinstance(pattern_data, dict):
                raise ValueError("패턴 데이터 형식이 잘못되었습니다.")

            input_pattern = pattern_data["input"]

            cross_filter = filters["Cross"]
            x_filter = filters["X"]

            validate_matrix(input_pattern, size, "입력 패턴")
            validate_matrix(cross_filter, size, "Cross 필터")
            validate_matrix(x_filter, size, "X 필터")

            expected = normalize_label(pattern_data["expected"])

            cross_score, cross_time = measure_mac(
                input_pattern,
                cross_filter
            )

            x_score, x_time = measure_mac(
                input_pattern,
                x_filter
            )

            result = decide(cross_score, x_score)

            if result == "A":
                result_label = "Cross"

            elif result == "B":
                result_label = "X"

            else:
                result_label = "UNDECIDED"

            if result_label == "UNDECIDED":

                status = "FAIL"
                reason = "두 점수가 같아 판정할 수 없음"

            elif result_label == expected:

                status = "PASS"
                reason = "정답 일치"

            else:

                status = "FAIL"
                reason = "예측 결과와 실제 정답이 다름"

            if status == "PASS":
                pass_count += 1

            else:
                fail_count += 1
                failures.append((pattern_key, reason))

            print(f"패턴 크기: {size} x {size}")
            print(f"Cross 점수: {cross_score:.6f}")
            print(f"X 점수: {x_score:.6f}")
            print(f"판정 결과: {result_label}")
            print(f"실제 정답: {expected}")
            print(f"테스트 결과: {status}")

            if status == "FAIL":
                print(f"실패 사유: {reason}")

        except (ValueError, KeyError, TypeError, IndexError) as error:

            fail_count += 1

            reason = str(error)
            failures.append((pattern_key, reason))

            print("테스트 결과: FAIL")
            print(f"실패 사유: {reason}")

    run_performance_test([3, 5, 13, 25])

    run_memory_optimization_test([3, 5, 13, 25])

    print("\n===== Mode 2 최종 결과 =====")
    print(f"전체 테스트: {total_count}")
    print(f"성공: {pass_count}")
    print(f"실패: {fail_count}")

    if failures:

        print("\n===== 실패 케이스 목록 =====")

        for case_name, reason in failures:
            print(f"- {case_name}: {reason}")

    else:
        print("\n실패 케이스가 없습니다.")


# ==========================================
# 10. 메인 메뉴
# ==========================================

def main():

    while True:

        print("\n==============================")
        print("       Mini NPU Simulator")
        print("==============================")
        print("1. Mode 1 - 사용자 입력 방식")
        print("2. Mode 2 - JSON 데이터 방식")
        print("3. 패턴 생성기")
        print("0. 종료")

        choice = input("\n실행할 모드를 선택하세요: ").strip()

        if choice == "1":
            run_mode1()

        elif choice == "2":
            run_mode2()

        elif choice == "3":
            run_pattern_generator()

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 선택입니다. 0, 1, 2, 3 중에서 선택해 주세요.")


if __name__ == "__main__":
    main()
