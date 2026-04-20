from numpy import int32, float32

from xs_converter.functions import (
    bit_cast_to_float,
    bit_cast_to_int,
    vector,
    xs_array_create_float,
    xs_array_create_int,
    xs_array_create_vector,
    xs_array_get_float,
    xs_array_get_size,
    xs_array_resize_float,
    xs_array_set_float,
    xs_array_set_vector,
    xs_vector_get_x,
    xs_vector_get_y,
    xs_vector_get_z,
    xs_vector_set,
)
from xs_converter.symbols import XsExternConst, XsVector, i32range

c_float_vector_dict_success: XsExternConst[int32] = int32(0)
c_float_vector_dict_generic_error: XsExternConst[int32] = int32(-1)
c_float_vector_dict_no_key_error: XsExternConst[int32] = int32(-2)
c_float_vector_dict_resize_failed_error: XsExternConst[int32] = int32(-3)
c_float_vector_dict_max_capacity_error: XsExternConst[int32] = int32(-4)
c_float_vector_dict_generic_error_vector: XsExternConst[XsVector] = vector(-1.0, -1.0, -1.0)
c_float_vector_dict_max_capacity: XsExternConst[int32] = int32(999999997)
c_float_vector_dict_max_load_factor: XsExternConst[float32] = float32(0.75)
c_float_vector_dict_empty_key: XsExternConst[float32] = float32(-9999999.0)
c_float_vector_dict_empty_key_bits: XsExternConst[int32] = int32(-887581057)
c_float_vector_dict_canonical_nan_bits: XsExternConst[int32] = int32(-8388607)
c_float_vector_dict_initial_capacity: XsExternConst[int32] = int32(65)
c_float_vector_dict_hash_constant: XsExternConst[int32] = int32(16777619)
_float_vector_dict_last_operation_status: int32 = c_float_vector_dict_success
_float_vector_dict_temp_array: int32 = int32(-1)


def _xs_float_vector_dict_key_bits(key: float32 = float32(0.0)) -> int32:
    if key != key:
        return c_float_vector_dict_canonical_nan_bits
    if key == float32(0.0):
        return int32(0)
    return bit_cast_to_int(key)


def _xs_float_vector_dict_canonical_key(key: float32 = float32(0.0)) -> float32:
    return bit_cast_to_float(_xs_float_vector_dict_key_bits(key))


def _xs_float_vector_dict_set_size(dct: int32 = int32(-1), size: int32 = int32(0)) -> None:
    xs_array_set_float(dct, 0, bit_cast_to_float(size))


def _xs_float_vector_dict_get_size(dct: int32 = int32(-1)) -> int32:
    return bit_cast_to_int(xs_array_get_float(dct, 0))


def _xs_float_vector_dict_get_stored_key(dct: int32 = int32(-1), slot: int32 = int32(1)) -> float32:
    return xs_array_get_float(dct, slot)


def _xs_float_vector_dict_clear_slot(dct: int32 = int32(-1), slot: int32 = int32(1)) -> None:
    xs_array_set_float(dct, slot, c_float_vector_dict_empty_key)


def _xs_float_vector_dict_set_stored_value(dct: int32 = int32(-1), slot: int32 = int32(1),
                                           value: XsVector = vector(0.0, 0.0, 0.0)) -> None:
    xs_array_set_float(dct, slot + 1, xs_vector_get_x(value))
    xs_array_set_float(dct, slot + 2, xs_vector_get_y(value))
    xs_array_set_float(dct, slot + 3, xs_vector_get_z(value))


def _xs_float_vector_dict_get_stored_value(dct: int32 = int32(-1), slot: int32 = int32(1)) -> XsVector:
    return xs_vector_set(
        xs_array_get_float(dct, slot + 1),
        xs_array_get_float(dct, slot + 2),
        xs_array_get_float(dct, slot + 3),
    )


def _xs_float_vector_dict_set_slot(dct: int32 = int32(-1), slot: int32 = int32(1),
                                   key: float32 = float32(0.0),
                                   value: XsVector = vector(0.0, 0.0, 0.0)) -> None:
    xs_array_set_float(dct, slot, _xs_float_vector_dict_canonical_key(key))
    _xs_float_vector_dict_set_stored_value(dct, slot, value)


