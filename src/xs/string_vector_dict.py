from numpy import int32

from xs_converter.functions import (
    vector,
    xs_array_create_float,
    xs_array_create_int,
    xs_array_create_string,
    xs_array_create_vector,
    xs_array_get_float,
    xs_array_get_int,
    xs_array_get_size,
    xs_array_get_string,
    xs_array_resize_float,
    xs_array_resize_int,
    xs_array_resize_string,
    xs_array_set_float,
    xs_array_set_int,
    xs_array_set_string,
    xs_array_set_vector,
    xs_vector_get_x,
    xs_vector_get_y,
    xs_vector_get_z,
    xs_vector_set,
)
from xs_converter.symbols import XsExternConst, XsVector, i32range

c_string_vector_dict_success: XsExternConst[int32] = int32(0)
c_string_vector_dict_generic_error: XsExternConst[int32] = int32(-1)
c_string_vector_dict_no_key_error: XsExternConst[int32] = int32(-2)
c_string_vector_dict_resize_failed_error: XsExternConst[int32] = int32(-3)
c_string_vector_dict_max_capacity_error: XsExternConst[int32] = int32(-4)
c_string_vector_dict_generic_error_vector: XsExternConst[XsVector] = vector(-1.0, -1.0, -1.0)
c_string_vector_dict_max_capacity: XsExternConst[int32] = int32(333333330)
c_string_vector_dict_initial_capacity: XsExternConst[int32] = int32(16)
c_string_vector_dict_header_size: XsExternConst[int32] = int32(5)
c_string_vector_dict_node_stride: XsExternConst[int32] = int32(3)
c_string_vector_dict_value_stride: XsExternConst[int32] = int32(3)
_string_vector_dict_last_operation_status: int32 = c_string_vector_dict_success


def _xs_string_vector_dict_effective_initial_capacity() -> int32:
    capacity: int32 = c_string_vector_dict_initial_capacity
    if capacity > c_string_vector_dict_max_capacity:
        capacity = c_string_vector_dict_max_capacity
    if capacity < 0:
        return int32(0)
    return capacity


def _xs_string_vector_dict_get_keys_array(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 1)


def _xs_string_vector_dict_set_keys_array(dct: int32 = int32(-1), arr: int32 = int32(-1)) -> None:
    xs_array_set_int(dct, 1, arr)


def _xs_string_vector_dict_get_values_array(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 2)


def _xs_string_vector_dict_set_values_array(dct: int32 = int32(-1), arr: int32 = int32(-1)) -> None:
    xs_array_set_int(dct, 2, arr)


def _xs_string_vector_dict_get_root(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 3)


def _xs_string_vector_dict_set_root(dct: int32 = int32(-1), root: int32 = int32(-1)) -> None:
    xs_array_set_int(dct, 3, root)


def _xs_string_vector_dict_get_free_head(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 4)


def _xs_string_vector_dict_set_free_head(dct: int32 = int32(-1), head: int32 = int32(-1)) -> None:
    xs_array_set_int(dct, 4, head)


def _xs_string_vector_dict_capacity_from_data_size(data_size: int32 = int32(0)) -> int32:
    return (data_size - c_string_vector_dict_header_size) // c_string_vector_dict_node_stride


def _xs_string_vector_dict_capacity(dct: int32 = int32(-1)) -> int32:
    return _xs_string_vector_dict_capacity_from_data_size(xs_array_get_size(dct))


def _xs_string_vector_dict_node_base(node: int32 = int32(0)) -> int32:
    return c_string_vector_dict_header_size + (node * c_string_vector_dict_node_stride)


def _xs_string_vector_dict_left_slot(node: int32 = int32(0)) -> int32:
    return _xs_string_vector_dict_node_base(node)


def _xs_string_vector_dict_right_slot(node: int32 = int32(0)) -> int32:
    return _xs_string_vector_dict_node_base(node) + 1


def _xs_string_vector_dict_height_slot(node: int32 = int32(0)) -> int32:
    return _xs_string_vector_dict_node_base(node) + 2


def _xs_string_vector_dict_value_base(node: int32 = int32(0)) -> int32:
    return node * c_string_vector_dict_value_stride


def _xs_string_vector_dict_get_stored_key(dct: int32 = int32(-1), node: int32 = int32(0)) -> str:
    return xs_array_get_string(_xs_string_vector_dict_get_keys_array(dct), node)


def _xs_string_vector_dict_set_stored_key(dct: int32 = int32(-1), node: int32 = int32(0), key: str = "") -> None:
    xs_array_set_string(_xs_string_vector_dict_get_keys_array(dct), node, key)


def _xs_string_vector_dict_get_stored_value(dct: int32 = int32(-1), node: int32 = int32(0)) -> XsVector:
    values_arr: int32 = _xs_string_vector_dict_get_values_array(dct)
    base: int32 = _xs_string_vector_dict_value_base(node)
    return xs_vector_set(
        xs_array_get_float(values_arr, base),
        xs_array_get_float(values_arr, base + 1),
        xs_array_get_float(values_arr, base + 2),
    )


