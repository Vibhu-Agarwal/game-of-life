from typing import Callable, List, Optional


def state_functions() -> List[Callable[[bool, int], Optional[bool]]]:
    def loneliness(is_alive, alive_neighbours) -> Optional[bool]:
        if is_alive and alive_neighbours < 2:
            return False
        return None

    def overcrowding(is_alive, alive_neighbours) -> Optional[bool]:
        if is_alive and alive_neighbours > 3:
            return False
        return None

    def live_unchanged(is_alive, alive_neighbours) -> Optional[bool]:
        if is_alive and 2 <= alive_neighbours <= 3:
            return True
        return None

    def dead_to_life(is_alive, alive_neighbours) -> Optional[bool]:
        if (not is_alive) and alive_neighbours == 3:
            return True
        return None

    return [
        loneliness,
        overcrowding,
        live_unchanged,
        dead_to_life,
    ]
