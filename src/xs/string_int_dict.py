from numpy import float32, int32

from xs_converter.functions import (
    ord,
    str_char_at,
    str_len,
    xs_array_create_int,
    xs_array_create_string,
    xs_array_get_int,
    xs_array_get_size,
    xs_array_get_string,
    xs_array_resize_int,
    xs_array_resize_string,
    xs_array_set_int,
    xs_array_set_string,
)
from xs_converter.symbols import XsExternConst, i32range

c_string_int_dict_success: XsExternConst[int32] = int32(0)
c_string_int_dict_generic_error: XsExternConst[int32] = int32(-1)
c_string_int_dict_no_key_error: XsExternConst[int32] = int32(-2)
c_string_int_dict_resize_failed_error: XsExternConst[int32] = int32(-3)
c_string_int_dict_max_capacity_error: XsExternConst[int32] = int32(-4)
c_string_int_dict_max_capacity: XsExternConst[int32] = int32(249999998)
c_string_int_dict_max_load_factor: XsExternConst[float32] = float32(0.75)
c_string_int_dict_initial_capacity: XsExternConst[int32] = int32(18)
c_string_int_dict_hash_constant: XsExternConst[int32] = int32(16777619)
_string_int_dict_last_operation_status: int32 = c_string_int_dict_success
_string_int_dict_temp_keys: int32 = int32(-1)
_string_int_dict_temp_values: int32 = int32(-1)


def _xs_string_int_dict_keys_capacity_from_int_capacity(capacity: int32 = int32(0)) -> int32:
    return capacity - 2


def _xs_string_int_dict_get_keys_array(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 1)


def _xs_string_int_dict_key_slot(slot: int32 = int32(2)) -> int32:
    return slot - 2


def _xs_string_int_dict_get_stored_key(dct: int32 = int32(-1), slot: int32 = int32(2)) -> str:
    return xs_array_get_string(_xs_string_int_dict_get_keys_array(dct), _xs_string_int_dict_key_slot(slot))


def _xs_string_int_dict_set_stored_key(dct: int32 = int32(-1), slot: int32 = int32(2), key: str = "") -> None:
    xs_array_set_string(_xs_string_int_dict_get_keys_array(dct), _xs_string_int_dict_key_slot(slot), key)


def _xs_string_int_dict_get_stored_value(dct: int32 = int32(-1), slot: int32 = int32(2)) -> int32:
    return xs_array_get_int(dct, slot)


def _xs_string_int_dict_set_stored_value(dct: int32 = int32(-1), slot: int32 = int32(2),
                                          value: int32 = int32(0)) -> None:
    xs_array_set_int(dct, slot, value)


def _xs_string_int_dict_clear_slot(dct: int32 = int32(-1), slot: int32 = int32(2)) -> None:
    _xs_string_int_dict_set_stored_key(dct, slot, "!<[empty")


def xs_string_int_dict_create() -> int32:
    """
    Creates an empty string-to-int dictionary.
    Keys equal to `"!<[empty"` are reserved as the internal
    empty-slot sentinel and cannot be stored. `put` and `put_if_absent` silently reject them.
    :return: created dict id, or `c_string_int_dict_generic_error` on error
    """
    dct: int32 = xs_array_create_int(c_string_int_dict_initial_capacity, int32(0))
    if dct < 0:
        return c_string_int_dict_generic_error
    keys_capacity: int32 = _xs_string_int_dict_keys_capacity_from_int_capacity(c_string_int_dict_initial_capacity)
    keys_arr: int32 = xs_array_create_string(keys_capacity, "!<[empty")
    if keys_arr < 0:
        xs_array_resize_int(dct, 0)
        return c_string_int_dict_generic_error
    xs_array_set_int(dct, 0, 0)
    xs_array_set_int(dct, 1, keys_arr)
    return dct


def _xs_string_int_dict_hash(key: str = "", capacity: int32 = int32(0)) -> int32:
    h: int32 = int32(0)
    n: int32 = str_len(key)
    for i in i32range(0, n):
        ch: int32 = ord(str_char_at(key, i))
        h = (h + ch) * c_string_int_dict_hash_constant
    num_slots: int32 = _xs_string_int_dict_keys_capacity_from_int_capacity(capacity)
    h = h % num_slots
    if h < 0:
        h += num_slots
    return h + 2