def _xs_string_vector_dict_set_stored_value(dct: int32 = int32(-1), node: int32 = int32(0),
                                             value: XsVector = vector(0.0, 0.0, 0.0)) -> None:
    values_arr: int32 = _xs_string_vector_dict_get_values_array(dct)
    base: int32 = _xs_string_vector_dict_value_base(node)
    xs_array_set_float(values_arr, base, xs_vector_get_x(value))
    xs_array_set_float(values_arr, base + 1, xs_vector_get_y(value))
    xs_array_set_float(values_arr, base + 2, xs_vector_get_z(value))


def _xs_string_vector_dict_get_left(dct: int32 = int32(-1), node: int32 = int32(0)) -> int32:
    return xs_array_get_int(dct, _xs_string_vector_dict_left_slot(node))


def _xs_string_vector_dict_set_left(dct: int32 = int32(-1), node: int32 = int32(0),
                                     child: int32 = int32(-1)) -> None:
    xs_array_set_int(dct, _xs_string_vector_dict_left_slot(node), child)


def _xs_string_vector_dict_get_right(dct: int32 = int32(-1), node: int32 = int32(0)) -> int32:
    return xs_array_get_int(dct, _xs_string_vector_dict_right_slot(node))


def _xs_string_vector_dict_set_right(dct: int32 = int32(-1), node: int32 = int32(0),
                                      child: int32 = int32(-1)) -> None:
    xs_array_set_int(dct, _xs_string_vector_dict_right_slot(node), child)


def _xs_string_vector_dict_get_height_or_next(dct: int32 = int32(-1), node: int32 = int32(0)) -> int32:
    return xs_array_get_int(dct, _xs_string_vector_dict_height_slot(node))


def _xs_string_vector_dict_set_height_or_next(dct: int32 = int32(-1), node: int32 = int32(0),
                                               value: int32 = int32(0)) -> None:
    xs_array_set_int(dct, _xs_string_vector_dict_height_slot(node), value)


def _xs_string_vector_dict_initialize_free_nodes(
        dct: int32 = int32(-1),
        start: int32 = int32(0),
        stop: int32 = int32(0),
        next_head: int32 = int32(-1),
) -> None:
    for i in i32range(start, stop):
        _xs_string_vector_dict_set_stored_key(dct, i, "!<[empty")
        _xs_string_vector_dict_set_stored_value(dct, i, vector(0.0, 0.0, 0.0))
        _xs_string_vector_dict_set_left(dct, i, int32(-1))
        _xs_string_vector_dict_set_right(dct, i, int32(-1))
        next_free: int32 = next_head
        if i + 1 < stop:
            next_free = i + 1
        _xs_string_vector_dict_set_height_or_next(dct, i, next_free)


def xs_string_vector_dict_create() -> int32:
    """
    Creates an empty string-to-vector dictionary.
    Keys equal to `"!<[empty"` are reserved as the internal empty-key sentinel
    and cannot be stored. `put` and `put_if_absent` silently reject them.
    :return: created dict id, or `c_string_vector_dict_generic_error` on error
    """
    capacity: int32 = _xs_string_vector_dict_effective_initial_capacity()
    data_size: int32 = c_string_vector_dict_header_size + (capacity * c_string_vector_dict_node_stride)
    dct: int32 = xs_array_create_int(data_size, int32(-1))
    if dct < 0:
        return c_string_vector_dict_generic_error
    keys_arr: int32 = xs_array_create_string(capacity, "!<[empty")
    if keys_arr < 0:
        xs_array_resize_int(dct, 0)
        return c_string_vector_dict_generic_error
    values_arr: int32 = xs_array_create_float(capacity * c_string_vector_dict_value_stride, 0.0)
    if values_arr < 0:
        xs_array_resize_string(keys_arr, 0)
        xs_array_resize_int(dct, 0)
        return c_string_vector_dict_generic_error
    xs_array_set_int(dct, 0, 0)
    _xs_string_vector_dict_set_keys_array(dct, keys_arr)
    _xs_string_vector_dict_set_values_array(dct, values_arr)
    _xs_string_vector_dict_set_root(dct, int32(-1))
    _xs_string_vector_dict_set_free_head(dct, int32(-1))
    if capacity > 0:
        _xs_string_vector_dict_initialize_free_nodes(dct, int32(0), capacity, int32(-1))
        _xs_string_vector_dict_set_free_head(dct, int32(0))
    return dct


