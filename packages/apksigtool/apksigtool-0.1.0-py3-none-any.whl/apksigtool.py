#!/usr/bin/python3
# encoding: utf-8
# SPDX-FileCopyrightText: 2021 Felix C. Stegerman <flx@obfusk.net>
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
FIXME: docstrings
"""

import binascii
import hashlib
import os
import struct
import sys

from collections import namedtuple

import asn1crypto.keys
import asn1crypto.x509
import click

from apksigcopier import extract_v2_sig, zip_data
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

__version__ = "0.1.0"
NAME = "apksigtool"

# FIXME: incomplete
APK_SIGNATURE_SCHEME_V2_BLOCK_ID = 0x7109871a
APK_SIGNATURE_SCHEME_V3_BLOCK_ID = 0xf05368c0
VERITY_PADDING_BLOCK_ID = 0x42726577
DEPENDENCY_INFO_BLOCK_ID = 0x504b4453
GOOGLE_PLAY_FROSTING_BLOCK_ID = 0x2146444e

# FIXME: unused
STRIPPING_PROTECTION_ATTR_ID = 0xbeeff00d
PROOF_OF_ROTATION_STRUCT_ID = 0x3ba06f8c

# FIXME: incomplete
SIGNATURE_ALGORITHM_IDS = {
    0x0101: "RSASSA-PSS with SHA2-256 digest, SHA2-256 MGF1, 32 bytes of salt, trailer: 0xbc, content digested using SHA2-256 in 1 MB chunks.",
    0x0102: "RSASSA-PSS with SHA2-512 digest, SHA2-512 MGF1, 64 bytes of salt, trailer: 0xbc, content digested using SHA2-512 in 1 MB chunks.",
    0x0103: "RSASSA-PKCS1-v1_5 with SHA2-256 digest, content digested using SHA2-256 in 1 MB chunks.",  # This is for build systems which require deterministic signatures.
    0x0104: "RSASSA-PKCS1-v1_5 with SHA2-512 digest, content digested using SHA2-512 in 1 MB chunks.",  # This is for build systems which require deterministic signatures.
    0x0201: "ECDSA with SHA2-256 digest, content digested using SHA2-256 in 1 MB chunks.",
    0x0202: "ECDSA with SHA2-512 digest, content digested using SHA2-512 in 1 MB chunks.",
    0x0301: "DSA with SHA2-256 digest, content digested using SHA2-256 in 1 MB chunks.",
#   0x0301: "DSA with SHA2-256 digest, content digested using SHA2-256 in 1 MB chunks. Signing is done deterministically according to RFC 6979.",   # noqa: E122
    0x0421: "RSASSA-PKCS1-v1_5 with SHA2-256 digest, content digested using SHA2-256 in 4 KB chunks, in the same way fsverity operates. This digest and the content length (before digestion, 8 bytes in little endian) construct the final digest.",
    0x0423: "ECDSA with SHA2-256 digest, content digested using SHA2-256 in 4 KB chunks, in the same way fsverity operates. This digest and the content length (before digestion, 8 bytes in little endian) construct the final digest.",
    0x0425: "DSA with SHA2-256 digest, content digested using SHA2-256 in 4 KB chunks, in the same way fsverity operates. This digest and the content length (before digestion, 8 bytes in little endian) construct the final digest.",
}

CHUNKED, VERITY = 1, 2

# FIXME: incomplete
HASHERS = {
    0x0103: (hashlib.sha256, hashes.SHA256, padding.PKCS1v15, CHUNKED),
    0x0104: (hashlib.sha512, hashes.SHA512, padding.PKCS1v15, CHUNKED),
    0x0421: (hashlib.sha256, hashes.SHA256, padding.PKCS1v15, VERITY),
}

CHUNK_SIZE = 1048576
VERITY_BLOCK_SIZE = 4096

# FIXME
VERITY_SALT = b"\x00" * 8


class VerificationError(Exception):
    pass


def _namedtuple(name, fields):
    nt = namedtuple(name, fields)
    nt.for_json = lambda self: {**self._asdict(), **dict(_type=name)}
    return nt


APKSigningBlock = _namedtuple("APKSigningBlock", ("pairs",))
Pair = _namedtuple("Pair", ("length", "id", "value"))

APKSignatureSchemeBlock = _namedtuple("APKSignatureSchemeBlock",
                                      ("version", "signers", "verified"))
VerityPaddingBlock = _namedtuple("VerityPaddingBlock", ())
DependencyInfoBlock = _namedtuple("DependencyInfoBlock", ("data",))
GooglePlayFrostingBlock = _namedtuple("GooglePlayFrostingBlock", ("data",))
UnknownBlock = _namedtuple("UnknownBlock", ("data",))

V2Signer = _namedtuple("V2Signer", ("signed_data", "signatures", "public_key"))
V3Signer = _namedtuple("V3Signer", ("signed_data", "min_sdk", "max_sdk", "signatures",
                                    "public_key"))

V2SignedData = _namedtuple("V2SignedData", ("raw", "digests", "certificates",
                                            "additional_attributes"))
V3SignedData = _namedtuple("V3SignedData", ("raw", "digests", "certificates", "min_sdk",
                                            "max_sdk", "additional_attributes"))

Digest = _namedtuple("Digest", ("signature_algorithm_id", "digest"))
Certificate = _namedtuple("Certificate", ("data",))
AdditionalAttribute = _namedtuple("AdditionalAttribute", ("id", "value"))
Signature = _namedtuple("Signature", ("signature_algorithm_id", "signature"))
PublicKey = _namedtuple("PublicKey", ("data",))


APKSignatureSchemeBlock.is_v2 = lambda self: self.version == 2
APKSignatureSchemeBlock.is_v3 = lambda self: self.version == 3

AdditionalAttribute.is_stripping_protection = lambda self: \
    self.id == STRIPPING_PROTECTION_ATTR_ID
AdditionalAttribute.is_proof_of_rotation_struct = lambda self: \
    self.id == PROOF_OF_ROTATION_STRUCT_ID


def parse_apk_signing_block(data, apkfile=None):
    return APKSigningBlock(tuple(_parse_apk_signing_block(data, apkfile)))


def _parse_apk_signing_block(data, apkfile=None):
    magic = data[-16:]
    sb_size1 = int.from_bytes(data[:8], "little")
    sb_size2 = int.from_bytes(data[-24:-16], "little")
    assert magic == b"APK Sig Block 42"
    assert sb_size1 == sb_size2 == len(data) - 8
    data = data[8:-24]
    while data:
        pair_len, pair_id = struct.unpack("<QL", data[:12])
        pair_val, data = data[12:8 + pair_len], data[8 + pair_len:]
        if pair_id == APK_SIGNATURE_SCHEME_V2_BLOCK_ID:
            value = parse_apk_signature_scheme_v2_block(pair_val, apkfile)
        elif pair_id == APK_SIGNATURE_SCHEME_V3_BLOCK_ID:
            value = parse_apk_signature_scheme_v3_block(pair_val, apkfile)
        elif pair_id == VERITY_PADDING_BLOCK_ID:
            assert all(b == 0 for b in pair_val)
            value = VerityPaddingBlock()
        elif pair_id == DEPENDENCY_INFO_BLOCK_ID:
            value = DependencyInfoBlock(pair_val)
        elif pair_id == GOOGLE_PLAY_FROSTING_BLOCK_ID:
            value = GooglePlayFrostingBlock(pair_val)
        else:
            value = UnknownBlock(pair_val)
        yield Pair(pair_len, pair_id, value)


def parse_apk_signature_scheme_v2_block(data, apkfile=None):
    signers = tuple(_parse_apk_signature_scheme_block(data, False))
    verified = None
    if apkfile is not None:
        try:
            verify_apk_signature_scheme_v2(signers, apkfile)
        except VerificationError:
            verified = False
        else:
            verified = True
    return APKSignatureSchemeBlock(2, signers, verified)


def parse_apk_signature_scheme_v3_block(data, apkfile=None):
    signers = tuple(_parse_apk_signature_scheme_block(data, True))
    verified = None
    if apkfile is not None:
        try:
            verify_apk_signature_scheme_v3(signers, apkfile)
        except VerificationError:
            verified = False
        else:
            verified = True
    return APKSignatureSchemeBlock(3, signers, verified)


def _parse_apk_signature_scheme_block(data, v3):
    seq_len, data = int.from_bytes(data[:4], "little"), data[4:]
    assert seq_len == len(data)
    while data:
        signer, data = _len_prefixed_field(data)
        yield parse_signer(signer, v3)


def parse_signer(data, v3):
    result = []
    sigdata, data = _len_prefixed_field(data)
    result.append(parse_signed_data(sigdata, v3))
    if v3:
        minSDK, maxSDK = struct.unpack("<LL", data[:8])
        data = data[8:]
        result.append(minSDK)
        result.append(maxSDK)
    sigs, data = _len_prefixed_field(data)
    result.append(parse_signatures(sigs))
    pubkey, data = _len_prefixed_field(data)
    result.append(PublicKey(pubkey))
    assert all(b == 0 for b in data)
    return (V3Signer if v3 else V2Signer)(*result)


def parse_signed_data(data, v3):
    result = [data]
    digests, data = _len_prefixed_field(data)
    result.append(parse_digests(digests))
    certs, data = _len_prefixed_field(data)
    result.append(parse_certificates(certs))
    if v3:
        minSDK, maxSDK = struct.unpack("<LL", data[:8])
        data = data[8:]
        result.append(minSDK)
        result.append(maxSDK)
    attrs, data = _len_prefixed_field(data)
    result.append(parse_additional_attributes(attrs))
    assert all(b == 0 for b in data)
    return (V3SignedData if v3 else V2SignedData)(*result)


def parse_digests(data):
    return tuple(_parse_digests(data))


def _parse_digests(data):
    while data:
        digest, data = _len_prefixed_field(data)
        sig_algo_id = int.from_bytes(digest[:4], "little")
        assert int.from_bytes(digest[4:8], "little") == len(digest) - 8
        yield Digest(sig_algo_id, digest[8:])


def parse_certificates(data):
    return tuple(_parse_certificates(data))


def _parse_certificates(data):
    while data:
        cert, data = _len_prefixed_field(data)
        yield Certificate(cert)


def parse_additional_attributes(data):
    return tuple(_parse_additional_attributes(data))


def _parse_additional_attributes(data):
    while data:
        attr, data = _len_prefixed_field(data)
        attr_id = int.from_bytes(attr[:4], "little")
        yield AdditionalAttribute(attr_id, attr[4:])


def parse_signatures(data):
    return tuple(_parse_signatures(data))


def _parse_signatures(data):
    while data:
        sig, data = _len_prefixed_field(data)
        sig_algo_id = int.from_bytes(sig[:4], "little")
        assert int.from_bytes(sig[4:8], "little") == len(sig) - 8
        yield Signature(sig_algo_id, sig[8:])


def _len_prefixed_field(data):
    assert len(data) >= 4
    field_len = int.from_bytes(data[:4], "little")
    assert len(data) >= 4 + field_len
    return data[4:4 + field_len], data[4 + field_len:]


# FIXME
# https://source.android.com/security/apksigning/v2#v2-verification
def verify_apk_signature_scheme_v2(signers, apkfile):
    sb_offset, _ = extract_v2_sig(apkfile)
    if not signers:
        raise VerificationError("No signers")
    for signer in signers:
        if not signer.signed_data.certificates:
            raise VerificationError("No certificates")
        if not signer.signed_data.digests:
            raise VerificationError("No digests")
        if not signer.signatures:
            raise VerificationError("No signatures")
        c0 = signer.signed_data.certificates[0].data
        pk = signer.public_key.data
        da = sorted(d.signature_algorithm_id for d in signer.signed_data.digests)
        sa = sorted(s.signature_algorithm_id for s in signer.signatures)
        if asn1crypto.x509.Certificate.load(c0).public_key.dump() != pk:
            raise VerificationError("Public key does not match first certificate")
        if da != sa:
            raise VerificationError("Signature algorithm IDs of digests and signatures "
                                    "are not identical")
        for dig in signer.signed_data.digests:
            h, _, _, t = HASHERS[dig.signature_algorithm_id]
            digest = _apk_digest(apkfile, sb_offset, h, t)
            if digest != dig.digest:
                raise VerificationError("Digest mismatch: expected {}, got {}"
                                        .format(dig.digest, digest))
        for sig in signer.signatures:
            _, a, p, _ = HASHERS[sig.signature_algorithm_id]
            verify_signature(pk, sig.signature, signer.signed_data.raw, a, p)


# FIXME
def verify_apk_signature_scheme_v3(signers, apkfile):
    verify_apk_signature_scheme_v2(signers, apkfile)


def _apk_digest(apkfile, sb_offset, hasher, chunk_type):
    if chunk_type == CHUNKED:
        return apk_digest_chunked(apkfile, sb_offset, hasher)
    elif chunk_type == VERITY:
        return apk_digest_verity(apkfile, sb_offset, hasher)
    else:
        raise ValueError("Unknown chunk type: {}".format(chunk_type))


def apk_digest_chunked(apkfile, sb_offset, hasher):
    def f(size):
        while size > 0:
            data = fh.read(min(size, CHUNK_SIZE))
            if not data:
                break
            size -= len(data)
            digests.append(_chunk_digest(data, hasher))
    digests = []
    cd_offset, eocd_offset, _ = zip_data(apkfile)
    with open(apkfile, "rb") as fh:
        f(sb_offset)
        fh.seek(cd_offset)
        f(eocd_offset - cd_offset)
        fh.seek(eocd_offset)
        data = fh.read()
        data = data[:16] + int.to_bytes(sb_offset, 4, "little") + data[20:]
        digests.extend(_chunk_digest(c, hasher) for c in _chunks(data, CHUNK_SIZE))
    return _top_level_chunked_digest(digests, hasher)


def apk_digest_verity(apkfile, sb_offset, hasher):
    assert sb_offset % VERITY_BLOCK_SIZE == 0
    digests = []
    cd_offset, eocd_offset, cd_and_eocd = zip_data(apkfile)
    with open(apkfile, "rb") as fh:
        size = sb_offset
        while size > 0:
            data = fh.read(min(size, VERITY_BLOCK_SIZE))
            if not data:
                break
            size -= len(data)
            digests.append(_verity_block_digest(data, hasher))
        fh.seek(0, os.SEEK_END)
        total_size = fh.tell() - (cd_offset - sb_offset)
    off = eocd_offset - cd_offset
    sbo = int.to_bytes(sb_offset, 4, "little")
    data = _verity_pad(cd_and_eocd[:off + 16] + sbo + cd_and_eocd[off + 20:])
    digests.extend(_verity_block_digest(c, hasher) for c in _chunks(data, VERITY_BLOCK_SIZE))
    return _top_level_verity_digest(digests, total_size, hasher)


def _chunk_digest(chunk, hasher):
    data = b"\xa5" + int.to_bytes(len(chunk), 4, "little") + chunk
    return hasher(data).digest()


def _top_level_chunked_digest(digests, hasher):
    digests = tuple(digests)
    data = b"\x5a" + int.to_bytes(len(digests), 4, "little") + b"".join(digests)
    return hasher(data).digest()


def _verity_block_digest(block, hasher):
    assert len(block) == VERITY_BLOCK_SIZE
    return hasher(VERITY_SALT + block).digest()


def _top_level_verity_digest(digests, total_size, hasher):
    data = _verity_pad(b"".join(digests))
    while len(data) > VERITY_BLOCK_SIZE:
        data = _verity_pad(b"".join(_verity_block_digest(c, hasher)
                                    for c in _chunks(data, VERITY_BLOCK_SIZE)))
    return hasher(VERITY_SALT + data).digest() + int.to_bytes(total_size, 8, "little")


def _verity_pad(data):
    if len(data) % VERITY_BLOCK_SIZE != 0:
        data += b"\x00" * (VERITY_BLOCK_SIZE - (len(data) % VERITY_BLOCK_SIZE))
    return data


def _chunks(msg, blocksize):
    while msg:
        chunk, msg = msg[:blocksize], msg[blocksize:]
        yield chunk


def verify_signature(key, sig, msg, algo, pad):
    k = serialization.load_der_public_key(key)
    try:
        k.verify(sig, msg, pad(), algo())
    except InvalidSignature:
        raise VerificationError("Invalid signature")


# FIXME: show more? s/Common Name:/CN=/ etc?
def show_x509_certificate(value, indent):
    cert = asn1crypto.x509.Certificate.load(value)
    fpr = cert.sha256_fingerprint.replace(" ", "").lower()
    print(" " * indent + "X.509 SUBJECT:", cert.subject.human_friendly)
    print(" " * indent + "X.509 SHA256 FINGERPRINT (HEX):", fpr)
    _show_public_key(cert.public_key, indent)


def show_public_key(value, indent):
    _show_public_key(asn1crypto.keys.PublicKeyInfo.load(value), indent)


def _show_public_key(key, indent):
    fpr = hashlib.sha256(key.dump()).hexdigest()
    print(" " * indent + "PUBLIC KEY ALGORITHM:", key.algorithm.upper())
    print(" " * indent + "PUBLIC KEY BIT SIZE:", key.bit_size)
    print(" " * indent + "PUBLIC KEY SHA256 FINGERPRINT (HEX):", fpr)


def _show_hex(data, indent):
    print(" " * indent + "VALUE (HEX):", binascii.hexlify(data).decode())


def _show_aid(x, indent):
    aid = x.signature_algorithm_id
    aid_s = SIGNATURE_ALGORITHM_IDS.get(aid, "UNKNOWN").split(",")[0]
    print(" " * indent + "SIGNATURE ALGORITHM ID: {} ({})".format(hex(aid), aid_s))


# FIXME
@click.group(help="""
    apksigtool - ...