def _xs_string_int_dict_find_slot(dct: int32 = int32(-1), key: str = "",
                                   capacity: int32 = int32(0)) -> int32:
    """Returns int-array index of slot containing key, or -1 if not found."""
    num_slots: int32 = _xs_string_int_dict_keys_capacity_from_int_capacity(capacity)
    home: int32 = _xs_string_int_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: str = _xs_string_int_dict_get_stored_key(dct, slot)
        if stored_key == "!<[empty":
            return int32(-1)
        if stored_key == key:
            return slot
        slot += 1
        if slot >= capacity:
            slot = int32(2)
        steps += 1
    return int32(-1)


def _xs_string_int_dict_upsert(dct: int32 = int32(-1), key: str = "", val: int32 = int32(0),
                                capacity: int32 = int32(0)) -> int32:
    global _string_int_dict_last_operation_status
    num_slots: int32 = _xs_string_int_dict_keys_capacity_from_int_capacity(capacity)
    slot: int32 = _xs_string_int_dict_hash(key, capacity)
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: str = _xs_string_int_dict_get_stored_key(dct, slot)
        if stored_key == "!<[empty":
            _xs_string_int_dict_set_stored_key(dct, slot, key)
            _xs_string_int_dict_set_stored_value(dct, slot, val)
            _string_int_dict_last_operation_status = c_string_int_dict_no_key_error
            return c_string_int_dict_generic_error
        if stored_key == key:
            old_val: int32 = _xs_string_int_dict_get_stored_value(dct, slot)
            _xs_string_int_dict_set_stored_value(dct, slot, val)
            _string_int_dict_last_operation_status = c_string_int_dict_success
            return old_val
        slot += 1
        if slot >= capacity:
            slot = int32(2)
        steps += 1
    _string_int_dict_last_operation_status = c_string_int_dict_max_capacity_error
    return c_string_int_dict_generic_error


def _xs_string_int_dict_move_to_temp_arrays(dct: int32 = int32(-1), size: int32 = int32(0),
                                             capacity: int32 = int32(0)) -> int32:
    global _string_int_dict_temp_keys, _string_int_dict_temp_values
    temp_data_size: int32 = size
    max_keys_capacity: int32 = c_string_int_dict_max_capacity - 2
    if _string_int_dict_temp_keys < 0:
        _string_int_dict_temp_keys = xs_array_create_string(temp_data_size, "!<[empty")
        if _string_int_dict_temp_keys < 0:
            return c_string_int_dict_resize_failed_error
    else:
        temp_keys_capacity: int32 = xs_array_get_size(_string_int_dict_temp_keys)
        if temp_keys_capacity < temp_data_size:
            if temp_data_size > max_keys_capacity:
                return c_string_int_dict_max_capacity_error
            r_keys: int32 = xs_array_resize_string(_string_int_dict_temp_keys, temp_data_size)
            if r_keys != 1:
                return c_string_int_dict_resize_failed_error
    if _string_int_dict_temp_values < 0:
        _string_int_dict_temp_values = xs_array_create_int(temp_data_size, int32(0))
        if _string_int_dict_temp_values < 0:
            return c_string_int_dict_resize_failed_error
    else:
        temp_values_capacity: int32 = xs_array_get_size(_string_int_dict_temp_values)
        if temp_values_capacity < temp_data_size:
            if temp_data_size > max_keys_capacity:
                return c_string_int_dict_max_capacity_error
            r_values: int32 = xs_array_resize_int(_string_int_dict_temp_values, temp_data_size)
            if r_values != 1:
                return c_string_int_dict_resize_failed_error
    t: int32 = int32(0)
    for i in i32range(2, capacity):
        stored_key: str = _xs_string_int_dict_get_stored_key(dct, i)
        if stored_key != "!<[empty":
            xs_array_set_string(_string_int_dict_temp_keys, t, stored_key)
            xs_array_set_int(_string_int_dict_temp_values, t, _xs_string_int_dict_get_stored_value(dct, i))
            t += 1
    return temp_data_size


