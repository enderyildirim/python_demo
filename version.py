import re
from functools import total_ordering


@total_ordering
class Version:

    def __init__(self, major=None, minor=None, micro=None, *,
                 max_major=9, max_minor=99, max_micro=999,
                 min_major=0, min_minor=0, min_micro=0,
                 major_inc=1, minor_inc=1, micro_inc=1,
                 major_dec=1, minor_dec=1, micro_dec=1):
        if major is None:
            major = min_major
        if minor is None:
            minor = min_minor
        if micro is None:
            micro = min_micro

        assert major >= 0
        assert minor >= 0
        assert micro >= 0
        assert max_major >= 0
        assert max_minor >= 0
        assert max_micro >= 0
        assert max_major > min_major
        assert max_minor > min_minor
        assert max_micro > min_micro
        assert min_major >= 0
        assert min_minor >= 0
        assert min_micro >= 0
        assert major_inc > 0
        assert minor_inc > 0
        assert micro_inc > 0
        assert major_dec > 0
        assert minor_dec > 0
        assert micro_dec > 0
        assert max_major >= major_dec
        assert max_minor >= minor_dec
        assert max_micro >= micro_dec
        assert max_major > min_major
        assert max_minor > min_minor
        assert max_micro > min_micro

        self.max_major = max_major
        self.max_minor = max_minor
        self.max_micro = max_micro
        self.min_major = min_major
        self.min_minor = min_minor
        self.min_micro = min_micro
        self.check_limits(major, minor, micro)
        self.major = major
        self.minor = minor
        self.micro = micro
        self.major_inc = major_inc
        self.minor_inc = minor_inc
        self.micro_inc = micro_inc
        self.major_dec = major_dec
        self.minor_dec = minor_dec
        self.micro_dec = micro_dec

    def create(self, major, minor, micro):
        return Version(major, minor, micro,
                       max_major=self.max_major, max_minor=self.max_minor, max_micro=self.max_micro,
                       min_major=self.min_major, min_minor=self.min_minor, min_micro=self.min_micro,
                       major_inc=self.major_inc, minor_inc=self.minor_inc, micro_inc=self.micro_inc,
                       major_dec=self.major_dec, minor_dec=self.minor_dec, micro_dec=self.micro_dec)

    def next(self):
        if self.major == self.max_major and self.minor == self.max_minor and self.micro == self.max_micro:
            raise VersionError("Version reached to maximum : {}".format(self))

        if self.micro == self.max_micro or self.micro + self.micro_inc > self.max_micro:
            if self.minor == self.max_minor or self.minor + self.micro_inc > self.max_minor:
                if self.major == self.max_major or self.major + self.major_inc > self.max_major:
                    raise VersionError("Version reached to maximum : {}".format(self))
                else:
                    return self.create(self.major + self.major_inc, 0, 0)
            else:
                return self.create(self.major, self.minor + self.micro_inc, 0)
        else:
            return self.create(self.major, self.minor, self.micro + self.micro_inc)

    def pre(self):
        if self.major == self.min_major and self.minor == self.min_minor and self.micro == self.min_micro:
            raise VersionError("Version reached to minimum : {}".format(self))

        if self.micro == self.min_micro or self.micro - self.micro_dec < self.min_micro:
            if self.minor == self.min_minor or self.minor - self.minor_dec < self.min_minor:
                if self.major == self.min_major or self.major - self.major_dec < self.min_major:
                    raise VersionError("Version reached to minimum : {}".format(self))
                else:
                    return self.create(self.major - self.major_dec,
                                       self.max_minor - (self.minor_dec - 1),
                                       self.max_micro)
            else:
                return self.create(self.major,
                                   self.minor - self.minor_dec,
                                   self.max_micro - (self.micro_dec - 1))
        else:
            return self.create(self.major,
                               self.minor,
                               self.micro - self.micro_dec)

    def minimum(self):
        return self.create(self.min_major, self.min_minor, self.min_micro)

    def maximum(self):
        return self.create(self.max_major, self.max_minor, self.max_micro)

    def parse(self, version):
        match = re.search(self.pattern(), version)
        if match:
            return self.create(int(match.group(1)) or 0, int(match.group(2)) or 0, int(match.group(3)) or 0)
        raise VersionError("Value must be in format {} : {}".format(self.pattern(), version))

    def check_limits(self, major, minor, micro):
        if self.min_major > major or major > self.max_major:
            raise VersionError("Major must be between {} <= major <= {} : {}"
                               .format(self.min_major, self.max_major, major))
        elif self.min_minor > minor or minor > self.max_minor:
            raise VersionError("Minor must be between {} <= minor <= {} : {}"
                               .format(self.min_minor, self.max_minor, minor))
        elif self.min_micro > micro or micro > self.max_micro:
            raise VersionError("Micro must be between {} <= micro <= {} : {}"
                               .format(self.min_micro, self.max_micro, micro))

    def is_valid(self, major, minor, micro):
        return self.min_major <= major <= self.max_major \
               and self.min_minor <= minor <= self.max_minor \
               and self.min_micro <= micro <= self.max_micro

    @staticmethod
    def pattern():
        return "^(\\d*)\\.(\\d*)\\.(\\d+)$"

    def __lt__(self, other):
        if self.major < other.major:
            return True
        elif self.major > other.major:
            return False
        elif self.minor < other.minor:
            return True
        elif self.minor > other.minor:
            return False
        return self.micro < other.micro

    def __gt__(self, other):
        if self.major > other.major:
            return True
        elif self.major < other.major:
            return False
        elif self.minor > other.minor:
            return True
        elif self.minor < other.minor:
            return False
        return self.micro > other.micro

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Version) \
               and self.major == o.major \
               and self.minor == o.minor \
               and self.micro == o.micro

    def __repr__(self) -> str:
        return "Version({}.{}.{})".format(self.major, self.minor, self.micro)

    def __str__(self) -> str:
        return "{}.{}.{}".format(self.major, self.minor, self.micro)


class VersionError(Exception):
    pass