def xs_float_vector_dict_create() -> int32:
    """
    Creates an empty float-to-vector dictionary.
    Keys equal to `c_float_vector_dict_empty_key` are reserved as the internal empty-slot sentinel
    and cannot be stored. `put` and `put_if_absent` silently reject them. Signed zero keys are
    canonicalized to `0.0`, and all NaN keys are canonicalized to a single NaN bit pattern.
    :return: created dict id, or `c_float_vector_dict_generic_error` on error
    """
    dct: int32 = xs_array_create_float(c_float_vector_dict_initial_capacity, c_float_vector_dict_empty_key)
    if dct < 0:
        return c_float_vector_dict_generic_error
    _xs_float_vector_dict_set_size(dct, int32(0))
    return dct


def _xs_float_vector_dict_hash(key: float32 = float32(0.0), capacity: int32 = int32(0)) -> int32:
    h: int32 = _xs_float_vector_dict_key_bits(key) * c_float_vector_dict_hash_constant
    num_slots: int32 = (capacity - 1) // 4
    h = h % num_slots
    if h < 0:
        h += num_slots
    return (h * 4) + 1


def _xs_float_vector_dict_find_slot(dct: int32 = int32(-1), key: float32 = float32(0.0),
                                    capacity: int32 = int32(0)) -> int32:
    num_slots: int32 = (capacity - 1) // 4
    key_bits: int32 = _xs_float_vector_dict_key_bits(key)
    home: int32 = _xs_float_vector_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: float32 = _xs_float_vector_dict_get_stored_key(dct, slot)
        if stored_key == c_float_vector_dict_empty_key:
            return int32(-1)
        if _xs_float_vector_dict_key_bits(stored_key) == key_bits:
            return slot
        slot += 4
        if slot >= capacity:
            slot = int32(1)
        steps += 1
    return int32(-1)


def _xs_float_vector_dict_upsert(dct: int32 = int32(-1), key: float32 = float32(0.0),
                                 val: XsVector = vector(0.0, 0.0, 0.0), capacity: int32 = int32(0)) -> XsVector:
    global _float_vector_dict_last_operation_status
    key_bits: int32 = _xs_float_vector_dict_key_bits(key)
    num_slots: int32 = (capacity - 1) // 4
    home: int32 = _xs_float_vector_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: float32 = _xs_float_vector_dict_get_stored_key(dct, slot)
        if stored_key == c_float_vector_dict_empty_key:
            _xs_float_vector_dict_set_slot(dct, slot, key, val)
            _float_vector_dict_last_operation_status = c_float_vector_dict_no_key_error
            return c_float_vector_dict_generic_error_vector
        if _xs_float_vector_dict_key_bits(stored_key) == key_bits:
            old_val: XsVector = _xs_float_vector_dict_get_stored_value(dct, slot)
            _xs_float_vector_dict_set_stored_value(dct, slot, val)
            _float_vector_dict_last_operation_status = c_float_vector_dict_success
            return old_val
        slot += 4
        if slot >= capacity:
            slot = int32(1)
        steps += 1
    _float_vector_dict_last_operation_status = c_float_vector_dict_max_capacity_error
    return c_float_vector_dict_generic_error_vector


