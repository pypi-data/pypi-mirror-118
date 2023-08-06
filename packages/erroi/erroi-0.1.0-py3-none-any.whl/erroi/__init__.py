from errant.edit import Edit
from typing import List
from SoundsLike.SoundsLike import Search


class Erroi:
    def __init__(self, only_errant_categories=True):
        self.only_errant_categories = only_errant_categories

    @staticmethod
    def are_homophones(word_a, word_b):
        try:
            if word_a in Search.perfectHomophones(word_b):
                return True
        # not all lookups are supported by the search
        except ValueError:
            return False

        return False

    def __call__(self, edits: List[Edit]) -> List[Edit]:

        for edit in edits:
            if edit.type == "R:OTHER":
                orig = edit.o_str
                cor = edit.c_str
                if self.are_homophones(orig, cor):
                    if self.only_errant_categories:
                        edit.type = "R:SPELL"
                    else:
                        edit.type = "R:HOMOPHONE"
        return edits
