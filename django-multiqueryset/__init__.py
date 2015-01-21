# -*- coding: utf-8 -*-

# based on https://djangosnippets.org/snippets/1103/
class MultiQuerySet(object):
    def __init__(self, *args, **kwargs):
        self.querysets = args
        self._count = None

    def __len__(self):
        return self.count()

    @staticmethod
    def _len_qs(qs):
        if isinstance(qs, list):
            return len(qs)
        return qs.count() if hasattr(qs, 'count') else len(qs)

    def count(self):
        if not self._count:
            count = 0
            for qs in self.querysets:
                count += self._len_qs(qs)
            self._count = count
        return self._count

    def __add__(self, another):
        mine = list(self.querysets)
        theirs = list(another.querysets)
        mine.extend(theirs)
        return MultiQuerySet(*mine)

    def __getitem__(self, item):
        if isinstance(item, slice):
            indices = (offset, stop, step) = item.indices(self.count())
            items = []
            total_len = stop - offset
            for qs in self.querysets:
                qs_len = self._len_qs(qs)
                if qs_len < offset:
                    offset -= qs_len
                else:
                    items += list(qs[offset:stop])
                    if len(items) >= total_len:
                        return items
                    else:
                        offset = 0
                        stop = total_len - len(items)
                        continue
        elif isinstance(item, int):
            count = 0
            last_count = 0
            qs_count = -1  # so the first iteration is 0
            # TODO: A wee bit of cleaning up might be good
            for qs in self.querysets:
                i = self._len_qs(qs)
                qs_count += 1
                last_count = count
                count += i
                if item >= last_count and item < count:
                    break
            qs = self.querysets[qs_count]
            index = item - last_count
            return qs[index]
        else:
            return NotImplementedError()
