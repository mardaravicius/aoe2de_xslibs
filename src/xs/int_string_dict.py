from numpy import int32, float32

from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size, xs_array_create_string, xs_array_set_string, xs_array_resize_string, xs_array_get_string
from xs_converter.symbols import XsExternConst, i32range

c_int_string_dict_success: XsExternConst[int32] = int32(0)
c_int_string_dict_generic_error: XsExternConst[int32] = int32(-1)
c_int_string_dict_no_key_error: XsExternConst[int32] = int32(-2)
c_int_string_dict_resize_failed_error: XsExternConst[int32] = int32(-3)
c_int_string_dict_max_capacity_error: XsExternConst[int32] = int32(-4)
c_int_string_dict_max_capacity: XsExternConst[int32] = int32(999999999)
c_int_string_dict_max_load_factor: XsExternConst[float32] = float32(0.75)
c_int_string_dict_empty_key: XsExternConst[int32] = int32(-999999999)
c_int_string_dict_initial_capacity: XsExternConst[int32] = int32(18)
c_int_string_dict_hash_constant: XsExternConst[int32] = int32(16777619)
_int_string_dict_last_operation_status: int32 = c_int_string_dict_success
_int_string_dict_temp_keys: int32 = int32(-1)
_int_string_dict_temp_values: int32 = int32(-1)


def _xs_int_string_dict_values_capacity_from_int_capacity(capacity: int32 = int32(0)) -> int32:
    return capacity - 2


def _xs_int_string_dict_get_values_array(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 1)


def _xs_int_string_dict_value_slot(slot: int32 = int32(2)) -> int32:
    return slot - 2


def _xs_int_string_dict_get_stored_value(dct: int32 = int32(-1), slot: int32 = int32(2)) -> str:
    return xs_array_get_string(_xs_int_string_dict_get_values_array(dct), _xs_int_string_dict_value_slot(slot))


def _xs_int_string_dict_set_stored_value(dct: int32 = int32(-1), slot: int32 = int32(2), value: str = "") -> None:
    xs_array_set_string(_xs_int_string_dict_get_values_array(dct), _xs_int_string_dict_value_slot(slot), value)


def _xs_int_string_dict_clear_slot(dct: int32 = int32(-1), slot: int32 = int32(2)) -> None:
    xs_array_set_int(dct, slot, c_int_string_dict_empty_key)


def xs_int_string_dict_create() -> int32:
    """
    Creates an empty int-to-string dictionary.
    Keys equal to `c_int_string_dict_empty_key` (-999999999) are reserved as the internal
    empty-slot sentinel and cannot be stored. `put` and `put_if_absent` silently reject them.
    :return: created dict id, or `c_int_string_dict_generic_error` on error
    """
    dct: int32 = xs_array_create_int(c_int_string_dict_initial_capacity, c_int_string_dict_empty_key)
    if dct < 0:
        return c_int_string_dict_generic_error
    values_arr: int32 = xs_array_create_string(c_int_string_dict_initial_capacity - 2)
    if values_arr < 0:
        xs_array_resize_int(dct, 0)
        return c_int_string_dict_generic_error
    xs_array_set_int(dct, 0, 0)
    xs_array_set_int(dct, 1, values_arr)
    return dct