def _xs_float_vector_dict_move_to_temp_array(dct: int32 = int32(-1), size: int32 = int32(0),
                                             capacity: int32 = int32(0)) -> int32:
    global _float_vector_dict_temp_array
    temp_data_size: int32 = size * 4
    if _float_vector_dict_temp_array < 0:
        _float_vector_dict_temp_array = xs_array_create_float(temp_data_size, c_float_vector_dict_empty_key)
        if _float_vector_dict_temp_array < 0:
            return c_float_vector_dict_resize_failed_error
    else:
        temp_arr_capacity: int32 = xs_array_get_size(_float_vector_dict_temp_array)
        if temp_arr_capacity < temp_data_size:
            if temp_data_size > c_float_vector_dict_max_capacity:
                return c_float_vector_dict_max_capacity_error
            r: int32 = xs_array_resize_float(_float_vector_dict_temp_array, temp_data_size)
            if r != 1:
                return c_float_vector_dict_resize_failed_error
    t: int32 = int32(0)
    for i in i32range(1, capacity, 4):
        stored_key: float32 = _xs_float_vector_dict_get_stored_key(dct, i)
        if stored_key != c_float_vector_dict_empty_key:
            xs_array_set_float(_float_vector_dict_temp_array, t, xs_array_get_float(dct, i))
            xs_array_set_float(_float_vector_dict_temp_array, t + 1, xs_array_get_float(dct, i + 1))
            xs_array_set_float(_float_vector_dict_temp_array, t + 2, xs_array_get_float(dct, i + 2))
            xs_array_set_float(_float_vector_dict_temp_array, t + 3, xs_array_get_float(dct, i + 3))
            t += 4
    return temp_data_size


def _xs_float_vector_dict_clear_slots(dct: int32 = int32(-1), capacity: int32 = int32(-1)) -> None:
    for j in i32range(1, capacity, 4):
        _xs_float_vector_dict_clear_slot(dct, j)


