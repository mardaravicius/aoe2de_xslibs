from numpy import int32

from xs_converter.symbols import XsVector
from xs_converter.testkit.xs_functions_testkit import *


def vector(x: float, y: float, z: float) -> XsVector:
    return XsVector(x, y, z)


def abs(x: float | float32) -> float32:
    return abs_impl(float32(x))


def pow(x: float | float32, y: float | float32) -> float32:
    return pow_impl(float32(x), float32(y))


def xs_chat_data(message: str, value: int = -1) -> None:
    xs_chat_data_impl(message, value)


def xs_effect_amount(effect_id: int, unit_or_technology_id: int, attribute_or_operation: int, value: float,
                     player_number: int = -1) -> None:
    pass


def xs_get_game_time() -> int:
    pass


def xs_get_map_height() -> int:
    pass


def xs_get_map_id() -> int:
    pass


def xs_get_map_name(show_file_extension: bool) -> str:
    pass


def xs_get_map_width() -> int:
    pass


def xs_get_num_players() -> int:
    pass


def xs_get_object_count_total(player_id: int, id: int) -> int:
    pass


def xs_get_player_civilization(player_number: int) -> int:
    pass


def xs_get_player_in_game(player_number: int) -> bool:
    pass


def xs_get_player_number_of_techs(player_number: int) -> int:
    pass


def xs_get_time() -> int:
    pass


def xs_get_victory_condition() -> int:
    pass


def xs_get_victory_condition_for_secondary_game_mode() -> int:
    pass


def xs_get_victory_player() -> int:
    pass


def xs_get_victory_player_for_secondary_game_mode() -> int:
    pass


def xs_get_victory_time() -> int:
    pass


def xs_get_victory_time_for_secondary_game_mode() -> int:
    pass


def xs_get_victory_type() -> int:
    pass


def xs_object_has_action(player_id: int, unit_type: int, action_id: int, target_player_id: int = -1,
                         target_type: int = -1, target_unit_level: int = -1) -> bool:
    pass


def xs_player_attribute(player_number: int, resource_id: int) -> float:
    pass


def xs_remove_task(unit_id: int, action_type: int, target_unit_id: int = -1, player_id: int = -1) -> None:
    pass


def xs_research_technology(tech_id: int, force: bool, tech_available: bool, player_number: int) -> None:
    pass


def xs_set_player_attribute(player_number: int, resource_id: int, value: float) -> float:
    pass


def xs_set_trigger_variable(variable_id: int, value: int) -> None:
    pass


def xs_task(unit_id: int, action_type: int, target_unit_id: int, player_id: int) -> None:
    pass


def xs_task_amount(task_field_id: int, value: float) -> None:
    pass


def xs_trigger_variable(variable_id: int) -> int:
    pass


def xs_array_get_size(array_id: int | int32 = -1) -> int:
    return xs_array_get_size_impl(array_id)


def xs_array_create_int(size: int | int32 = -1, default_value: int | int32 = 0, unique_name: str = "") -> int:
    return xs_array_create_int_impl(size, default_value, unique_name)


def xs_array_set_int(array_id: int | int32 = -1, idx: int | int32 = 0, value: int | int32 = 0) -> int:
    return xs_array_set_int_impl(array_id, idx, value)


def xs_array_get_int(array_id: int | int32 = -1, idx: int | int32 = 0) -> int:
    return xs_array_get_int_impl(array_id, idx)


def xs_array_resize_int(array_id: int | int32 = -1, new_size: int | int32 = 0) -> int:
    return xs_array_resize_int_impl(array_id, new_size)


def xs_array_create_float(size: int = -1, default_value: float = 0.0, unique_name: str = "") -> int:
    return xs_array_create_float_impl(size, default_value, unique_name)


def xs_array_set_float(array_id: int = -1, idx: int = 0, value: float = 0.0) -> int:
    return xs_array_set_float_impl(array_id, idx, value)


def xs_array_get_float(array_id: int = -1, idx: int = 0) -> float:
    return xs_array_get_float_impl(array_id, idx)


def xs_array_resize_float(array_id: int = -1, new_size: int = 0) -> int:
    return xs_array_resize_float_impl(array_id, new_size)


def bit_cast_to_float(number: int) -> float:
    return bit_cast_to_float_impl(number)


def bit_cast_to_int(number: float) -> int:
    return bit_cast_to_int_impl(number)


def xs_get_random_number() -> int32:
    return xs_get_random_number_impl()