def _xs_string_int_dict_clear_slots(dct: int32 = int32(-1), capacity: int32 = int32(-1)) -> None:
    for j in i32range(2, capacity):
        _xs_string_int_dict_clear_slot(dct, j)


def _xs_string_int_dict_rehash_if_needed(dct: int32 = int32(-1), size: int32 = int32(0),
                                          capacity: int32 = int32(0),
                                          required_size: int32 = int32(-1)) -> int32:
    global _string_int_dict_last_operation_status
    if required_size < 0:
        required_size = size
    load_factor: float = float(required_size) / _xs_string_int_dict_keys_capacity_from_int_capacity(capacity)
    if load_factor > c_string_int_dict_max_load_factor:
        store_status: int32 = _string_int_dict_last_operation_status
        new_keys_capacity: int32 = _xs_string_int_dict_keys_capacity_from_int_capacity(capacity) * 2
        new_capacity: int32 = new_keys_capacity + 2
        if new_capacity > c_string_int_dict_max_capacity:
            new_capacity = c_string_int_dict_max_capacity
        if new_capacity <= capacity:
            _string_int_dict_last_operation_status = c_string_int_dict_max_capacity_error
            return c_string_int_dict_generic_error
        new_keys_capacity = _xs_string_int_dict_keys_capacity_from_int_capacity(new_capacity)
        temp_data_size: int32 = _xs_string_int_dict_move_to_temp_arrays(dct, size, capacity)
        if temp_data_size < 0:
            _string_int_dict_last_operation_status = temp_data_size
            return c_string_int_dict_generic_error
        keys_arr: int32 = _xs_string_int_dict_get_keys_array(dct)
        r_keys: int32 = xs_array_resize_string(keys_arr, new_keys_capacity)
        if r_keys != 1:
            _string_int_dict_last_operation_status = c_string_int_dict_resize_failed_error
            return c_string_int_dict_generic_error
        r: int32 = xs_array_resize_int(dct, new_capacity)
        if r != 1:
            _string_int_dict_last_operation_status = c_string_int_dict_resize_failed_error
            return c_string_int_dict_generic_error
        _xs_string_int_dict_clear_slots(dct, new_capacity)
        for t in i32range(0, temp_data_size):
            _xs_string_int_dict_upsert(
                dct,
                xs_array_get_string(_string_int_dict_temp_keys, t),
                xs_array_get_int(_string_int_dict_temp_values, t),
                new_capacity,
            )
            if _string_int_dict_last_operation_status < 0 and _string_int_dict_last_operation_status != c_string_int_dict_no_key_error:
                return c_string_int_dict_generic_error
        _string_int_dict_last_operation_status = store_status
    return c_string_int_dict_success


def xs_string_int_dict_put(dct: int32 = int32(-1), key: str = "", val: int32 = int32(0)) -> int32:
    """
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `c_string_int_dict_generic_error` with last error set to `c_string_int_dict_generic_error`.
    :return: previous value if the key already existed, or `c_string_int_dict_generic_error`
        if newly inserted or on error. Callers must check `xs_string_int_dict_last_error()`.
    """
    global _string_int_dict_last_operation_status
    if key == "!<[empty":
        _string_int_dict_last_operation_status = c_string_int_dict_generic_error
        return c_string_int_dict_generic_error
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_string_int_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        old_val: int32 = _xs_string_int_dict_get_stored_value(dct, slot)
        _xs_string_int_dict_set_stored_value(dct, slot, val)
        _string_int_dict_last_operation_status = c_string_int_dict_success
        return old_val

    r: int32 = _xs_string_int_dict_rehash_if_needed(dct, size, capacity, size + 1)
    if r != c_string_int_dict_success:
        return c_string_int_dict_generic_error

    capacity = xs_array_get_size(dct)
    previous_value: int32 = _xs_string_int_dict_upsert(dct, key, val, capacity)
    if _string_int_dict_last_operation_status == c_string_int_dict_no_key_error:
        xs_array_set_int(dct, 0, size + 1)
        return c_string_int_dict_generic_error
    if _string_int_dict_last_operation_status != c_string_int_dict_success:
        return c_string_int_dict_generic_error
    return previous_value


