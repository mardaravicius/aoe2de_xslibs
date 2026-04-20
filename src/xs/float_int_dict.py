from numpy import int32, float32

from xs_converter.functions import (
    bit_cast_to_float,
    bit_cast_to_int,
    xs_array_create_float,
    xs_array_create_int,
    xs_array_get_int,
    xs_array_get_size,
    xs_array_resize_int,
    xs_array_set_float,
    xs_array_set_int,
)
from xs_converter.symbols import XsExternConst, i32range

c_float_int_dict_success: XsExternConst[int32] = int32(0)
c_float_int_dict_generic_error: XsExternConst[int32] = int32(-1)
c_float_int_dict_generic_error_float: XsExternConst[float32] = float32(-1.0)
c_float_int_dict_no_key_error: XsExternConst[int32] = int32(-2)
c_float_int_dict_resize_failed_error: XsExternConst[int32] = int32(-3)
c_float_int_dict_max_capacity_error: XsExternConst[int32] = int32(-4)
c_float_int_dict_max_capacity: XsExternConst[int32] = int32(999999999)
c_float_int_dict_max_load_factor: XsExternConst[float32] = float32(0.75)
c_float_int_dict_empty_key: XsExternConst[float32] = float32(-9999999.0)
c_float_int_dict_empty_key_bits: XsExternConst[int32] = int32(-887581057)
c_float_int_dict_canonical_nan_bits: XsExternConst[int32] = int32(-8388607)
c_float_int_dict_initial_capacity: XsExternConst[int32] = int32(33)
c_float_int_dict_hash_constant: XsExternConst[int32] = int32(16777619)
_float_int_dict_last_operation_status: int32 = c_float_int_dict_success
_float_int_dict_temp_array: int32 = int32(-1)


def _xs_float_int_dict_key_bits(key: float32 = float32(0.0)) -> int32:
    if key != key:
        return c_float_int_dict_canonical_nan_bits
    if key == float32(0.0):
        return int32(0)
    return bit_cast_to_int(key)


def xs_float_int_dict_create() -> int32:
    """
    Creates an empty float-to-int dictionary.
    Keys equal to `c_float_int_dict_empty_key` (-9999999.0) are reserved as the internal empty-slot
    sentinel and cannot be stored. `put` and `put_if_absent` silently reject them. Signed zero keys
    are canonicalized to `0.0`, and all NaN keys are canonicalized to a single NaN bit pattern.
    :return: created dict id, or `c_float_int_dict_generic_error` on error
    """
    dct: int32 = xs_array_create_int(c_float_int_dict_initial_capacity, c_float_int_dict_empty_key_bits)
    if dct < 0:
        return c_float_int_dict_generic_error
    xs_array_set_int(dct, 0, 0)
    return dct


def _xs_float_int_dict_hash(key: float32 = float32(0.0), capacity: int32 = int32(0)) -> int32:
    h: int32 = _xs_float_int_dict_key_bits(key) * c_float_int_dict_hash_constant
    num_slots: int32 = (capacity - 1) // 2
    h = h % num_slots
    if h < 0:
        h += num_slots
    return (h * 2) + 1


def _xs_float_int_dict_find_slot(dct: int32 = int32(-1), key: float32 = float32(0.0),
                                 capacity: int32 = int32(0)) -> int32:
    """Returns array index of slot containing key, or -1 if not found."""
    key_bits: int32 = _xs_float_int_dict_key_bits(key)
    num_slots: int32 = (capacity - 1) // 2
    home: int32 = _xs_float_int_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key_bits: int32 = xs_array_get_int(dct, slot)
        if stored_key_bits == c_float_int_dict_empty_key_bits:
            return int32(-1)
        if stored_key_bits == key_bits:
            return slot
        slot += 2
        if slot >= capacity:
            slot = int32(1)
        steps += 1
    return int32(-1)