def _xs_string_vector_dict_resize(dct: int32 = int32(-1), new_capacity: int32 = int32(0)) -> int32:
    old_capacity: int32 = _xs_string_vector_dict_capacity(dct)
    if new_capacity <= old_capacity:
        return c_string_vector_dict_success
    if new_capacity > c_string_vector_dict_max_capacity:
        return c_string_vector_dict_max_capacity_error
    keys_arr: int32 = _xs_string_vector_dict_get_keys_array(dct)
    r_keys: int32 = xs_array_resize_string(keys_arr, new_capacity)
    if r_keys != 1:
        return c_string_vector_dict_resize_failed_error
    values_arr: int32 = _xs_string_vector_dict_get_values_array(dct)
    new_values_size: int32 = new_capacity * c_string_vector_dict_value_stride
    r_values: int32 = xs_array_resize_float(values_arr, new_values_size)
    if r_values != 1:
        return c_string_vector_dict_resize_failed_error
    old_free_head: int32 = _xs_string_vector_dict_get_free_head(dct)
    new_data_size: int32 = c_string_vector_dict_header_size + (new_capacity * c_string_vector_dict_node_stride)
    r: int32 = xs_array_resize_int(dct, new_data_size)
    if r != 1:
        return c_string_vector_dict_resize_failed_error
    _xs_string_vector_dict_initialize_free_nodes(dct, old_capacity, new_capacity, old_free_head)
    _xs_string_vector_dict_set_free_head(dct, old_capacity)
    return c_string_vector_dict_success


def _xs_string_vector_dict_ensure_capacity(dct: int32 = int32(-1), required_size: int32 = int32(0)) -> int32:
    capacity: int32 = _xs_string_vector_dict_capacity(dct)
    if required_size <= capacity:
        return c_string_vector_dict_success
    if required_size > c_string_vector_dict_max_capacity:
        return c_string_vector_dict_max_capacity_error
    new_capacity: int32 = capacity
    if new_capacity < 1:
        new_capacity = int32(1)
    while new_capacity < required_size:
        if new_capacity > c_string_vector_dict_max_capacity // 2:
            new_capacity = c_string_vector_dict_max_capacity
        else:
            new_capacity = new_capacity * 2
    return _xs_string_vector_dict_resize(dct, new_capacity)