def xs_string_int_dict(
        k1: str = "!<[empty",
        v1: int32 = int32(0),
        k2: str = "!<[empty",
        v2: int32 = int32(0),
        k3: str = "!<[empty",
        v3: int32 = int32(0),
        k4: str = "!<[empty",
        v4: int32 = int32(0),
        k5: str = "!<[empty",
        v5: int32 = int32(0),
        k6: str = "!<[empty",
        v6: int32 = int32(0),
) -> int32:
    """
    Creates a dict with provided key-value pairs. The first key that equals
    `"!<[empty"` will stop further insertion.
    """
    dct: int32 = xs_string_int_dict_create()
    if dct < 0:
        return c_string_int_dict_generic_error
    if k1 == "!<[empty":
        return dct
    xs_string_int_dict_put(dct, k1, v1)
    if k2 == "!<[empty":
        return dct
    xs_string_int_dict_put(dct, k2, v2)
    if k3 == "!<[empty":
        return dct
    xs_string_int_dict_put(dct, k3, v3)
    if k4 == "!<[empty":
        return dct
    xs_string_int_dict_put(dct, k4, v4)
    if k5 == "!<[empty":
        return dct
    xs_string_int_dict_put(dct, k5, v5)
    if k6 == "!<[empty":
        return dct
    xs_string_int_dict_put(dct, k6, v6)
    return dct


def xs_string_int_dict_get(dct: int32 = int32(-1), key: str = "", dft: int32 = int32(-1)) -> int32:
    """
    Returns the value associated with the given key. Sets last error on completion.
    """
    global _string_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_string_int_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _string_int_dict_last_operation_status = c_string_int_dict_success
        return _xs_string_int_dict_get_stored_value(dct, slot)
    _string_int_dict_last_operation_status = c_string_int_dict_no_key_error
    return dft


def xs_string_int_dict_remove(dct: int32 = int32(-1), key: str = "") -> int32:
    """
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
    """
    global _string_int_dict_last_operation_status
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    num_slots: int32 = _xs_string_int_dict_keys_capacity_from_int_capacity(capacity)
    slot: int32 = _xs_string_int_dict_find_slot(dct, key, capacity)
    if slot < 0:
        _string_int_dict_last_operation_status = c_string_int_dict_no_key_error
        return c_string_int_dict_generic_error
    found_val: int32 = _xs_string_int_dict_get_stored_value(dct, slot)

    g: int32 = slot
    q: int32 = g + 1
    if q >= capacity:
        q = int32(2)
    shift_steps: int32 = int32(0)
    q_key: str = _xs_string_int_dict_get_stored_key(dct, q)
    while q_key != "!<[empty" and shift_steps < num_slots:
        q_home: int32 = _xs_string_int_dict_hash(q_key, capacity)
        g_slot: int32 = g - 2
        q_slot: int32 = q - 2
        h_slot: int32 = q_home - 2
        dist_g: int32 = (g_slot - h_slot + num_slots) % num_slots
        dist_q: int32 = (q_slot - h_slot + num_slots) % num_slots
        if dist_g < dist_q:
            _xs_string_int_dict_set_stored_key(dct, g, q_key)
            _xs_string_int_dict_set_stored_value(dct, g, _xs_string_int_dict_get_stored_value(dct, q))
            g = q
        q += 1
        if q >= capacity:
            q = int32(2)
        shift_steps += 1
        q_key = _xs_string_int_dict_get_stored_key(dct, q)
    _xs_string_int_dict_clear_slot(dct, g)
    xs_array_set_int(dct, 0, size - 1)
    _string_int_dict_last_operation_status = c_string_int_dict_success
    return found_val


def xs_string_int_dict_contains(dct: int32 = int32(-1), key: str = "") -> bool:
    capacity: int32 = xs_array_get_size(dct)
    return _xs_string_int_dict_find_slot(dct, key, capacity) >= 0


def xs_string_int_dict_size(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 0)