def _xs_int_string_dict_hash(key: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    hash: int32 = key * c_int_string_dict_hash_constant
    num_slots: int32 = _xs_int_string_dict_values_capacity_from_int_capacity(capacity)
    hash = hash % num_slots
    if hash < 0:
        hash += num_slots
    return hash + 2


def _xs_int_string_dict_find_slot(dct: int32 = int32(-1), key: int32 = int32(-1),
                                   capacity: int32 = int32(0)) -> int32:
    """Returns int-array index of slot containing key, or -1 if not found."""
    num_slots: int32 = _xs_int_string_dict_values_capacity_from_int_capacity(capacity)
    home: int32 = _xs_int_string_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: int32 = xs_array_get_int(dct, slot)
        if stored_key == c_int_string_dict_empty_key:
            return int32(-1)
        if stored_key == key:
            return slot
        slot += 1
        if slot >= capacity:
            slot = int32(2)
        steps += 1
    return int32(-1)


def _xs_int_string_dict_upsert(dct: int32 = int32(-1), key: int32 = int32(-1), val: str = "",
                                capacity: int32 = int32(0)) -> str:
    global _int_string_dict_last_operation_status
    num_slots: int32 = _xs_int_string_dict_values_capacity_from_int_capacity(capacity)
    home: int32 = _xs_int_string_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: int32 = xs_array_get_int(dct, slot)
        if stored_key == c_int_string_dict_empty_key:
            xs_array_set_int(dct, slot, key)
            _xs_int_string_dict_set_stored_value(dct, slot, val)
            _int_string_dict_last_operation_status = c_int_string_dict_no_key_error
            return "-1"
        if stored_key == key:
            old_val: str = _xs_int_string_dict_get_stored_value(dct, slot)
            _xs_int_string_dict_set_stored_value(dct, slot, val)
            _int_string_dict_last_operation_status = c_int_string_dict_success
            return old_val
        slot += 1
        if slot >= capacity:
            slot = int32(2)
        steps += 1
    _int_string_dict_last_operation_status = c_int_string_dict_max_capacity_error
    return "-1"


def _xs_int_string_dict_move_to_temp_arrays(dct: int32 = int32(-1), size: int32 = int32(0),
                                             capacity: int32 = int32(0)) -> int32:
    global _int_string_dict_temp_keys, _int_string_dict_temp_values
    temp_data_size: int32 = size
    max_values_capacity: int32 = c_int_string_dict_max_capacity - 2
    if _int_string_dict_temp_keys < 0:
        _int_string_dict_temp_keys = xs_array_create_int(temp_data_size, c_int_string_dict_empty_key)
        if _int_string_dict_temp_keys < 0:
            return c_int_string_dict_resize_failed_error
    else:
        temp_keys_capacity: int32 = xs_array_get_size(_int_string_dict_temp_keys)
        if temp_keys_capacity < temp_data_size:
            if temp_data_size > max_values_capacity:
                return c_int_string_dict_max_capacity_error
            r_keys: int32 = xs_array_resize_int(_int_string_dict_temp_keys, temp_data_size)
            if r_keys != 1:
                return c_int_string_dict_resize_failed_error
    if _int_string_dict_temp_values < 0:
        _int_string_dict_temp_values = xs_array_create_string(temp_data_size)
        if _int_string_dict_temp_values < 0:
            return c_int_string_dict_resize_failed_error
    else:
        temp_values_capacity: int32 = xs_array_get_size(_int_string_dict_temp_values)
        if temp_values_capacity < temp_data_size:
            if temp_data_size > max_values_capacity:
                return c_int_string_dict_max_capacity_error
            r_values: int32 = xs_array_resize_string(_int_string_dict_temp_values, temp_data_size)
            if r_values != 1:
                return c_int_string_dict_resize_failed_error
    t: int32 = int32(0)
    for i in i32range(2, capacity):
        stored_key: int32 = xs_array_get_int(dct, i)
        if stored_key != c_int_string_dict_empty_key:
            xs_array_set_int(_int_string_dict_temp_keys, t, stored_key)
            xs_array_set_string(_int_string_dict_temp_values, t, _xs_int_string_dict_get_stored_value(dct, i))
            t += 1
    return temp_data_size


def _xs_int_string_dict_clear_slots(dct: int32 = int32(-1), capacity: int32 = int32(-1)) -> None:
    for j in i32range(2, capacity):
        _xs_int_string_dict_clear_slot(dct, j)


def _xs_int_string_dict_rehash_if_needed(dct: int32 = int32(-1), size: int32 = int32(0),
                                          capacity: int32 = int32(0),
                                          required_size: int32 = int32(-1)) -> int32:
    global _int_string_dict_last_operation_status
    if required_size < 0:
        required_size = size
    load_factor: float = float(required_size) / _xs_int_string_dict_values_capacity_from_int_capacity(capacity)
    if load_factor > c_int_string_dict_max_load_factor:
        store_status: int32 = _int_string_dict_last_operation_status
        new_values_capacity: int32 = _xs_int_string_dict_values_capacity_from_int_capacity(capacity) * 2
        new_capacity: int32 = new_values_capacity + 2
        if new_capacity > c_int_string_dict_max_capacity:
            _int_string_dict_last_operation_status = c_int_string_dict_max_capacity_error
            return c_int_string_dict_generic_error
        temp_data_size: int32 = _xs_int_string_dict_move_to_temp_arrays(dct, size, capacity)
        if temp_data_size < 0:
            _int_string_dict_last_operation_status = temp_data_size
            return c_int_string_dict_generic_error
        values_arr: int32 = _xs_int_string_dict_get_values_array(dct)
        r_values: int32 = xs_array_resize_string(values_arr, new_values_capacity)
        if r_values != 1:
            _int_string_dict_last_operation_status = c_int_string_dict_resize_failed_error
            return c_int_string_dict_generic_error
        r: int32 = xs_array_resize_int(dct, new_capacity)
        if r != 1:
            _int_string_dict_last_operation_status = c_int_string_dict_resize_failed_error
            return c_int_string_dict_generic_error
        _xs_int_string_dict_clear_slots(dct, new_capacity)
        for t in i32range(0, temp_data_size):
            _xs_int_string_dict_upsert(
                dct,
                xs_array_get_int(_int_string_dict_temp_keys, t),
                xs_array_get_string(_int_string_dict_temp_values, t),
                new_capacity,
            )
            if _int_string_dict_last_operation_status < 0 and _int_string_dict_last_operation_status != c_int_string_dict_no_key_error:
                return c_int_string_dict_generic_error
        _int_string_dict_last_operation_status = store_status
    return c_int_string_dict_success


def xs_int_string_dict_put(dct: int32 = int32(-1), key: int32 = int32(-1), val: str = "") -> str:
    """
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    Sets last error on completion.
    If `key` equals `c_int_string_dict_empty_key`, the call is a no-op and returns
    `"-1"` with last error set to `c_int_string_dict_generic_error`.
    :return: previous value if the key already existed, or `"-1"`
        if newly inserted or on error. Callers must check `xs_int_string_dict_last_error()`.
    """
    global _int_string_dict_last_operation_status
    if key == c_int_string_dict_empty_key:
        _int_string_dict_last_operation_status = c_int_string_dict_generic_error
        return "-1"
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_int_string_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        old_val: str = _xs_int_string_dict_get_stored_value(dct, slot)
        _xs_int_string_dict_set_stored_value(dct, slot, val)
        _int_string_dict_last_operation_status = c_int_string_dict_success
        return old_val

    r: int32 = _xs_int_string_dict_rehash_if_needed(dct, size, capacity, size + 1)
    if r != c_int_string_dict_success:
        return "-1"

    capacity = xs_array_get_size(dct)
    previous_value: str = _xs_int_string_dict_upsert(dct, key, val, capacity)
    if _int_string_dict_last_operation_status == c_int_string_dict_no_key_error:
        xs_array_set_int(dct, 0, size + 1)
        return "-1"
    if _int_string_dict_last_operation_status != c_int_string_dict_success:
        return "-1"
    return previous_value


def xs_int_string_dict(
        k1: int32 = c_int_string_dict_empty_key,
        v1: str = "",
        k2: int32 = c_int_string_dict_empty_key,
        v2: str = "",
        k3: int32 = c_int_string_dict_empty_key,
        v3: str = "",
        k4: int32 = c_int_string_dict_empty_key,
        v4: str = "",
        k5: int32 = c_int_string_dict_empty_key,
        v5: str = "",
        k6: int32 = c_int_string_dict_empty_key,
        v6: str = "",
) -> int32:
    """
    Creates a dict with provided key-value pairs. The first key that equals
    `c_int_string_dict_empty_key` will stop further insertion.
    """
    dct: int32 = xs_int_string_dict_create()
    if dct < 0:
        return c_int_string_dict_generic_error
    if k1 == c_int_string_dict_empty_key:
        return dct
    xs_int_string_dict_put(dct, k1, v1)
    if k2 == c_int_string_dict_empty_key:
        return dct
    xs_int_string_dict_put(dct, k2, v2)
    if k3 == c_int_string_dict_empty_key:
        return dct
    xs_int_string_dict_put(dct, k3, v3)
    if k4 == c_int_string_dict_empty_key:
        return dct
    xs_int_string_dict_put(dct, k4, v4)
    if k5 == c_int_string_dict_empty_key:
        return dct
    xs_int_string_dict_put(dct, k5, v5)
    if k6 == c_int_string_dict_empty_key:
        return dct
    xs_int_string_dict_put(dct, k6, v6)
    return dct


def xs_int_string_dict_get(dct: int32 = int32(-1), key: int32 = int32(-1), dft: str = "-1") -> str:
    """
    Returns the value associated with the given key. Sets last error on completion.
    """
    global _int_string_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_int_string_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _int_string_dict_last_operation_status = c_int_string_dict_success
        return _xs_int_string_dict_get_stored_value(dct, slot)
    _int_string_dict_last_operation_status = c_int_string_dict_no_key_error
    return dft


def xs_int_string_dict_remove(dct: int32 = int32(-1), key: int32 = int32(-1)) -> str:
    """
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
    """
    global _int_string_dict_last_operation_status
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    num_slots: int32 = _xs_int_string_dict_values_capacity_from_int_capacity(capacity)
    slot: int32 = _xs_int_string_dict_find_slot(dct, key, capacity)
    if slot < 0:
        _int_string_dict_last_operation_status = c_int_string_dict_no_key_error
        return "-1"
    found_val: str = _xs_int_string_dict_get_stored_value(dct, slot)

    g: int32 = slot
    q: int32 = g + 1
    if q >= capacity:
        q = int32(2)
    shift_steps: int32 = int32(0)
    q_key: int32 = xs_array_get_int(dct, q)
    while q_key != c_int_string_dict_empty_key and shift_steps < num_slots:
        q_home: int32 = _xs_int_string_dict_hash(q_key, capacity)
        g_slot: int32 = g - 2
        q_slot: int32 = q - 2
        h_slot: int32 = q_home - 2
        dist_g: int32 = (g_slot - h_slot + num_slots) % num_slots
        dist_q: int32 = (q_slot - h_slot + num_slots) % num_slots
        if dist_g < dist_q:
            xs_array_set_int(dct, g, q_key)
            _xs_int_string_dict_set_stored_value(dct, g, _xs_int_string_dict_get_stored_value(dct, q))
            g = q
        q += 1
        if q >= capacity:
            q = int32(2)
        shift_steps += 1
        q_key = xs_array_get_int(dct, q)
    _xs_int_string_dict_clear_slot(dct, g)
    xs_array_set_int(dct, 0, size - 1)
    _int_string_dict_last_operation_status = c_int_string_dict_success
    return found_val


def xs_int_string_dict_contains(dct: int32 = int32(-1), key: int32 = int32(-1)) -> bool:
    capacity: int32 = xs_array_get_size(dct)
    return _xs_int_string_dict_find_slot(dct, key, capacity) >= 0


def xs_int_string_dict_size(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 0)


def xs_int_string_dict_clear(dct: int32 = int32(-1)) -> int32:
    """
    Removes all entries from the dict and shrinks the backing arrays.
    """
    capacity: int32 = xs_array_get_size(dct)
    _xs_int_string_dict_clear_slots(dct, capacity)
    xs_array_set_int(dct, 0, 0)
    if capacity > c_int_string_dict_initial_capacity:
        values_arr: int32 = _xs_int_string_dict_get_values_array(dct)
        r: int32 = xs_array_resize_int(dct, c_int_string_dict_initial_capacity)
        if r != 1:
            return c_int_string_dict_generic_error
        r_values: int32 = xs_array_resize_string(values_arr, c_int_string_dict_initial_capacity - 2)
        if r_values != 1:
            return c_int_string_dict_generic_error
    return c_int_string_dict_success


def xs_int_string_dict_copy(dct: int32 = int32(-1)) -> int32:
    """
    Returns a deep copy of the dict.
    """
    capacity: int32 = xs_array_get_size(dct)
    values_capacity: int32 = _xs_int_string_dict_values_capacity_from_int_capacity(capacity)
    new_dct: int32 = xs_array_create_int(capacity, c_int_string_dict_empty_key)
    if new_dct < 0:
        return c_int_string_dict_resize_failed_error
    new_values_arr: int32 = xs_array_create_string(values_capacity)
    if new_values_arr < 0:
        xs_array_resize_int(new_dct, 0)
        return c_int_string_dict_resize_failed_error
    xs_array_set_int(new_dct, 0, xs_array_get_int(dct, 0))
    xs_array_set_int(new_dct, 1, new_values_arr)
    for i in i32range(2, capacity):
        stored_key: int32 = xs_array_get_int(dct, i)
        if stored_key != c_int_string_dict_empty_key:
            xs_array_set_int(new_dct, i, stored_key)
            xs_array_set_string(new_values_arr, i - 2, _xs_int_string_dict_get_stored_value(dct, i))
    return new_dct


def xs_int_string_dict_to_string(dct: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the dict in the format `{k1: "v1", k2: "v2", ...}`.
    """
    capacity: int32 = xs_array_get_size(dct)
    s: str = "{"
    first: bool = True
    for i in i32range(2, capacity):
        key: int32 = xs_array_get_int(dct, i)
        if key != c_int_string_dict_empty_key:
            if first:
                first = False
            else:
                s += ", "
            s += f'{key}: "{_xs_int_string_dict_get_stored_value(dct, i)}"'
    s += "}"
    return s


def xs_int_string_dict_last_error() -> int32:
    return _int_string_dict_last_operation_status


def _xs_int_string_dict_find_next_occupied(dct: int32 = int32(-1), start: int32 = int32(2),
                                            capacity: int32 = int32(0)) -> int32:
    global _int_string_dict_last_operation_status
    slot: int32 = start
    while slot < capacity:
        stored_key: int32 = xs_array_get_int(dct, slot)
        if stored_key != c_int_string_dict_empty_key:
            _int_string_dict_last_operation_status = c_int_string_dict_success
            return stored_key
        slot += 1
    _int_string_dict_last_operation_status = c_int_string_dict_no_key_error
    return c_int_string_dict_generic_error


def xs_int_string_dict_next_key(dct: int32 = int32(-1), is_first: bool = True,
                                 prev_key: int32 = int32(-1)) -> int32:
    """
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    """
    global _int_string_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    if is_first:
        return _xs_int_string_dict_find_next_occupied(dct, int32(2), capacity)
    slot: int32 = _xs_int_string_dict_find_slot(dct, prev_key, capacity)
    if slot < 0:
        _int_string_dict_last_operation_status = c_int_string_dict_no_key_error
        return c_int_string_dict_generic_error
    next_start: int32 = slot + 1
    return _xs_int_string_dict_find_next_occupied(dct, next_start, capacity)


def xs_int_string_dict_has_next(dct: int32 = int32(-1), is_first: bool = True,
                                 prev_key: int32 = int32(-1)) -> bool:
    capacity: int32 = xs_array_get_size(dct)
    start: int32 = int32(2)
    if not is_first:
        slot: int32 = _xs_int_string_dict_find_slot(dct, prev_key, capacity)
        if slot < 0:
            return False
        start = slot + 1
    while start < capacity:
        if xs_array_get_int(dct, start) != c_int_string_dict_empty_key:
            return True
        start += 1
    return False


def xs_int_string_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
    """
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
    """
    global _int_string_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    for i in i32range(2, capacity):
        key: int32 = xs_array_get_int(dct, i)
        if key != c_int_string_dict_empty_key:
            xs_int_string_dict_put(source, key, _xs_int_string_dict_get_stored_value(dct, i))
            if _int_string_dict_last_operation_status != c_int_string_dict_success and _int_string_dict_last_operation_status != c_int_string_dict_no_key_error:
                return _int_string_dict_last_operation_status
    _int_string_dict_last_operation_status = c_int_string_dict_success
    return c_int_string_dict_success


def xs_int_string_dict_put_if_absent(dct: int32 = int32(-1), key: int32 = int32(-1),
                                      val: str = "") -> str:
    """
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `c_int_string_dict_empty_key`, the call is a no-op and returns
    `"-1"` with last error set to `c_int_string_dict_generic_error`.
    """
    global _int_string_dict_last_operation_status
    if key == c_int_string_dict_empty_key:
        _int_string_dict_last_operation_status = c_int_string_dict_generic_error
        return "-1"
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_int_string_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _int_string_dict_last_operation_status = c_int_string_dict_success
        return _xs_int_string_dict_get_stored_value(dct, slot)

    r: int32 = _xs_int_string_dict_rehash_if_needed(dct, size, capacity, size + 1)
    if r != c_int_string_dict_success:
        return "-1"

    capacity = xs_array_get_size(dct)
    result: str = _xs_int_string_dict_upsert(dct, key, val, capacity)
    if _int_string_dict_last_operation_status == c_int_string_dict_no_key_error:
        xs_array_set_int(dct, 0, size + 1)
        return "-1"
    if _int_string_dict_last_operation_status != c_int_string_dict_success:
        return "-1"
    return result


def xs_int_string_dict_keys(dct: int32 = int32(-1)) -> int32:
    """
    Returns a new int array containing all keys in the dict. Order is arbitrary.
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = xs_array_create_int(size, 0)
    if arr < 0:
        return c_int_string_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(2, capacity):
        stored_key: int32 = xs_array_get_int(dct, i)
        if stored_key != c_int_string_dict_empty_key:
            xs_array_set_int(arr, idx, stored_key)
            idx += 1
    return arr


def xs_int_string_dict_values(dct: int32 = int32(-1)) -> int32:
    """
    Returns a new string array containing all values in the dict. Order matches
    `xs_int_string_dict_keys`.
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = xs_array_create_string(size)
    if arr < 0:
        return c_int_string_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(2, capacity):
        stored_key: int32 = xs_array_get_int(dct, i)
        if stored_key != c_int_string_dict_empty_key:
            xs_array_set_string(arr, idx, _xs_int_string_dict_get_stored_value(dct, i))
            idx += 1
    return arr


def xs_int_string_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
    """
    Returns true if both dicts contain the same key-value pairs.
    """
    size_a: int32 = xs_array_get_int(a, 0)
    size_b: int32 = xs_array_get_int(b, 0)
    if size_a != size_b:
        return False
    capacity: int32 = xs_array_get_size(a)
    for i in i32range(2, capacity):
        key: int32 = xs_array_get_int(a, i)
        if key != c_int_string_dict_empty_key:
            val: str = _xs_int_string_dict_get_stored_value(a, i)
            if xs_int_string_dict_get(b, key) != val:
                return False
            if xs_int_string_dict_last_error() != c_int_string_dict_success:
                return False
    return True