def _xs_string_vector_dict_allocate_node(dct: int32 = int32(-1), key: str = "",
                                          value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    free_head: int32 = _xs_string_vector_dict_get_free_head(dct)
    if free_head < 0:
        return int32(-1)
    _xs_string_vector_dict_set_free_head(dct, _xs_string_vector_dict_get_height_or_next(dct, free_head))
    _xs_string_vector_dict_set_stored_key(dct, free_head, key)
    _xs_string_vector_dict_set_stored_value(dct, free_head, value)
    _xs_string_vector_dict_set_left(dct, free_head, int32(-1))
    _xs_string_vector_dict_set_right(dct, free_head, int32(-1))
    _xs_string_vector_dict_set_height_or_next(dct, free_head, int32(1))
    return free_head


def _xs_string_vector_dict_free_node(dct: int32 = int32(-1), node: int32 = int32(-1)) -> None:
    _xs_string_vector_dict_set_stored_key(dct, node, "!<[empty")
    _xs_string_vector_dict_set_stored_value(dct, node, vector(0.0, 0.0, 0.0))
    _xs_string_vector_dict_set_left(dct, node, int32(-1))
    _xs_string_vector_dict_set_right(dct, node, int32(-1))
    _xs_string_vector_dict_set_height_or_next(dct, node, _xs_string_vector_dict_get_free_head(dct))
    _xs_string_vector_dict_set_free_head(dct, node)


def _xs_string_vector_dict_height(dct: int32 = int32(-1), node: int32 = int32(-1)) -> int32:
    if node < 0:
        return int32(0)
    return _xs_string_vector_dict_get_height_or_next(dct, node)


def _xs_string_vector_dict_refresh_height(dct: int32 = int32(-1), node: int32 = int32(-1)) -> None:
    left_height: int32 = _xs_string_vector_dict_height(dct, _xs_string_vector_dict_get_left(dct, node))
    right_height: int32 = _xs_string_vector_dict_height(dct, _xs_string_vector_dict_get_right(dct, node))
    if left_height > right_height:
        _xs_string_vector_dict_set_height_or_next(dct, node, left_height + 1)
    else:
        _xs_string_vector_dict_set_height_or_next(dct, node, right_height + 1)


def _xs_string_vector_dict_balance_factor(dct: int32 = int32(-1), node: int32 = int32(-1)) -> int32:
    return _xs_string_vector_dict_height(dct, _xs_string_vector_dict_get_left(dct, node)) - \
        _xs_string_vector_dict_height(dct, _xs_string_vector_dict_get_right(dct, node))


def _xs_string_vector_dict_rotate_left(dct: int32 = int32(-1), node: int32 = int32(-1)) -> int32:
    new_root: int32 = _xs_string_vector_dict_get_right(dct, node)
    moved: int32 = _xs_string_vector_dict_get_left(dct, new_root)
    _xs_string_vector_dict_set_right(dct, node, moved)
    _xs_string_vector_dict_set_left(dct, new_root, node)
    _xs_string_vector_dict_refresh_height(dct, node)
    _xs_string_vector_dict_refresh_height(dct, new_root)
    return new_root


def _xs_string_vector_dict_rotate_right(dct: int32 = int32(-1), node: int32 = int32(-1)) -> int32:
    new_root: int32 = _xs_string_vector_dict_get_left(dct, node)
    moved: int32 = _xs_string_vector_dict_get_right(dct, new_root)
    _xs_string_vector_dict_set_left(dct, node, moved)
    _xs_string_vector_dict_set_right(dct, new_root, node)
    _xs_string_vector_dict_refresh_height(dct, node)
    _xs_string_vector_dict_refresh_height(dct, new_root)
    return new_root


def _xs_string_vector_dict_rebalance(dct: int32 = int32(-1), node: int32 = int32(-1)) -> int32:
    _xs_string_vector_dict_refresh_height(dct, node)
    balance: int32 = _xs_string_vector_dict_balance_factor(dct, node)
    if balance > 1:
        left: int32 = _xs_string_vector_dict_get_left(dct, node)
        if _xs_string_vector_dict_balance_factor(dct, left) < 0:
            _xs_string_vector_dict_set_left(dct, node, _xs_string_vector_dict_rotate_left(dct, left))
        return _xs_string_vector_dict_rotate_right(dct, node)
    if balance < -1:
        right: int32 = _xs_string_vector_dict_get_right(dct, node)
        if _xs_string_vector_dict_balance_factor(dct, right) > 0:
            _xs_string_vector_dict_set_right(dct, node, _xs_string_vector_dict_rotate_right(dct, right))
        return _xs_string_vector_dict_rotate_left(dct, node)
    return node


def _xs_string_vector_dict_find_node(dct: int32 = int32(-1), key: str = "") -> int32:
    node: int32 = _xs_string_vector_dict_get_root(dct)
    while node >= 0:
        stored_key: str = _xs_string_vector_dict_get_stored_key(dct, node)
        if key == stored_key:
            return node
        if key < stored_key:
            node = _xs_string_vector_dict_get_left(dct, node)
        else:
            node = _xs_string_vector_dict_get_right(dct, node)
    return int32(-1)


def _xs_string_vector_dict_insert_node(dct: int32 = int32(-1), node: int32 = int32(-1), key: str = "",
                                        value: XsVector = vector(0.0, 0.0, 0.0)) -> int32:
    if node < 0:
        return _xs_string_vector_dict_allocate_node(dct, key, value)
    stored_key: str = _xs_string_vector_dict_get_stored_key(dct, node)
    if key == stored_key:
        _xs_string_vector_dict_set_stored_value(dct, node, value)
        return node
    if key < stored_key:
        _xs_string_vector_dict_set_left(
            dct,
            node,
            _xs_string_vector_dict_insert_node(dct, _xs_string_vector_dict_get_left(dct, node), key, value),
        )
    else:
        _xs_string_vector_dict_set_right(
            dct,
            node,
            _xs_string_vector_dict_insert_node(dct, _xs_string_vector_dict_get_right(dct, node), key, value),
        )
    return _xs_string_vector_dict_rebalance(dct, node)


def _xs_string_vector_dict_min_node(dct: int32 = int32(-1), node: int32 = int32(-1)) -> int32:
    current: int32 = node
    while current >= 0:
        left: int32 = _xs_string_vector_dict_get_left(dct, current)
        if left < 0:
            return current
        current = left
    return int32(-1)


def _xs_string_vector_dict_remove_min(dct: int32 = int32(-1), node: int32 = int32(-1)) -> int32:
    left: int32 = _xs_string_vector_dict_get_left(dct, node)
    if left < 0:
        right: int32 = _xs_string_vector_dict_get_right(dct, node)
        _xs_string_vector_dict_free_node(dct, node)
        return right
    _xs_string_vector_dict_set_left(dct, node, _xs_string_vector_dict_remove_min(dct, left))
    return _xs_string_vector_dict_rebalance(dct, node)


def _xs_string_vector_dict_remove_node(dct: int32 = int32(-1), node: int32 = int32(-1), key: str = "") -> int32:
    if node < 0:
        return int32(-1)
    stored_key: str = _xs_string_vector_dict_get_stored_key(dct, node)
    if key < stored_key:
        _xs_string_vector_dict_set_left(
            dct,
            node,
            _xs_string_vector_dict_remove_node(dct, _xs_string_vector_dict_get_left(dct, node), key),
        )
        return _xs_string_vector_dict_rebalance(dct, node)
    if key > stored_key:
        _xs_string_vector_dict_set_right(
            dct,
            node,
            _xs_string_vector_dict_remove_node(dct, _xs_string_vector_dict_get_right(dct, node), key),
        )
        return _xs_string_vector_dict_rebalance(dct, node)

    left: int32 = _xs_string_vector_dict_get_left(dct, node)
    right: int32 = _xs_string_vector_dict_get_right(dct, node)
    if left < 0:
        _xs_string_vector_dict_free_node(dct, node)
        return right
    if right < 0:
        _xs_string_vector_dict_free_node(dct, node)
        return left

    successor: int32 = _xs_string_vector_dict_min_node(dct, right)
    _xs_string_vector_dict_set_stored_key(dct, node, _xs_string_vector_dict_get_stored_key(dct, successor))
    _xs_string_vector_dict_set_stored_value(dct, node, _xs_string_vector_dict_get_stored_value(dct, successor))
    _xs_string_vector_dict_set_right(dct, node, _xs_string_vector_dict_remove_min(dct, right))
    return _xs_string_vector_dict_rebalance(dct, node)


def _xs_string_vector_dict_find_successor_node(dct: int32 = int32(-1), key: str = "") -> int32:
    node: int32 = _xs_string_vector_dict_get_root(dct)
    successor: int32 = int32(-1)
    while node >= 0:
        stored_key: str = _xs_string_vector_dict_get_stored_key(dct, node)
        if key < stored_key:
            successor = node
            node = _xs_string_vector_dict_get_left(dct, node)
        elif key > stored_key:
            node = _xs_string_vector_dict_get_right(dct, node)
        else:
            right: int32 = _xs_string_vector_dict_get_right(dct, node)
            if right >= 0:
                return _xs_string_vector_dict_min_node(dct, right)
            return successor
    return int32(-1)


def _xs_string_vector_dict_keys_fill(dct: int32 = int32(-1), node: int32 = int32(-1),
                                      arr: int32 = int32(-1), idx: int32 = int32(0)) -> int32:
    if node < 0:
        return idx
    idx = _xs_string_vector_dict_keys_fill(dct, _xs_string_vector_dict_get_left(dct, node), arr, idx)
    xs_array_set_string(arr, idx, _xs_string_vector_dict_get_stored_key(dct, node))
    idx += 1
    return _xs_string_vector_dict_keys_fill(dct, _xs_string_vector_dict_get_right(dct, node), arr, idx)


def _xs_string_vector_dict_values_fill(dct: int32 = int32(-1), node: int32 = int32(-1),
                                        arr: int32 = int32(-1), idx: int32 = int32(0)) -> int32:
    if node < 0:
        return idx
    idx = _xs_string_vector_dict_values_fill(dct, _xs_string_vector_dict_get_left(dct, node), arr, idx)
    xs_array_set_vector(arr, idx, _xs_string_vector_dict_get_stored_value(dct, node))
    idx += 1
    return _xs_string_vector_dict_values_fill(dct, _xs_string_vector_dict_get_right(dct, node), arr, idx)


def _xs_string_vector_dict_equals_walk(a: int32 = int32(-1), b: int32 = int32(-1),
                                        node: int32 = int32(-1)) -> bool:
    if node < 0:
        return True
    if not _xs_string_vector_dict_equals_walk(a, b, _xs_string_vector_dict_get_left(a, node)):
        return False
    key: str = _xs_string_vector_dict_get_stored_key(a, node)
    val: XsVector = _xs_string_vector_dict_get_stored_value(a, node)
    other: int32 = _xs_string_vector_dict_find_node(b, key)
    if other < 0:
        return False
    if _xs_string_vector_dict_get_stored_value(b, other) != val:
        return False
    return _xs_string_vector_dict_equals_walk(a, b, _xs_string_vector_dict_get_right(a, node))


def _xs_string_vector_dict_update_walk(source: int32 = int32(-1), dct: int32 = int32(-1),
                                        node: int32 = int32(-1)) -> int32:
    global _string_vector_dict_last_operation_status
    if node < 0:
        return c_string_vector_dict_success
    left_result: int32 = _xs_string_vector_dict_update_walk(source, dct, _xs_string_vector_dict_get_left(dct, node))
    if left_result != c_string_vector_dict_success:
        return left_result
    key: str = _xs_string_vector_dict_get_stored_key(dct, node)
    val: XsVector = _xs_string_vector_dict_get_stored_value(dct, node)
    existing: int32 = _xs_string_vector_dict_find_node(source, key)
    if existing >= 0:
        _xs_string_vector_dict_set_stored_value(source, existing, val)
        _string_vector_dict_last_operation_status = c_string_vector_dict_success
    else:
        size: int32 = xs_array_get_int(source, 0)
        resize_result: int32 = _xs_string_vector_dict_ensure_capacity(source, size + 1)
        if resize_result != c_string_vector_dict_success:
            _string_vector_dict_last_operation_status = resize_result
            return resize_result
        _xs_string_vector_dict_set_root(
            source,
            _xs_string_vector_dict_insert_node(source, _xs_string_vector_dict_get_root(source), key, val),
        )
        xs_array_set_int(source, 0, size + 1)
        _string_vector_dict_last_operation_status = c_string_vector_dict_no_key_error
    return _xs_string_vector_dict_update_walk(source, dct, _xs_string_vector_dict_get_right(dct, node))


def _xs_string_vector_dict_to_string_contents(dct: int32 = int32(-1), node: int32 = int32(-1)) -> str:
    if node < 0:
        return ""
    left: str = _xs_string_vector_dict_to_string_contents(dct, _xs_string_vector_dict_get_left(dct, node))
    current: str = '"' + _xs_string_vector_dict_get_stored_key(dct, node) + '": ' + \
        str(_xs_string_vector_dict_get_stored_value(dct, node))
    combined: str = current
    if left != "":
        combined = left + ", " + current
    right: str = _xs_string_vector_dict_to_string_contents(dct, _xs_string_vector_dict_get_right(dct, node))
    if right != "":
        combined += ", " + right
    return combined


def xs_string_vector_dict_put(dct: int32 = int32(-1), key: str = "",
                               val: XsVector = vector(0.0, 0.0, 0.0)) -> XsVector:
    """
    Inserts or updates a key-value pair. Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `c_string_vector_dict_generic_error_vector` with last error set to `c_string_vector_dict_generic_error`.
    :return: previous value if the key already existed, or `c_string_vector_dict_generic_error_vector`
        if newly inserted or on error. Callers must check `xs_string_vector_dict_last_error()`.
    """
    global _string_vector_dict_last_operation_status
    if key == "!<[empty":
        _string_vector_dict_last_operation_status = c_string_vector_dict_generic_error
        return c_string_vector_dict_generic_error_vector
    existing: int32 = _xs_string_vector_dict_find_node(dct, key)
    if existing >= 0:
        old_val: XsVector = _xs_string_vector_dict_get_stored_value(dct, existing)
        _xs_string_vector_dict_set_stored_value(dct, existing, val)
        _string_vector_dict_last_operation_status = c_string_vector_dict_success
        return old_val
    size: int32 = xs_array_get_int(dct, 0)
    r: int32 = _xs_string_vector_dict_ensure_capacity(dct, size + 1)
    if r != c_string_vector_dict_success:
        _string_vector_dict_last_operation_status = r
        return c_string_vector_dict_generic_error_vector
    _xs_string_vector_dict_set_root(
        dct,
        _xs_string_vector_dict_insert_node(dct, _xs_string_vector_dict_get_root(dct), key, val),
    )
    xs_array_set_int(dct, 0, size + 1)
    _string_vector_dict_last_operation_status = c_string_vector_dict_no_key_error
    return c_string_vector_dict_generic_error_vector


def xs_string_vector_dict(
        k1: str = "!<[empty",
        v1: XsVector = vector(0.0, 0.0, 0.0),
        k2: str = "!<[empty",
        v2: XsVector = vector(0.0, 0.0, 0.0),
        k3: str = "!<[empty",
        v3: XsVector = vector(0.0, 0.0, 0.0),
        k4: str = "!<[empty",
        v4: XsVector = vector(0.0, 0.0, 0.0),
        k5: str = "!<[empty",
        v5: XsVector = vector(0.0, 0.0, 0.0),
        k6: str = "!<[empty",
        v6: XsVector = vector(0.0, 0.0, 0.0),
) -> int32:
    """
    Creates a dict with provided key-value pairs. The first key that equals
    the reserved empty-key sentinel will stop further insertion.
    """
    dct: int32 = xs_string_vector_dict_create()
    if dct < 0:
        return c_string_vector_dict_generic_error
    if k1 == "!<[empty":
        return dct
    xs_string_vector_dict_put(dct, k1, v1)
    if k2 == "!<[empty":
        return dct
    xs_string_vector_dict_put(dct, k2, v2)
    if k3 == "!<[empty":
        return dct
    xs_string_vector_dict_put(dct, k3, v3)
    if k4 == "!<[empty":
        return dct
    xs_string_vector_dict_put(dct, k4, v4)
    if k5 == "!<[empty":
        return dct
    xs_string_vector_dict_put(dct, k5, v5)
    if k6 == "!<[empty":
        return dct
    xs_string_vector_dict_put(dct, k6, v6)
    return dct


def xs_string_vector_dict_get(dct: int32 = int32(-1), key: str = "",
                               dft: XsVector = c_string_vector_dict_generic_error_vector) -> XsVector:
    """
    Returns the value associated with the given key. Sets last error on completion.
    """
    global _string_vector_dict_last_operation_status
    node: int32 = _xs_string_vector_dict_find_node(dct, key)
    if node >= 0:
        _string_vector_dict_last_operation_status = c_string_vector_dict_success
        return _xs_string_vector_dict_get_stored_value(dct, node)
    _string_vector_dict_last_operation_status = c_string_vector_dict_no_key_error
    return dft


def xs_string_vector_dict_remove(dct: int32 = int32(-1), key: str = "") -> XsVector:
    """
    Removes the entry with the given key from the dict. Sets last error on completion.
    """
    global _string_vector_dict_last_operation_status
    node: int32 = _xs_string_vector_dict_find_node(dct, key)
    if node < 0:
        _string_vector_dict_last_operation_status = c_string_vector_dict_no_key_error
        return c_string_vector_dict_generic_error_vector
    old_val: XsVector = _xs_string_vector_dict_get_stored_value(dct, node)
    _xs_string_vector_dict_set_root(
        dct,
        _xs_string_vector_dict_remove_node(dct, _xs_string_vector_dict_get_root(dct), key),
    )
    xs_array_set_int(dct, 0, xs_array_get_int(dct, 0) - 1)
    _string_vector_dict_last_operation_status = c_string_vector_dict_success
    return old_val


def xs_string_vector_dict_contains(dct: int32 = int32(-1), key: str = "") -> bool:
    return _xs_string_vector_dict_find_node(dct, key) >= 0


def xs_string_vector_dict_size(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 0)


def xs_string_vector_dict_clear(dct: int32 = int32(-1)) -> int32:
    """
    Removes all entries from the dict and shrinks the backing arrays.
    """
    target_capacity: int32 = _xs_string_vector_dict_effective_initial_capacity()
    current_capacity: int32 = _xs_string_vector_dict_capacity(dct)
    if current_capacity > target_capacity:
        old_keys_arr: int32 = _xs_string_vector_dict_get_keys_array(dct)
        new_keys_arr: int32 = xs_array_create_string(target_capacity, "!<[empty")
        if new_keys_arr < 0:
            return c_string_vector_dict_generic_error
        new_values_arr: int32 = xs_array_create_float(target_capacity * c_string_vector_dict_value_stride, 0.0)
        if new_values_arr < 0:
            xs_array_resize_string(new_keys_arr, 0)
            return c_string_vector_dict_generic_error
        new_data_size: int32 = c_string_vector_dict_header_size + (target_capacity * c_string_vector_dict_node_stride)
        r: int32 = xs_array_resize_int(dct, new_data_size)
        if r != 1:
            xs_array_resize_string(new_keys_arr, 0)
            xs_array_resize_float(new_values_arr, 0)
            return c_string_vector_dict_generic_error
        old_values_arr: int32 = _xs_string_vector_dict_get_values_array(dct)
        _xs_string_vector_dict_set_keys_array(dct, new_keys_arr)
        _xs_string_vector_dict_set_values_array(dct, new_values_arr)
        xs_array_resize_string(old_keys_arr, 0)
        xs_array_resize_float(old_values_arr, 0)
        current_capacity = target_capacity
    xs_array_set_int(dct, 0, 0)
    _xs_string_vector_dict_set_root(dct, int32(-1))
    _xs_string_vector_dict_set_free_head(dct, int32(-1))
    if current_capacity > 0:
        _xs_string_vector_dict_initialize_free_nodes(dct, int32(0), current_capacity, int32(-1))
        _xs_string_vector_dict_set_free_head(dct, int32(0))
    return c_string_vector_dict_success


def xs_string_vector_dict_copy(dct: int32 = int32(-1)) -> int32:
    """
    Returns a deep copy of the dict.
    """
    data_size: int32 = xs_array_get_size(dct)
    capacity: int32 = _xs_string_vector_dict_capacity(dct)
    new_dct: int32 = xs_array_create_int(data_size, int32(-1))
    if new_dct < 0:
        return c_string_vector_dict_resize_failed_error
    new_keys_arr: int32 = xs_array_create_string(capacity, "!<[empty")
    if new_keys_arr < 0:
        xs_array_resize_int(new_dct, 0)
        return c_string_vector_dict_resize_failed_error
    new_values_arr: int32 = xs_array_create_float(capacity * c_string_vector_dict_value_stride, 0.0)
    if new_values_arr < 0:
        xs_array_resize_string(new_keys_arr, 0)
        xs_array_resize_int(new_dct, 0)
        return c_string_vector_dict_resize_failed_error
    for i in i32range(0, data_size):
        xs_array_set_int(new_dct, i, xs_array_get_int(dct, i))
    _xs_string_vector_dict_set_keys_array(new_dct, new_keys_arr)
    _xs_string_vector_dict_set_values_array(new_dct, new_values_arr)
    keys_arr: int32 = _xs_string_vector_dict_get_keys_array(dct)
    for j in i32range(0, capacity):
        xs_array_set_string(new_keys_arr, j, xs_array_get_string(keys_arr, j))
    values_arr: int32 = _xs_string_vector_dict_get_values_array(dct)
    values_size: int32 = capacity * c_string_vector_dict_value_stride
    for k in i32range(0, values_size):
        xs_array_set_float(new_values_arr, k, xs_array_get_float(values_arr, k))
    return new_dct


def xs_string_vector_dict_to_string(dct: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the dict in the format `{"k1": (x1, y1, z1), ...}`.
    """
    return "{" + _xs_string_vector_dict_to_string_contents(dct, _xs_string_vector_dict_get_root(dct)) + "}"


def xs_string_vector_dict_last_error() -> int32:
    return _string_vector_dict_last_operation_status


def xs_string_vector_dict_next_key(dct: int32 = int32(-1), is_first: bool = True,
                                    prev_key: str = "!<[empty") -> str:
    """
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    """
    global _string_vector_dict_last_operation_status
    next_node: int32 = int32(-1)
    if is_first:
        next_node = _xs_string_vector_dict_min_node(dct, _xs_string_vector_dict_get_root(dct))
    else:
        node: int32 = _xs_string_vector_dict_find_node(dct, prev_key)
        if node < 0:
            _string_vector_dict_last_operation_status = c_string_vector_dict_no_key_error
            return "-1"
        next_node = _xs_string_vector_dict_find_successor_node(dct, prev_key)
    if next_node < 0:
        _string_vector_dict_last_operation_status = c_string_vector_dict_no_key_error
        return "-1"
    _string_vector_dict_last_operation_status = c_string_vector_dict_success
    return _xs_string_vector_dict_get_stored_key(dct, next_node)


def xs_string_vector_dict_has_next(dct: int32 = int32(-1), is_first: bool = True,
                                    prev_key: str = "!<[empty") -> bool:
    if is_first:
        return _xs_string_vector_dict_get_root(dct) >= 0
    if _xs_string_vector_dict_find_node(dct, prev_key) < 0:
        return False
    return _xs_string_vector_dict_find_successor_node(dct, prev_key) >= 0


def xs_string_vector_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
    """
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
    """
    global _string_vector_dict_last_operation_status
    result: int32 = _xs_string_vector_dict_update_walk(source, dct, _xs_string_vector_dict_get_root(dct))
    if result != c_string_vector_dict_success:
        return result
    _string_vector_dict_last_operation_status = c_string_vector_dict_success
    return c_string_vector_dict_success


def xs_string_vector_dict_put_if_absent(dct: int32 = int32(-1), key: str = "",
                                         val: XsVector = vector(0.0, 0.0, 0.0)) -> XsVector:
    """
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals the reserved empty-key sentinel, the call is a no-op and returns
    `c_string_vector_dict_generic_error_vector` with last error set to `c_string_vector_dict_generic_error`.
    """
    global _string_vector_dict_last_operation_status
    if key == "!<[empty":
        _string_vector_dict_last_operation_status = c_string_vector_dict_generic_error
        return c_string_vector_dict_generic_error_vector
    existing: int32 = _xs_string_vector_dict_find_node(dct, key)
    if existing >= 0:
        _string_vector_dict_last_operation_status = c_string_vector_dict_success
        return _xs_string_vector_dict_get_stored_value(dct, existing)
    size: int32 = xs_array_get_int(dct, 0)
    r: int32 = _xs_string_vector_dict_ensure_capacity(dct, size + 1)
    if r != c_string_vector_dict_success:
        _string_vector_dict_last_operation_status = r
        return c_string_vector_dict_generic_error_vector
    _xs_string_vector_dict_set_root(
        dct,
        _xs_string_vector_dict_insert_node(dct, _xs_string_vector_dict_get_root(dct), key, val),
    )
    xs_array_set_int(dct, 0, size + 1)
    _string_vector_dict_last_operation_status = c_string_vector_dict_no_key_error
    return c_string_vector_dict_generic_error_vector


def xs_string_vector_dict_keys(dct: int32 = int32(-1)) -> int32:
    """
    Returns a new string array containing all keys in the dict. Order is lexicographic.
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = xs_array_create_string(size)
    if arr < 0:
        return c_string_vector_dict_resize_failed_error
    _xs_string_vector_dict_keys_fill(dct, _xs_string_vector_dict_get_root(dct), arr)
    return arr


def xs_string_vector_dict_values(dct: int32 = int32(-1)) -> int32:
    """
    Returns a new vector array containing all values in the dict. Order matches `xs_string_vector_dict_keys`.
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = xs_array_create_vector(size, vector(0.0, 0.0, 0.0))
    if arr < 0:
        return c_string_vector_dict_resize_failed_error
    _xs_string_vector_dict_values_fill(dct, _xs_string_vector_dict_get_root(dct), arr)
    return arr


def xs_string_vector_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
    """
    Returns true if both dicts contain the same key-value pairs.
    """
    if xs_array_get_int(a, 0) != xs_array_get_int(b, 0):
        return False
    return _xs_string_vector_dict_equals_walk(a, b, _xs_string_vector_dict_get_root(a))