def _xs_float_int_dict_upsert(dct: int32 = int32(-1), key: float32 = float32(0.0), val: int32 = int32(0),
                              capacity: int32 = int32(0)) -> int32:
    global _float_int_dict_last_operation_status
    key_bits: int32 = _xs_float_int_dict_key_bits(key)
    num_slots: int32 = (capacity - 1) // 2
    home: int32 = _xs_float_int_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key_bits: int32 = xs_array_get_int(dct, slot)
        if stored_key_bits == c_float_int_dict_empty_key_bits:
            xs_array_set_int(dct, slot, key_bits)
            xs_array_set_int(dct, slot + 1, val)
            _float_int_dict_last_operation_status = c_float_int_dict_no_key_error
            return c_float_int_dict_generic_error
        if stored_key_bits == key_bits:
            old_val: int32 = xs_array_get_int(dct, slot + 1)
            xs_array_set_int(dct, slot + 1, val)
            _float_int_dict_last_operation_status = c_float_int_dict_success
            return old_val
        slot += 2
        if slot >= capacity:
            slot = int32(1)
        steps += 1
    _float_int_dict_last_operation_status = c_float_int_dict_max_capacity_error
    return c_float_int_dict_generic_error


def _xs_float_int_dict_move_to_temp_array(dct: int32 = int32(-1), size: int32 = int32(0),
                                          capacity: int32 = int32(0)) -> int32:
    global _float_int_dict_temp_array
    temp_data_size: int32 = size * 2
    if _float_int_dict_temp_array < 0:
        _float_int_dict_temp_array = xs_array_create_int(temp_data_size, c_float_int_dict_empty_key_bits)
        if _float_int_dict_temp_array < 0:
            return c_float_int_dict_resize_failed_error
    else:
        temp_arr_capacity: int32 = xs_array_get_size(_float_int_dict_temp_array)
        if temp_arr_capacity < temp_data_size:
            if temp_data_size > c_float_int_dict_max_capacity:
                return c_float_int_dict_max_capacity_error
            r: int32 = xs_array_resize_int(_float_int_dict_temp_array, temp_data_size)
            if r != 1:
                return c_float_int_dict_resize_failed_error
    t: int32 = int32(0)
    for i in i32range(1, capacity, 2):
        stored_key_bits: int32 = xs_array_get_int(dct, i)
        if stored_key_bits != c_float_int_dict_empty_key_bits:
            xs_array_set_int(_float_int_dict_temp_array, t, stored_key_bits)
            xs_array_set_int(_float_int_dict_temp_array, t + 1, xs_array_get_int(dct, i + 1))
            t += 2
    return temp_data_size


def _xs_float_int_dict_clear_slots(dct: int32 = int32(-1), capacity: int32 = int32(-1)) -> None:
    for j in i32range(1, capacity, 2):
        xs_array_set_int(dct, j, c_float_int_dict_empty_key_bits)