def xs_string_int_dict_clear(dct: int32 = int32(-1)) -> int32:
    """
    Removes all entries from the dict and shrinks the backing arrays.
    """
    capacity: int32 = xs_array_get_size(dct)
    if capacity > c_string_int_dict_initial_capacity:
        keys_capacity: int32 = _xs_string_int_dict_keys_capacity_from_int_capacity(c_string_int_dict_initial_capacity)
        new_keys_arr: int32 = xs_array_create_string(keys_capacity, "!<[empty")
        if new_keys_arr < 0:
            return c_string_int_dict_generic_error
        old_keys_arr: int32 = _xs_string_int_dict_get_keys_array(dct)
        r: int32 = xs_array_resize_int(dct, c_string_int_dict_initial_capacity)
        if r != 1:
            xs_array_resize_string(new_keys_arr, 0)
            return c_string_int_dict_generic_error
        xs_array_set_int(dct, 0, 0)
        xs_array_set_int(dct, 1, new_keys_arr)
        xs_array_resize_string(old_keys_arr, 0)
        return c_string_int_dict_success
    _xs_string_int_dict_clear_slots(dct, capacity)
    xs_array_set_int(dct, 0, 0)
    return c_string_int_dict_success


def xs_string_int_dict_copy(dct: int32 = int32(-1)) -> int32:
    """
    Returns a deep copy of the dict.
    """
    capacity: int32 = xs_array_get_size(dct)
    keys_capacity: int32 = _xs_string_int_dict_keys_capacity_from_int_capacity(capacity)
    new_dct: int32 = xs_array_create_int(capacity, int32(0))
    if new_dct < 0:
        return c_string_int_dict_resize_failed_error
    new_keys_arr: int32 = xs_array_create_string(keys_capacity, "!<[empty")
    if new_keys_arr < 0:
        xs_array_resize_int(new_dct, 0)
        return c_string_int_dict_resize_failed_error
    xs_array_set_int(new_dct, 0, xs_array_get_int(dct, 0))
    xs_array_set_int(new_dct, 1, new_keys_arr)
    for i in i32range(2, capacity):
        stored_key: str = _xs_string_int_dict_get_stored_key(dct, i)
        if stored_key != "!<[empty":
            xs_array_set_string(new_keys_arr, i - 2, stored_key)
            xs_array_set_int(new_dct, i, _xs_string_int_dict_get_stored_value(dct, i))
    return new_dct


