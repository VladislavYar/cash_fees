from django.core.cache import cache

from src.utils.caching import clean_cache_by_tag, clean_group_cache_by_tags


def test_clean_cache_by_tag() -> None:
    """Тест очистки кэша по тегу."""
    cache.set('test_1', 'test')
    clean_cache_by_tag('test_')
    assert cache.get('test_1') is None


def test_clean_group_cache_by_tags() -> None:
    """Тест очистки кэша по тегам."""
    tags_cache = ('test_1_', 'test_2_')
    cache.set(f'{tags_cache[0]}1', 'test')
    cache.set(f'{tags_cache[1]}2', 'test')
    clean_group_cache_by_tags(tags_cache)
    assert (cache.get(f'{tags_cache[0]}1') is None and
            cache.get(f'{tags_cache[1]}2') is None)