def _xs_float_int_dict_rehash_if_needed(dct: int32 = int32(-1), size: int32 = int32(0),
                                        capacity: int32 = int32(0),
                                        required_size: int32 = int32(-1)) -> int32:
    global _float_int_dict_last_operation_status
    if required_size < 0:
        required_size = size
    load_factor: float = float(required_size) / ((capacity - 1) // 2)
    if load_factor > c_float_int_dict_max_load_factor:
        store_status: int32 = _float_int_dict_last_operation_status
        new_capacity: int32 = (capacity - 1) * 2 + 1
        if new_capacity > c_float_int_dict_max_capacity:
            _float_int_dict_last_operation_status = c_float_int_dict_max_capacity_error
            return c_float_int_dict_generic_error
        temp_data_size: int32 = _xs_float_int_dict_move_to_temp_array(dct, size, capacity)
        if temp_data_size < 0:
            _float_int_dict_last_operation_status = temp_data_size
            return c_float_int_dict_generic_error
        r: int32 = xs_array_resize_int(dct, new_capacity)
        if r != 1:
            _float_int_dict_last_operation_status = c_float_int_dict_resize_failed_error
            return c_float_int_dict_generic_error
        _xs_float_int_dict_clear_slots(dct, new_capacity)
        for t in i32range(0, temp_data_size, 2):
            _xs_float_int_dict_upsert(
                dct,
                bit_cast_to_float(xs_array_get_int(_float_int_dict_temp_array, t)),
                xs_array_get_int(_float_int_dict_temp_array, t + 1),
                new_capacity,
            )
            if _float_int_dict_last_operation_status < 0 and _float_int_dict_last_operation_status != c_float_int_dict_no_key_error:
                return c_float_int_dict_generic_error
        _float_int_dict_last_operation_status = store_status
    return c_float_int_dict_success


def xs_float_int_dict_put(dct: int32 = int32(-1), key: float32 = float32(0.0), val: int32 = int32(0)) -> int32:
    """
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    Sets last error on completion.
    If `key` equals `c_float_int_dict_empty_key`, the call is a no-op and returns `c_float_int_dict_generic_error`
    with last error set to `c_float_int_dict_generic_error`.
    :return: previous value if the key already existed, or `c_float_int_dict_generic_error` if newly inserted or on error.
        Because -1 is both the error sentinel and a valid previous value, callers must check
        `xs_float_int_dict_last_error()` to distinguish: `c_float_int_dict_success` means the key
        existed and the returned value is valid; `c_float_int_dict_no_key_error` means a new key
        was inserted; any other negative status indicates an error.
    """
    global _float_int_dict_last_operation_status
    if key == c_float_int_dict_empty_key:
        _float_int_dict_last_operation_status = c_float_int_dict_generic_error
        return c_float_int_dict_generic_error
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_float_int_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        old_val: int32 = xs_array_get_int(dct, slot + 1)
        xs_array_set_int(dct, slot + 1, val)
        _float_int_dict_last_operation_status = c_float_int_dict_success
        return old_val

    r: int32 = _xs_float_int_dict_rehash_if_needed(dct, size, capacity, size + 1)
    if r != c_float_int_dict_success:
        return c_float_int_dict_generic_error

    capacity = xs_array_get_size(dct)
    previous_value: int32 = _xs_float_int_dict_upsert(dct, key, val, capacity)
    if _float_int_dict_last_operation_status == c_float_int_dict_no_key_error:
        xs_array_set_int(dct, 0, size + 1)
        return c_float_int_dict_generic_error
    if _float_int_dict_last_operation_status != c_float_int_dict_success:
        return c_float_int_dict_generic_error
    return previous_value


def xs_float_int_dict(
        k1: float32 = c_float_int_dict_empty_key,
        v1: int32 = int32(0),
        k2: float32 = c_float_int_dict_empty_key,
        v2: int32 = int32(0),
        k3: float32 = c_float_int_dict_empty_key,
        v3: int32 = int32(0),
        k4: float32 = c_float_int_dict_empty_key,
        v4: int32 = int32(0),
        k5: float32 = c_float_int_dict_empty_key,
        v5: int32 = int32(0),
        k6: float32 = c_float_int_dict_empty_key,
        v6: int32 = int32(0),
) -> int32:
    """
    Creates a dict with provided key-value pairs. The first key that equals `c_float_int_dict_empty_key`
    will stop further insertion.
    This function can create a dict with 6 entries at the maximum, but further entries can be added with
    `xs_float_int_dict_put`.
    :return: created dict id, or `c_float_int_dict_generic_error` on error
    """
    dct: int32 = xs_float_int_dict_create()
    if dct < 0:
        return c_float_int_dict_generic_error
    if k1 == c_float_int_dict_empty_key:
        return dct
    xs_float_int_dict_put(dct, k1, v1)
    if k2 == c_float_int_dict_empty_key:
        return dct
    xs_float_int_dict_put(dct, k2, v2)
    if k3 == c_float_int_dict_empty_key:
        return dct
    xs_float_int_dict_put(dct, k3, v3)
    if k4 == c_float_int_dict_empty_key:
        return dct
    xs_float_int_dict_put(dct, k4, v4)
    if k5 == c_float_int_dict_empty_key:
        return dct
    xs_float_int_dict_put(dct, k5, v5)
    if k6 == c_float_int_dict_empty_key:
        return dct
    xs_float_int_dict_put(dct, k6, v6)
    return dct


def xs_float_int_dict_get(dct: int32 = int32(-1), key: float32 = float32(0.0), dft: int32 = int32(-1)) -> int32:
    """
    Returns the value associated with the given key. Sets last error on completion.
    :param dft: default value returned if the key is not found
    :return: value for the key, or `dft` if not found
    """
    global _float_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_float_int_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _float_int_dict_last_operation_status = c_float_int_dict_success
        return xs_array_get_int(dct, slot + 1)
    _float_int_dict_last_operation_status = c_float_int_dict_no_key_error
    return dft


def xs_float_int_dict_remove(dct: int32 = int32(-1), key: float32 = float32(0.0)) -> int32:
    """
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain the linear probing invariant (no tombstones).
    :return: value that was associated with the key, or `c_float_int_dict_generic_error` if not found
    """
    global _float_int_dict_last_operation_status
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    num_slots: int32 = (capacity - 1) // 2
    slot: int32 = _xs_float_int_dict_find_slot(dct, key, capacity)
    if slot < 0:
        _float_int_dict_last_operation_status = c_float_int_dict_no_key_error
        return c_float_int_dict_generic_error
    found_val: int32 = xs_array_get_int(dct, slot + 1)

    # Backward shift to restore linear probing invariant.
    g: int32 = slot
    q: int32 = g + 2
    if q >= capacity:
        q = int32(1)
    shift_steps: int32 = int32(0)
    q_key_bits: int32 = xs_array_get_int(dct, q)
    while q_key_bits != c_float_int_dict_empty_key_bits and shift_steps < num_slots:
        q_home: int32 = _xs_float_int_dict_hash(bit_cast_to_float(q_key_bits), capacity)
        g_slot: int32 = (g - 1) // 2
        q_slot: int32 = (q - 1) // 2
        h_slot: int32 = (q_home - 1) // 2
        dist_g: int32 = (g_slot - h_slot + num_slots) % num_slots
        dist_q: int32 = (q_slot - h_slot + num_slots) % num_slots
        if dist_g < dist_q:
            xs_array_set_int(dct, g, q_key_bits)
            xs_array_set_int(dct, g + 1, xs_array_get_int(dct, q + 1))
            g = q
        q += 2
        if q >= capacity:
            q = int32(1)
        shift_steps += 1
        q_key_bits = xs_array_get_int(dct, q)
    xs_array_set_int(dct, g, c_float_int_dict_empty_key_bits)
    xs_array_set_int(dct, 0, size - 1)
    _float_int_dict_last_operation_status = c_float_int_dict_success
    return found_val


def xs_float_int_dict_contains(dct: int32 = int32(-1), key: float32 = float32(0.0)) -> bool:
    """
    Checks whether the given key exists in the dict.
    :return: true if the key is found, false otherwise
    """
    capacity: int32 = xs_array_get_size(dct)
    return _xs_float_int_dict_find_slot(dct, key, capacity) >= 0


def xs_float_int_dict_size(dct: int32 = int32(-1)) -> int32:
    """
    Returns the number of key-value pairs stored in the dict.
    :return: dict size
    """
    return xs_array_get_int(dct, 0)


def xs_float_int_dict_clear(dct: int32 = int32(-1)) -> int32:
    """
    Removes all entries from the dict and shrinks storage back to the initial capacity when possible.
    :return: `c_float_int_dict_success` on success, or `c_float_int_dict_generic_error` on error
    """
    capacity: int32 = xs_array_get_size(dct)
    for i in i32range(1, capacity, 2):
        xs_array_set_int(dct, i, c_float_int_dict_empty_key_bits)
    xs_array_set_int(dct, 0, 0)
    if capacity > c_float_int_dict_initial_capacity:
        r: int32 = xs_array_resize_int(dct, c_float_int_dict_initial_capacity)
        if r != 1:
            return c_float_int_dict_generic_error
    return c_float_int_dict_success


def xs_float_int_dict_copy(dct: int32 = int32(-1)) -> int32:
    """
    Creates a shallow copy of the dict.
    :return: new dict id, or `c_float_int_dict_resize_failed_error` on error
    """
    capacity: int32 = xs_array_get_size(dct)
    new_dct: int32 = xs_array_create_int(capacity, c_float_int_dict_empty_key_bits)
    if new_dct < 0:
        return c_float_int_dict_resize_failed_error
    for i in i32range(1, capacity, 2):
        stored_key_bits: int32 = xs_array_get_int(dct, i)
        if stored_key_bits != c_float_int_dict_empty_key_bits:
            xs_array_set_int(new_dct, i, stored_key_bits)
            xs_array_set_int(new_dct, i + 1, xs_array_get_int(dct, i + 1))
    xs_array_set_int(new_dct, 0, xs_array_get_int(dct, 0))
    return new_dct


def xs_float_int_dict_to_string(dct: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the dict.
    :return: string representation of the dict
    """
    capacity: int32 = xs_array_get_size(dct)
    s: str = "{"
    first: bool = True
    for i in i32range(1, capacity, 2):
        key_bits: int32 = xs_array_get_int(dct, i)
        if key_bits != c_float_int_dict_empty_key_bits:
            if first:
                first = False
            else:
                s += ", "
            s += f"{bit_cast_to_float(key_bits)}: {xs_array_get_int(dct, i + 1)}"
    s += "}"
    return s


def xs_float_int_dict_last_error() -> int32:
    """
    Returns the status of the last operation that reports errors through the dict API.
    :return: `c_float_int_dict_success` if the last such operation succeeded, or a negative error code
    """
    return _float_int_dict_last_operation_status


def _xs_float_int_dict_find_next_occupied(dct: int32 = int32(-1), start: int32 = int32(1),
                                          capacity: int32 = int32(0)) -> float32:
    global _float_int_dict_last_operation_status
    slot: int32 = start
    while slot < capacity:
        stored_key_bits: int32 = xs_array_get_int(dct, slot)
        if stored_key_bits != c_float_int_dict_empty_key_bits:
            _float_int_dict_last_operation_status = c_float_int_dict_success
            return bit_cast_to_float(stored_key_bits)
        slot += 2
    _float_int_dict_last_operation_status = c_float_int_dict_no_key_error
    return c_float_int_dict_generic_error_float


def xs_float_int_dict_next_key(dct: int32 = int32(-1), is_first: bool = True,
                               prev_key: float32 = c_float_int_dict_empty_key) -> float32:
    """
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    :param is_first: if true, returns the first key in the dict
    :param prev_key: the previous key returned by this function (ignored if `is_first` is true)
    :return: next key, or `c_float_int_dict_generic_error_float` if no more keys
        (last error set to `c_float_int_dict_no_key_error`)
    """
    global _float_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    if is_first:
        return _xs_float_int_dict_find_next_occupied(dct, int32(1), capacity)
    slot: int32 = _xs_float_int_dict_find_slot(dct, prev_key, capacity)
    if slot < 0:
        _float_int_dict_last_operation_status = c_float_int_dict_no_key_error
        return c_float_int_dict_generic_error_float
    next_start: int32 = slot + 2
    return _xs_float_int_dict_find_next_occupied(dct, next_start, capacity)


def xs_float_int_dict_has_next(dct: int32 = int32(-1), is_first: bool = True,
                               prev_key: float32 = c_float_int_dict_empty_key) -> bool:
    """
    Checks whether there is a next key in the dict for stateless iteration.
    :param is_first: if true, checks whether the dict has any keys
    :param prev_key: the previous key (ignored if `is_first` is true)
    :return: true if there is a next key, false otherwise
    """
    capacity: int32 = xs_array_get_size(dct)
    start: int32 = int32(1)
    if not is_first:
        slot: int32 = _xs_float_int_dict_find_slot(dct, prev_key, capacity)
        if slot < 0:
            return False
        start = slot + 2
    while start < capacity:
        if xs_array_get_int(dct, start) != c_float_int_dict_empty_key_bits:
            return True
        start += 2
    return False


def xs_float_int_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
    """
    Updates `source` with all entries from `dct`. Existing keys in `source` are overwritten.
    :return: `c_float_int_dict_success` on success, or a negative error code
    """
    global _float_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    for i in i32range(1, capacity, 2):
        key_bits: int32 = xs_array_get_int(dct, i)
        if key_bits != c_float_int_dict_empty_key_bits:
            xs_float_int_dict_put(source, bit_cast_to_float(key_bits), xs_array_get_int(dct, i + 1))
            if _float_int_dict_last_operation_status != c_float_int_dict_success and _float_int_dict_last_operation_status != c_float_int_dict_no_key_error:
                return _float_int_dict_last_operation_status
    _float_int_dict_last_operation_status = c_float_int_dict_success
    return c_float_int_dict_success


def xs_float_int_dict_put_if_absent(dct: int32 = int32(-1), key: float32 = float32(0.0),
                                    val: int32 = int32(0)) -> int32:
    """
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `c_float_int_dict_empty_key`, the call is a no-op and returns
    `c_float_int_dict_generic_error` with last error set to `c_float_int_dict_generic_error`.
    :return: existing value if the key was already present, or `c_float_int_dict_generic_error`
        if newly inserted or on error. Because -1 is both the error sentinel and a valid stored
        value, callers must check `xs_float_int_dict_last_error()` to distinguish the cases.
    """
    global _float_int_dict_last_operation_status
    if key == c_float_int_dict_empty_key:
        _float_int_dict_last_operation_status = c_float_int_dict_generic_error
        return c_float_int_dict_generic_error
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_float_int_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _float_int_dict_last_operation_status = c_float_int_dict_success
        return xs_array_get_int(dct, slot + 1)

    r: int32 = _xs_float_int_dict_rehash_if_needed(dct, size, capacity, size + 1)
    if r != c_float_int_dict_success:
        return c_float_int_dict_generic_error

    capacity = xs_array_get_size(dct)
    result: int32 = _xs_float_int_dict_upsert(dct, key, val, capacity)
    if _float_int_dict_last_operation_status == c_float_int_dict_no_key_error:
        xs_array_set_int(dct, 0, size + 1)
        return c_float_int_dict_generic_error
    if _float_int_dict_last_operation_status != c_float_int_dict_success:
        return c_float_int_dict_generic_error
    return result


def xs_float_int_dict_keys(dct: int32 = int32(-1)) -> int32:
    """
    Returns a float array containing all keys in iteration order.
    Keys are returned in canonicalized form, so `-0.0` becomes `0.0` and NaN keys use the canonical NaN payload.
    :return: array id, or `c_float_int_dict_resize_failed_error` on allocation failure
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = xs_array_create_float(size, float32(0.0))
    if arr < 0:
        return c_float_int_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(1, capacity, 2):
        stored_key_bits: int32 = xs_array_get_int(dct, i)
        if stored_key_bits != c_float_int_dict_empty_key_bits:
            xs_array_set_float(arr, idx, bit_cast_to_float(stored_key_bits))
            idx += 1
    return arr


def xs_float_int_dict_values(dct: int32 = int32(-1)) -> int32:
    """
    Returns an int array containing all values in the same order as `xs_float_int_dict_keys`.
    :return: array id, or `c_float_int_dict_resize_failed_error` on allocation failure
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = xs_array_create_int(size, 0)
    if arr < 0:
        return c_float_int_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(1, capacity, 2):
        stored_key_bits: int32 = xs_array_get_int(dct, i)
        if stored_key_bits != c_float_int_dict_empty_key_bits:
            xs_array_set_int(arr, idx, xs_array_get_int(dct, i + 1))
            idx += 1
    return arr


def xs_float_int_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
    """
    Checks whether both dicts contain the same keys and values.
    Float keys are compared using the dict's canonical key semantics for signed zero and NaN.
    :return: true if both dicts are equal, false otherwise
    """
    size_a: int32 = xs_array_get_int(a, 0)
    size_b: int32 = xs_array_get_int(b, 0)
    if size_a != size_b:
        return False
    capacity: int32 = xs_array_get_size(a)
    for i in i32range(1, capacity, 2):
        key_bits: int32 = xs_array_get_int(a, i)
        if key_bits != c_float_int_dict_empty_key_bits:
            val: int32 = xs_array_get_int(a, i + 1)
            if xs_float_int_dict_get(b, bit_cast_to_float(key_bits)) != val:
                return False
            if xs_float_int_dict_last_error() != c_float_int_dict_success:
                return False
    return True
