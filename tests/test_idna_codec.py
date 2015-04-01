#!/usr/bin/env python

import unittest
import sys

sys.path.append('..')
import idna.codec
import codecs
import six

class IDNACodecTests(unittest.TestCase):

    def testCodec(self):
        pass

    def testIncrementalDecoder(self):

        # Tests derived from Python standard library test/test_codecs.py

        incremental_tests = (
            (six.u("python.org"), b"python.org"),
            (six.u("python.org."), b"python.org."),
            (six.u("pyth\xf6n.org"), b"xn--pythn-mua.org"),
            (six.u("pyth\xf6n.org."), b"xn--pythn-mua.org."),
        )

        for decoded, encoded in incremental_tests:
            if sys.version_info.major == 2:
                self.assertEqual("".join(codecs.iterdecode(encoded, "idna")),
                                decoded)
            else:
                self.assertEqual("".join(codecs.iterdecode((bytes([c]) for c in encoded), "idna")),
                                decoded)

        decoder = codecs.getincrementaldecoder("idna")()
        self.assertEqual(decoder.decode(b"xn--xam", ), six.u(""))
        self.assertEqual(decoder.decode(b"ple-9ta.o", ), six.u("\xe4xample."))
        self.assertEqual(decoder.decode(b"rg"), six.u(""))
        self.assertEqual(decoder.decode(b"", True), six.u("org"))

        decoder.reset()
        self.assertEqual(decoder.decode(b"xn--xam", ), six.u(""))
        self.assertEqual(decoder.decode(b"ple-9ta.o", ), six.u("\xe4xample."))
        self.assertEqual(decoder.decode(b"rg."), six.u("org."))
        self.assertEqual(decoder.decode(b"", True), six.u(""))


    def testIncrementalEncoder(self):

        # Tests derived from Python standard library test/test_codecs.py

        incremental_tests = (
            (six.u("python.org"), b"python.org"),
            (six.u("python.org."), b"python.org."),
            (six.u("pyth\xf6n.org"), b"xn--pythn-mua.org"),
            (six.u("pyth\xf6n.org."), b"xn--pythn-mua.org."),
        )
        for decoded, encoded in incremental_tests:
            self.assertEqual(b"".join(codecs.iterencode(decoded, "idna")),
                             encoded)

        encoder = codecs.getincrementalencoder("idna")()
        self.assertEqual(encoder.encode(six.u("\xe4x")), b"")
        self.assertEqual(encoder.encode(six.u("ample.org")), b"xn--xample-9ta.")
        self.assertEqual(encoder.encode(six.u(""), True), b"org")

        encoder.reset()
        self.assertEqual(encoder.encode(six.u("\xe4x")), b"")
        self.assertEqual(encoder.encode(six.u("ample.org.")), b"xn--xample-9ta.org.")
        self.assertEqual(encoder.encode(six.u(""), True), b"")

if __name__ == '__main__':
    unittest.main()
