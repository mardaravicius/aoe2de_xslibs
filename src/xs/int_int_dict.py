from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size
from xs_converter.symbols import XsExternConst

c_int_int_dict_success = 0
c_int_int_dict_generic_error = -1
c_int_int_dict_no_key = -2
c_int_int_dict_resize_failed_error = -3
c_int_int_dict_max_capacity_error = -4
c_int_int_dict_max_capacity = 999999999
c_int_int_dict_max_load_factor = 0.75
c_int_int_dict_empty_param = -999999999
c_int_int_dict_initial_num_of_buckets = 17
c_int_int_dict_initial_bucket_size = 3
c_int_int_dict_min_bucket_size = 3
_c_int_int_dict_last_operation_status = c_int_int_dict_success
_c_int_int_dict_key_exists = False
_int_int_dict_temp_array = -1


def constants() -> None:
    c_int_int_dict_success: XsExternConst[int] = 0
    c_int_int_dict_generic_error: XsExternConst[int] = -1
    c_int_int_dict_no_key: XsExternConst[int] = -2
    c_int_int_dict_resize_failed_error: XsExternConst[int] = -3
    c_int_int_dict_max_capacity_error: XsExternConst[int] = -4
    c_int_int_dict_max_capacity: XsExternConst[int] = 999999999
    c_int_int_dict_max_load_factor: XsExternConst[float] = 0.75
    c_int_int_dict_empty_param: XsExternConst[int] = -999999999
    c_int_int_dict_initial_num_of_buckets: XsExternConst[int] = 17
    c_int_int_dict_initial_bucket_size: XsExternConst[int] = 3
    c_int_int_dict_min_bucket_size: XsExternConst[int] = 3
    _c_int_int_dict_last_operation_status: int = c_int_int_dict_success
    _c_int_int_dict_key_exists: bool = False
    _int_int_dict_temp_array: int = -1


def xs_int_int_dict_create() -> int:
    dct: int = xs_array_create_int(c_int_int_dict_initial_num_of_buckets, c_int_int_dict_empty_param)
    xs_array_set_int(dct, 0, 0)
    return dct


def _xs_int_int_dict_hash(key: int = -1, num_of_buckets: int = 0) -> int:
    hash: int = key * 16777619
    hash = hash % num_of_buckets
    if hash < 0:
        hash = hash + num_of_buckets
    return hash + 1


def _xs_int_int_dict_replace(dct: int = -1, key: int = -1, val: int = 0, num_of_buckets: int = 0) -> int:
    global _c_int_int_dict_last_operation_status
    hash: int = _xs_int_int_dict_hash(key, num_of_buckets)
    bucket: int = xs_array_get_int(dct, hash)
    if bucket < 0:
        bucket = xs_array_create_int(c_int_int_dict_initial_bucket_size, c_int_int_dict_empty_param)
        if bucket < 0:
            _c_int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        xs_array_set_int(bucket, 1, key)
        xs_array_set_int(bucket, 2, val)
        xs_array_set_int(bucket, 0, 2)
        xs_array_set_int(dct, hash, bucket)
        _c_int_int_dict_last_operation_status = c_int_int_dict_no_key
        return c_int_int_dict_generic_error
    bucket_size: int = xs_array_get_int(bucket, 0)
    j: int = 1
    found: bool = False
    found_value: int = c_int_int_dict_generic_error
    while j <= bucket_size and not found:
        stored_key: int = xs_array_get_int(bucket, j)
        if stored_key == key:
            found_value = xs_array_get_int(bucket, j + 1)
            xs_array_set_int(bucket, j + 1, val)
            found = True
        j += 2
    if not found:
        bucket_capacity: int = xs_array_get_size(bucket)
        if (bucket_capacity - 1 - bucket_size) < 2:
            new_bucket_capacity: int = (bucket_capacity - 1) * 2 + 1
            if new_bucket_capacity > c_int_int_dict_max_capacity:
                _c_int_int_dict_last_operation_status = c_int_int_dict_max_capacity_error
                return c_int_int_dict_generic_error
            r: int = xs_array_resize_int(bucket, new_bucket_capacity)
            if r != 1:
                _c_int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
                return c_int_int_dict_generic_error
        xs_array_set_int(bucket, bucket_size + 1, key)
        xs_array_set_int(bucket, bucket_size + 2, val)
        xs_array_set_int(bucket, 0, bucket_size + 2)
        _c_int_int_dict_last_operation_status = c_int_int_dict_no_key
    else:
        _c_int_int_dict_last_operation_status = c_int_int_dict_success
    return found_value


