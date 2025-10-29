from xs_converter.impl.xs_functions_impl import *
from xs_converter.symbols import XsVector


def vector(x: float | float32, y: float | float32, z: float | float32) -> XsVector:
    return XsVector(float32(x), float32(y), float32(z))


def abs(x: float | float32) -> float32:
    return abs_impl(float32(x))


def pow(x: float | float32, y: float | float32) -> float32:
    return pow_impl(float32(x), float32(y))


def xs_chat_data(message: str, value: int | int32 = -1) -> None:
    xs_chat_data_impl(message, int32(value))


def xs_effect_amount(effect_id: int | int32, unit_or_technology_id: int | int32, attribute_or_operation: int | int32,
                     value: float | float32, player_number: int | int32 = -1) -> None:
    pass


def xs_get_game_time() -> int32:
    pass


def xs_get_map_height() -> int32:
    pass


def xs_get_map_id() -> int32:
    pass


def xs_get_map_name(show_file_extension: bool) -> str:
    pass


def xs_get_map_width() -> int32:
    pass


def xs_get_num_players() -> int32:
    pass


def xs_get_object_count_total(player_id: int | int32, id: int | int32) -> int32:
    pass


def xs_get_player_civilization(player_number: int | int32) -> int:
    pass


def xs_get_player_in_game(player_number: int | int32) -> bool:
    pass


def xs_get_player_number_of_techs(player_number: int | int32) -> int32:
    pass


def xs_get_time() -> int32:
    pass


def xs_get_victory_condition() -> int32:
    pass


def xs_get_victory_condition_for_secondary_game_mode() -> int32:
    pass


def xs_get_victory_player() -> int32:
    pass


def xs_get_victory_player_for_secondary_game_mode() -> int32:
    pass


def xs_get_victory_time() -> int32:
    pass


def xs_get_victory_time_for_secondary_game_mode() -> int32:
    pass


def xs_get_victory_type() -> int32:
    pass


def xs_object_has_action(player_id: int | int32, unit_type: int | int32, action_id: int | int32,
                         target_player_id: int | int32 = -1, target_type: int | int32 = -1,
                         target_unit_level: int | int32 = -1) -> bool:
    pass


def xs_player_attribute(player_number: int | int32, resource_id: int | int32) -> float:
    pass


def xs_remove_task(unit_id: int | int32, action_type: int | int32, target_unit_id: int | int32 = -1,
                   player_id: int | int32 = -1) -> None:
    pass


def xs_research_technology(tech_id: int | int32, force: bool, tech_available: bool, player_number: int | int32) -> None:
    pass


def xs_set_player_attribute(player_number: int | int32, resource_id: int | int32, value: float | float32) -> None:
    pass


def xs_set_trigger_variable(variable_id: int | int32, value: int | int32) -> None:
    pass


def xs_task(unit_id: int, action_type: int | int32, target_unit_id: int | int32, player_id: int | int32) -> None:
    pass


def xs_task_amount(task_field_id: int | int32, value: float | float32) -> None:
    pass


def xs_trigger_variable(variable_id: int | int32) -> int:
    pass


def xs_array_get_size(array_id: int | int32) -> int32:
    """

    :rtype: int32
    """
    return xs_array_get_size_impl(int32(array_id))


def xs_array_create_int(size: int | int32, default_value: int | int32 = 0, unique_name: str = "") -> int32:
    return xs_array_create_int_impl(int32(size), int32(default_value), unique_name)


def xs_array_set_int(array_id: int | int32, idx: int | int32, value: int | int32) -> int32:
    return xs_array_set_int_impl(int32(array_id), int32(idx), int32(value))


def xs_array_get_int(array_id: int | int32, idx: int | int32) -> int32:
    return xs_array_get_int_impl(int32(array_id), int32(idx))


def xs_array_resize_int(array_id: int | int32, new_size: int | int32) -> int32:
    return xs_array_resize_int_impl(int32(array_id), int32(new_size))


def xs_array_create_float(size: int | int32, default_value: float | float32 = 0.0, unique_name: str = "") -> int32:
    return xs_array_create_float_impl(int32(size), float32(default_value), unique_name)


def xs_array_set_float(array_id: int | int32, idx: int | int32, value: float | float32) -> int32:
    return xs_array_set_float_impl(int32(array_id), int32(idx), float32(value))


def xs_array_get_float(array_id: int | int32, idx: int | int32) -> float32:
    return xs_array_get_float_impl(int32(array_id), int32(idx))


def xs_array_resize_float(array_id: int | int32, new_size: int | int32) -> int32:
    return xs_array_resize_float_impl(int32(array_id), int32(new_size))


def xs_array_create_string(size: int | int32, default_value: str = "", unique_name: str = "") -> int32:
    return xs_array_create_string_impl(int32(size), default_value, unique_name)


def xs_array_set_string(array_id: int | int32, idx: int | int32, value: str) -> int32:
    return xs_array_set_string_impl(int32(array_id), int32(idx), value)


def xs_array_get_string(array_id: int | int32, idx: int | int32) -> str:
    return xs_array_get_string_impl(int32(array_id), int32(idx))


def xs_array_resize_string(array_id: int | int32, new_size: int | int32) -> int32:
    return xs_array_resize_string_impl(int32(array_id), int32(new_size))


def bit_cast_to_float(number: int | int32) -> float32:
    return bit_cast_to_float_impl(int32(number))


def bit_cast_to_int(number: float | float32) -> int32:
    return bit_cast_to_int_impl(float32(number))


def xs_get_random_number() -> int32:
    return xs_get_random_number_impl()