""")
@click.version_option(__version__)
def cli():
    pass


# FIXME
@cli.command(help="""
    ...
""")
@click.option("--json", is_flag=True)
@click.option("-v", "--verbose", is_flag=True)
@click.argument("apk", type=click.Path(exists=True, dir_okay=False))
def parse(apk, json, verbose):
    _, sig_block = extract_v2_sig(apk)
    if json:
        def encode_bytes(obj):
            if isinstance(obj, bytes):
                return binascii.hexlify(obj).decode()
            raise TypeError(repr(obj) + " is not JSON serializable")
        import simplejson
        data = parse_apk_signing_block(sig_block, apk)
        simplejson.dump(data, sys.stdout, indent=2, sort_keys=True, encoding=None,
                        default=encode_bytes, for_json=True)
        print()
    else:
        for pair in parse_apk_signing_block(sig_block).pairs:
            b = pair.value
            if verbose:
                print("PAIR LENGTH:", pair.length)
            print("PAIR ID:", hex(pair.id))
            if isinstance(b, APKSignatureSchemeBlock):
                print("  APK SIGNATURE SCHEME v{} BLOCK".format(b.version))
                for i, signer in enumerate(b.signers):
                    print("  SIGNER", i)
                    print("    SIGNED DATA")
                    for j, digest in enumerate(signer.signed_data.digests):
                        print("      DIGEST", j)
                        _show_aid(digest, 8)
                        _show_hex(digest.digest, 8)
                    for j, cert in enumerate(signer.signed_data.certificates):
                        print("      CERTIFICATE", j)
                        show_x509_certificate(cert.data, 8)
                    if b.is_v3():
                        print("      MIN SDK:", signer.signed_data.min_sdk)
                        print("      MAX SDK:", signer.signed_data.max_sdk)
                    for j, attr in enumerate(signer.signed_data.additional_attributes):
                        print("      ADDITIONAL ATTRIBUTE", j)
                        print("        ADDITIONAL ATTRIBUTE ID:", hex(attr.id))
                        if attr.is_stripping_protection():
                            print("        STRIPPING PROTECTION ATTR")
                        elif attr.is_proof_of_rotation_struct():
                            print("        PROOF OF ROTATION STRUCT")
                        _show_hex(attr.value, 8)
                    if b.is_v3():
                        print("    MIN SDK:", signer.min_sdk)
                        print("    MAX SDK:", signer.max_sdk)
                    for j, sig in enumerate(signer.signatures):
                        print("    SIGNATURE", j)
                        _show_aid(sig, 6)
                        _show_hex(sig.signature, 6)
                    print("    PUBLIC KEY")
                    show_public_key(signer.public_key.data, 6)
                try:
                    if b.is_v2():
                        verify_apk_signature_scheme_v2(b.signers, apk)
                    else:
                        verify_apk_signature_scheme_v3(b.signers, apk)
                except VerificationError as e:
                    print("  NOT VERIFIED ({})".format(e))
                else:
                    print("  VERIFIED")
            elif isinstance(b, VerityPaddingBlock):
                print("  VERITY PADDING BLOCK")
            elif isinstance(b, DependencyInfoBlock):
                print("  DEPENDENCY INFO BLOCK")
            elif isinstance(b, GooglePlayFrostingBlock):
                print("  GOOGLE PLAY FROSTING BLOCK")
            else:
                print("  UNKNOWN BLOCK")
            if verbose and hasattr(b, "data"):
                _show_hex(b.data, 2)


# FIXME
@cli.command(help="""
    ...
""")
@click.argument("apk", type=click.Path(exists=True, dir_okay=False))
def verify(apk):
    print("WARNING: THIS IS A PROTOTYPE; DO NOT USE IN PRODUCTION!", file=sys.stderr)
    verified, failed = 0, 0
    _, sig_block = extract_v2_sig(apk)
    for pair in parse_apk_signing_block(sig_block).pairs:
        b = pair.value
        if isinstance(b, APKSignatureSchemeBlock):
            try:
                if b.is_v2():
                    verify_apk_signature_scheme_v2(b.signers, apk)
                else:
                    verify_apk_signature_scheme_v3(b.signers, apk)
            except VerificationError as e:
                failed += 1
                print("v{} not verified ({})".format(b.version, e))
            else:
                verified += 1
                print("v{} verified".format(b.version))
    if failed or not verified:
        sys.exit(1)


# FIXME
# @cli.command(help="""
#     ...
# """)
# @click.argument("apk", type=click.Path(exists=True, dir_okay=False))
# def sign(apk):
#     ...


def main():
    cli(prog_name=NAME)


if __name__ == "__main__":
    main()

# vim: set tw=80 sw=4 sts=4 et fdm=marker :