def _xs_int_int_dict_move_to_temp_array(dct: int = -1, total_size: int = 0, dict_capacity: int = 0) -> int:
    global _int_int_dict_temp_array
    temp_data_size: int = total_size * 2
    if _int_int_dict_temp_array < 0:
        _int_int_dict_temp_array = xs_array_create_int(temp_data_size, c_int_int_dict_empty_param)
        if _int_int_dict_temp_array < 0:
            return c_int_int_dict_resize_failed_error
    else:
        temp_arr_capacity: int = xs_array_get_size(_int_int_dict_temp_array)
        if temp_arr_capacity < temp_data_size:
            if temp_data_size > c_int_int_dict_max_capacity:
                return c_int_int_dict_max_capacity_error
            r: int = xs_array_resize_int(_int_int_dict_temp_array, temp_data_size)
            if r != 1:
                return c_int_int_dict_resize_failed_error
    t: int = 0
    for i in range(1, dict_capacity):
        bucket: int = xs_array_get_int(dct, i)
        if bucket >= 0:
            bucket_size: int = xs_array_get_int(bucket, 0)
            for j in range(1, bucket_size + 1, 2):
                stored_key: int = xs_array_get_int(bucket, j)
                stored_val: int = xs_array_get_int(bucket, j + 1)
                xs_array_set_int(_int_int_dict_temp_array, t, stored_key)
                xs_array_set_int(_int_int_dict_temp_array, t + 1, stored_val)
                t += 2
            xs_array_set_int(bucket, 0, 0)
    return temp_data_size


def xs_int_int_dict_put(dct: int = -1, key: int = -1, val: int = 0) -> int:
    global _int_int_dict_temp_array, _c_int_int_dict_last_operation_status
    total_size: int = xs_array_get_int(dct, 0)
    dict_capacity: int = xs_array_get_size(dct)

    previous_value: int = _xs_int_int_dict_replace(dct, key, val, dict_capacity - 1)
    if _c_int_int_dict_last_operation_status == c_int_int_dict_no_key:
        total_size += 1
        xs_array_set_int(dct, 0, total_size)
    elif _c_int_int_dict_last_operation_status == c_int_int_dict_success:
        return previous_value
    else:
        return c_int_int_dict_generic_error

    load_factor: float = total_size / (dict_capacity - 1)
    if load_factor > c_int_int_dict_max_load_factor:
        store_status: int = _c_int_int_dict_last_operation_status
        temp_data_size: int = _xs_int_int_dict_move_to_temp_array(dct, total_size, dict_capacity)
        if temp_data_size < 0:
            _c_int_int_dict_last_operation_status = temp_data_size
            return c_int_int_dict_generic_error
        new_dict_capacity: int = (dict_capacity - 1) * 2 + 1
        if new_dict_capacity > c_int_int_dict_max_capacity:
            _c_int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        r: int = xs_array_resize_int(dct, new_dict_capacity)
        if r != 1:
            _c_int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        for b in range(dict_capacity, new_dict_capacity):
            xs_array_set_int(dct, b, c_int_int_dict_empty_param)
        dict_capacity = new_dict_capacity
        for t in range(0, temp_data_size, 2):
            _xs_int_int_dict_replace(dct, xs_array_get_int(_int_int_dict_temp_array, t),
                                     xs_array_get_int(_int_int_dict_temp_array, t + 1), dict_capacity - 1)
            if _c_int_int_dict_last_operation_status < 0 and _c_int_int_dict_last_operation_status != c_int_int_dict_no_key:
                return c_int_int_dict_generic_error
        _c_int_int_dict_last_operation_status = store_status
    return c_int_int_dict_generic_error


def xs_int_int_dict(
        k1: int = c_int_int_dict_empty_param,
        v1: int = 0,
        k2: int = c_int_int_dict_empty_param,
        v2: int = 0,
        k3: int = c_int_int_dict_empty_param,
        v3: int = 0,
        k4: int = c_int_int_dict_empty_param,
        v4: int = 0,
        k5: int = c_int_int_dict_empty_param,
        v5: int = 0,
        k6: int = c_int_int_dict_empty_param,
        v6: int = 0,
) -> int:
    dct: int = xs_int_int_dict_create()
    if dct < 0:
        return c_int_int_dict_generic_error
    if k1 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k1, v1)
    if k2 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k2, v2)
    if k3 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k3, v3)
    if k4 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k4, v4)
    if k5 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k5, v5)
    if k6 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k6, v6)
    return dct


def xs_int_int_dict_remove(dct: int = -1, key: int = -1) -> int:
    global _c_int_int_dict_last_operation_status, _int_int_dict_temp_array
    total_size: int = xs_array_get_int(dct, 0)
    dict_capacity: int = xs_array_get_size(dct)
    hash: int = _xs_int_int_dict_hash(key, dict_capacity - 1)
    bucket: int = xs_array_get_int(dct, hash)
    if bucket < 0:
        _c_int_int_dict_last_operation_status = c_int_int_dict_no_key
        return c_int_int_dict_generic_error
    found: bool = False
    found_value: int = c_int_int_dict_generic_error
    bucket_size: int = xs_array_get_int(bucket, 0)
    for j in range(1, bucket_size + 1, 2):
        stored_key: int = xs_array_get_int(bucket, j)
        if found:
            xs_array_set_int(bucket, j - 2, stored_key)
            xs_array_set_int(bucket, j - 1, xs_array_get_int(bucket, j + 1))
        elif stored_key == key:
            found = True
            found_value = xs_array_get_int(bucket, j + 1)
            xs_array_set_int(bucket, 0, bucket_size - 2)
            xs_array_set_int(dct, 0, total_size - 1)
    bucket_capacity: int = xs_array_get_size(bucket)
    if found:
        size_threshold: int = (bucket_capacity - 1) // 2
        if size_threshold >= (bucket_size - 2) and bucket_capacity > c_int_int_dict_min_bucket_size:
            r: int = xs_array_resize_int(bucket, size_threshold + 1)
            if r != 0:
                _c_int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
                return c_int_int_dict_generic_error
        _c_int_int_dict_last_operation_status = c_int_int_dict_success
    else:
        _c_int_int_dict_last_operation_status = c_int_int_dict_no_key
    return found_value


