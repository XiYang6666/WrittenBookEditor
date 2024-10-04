import time


from writtenbookeditor.font import get_char_info, char_info_cache


def test_get_char_info():
    with open("data/test/test_txt_1.txt", "r", encoding="utf-8") as f:
        texts = f.read()

    start_time = time.time()

    for char in texts:
        info = get_char_info(char)
        assert info is not None

    print(f"using time: {time.time()-start_time:.3}s")
    print(f"cache size: {len(char_info_cache)}")
