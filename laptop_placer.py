import argparse
from subprocess import PIPE, run
from typing import List


VALID_SIDES = ["right", "left", "below"]


def get_external_screen_info(raw_display_info: List[str]) -> dict:
    external_screen_candidates = [
        r for r in raw_display_info if "external" in r]
    if len(external_screen_candidates) > 1:
        assert False
        # TODO: Raise exception that we cant identify external monitor
    index = raw_display_info.index(external_screen_candidates[0])
    info = {
        "id": raw_display_info[index - 2].split(":")[1].strip(),
        "res_x": raw_display_info[index + 1].split(" ")[1].split("x")[0],
        "res_y": raw_display_info[index + 1].split(" ")[1].split("x")[1],
    }
    return info


def get_build_in_screen_info(raw_display_info: List[str]) -> dict:
    index = raw_display_info.index("Type: MacBook built in screen")
    info = {
        "id": raw_display_info[index - 2].split(":")[1].strip(),
        "res_x": raw_display_info[index + 1].split(" ")[1].split("x")[0],
        "res_y": raw_display_info[index + 1].split(" ")[1].split("x")[1],
        "hz": raw_display_info[index + 2].split(":")[1].strip(),
        "color_depth": raw_display_info[index + 3].split(":")[1].strip(),
        "scaling": raw_display_info[index + 4].split(":")[1].strip(),
        "degree": 0,
    }
    return info


def compute_new_origin(
    side: str, build_in_screen_info: dict, external_screen_info: dict
) -> tuple:
    if side == "left":
        origin_x = 0
        origin_y = int(
            abs(
                int(external_screen_info["res_y"]) / 2
                - int(build_in_screen_info["res_y"])
            )
        )
    elif side == "right":
        origin_x = external_screen_info["res_x"]
        origin_y = int(
            abs(
                int(external_screen_info["res_y"]) / 2
                - int(build_in_screen_info["res_y"])
            )
        )
    elif side == "below":
        origin_x = int(
            abs(
                int(external_screen_info["res_x"]) / 2
                - int(build_in_screen_info["res_x"]) / 2
            )
        )
        origin_y = external_screen_info["res_y"]
    else:
        raise Exception("asdasda")
        # TODO: Fix this excpetion
    return (origin_x, origin_y)


def get_display_information() -> List[str]:
    command = ["displayplacer", "list"]
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    # TODO: Verify command returned 0 etc
    return result.stdout.split("\n")


def update_placement(
    origin: tuple,
    id: str,
    res_x: str,
    res_y: str,
    hz: str,
    color_depth: str,
    scaling: str,
    degree: str,
) -> None:
    if hz == "N/A":
        UPDATE_COMMAND = (f"id:{id} "
                          f"res:{res_x}x{res_y} "
                          f"color_depth:{color_depth} "
                          f"scaling:{scaling} "
                          f"origin:({origin[0]},{origin[1]}) "
                          f"degree:{degree}")
    else:
        UPDATE_COMMAND = (f"id:{id} "
                          f"res:{res_x}x{res_y} "
                          f"hz:{hz} "
                          f"color_depth:{color_depth} "
                          f"scaling:{scaling} "
                          f"origin:({origin[0]},{origin[1]}) "
                          f"degree:{degree}")

    print(UPDATE_COMMAND)
    run(
        ["displayplacer", UPDATE_COMMAND],
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
    )
    # TODO: Handle errors!


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Command line tool for moving the laptop to the specified "
            "side of the external monitor"
        )
    )
    parser.add_argument(
        "--side",
        type=str,
        required=True,
        help=("Side of the external monitor to move the laptop to."
              "Needs to be one of [right, left, below]"),
    )
    args = parser.parse_args()

    if args.side not in VALID_SIDES:
        print(
            f"{args.side} is not a valid side. "
            "Please set side to one of [right, left, below]"
        )
        return 1

    raw_display_info = get_display_information()
    build_in_screen_info = get_build_in_screen_info(raw_display_info)
    external_screen_info = get_external_screen_info(raw_display_info)
    new_origin = compute_new_origin(
        args.side, build_in_screen_info, external_screen_info
    )
    update_placement(
        new_origin,
        build_in_screen_info["id"],
        build_in_screen_info["res_x"],
        build_in_screen_info["res_y"],
        build_in_screen_info["hz"],
        build_in_screen_info["color_depth"],
        build_in_screen_info["scaling"],
        build_in_screen_info["degree"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