def xs_int_int_dict_get(dct: int = -1, key: int = -1, dft: int = -1) -> int:
    global _c_int_int_dict_last_operation_status
    dict_capacity: int = xs_array_get_size(dct)
    hash: int = _xs_int_int_dict_hash(key, dict_capacity - 1)
    bucket: int = xs_array_get_int(dct, hash)
    if bucket < 0:
        _c_int_int_dict_last_operation_status = c_int_int_dict_no_key
        return dft
    bucket_size: int = xs_array_get_int(bucket, 0)
    for j in range(1, bucket_size + 1, 2):
        stored_key: int = xs_array_get_int(bucket, j)
        if key == stored_key:
            _c_int_int_dict_last_operation_status = c_int_int_dict_success
            return xs_array_get_int(bucket, j + 1)
    _c_int_int_dict_last_operation_status = c_int_int_dict_no_key
    return dft


def xs_int_int_dict_contains(dct: int = -1, key: int = -1) -> bool:
    dict_capacity: int = xs_array_get_size(dct)
    hash: int = _xs_int_int_dict_hash(key, dict_capacity - 1)
    bucket: int = xs_array_get_int(dct, hash)
    if bucket < 0:
        return False
    bucket_size: int = xs_array_get_int(bucket, 0)
    for j in range(1, bucket_size + 1, 2):
        stored_key: int = xs_array_get_int(bucket, j)
        if key == stored_key:
            return True
    return False


def xs_int_int_dict_size(dct: int = -1) -> int:
    return xs_array_get_int(dct, 0)


def xs_int_int_dict_clear(dct: int = -1) -> int:
    dict_capacity: int = xs_array_get_size(dct)
    for i in range(1, dict_capacity):
        bucket: int = xs_array_get_int(dct, i)
        if bucket >= 0:
            xs_array_set_int(bucket, 0, 0)
            bucket_capacity: int = xs_array_get_size(bucket)
            if bucket_capacity > c_int_int_dict_min_bucket_size:
                r1: int = xs_array_resize_int(bucket, c_int_int_dict_min_bucket_size)
                if r1 != 1:
                    return c_int_int_dict_generic_error
    xs_array_set_int(dct, 0, 0)
    if dict_capacity > c_int_int_dict_initial_num_of_buckets:
        r2: int = xs_array_resize_int(dct, c_int_int_dict_initial_num_of_buckets)
        if r2 != 1:
            return c_int_int_dict_generic_error
    return c_int_int_dict_success


def xs_int_int_dict_to_string(dct: int = -1) -> str:
    dict_size: int = xs_array_get_size(dct)
    s: str = "{"
    first: bool = True
    for i in range(1, dict_size):
        bucket: int = xs_array_get_int(dct, i)
        if bucket >= 0:
            bucket_size: int = xs_array_get_int(bucket, 0)
            for j in range(1, bucket_size + 1, 2):
                key: int = xs_array_get_int(bucket, j)
                val: int = xs_array_get_int(bucket, j + 1)
                if first:
                    first = False
                else:
                    s += ", "
                s += f"{key}: {val}"
    s += "}"
    return s


def xs_int_int_dict_last_error() -> int:
    return _c_int_int_dict_last_operation_status


def test() -> None:
    pass


def int_int_dict(include_test: bool) -> (str, str):
    test()
    constants_function_xs = PythonToXsConverter.to_xs_script(
        constants,
        indent=True,
    )
    constants_xs = (constants_function_xs[constants_function_xs.find("extern"):constants_function_xs.rfind("}")]
                    .strip()
                    .replace("    ", "")
                    ) + "\n\n"
    xs = constants_xs + PythonToXsConverter.to_xs_script(
        _xs_int_int_dict_hash,
        _xs_int_int_dict_replace,
        _xs_int_int_dict_move_to_temp_array,
        xs_int_int_dict_put,
        xs_int_int_dict_create,
        xs_int_int_dict,
        xs_int_int_dict_get,
        xs_int_int_dict_remove,
        xs_int_int_dict_contains,
        xs_int_int_dict_size,
        xs_int_int_dict_clear,
        xs_int_int_dict_to_string,
        xs_int_int_dict_last_error,
        indent=True,
    )
    if include_test:
        xs += constants_xs + PythonToXsConverter.to_xs_script(
            test,
            indent=True,
        )
    print(xs)
    return (xs, "intIntDict")


if __name__ == '__main__':
    int_int_dict(True)