def _xs_float_vector_dict_rehash_if_needed(dct: int32 = int32(-1), size: int32 = int32(0),
                                           capacity: int32 = int32(0),
                                           required_size: int32 = int32(-1)) -> int32:
    global _float_vector_dict_last_operation_status
    if required_size < 0:
        required_size = size
    load_factor: float = float(required_size) / ((capacity - 1) // 4)
    if load_factor > c_float_vector_dict_max_load_factor:
        store_status: int32 = _float_vector_dict_last_operation_status
        new_capacity: int32 = (capacity - 1) * 2 + 1
        if new_capacity > c_float_vector_dict_max_capacity:
            _float_vector_dict_last_operation_status = c_float_vector_dict_max_capacity_error
            return c_float_vector_dict_generic_error
        temp_data_size: int32 = _xs_float_vector_dict_move_to_temp_array(dct, size, capacity)
        if temp_data_size < 0:
            _float_vector_dict_last_operation_status = temp_data_size
            return c_float_vector_dict_generic_error
        r: int32 = xs_array_resize_float(dct, new_capacity)
        if r != 1:
            _float_vector_dict_last_operation_status = c_float_vector_dict_resize_failed_error
            return c_float_vector_dict_generic_error
        _xs_float_vector_dict_clear_slots(dct, new_capacity)
        for t in i32range(0, temp_data_size, 4):
            _xs_float_vector_dict_upsert(
                dct,
                xs_array_get_float(_float_vector_dict_temp_array, t),
                xs_vector_set(
                    xs_array_get_float(_float_vector_dict_temp_array, t + 1),
                    xs_array_get_float(_float_vector_dict_temp_array, t + 2),
                    xs_array_get_float(_float_vector_dict_temp_array, t + 3),
                ),
                new_capacity,
            )
            if _float_vector_dict_last_operation_status < 0 and _float_vector_dict_last_operation_status != c_float_vector_dict_no_key_error:
                return c_float_vector_dict_generic_error
        _float_vector_dict_last_operation_status = store_status
    return c_float_vector_dict_success


def xs_float_vector_dict_put(dct: int32 = int32(-1), key: float32 = float32(0.0),
                             val: XsVector = vector(0.0, 0.0, 0.0)) -> XsVector:
    """
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    If `key` equals `c_float_vector_dict_empty_key`, the call is a no-op and returns
    `c_float_vector_dict_generic_error_vector` with last error set to `c_float_vector_dict_generic_error`.
    """
    global _float_vector_dict_last_operation_status
    if key == c_float_vector_dict_empty_key:
        _float_vector_dict_last_operation_status = c_float_vector_dict_generic_error
        return c_float_vector_dict_generic_error_vector
    size: int32 = _xs_float_vector_dict_get_size(dct)
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_float_vector_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        old_val: XsVector = _xs_float_vector_dict_get_stored_value(dct, slot)
        _xs_float_vector_dict_set_stored_value(dct, slot, val)
        _float_vector_dict_last_operation_status = c_float_vector_dict_success
        return old_val

    r: int32 = _xs_float_vector_dict_rehash_if_needed(dct, size, capacity, size + 1)
    if r != c_float_vector_dict_success:
        return c_float_vector_dict_generic_error_vector

    capacity = xs_array_get_size(dct)
    previous_value: XsVector = _xs_float_vector_dict_upsert(dct, key, val, capacity)
    if _float_vector_dict_last_operation_status == c_float_vector_dict_no_key_error:
        _xs_float_vector_dict_set_size(dct, size + 1)
        return c_float_vector_dict_generic_error_vector
    if _float_vector_dict_last_operation_status != c_float_vector_dict_success:
        return c_float_vector_dict_generic_error_vector
    return previous_value


def xs_float_vector_dict(
        k1: float32 = c_float_vector_dict_empty_key,
        v1: XsVector = vector(0.0, 0.0, 0.0),
        k2: float32 = c_float_vector_dict_empty_key,
        v2: XsVector = vector(0.0, 0.0, 0.0),
        k3: float32 = c_float_vector_dict_empty_key,
        v3: XsVector = vector(0.0, 0.0, 0.0),
        k4: float32 = c_float_vector_dict_empty_key,
        v4: XsVector = vector(0.0, 0.0, 0.0),
        k5: float32 = c_float_vector_dict_empty_key,
        v5: XsVector = vector(0.0, 0.0, 0.0),
        k6: float32 = c_float_vector_dict_empty_key,
        v6: XsVector = vector(0.0, 0.0, 0.0),
) -> int32:
    """
    Creates a dict with provided key-value pairs. The first key that equals
    `c_float_vector_dict_empty_key` will stop further insertion.
    """
    dct: int32 = xs_float_vector_dict_create()
    if dct < 0:
        return c_float_vector_dict_generic_error
    if k1 == c_float_vector_dict_empty_key:
        return dct
    xs_float_vector_dict_put(dct, k1, v1)
    if k2 == c_float_vector_dict_empty_key:
        return dct
    xs_float_vector_dict_put(dct, k2, v2)
    if k3 == c_float_vector_dict_empty_key:
        return dct
    xs_float_vector_dict_put(dct, k3, v3)
    if k4 == c_float_vector_dict_empty_key:
        return dct
    xs_float_vector_dict_put(dct, k4, v4)
    if k5 == c_float_vector_dict_empty_key:
        return dct
    xs_float_vector_dict_put(dct, k5, v5)
    if k6 == c_float_vector_dict_empty_key:
        return dct
    xs_float_vector_dict_put(dct, k6, v6)
    return dct


def xs_float_vector_dict_get(dct: int32 = int32(-1), key: float32 = float32(0.0),
                             dft: XsVector = c_float_vector_dict_generic_error_vector) -> XsVector:
    """
    Returns the value associated with the given key. Sets last error on completion.
    :return: value for the key, or `dft` if not found
    """
    global _float_vector_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_float_vector_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _float_vector_dict_last_operation_status = c_float_vector_dict_success
        return _xs_float_vector_dict_get_stored_value(dct, slot)
    _float_vector_dict_last_operation_status = c_float_vector_dict_no_key_error
    return dft


def xs_float_vector_dict_remove(dct: int32 = int32(-1), key: float32 = float32(0.0)) -> XsVector:
    """
    Removes the entry with the given key from the dict. Uses backward shift deletion to
    maintain linear probing invariant. Sets last error on completion.
    :return: value that was associated with the key, or `c_float_vector_dict_generic_error_vector` if not found
    """
    global _float_vector_dict_last_operation_status
    size: int32 = _xs_float_vector_dict_get_size(dct)
    capacity: int32 = xs_array_get_size(dct)
    num_slots: int32 = (capacity - 1) // 4
    slot: int32 = _xs_float_vector_dict_find_slot(dct, key, capacity)
    if slot < 0:
        _float_vector_dict_last_operation_status = c_float_vector_dict_no_key_error
        return c_float_vector_dict_generic_error_vector
    found_val: XsVector = _xs_float_vector_dict_get_stored_value(dct, slot)

    g: int32 = slot
    q: int32 = g + 4
    if q >= capacity:
        q = int32(1)
    shift_steps: int32 = int32(0)
    q_key: float32 = _xs_float_vector_dict_get_stored_key(dct, q)
    while q_key != c_float_vector_dict_empty_key and shift_steps < num_slots:
        q_home: int32 = _xs_float_vector_dict_hash(q_key, capacity)
        g_slot: int32 = (g - 1) // 4
        q_slot: int32 = (q - 1) // 4
        h_slot: int32 = (q_home - 1) // 4
        dist_g: int32 = (g_slot - h_slot + num_slots) % num_slots
        dist_q: int32 = (q_slot - h_slot + num_slots) % num_slots
        if dist_g < dist_q:
            xs_array_set_float(dct, g, xs_array_get_float(dct, q))
            xs_array_set_float(dct, g + 1, xs_array_get_float(dct, q + 1))
            xs_array_set_float(dct, g + 2, xs_array_get_float(dct, q + 2))
            xs_array_set_float(dct, g + 3, xs_array_get_float(dct, q + 3))
            g = q
        q += 4
        if q >= capacity:
            q = int32(1)
        shift_steps += 1
        q_key = _xs_float_vector_dict_get_stored_key(dct, q)
    _xs_float_vector_dict_clear_slot(dct, g)
    _xs_float_vector_dict_set_size(dct, size - 1)
    _float_vector_dict_last_operation_status = c_float_vector_dict_success
    return found_val


def xs_float_vector_dict_contains(dct: int32 = int32(-1), key: float32 = float32(0.0)) -> bool:
    """
    Checks whether the given key exists in the dict.
    :return: true if the key is found, false otherwise
    """
    capacity: int32 = xs_array_get_size(dct)
    return _xs_float_vector_dict_find_slot(dct, key, capacity) >= 0


def xs_float_vector_dict_size(dct: int32 = int32(-1)) -> int32:
    """
    Returns the number of key-value pairs stored in the dict.
    :return: dict size
    """
    return _xs_float_vector_dict_get_size(dct)


def xs_float_vector_dict_clear(dct: int32 = int32(-1)) -> int32:
    """
    Removes all entries from the dict and shrinks storage back to the initial capacity when possible.
    :return: `c_float_vector_dict_success` on success, or `c_float_vector_dict_generic_error` on error
    """
    capacity: int32 = xs_array_get_size(dct)
    for i in i32range(1, capacity, 4):
        _xs_float_vector_dict_clear_slot(dct, i)
    _xs_float_vector_dict_set_size(dct, int32(0))
    if capacity > c_float_vector_dict_initial_capacity:
        r: int32 = xs_array_resize_float(dct, c_float_vector_dict_initial_capacity)
        if r != 1:
            return c_float_vector_dict_generic_error
    return c_float_vector_dict_success


def xs_float_vector_dict_copy(dct: int32 = int32(-1)) -> int32:
    """
    Creates a shallow copy of the dict.
    :return: new dict id, or `c_float_vector_dict_resize_failed_error` on error
    """
    capacity: int32 = xs_array_get_size(dct)
    new_dct: int32 = xs_array_create_float(capacity, c_float_vector_dict_empty_key)
    if new_dct < 0:
        return c_float_vector_dict_resize_failed_error
    for i in i32range(1, capacity, 4):
        stored_key: float32 = _xs_float_vector_dict_get_stored_key(dct, i)
        if stored_key != c_float_vector_dict_empty_key:
            xs_array_set_float(new_dct, i, xs_array_get_float(dct, i))
            xs_array_set_float(new_dct, i + 1, xs_array_get_float(dct, i + 1))
            xs_array_set_float(new_dct, i + 2, xs_array_get_float(dct, i + 2))
            xs_array_set_float(new_dct, i + 3, xs_array_get_float(dct, i + 3))
    _xs_float_vector_dict_set_size(new_dct, _xs_float_vector_dict_get_size(dct))
    return new_dct


def xs_float_vector_dict_to_string(dct: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the dict.
    :return: string representation of the dict
    """
    capacity: int32 = xs_array_get_size(dct)
    s: str = "{"
    first: bool = True
    for i in i32range(1, capacity, 4):
        key: float32 = _xs_float_vector_dict_get_stored_key(dct, i)
        if key != c_float_vector_dict_empty_key:
            if first:
                first = False
            else:
                s += ", "
            s += f"{key}: {_xs_float_vector_dict_get_stored_value(dct, i)}"
    s += "}"
    return s


def xs_float_vector_dict_last_error() -> int32:
    """
    Returns the status of the last operation that reports errors through the dict API.
    :return: `c_float_vector_dict_success` if the last such operation succeeded, or a negative error code
    """
    return _float_vector_dict_last_operation_status


def _xs_float_vector_dict_find_next_occupied(dct: int32 = int32(-1), start: int32 = int32(1),
                                             capacity: int32 = int32(0)) -> float32:
    global _float_vector_dict_last_operation_status
    slot: int32 = start
    while slot < capacity:
        stored_key: float32 = _xs_float_vector_dict_get_stored_key(dct, slot)
        if stored_key != c_float_vector_dict_empty_key:
            _float_vector_dict_last_operation_status = c_float_vector_dict_success
            return stored_key
        slot += 4
    _float_vector_dict_last_operation_status = c_float_vector_dict_no_key_error
    return c_float_vector_dict_empty_key


def xs_float_vector_dict_next_key(dct: int32 = int32(-1), is_first: bool = True,
                                  prev_key: float32 = c_float_vector_dict_empty_key) -> float32:
    """
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    :param is_first: if true, returns the first key in the dict
    :param prev_key: the previous key returned by this function (ignored if `is_first` is true)
    :return: next key, or `c_float_vector_dict_empty_key` if no more keys
        (last error set to `c_float_vector_dict_no_key_error`)
    """
    global _float_vector_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    if is_first:
        return _xs_float_vector_dict_find_next_occupied(dct, int32(1), capacity)
    slot: int32 = _xs_float_vector_dict_find_slot(dct, prev_key, capacity)
    if slot < 0:
        _float_vector_dict_last_operation_status = c_float_vector_dict_no_key_error
        return c_float_vector_dict_empty_key
    next_start: int32 = slot + 4
    return _xs_float_vector_dict_find_next_occupied(dct, next_start, capacity)


def xs_float_vector_dict_has_next(dct: int32 = int32(-1), is_first: bool = True,
                                  prev_key: float32 = c_float_vector_dict_empty_key) -> bool:
    """
    Checks whether there is a next key in the dict for stateless iteration.
    :param is_first: if true, checks whether the dict has any keys
    :param prev_key: the previous key (ignored if `is_first` is true)
    :return: true if there is a next key, false otherwise
    """
    capacity: int32 = xs_array_get_size(dct)
    start: int32 = int32(1)
    if not is_first:
        slot: int32 = _xs_float_vector_dict_find_slot(dct, prev_key, capacity)
        if slot < 0:
            return False
        start = slot + 4
    while start < capacity:
        if _xs_float_vector_dict_get_stored_key(dct, start) != c_float_vector_dict_empty_key:
            return True
        start += 4
    return False


def xs_float_vector_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
    """
    Updates `source` with all entries from `dct`. Existing keys in `source` are overwritten.
    :return: `c_float_vector_dict_success` on success, or a negative error code
    """
    global _float_vector_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    for i in i32range(1, capacity, 4):
        key: float32 = _xs_float_vector_dict_get_stored_key(dct, i)
        if key != c_float_vector_dict_empty_key:
            xs_float_vector_dict_put(source, key, _xs_float_vector_dict_get_stored_value(dct, i))
            if _float_vector_dict_last_operation_status != c_float_vector_dict_success and _float_vector_dict_last_operation_status != c_float_vector_dict_no_key_error:
                return _float_vector_dict_last_operation_status
    _float_vector_dict_last_operation_status = c_float_vector_dict_success
    return c_float_vector_dict_success


def xs_float_vector_dict_put_if_absent(dct: int32 = int32(-1), key: float32 = float32(0.0),
                                       val: XsVector = vector(0.0, 0.0, 0.0)) -> XsVector:
    """
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `c_float_vector_dict_empty_key`, the call is a no-op and returns
    `c_float_vector_dict_generic_error_vector` with last error set to `c_float_vector_dict_generic_error`.
    """
    global _float_vector_dict_last_operation_status
    if key == c_float_vector_dict_empty_key:
        _float_vector_dict_last_operation_status = c_float_vector_dict_generic_error
        return c_float_vector_dict_generic_error_vector
    size: int32 = _xs_float_vector_dict_get_size(dct)
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_float_vector_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _float_vector_dict_last_operation_status = c_float_vector_dict_success
        return _xs_float_vector_dict_get_stored_value(dct, slot)

    r: int32 = _xs_float_vector_dict_rehash_if_needed(dct, size, capacity, size + 1)
    if r != c_float_vector_dict_success:
        return c_float_vector_dict_generic_error_vector

    capacity = xs_array_get_size(dct)
    result: XsVector = _xs_float_vector_dict_upsert(dct, key, val, capacity)
    if _float_vector_dict_last_operation_status == c_float_vector_dict_no_key_error:
        _xs_float_vector_dict_set_size(dct, size + 1)
        return c_float_vector_dict_generic_error_vector
    if _float_vector_dict_last_operation_status != c_float_vector_dict_success:
        return c_float_vector_dict_generic_error_vector
    return result


def xs_float_vector_dict_keys(dct: int32 = int32(-1)) -> int32:
    """
    Returns a float array containing all keys in iteration order.
    Keys are returned in canonicalized form, so `-0.0` becomes `0.0` and NaN keys use the canonical NaN payload.
    :return: array id, or `c_float_vector_dict_resize_failed_error` on allocation failure
    """
    size: int32 = _xs_float_vector_dict_get_size(dct)
    arr: int32 = xs_array_create_float(size, float32(0.0))
    if arr < 0:
        return c_float_vector_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(1, capacity, 4):
        stored_key: float32 = _xs_float_vector_dict_get_stored_key(dct, i)
        if stored_key != c_float_vector_dict_empty_key:
            xs_array_set_float(arr, idx, stored_key)
            idx += 1
    return arr


def xs_float_vector_dict_values(dct: int32 = int32(-1)) -> int32:
    """
    Returns a vector array containing all values in the same order as `xs_float_vector_dict_keys`.
    :return: array id, or `c_float_vector_dict_resize_failed_error` on allocation failure
    """
    size: int32 = _xs_float_vector_dict_get_size(dct)
    arr: int32 = xs_array_create_vector(size, vector(0.0, 0.0, 0.0))
    if arr < 0:
        return c_float_vector_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(1, capacity, 4):
        stored_key: float32 = _xs_float_vector_dict_get_stored_key(dct, i)
        if stored_key != c_float_vector_dict_empty_key:
            xs_array_set_vector(arr, idx, _xs_float_vector_dict_get_stored_value(dct, i))
            idx += 1
    return arr


def xs_float_vector_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
    """
    Checks whether both dicts contain the same keys and values.
    Float keys are compared using the dict's canonical key semantics for signed zero and NaN.
    :return: true if both dicts are equal, false otherwise
    """
    size_a: int32 = _xs_float_vector_dict_get_size(a)
    size_b: int32 = _xs_float_vector_dict_get_size(b)
    if size_a != size_b:
        return False
    capacity: int32 = xs_array_get_size(a)
    for i in i32range(1, capacity, 4):
        key: float32 = _xs_float_vector_dict_get_stored_key(a, i)
        if key != c_float_vector_dict_empty_key:
            val: XsVector = _xs_float_vector_dict_get_stored_value(a, i)
            if xs_float_vector_dict_get(b, key) != val:
                return False
            if xs_float_vector_dict_last_error() != c_float_vector_dict_success:
                return False
    return True