def xs_string_int_dict_to_string(dct: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the dict in the format `{"k1": v1, "k2": v2, ...}`.
    """
    capacity: int32 = xs_array_get_size(dct)
    s: str = "{"
    first: bool = True
    for i in i32range(2, capacity):
        key: str = _xs_string_int_dict_get_stored_key(dct, i)
        if key != "!<[empty":
            if first:
                first = False
            else:
                s += ", "
            s += f'"{key}": {_xs_string_int_dict_get_stored_value(dct, i)}'
    s += "}"
    return s


def xs_string_int_dict_last_error() -> int32:
    return _string_int_dict_last_operation_status


def _xs_string_int_dict_find_next_occupied(dct: int32 = int32(-1), start: int32 = int32(2),
                                            capacity: int32 = int32(0)) -> str:
    global _string_int_dict_last_operation_status
    slot: int32 = start
    while slot < capacity:
        stored_key: str = _xs_string_int_dict_get_stored_key(dct, slot)
        if stored_key != "!<[empty":
            _string_int_dict_last_operation_status = c_string_int_dict_success
            return stored_key
        slot += 1
    _string_int_dict_last_operation_status = c_string_int_dict_no_key_error
    return "-1"


def xs_string_int_dict_next_key(dct: int32 = int32(-1), is_first: bool = True,
                                 prev_key: str = "!<[empty") -> str:
    """
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    Order is arbitrary.
    """
    global _string_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    if is_first:
        return _xs_string_int_dict_find_next_occupied(dct, int32(2), capacity)
    slot: int32 = _xs_string_int_dict_find_slot(dct, prev_key, capacity)
    if slot < 0:
        _string_int_dict_last_operation_status = c_string_int_dict_no_key_error
        return "-1"
    next_start: int32 = slot + 1
    return _xs_string_int_dict_find_next_occupied(dct, next_start, capacity)


def xs_string_int_dict_has_next(dct: int32 = int32(-1), is_first: bool = True,
                                 prev_key: str = "!<[empty") -> bool:
    capacity: int32 = xs_array_get_size(dct)
    start: int32 = int32(2)
    if not is_first:
        slot: int32 = _xs_string_int_dict_find_slot(dct, prev_key, capacity)
        if slot < 0:
            return False
        start = slot + 1
    while start < capacity:
        if _xs_string_int_dict_get_stored_key(dct, start) != "!<[empty":
            return True
        start += 1
    return False


def xs_string_int_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
    """
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
    """
    global _string_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    for i in i32range(2, capacity):
        key: str = _xs_string_int_dict_get_stored_key(dct, i)
        if key != "!<[empty":
            xs_string_int_dict_put(source, key, _xs_string_int_dict_get_stored_value(dct, i))
            if _string_int_dict_last_operation_status != c_string_int_dict_success and _string_int_dict_last_operation_status != c_string_int_dict_no_key_error:
                return _string_int_dict_last_operation_status
    _string_int_dict_last_operation_status = c_string_int_dict_success
    return c_string_int_dict_success


def xs_string_int_dict_put_if_absent(dct: int32 = int32(-1), key: str = "",
                                      val: int32 = int32(0)) -> int32:
    """
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `c_string_int_dict_generic_error` with last error set to `c_string_int_dict_generic_error`.
    """
    global _string_int_dict_last_operation_status
    if key == "!<[empty":
        _string_int_dict_last_operation_status = c_string_int_dict_generic_error
        return c_string_int_dict_generic_error
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_string_int_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _string_int_dict_last_operation_status = c_string_int_dict_success
        return _xs_string_int_dict_get_stored_value(dct, slot)

    r: int32 = _xs_string_int_dict_rehash_if_needed(dct, size, capacity, size + 1)
    if r != c_string_int_dict_success:
        return c_string_int_dict_generic_error

    capacity = xs_array_get_size(dct)
    result: int32 = _xs_string_int_dict_upsert(dct, key, val, capacity)
    if _string_int_dict_last_operation_status == c_string_int_dict_no_key_error:
        xs_array_set_int(dct, 0, size + 1)
        return c_string_int_dict_generic_error
    if _string_int_dict_last_operation_status != c_string_int_dict_success:
        return c_string_int_dict_generic_error
    return result


def xs_string_int_dict_keys(dct: int32 = int32(-1), out_arr: int32 = int32(-1)) -> int32:
    """
    Returns a new string array containing all keys in the dict. Order is arbitrary.
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = out_arr
    if arr < 0:
        arr = xs_array_create_string(size)
        if arr < 0:
            return c_string_int_dict_resize_failed_error
    else:
        r: int32 = xs_array_resize_string(arr, size)
        if r != 1:
            return c_string_int_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(2, capacity):
        stored_key: str = _xs_string_int_dict_get_stored_key(dct, i)
        if stored_key != "!<[empty":
            xs_array_set_string(arr, idx, stored_key)
            idx += 1
    return arr


def xs_string_int_dict_values(dct: int32 = int32(-1), out_arr: int32 = int32(-1)) -> int32:
    """
    Returns a new int array containing all values in the dict. Order matches `xs_string_int_dict_keys`.
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = out_arr
    if arr < 0:
        arr = xs_array_create_int(size, int32(0))
        if arr < 0:
            return c_string_int_dict_resize_failed_error
    else:
        r: int32 = xs_array_resize_int(arr, size)
        if r != 1:
            return c_string_int_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(2, capacity):
        stored_key: str = _xs_string_int_dict_get_stored_key(dct, i)
        if stored_key != "!<[empty":
            xs_array_set_int(arr, idx, _xs_string_int_dict_get_stored_value(dct, i))
            idx += 1
    return arr


def xs_string_int_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
    """
    Returns true if both dicts contain the same key-value pairs.
    """
    size_a: int32 = xs_array_get_int(a, 0)
    size_b: int32 = xs_array_get_int(b, 0)
    if size_a != size_b:
        return False
    capacity: int32 = xs_array_get_size(a)
    for i in i32range(2, capacity):
        key: str = _xs_string_int_dict_get_stored_key(a, i)
        if key != "!<[empty":
            val: int32 = _xs_string_int_dict_get_stored_value(a, i)
            if xs_string_int_dict_get(b, key) != val:
                return False
            if xs_string_int_dict_last_error() != c_string_int_dict_success:
                return False
    return True
