from assembler import ASM


def useMBC1(rom):
    rom.patch(0x00, 0x00A0, "00" * 42, ASM("""
        push af
        cp   $20
        jr   c, lowerBanks
        inc  a
        ld   [$2001], a
        ld   a, $01
        ld   [$4001], a
        pop  af
        ret
lowerBanks:
        ld   [$2001], a
        xor  a
        ld   [$4001], a
        pop  af
        ret
    """), fill_nop=True)
    rom.patch(0x00, 0x0030, "00" * 0x10, ASM("""
        jp   $00A0
    """), fill_nop=True)

    for addr in (0x080F, 0x0819, 0x0821, 0x082B, 0x08E2, 0x0919, 0x0939, 0x0974, 0x098D, 0x0A13, 0x0A2E, 0x0A35, 0x0A62, 0x0B1C, 0x0B2B, 0x0B58, 0x0B5D, 0x0B65, 0x0B6A, 0x0B92, 0x0BC8, 0x0BD3, 0x0BDA, 0x0BE3, 0x0BF2, 0x0C2F, 0x0C3C, 0x0C47, 0x0D20, 0x0EEF, 0x0EFE, 0x0F07, 0x1298, 0x1356, 0x137E, 0x1399, 0x14BF, 0x1824, 0x1833, 0x19A6, 0x1A35, 0x1A4C, 0x1E38, 0x1E65, 0x1E6E, 0x1E98, 0x1EAC, 0x1EC4, 0x1EDD, 0x1F43, 0x2050, 0x220B, 0x223E, 0x22BA, 0x22E7, 0x27DF, 0x2A03, 0x2A14, 0x2A32, 0x2A3C, 0x2A6B, 0x2A7F, 0x2A93, 0x2AB3, 0x2AC7, 0x2ADB, 0x2B06, 0x2B17, 0x2B39, 0x2B52, 0x2B63, 0x2B95, 0x2BA6, 0x2C3B, 0x2C79, 0x2C9F, 0x2CB3, 0x2CCE, 0x2CDD, 0x2D5D, 0x2E26, 0x2EF2, 0x2F21, 0x2F77, 0x2F91, 0x2FB2, 0x3058, 0x3084, 0x311B, 0x3126, 0x317E, 0x31B5, 0x3237, 0x3547, 0x3808, 0x38E6, 0x38ED, 0x38F8, 0x3911, 0x3F95, 0x3FAB, 0x3FCB, 0x3FDA, 0x3FEB, 0x1AD6, 0x1B2C, 0x1C0D, 0x1C62, 0x1C6C, 0x1C74, 0x1C7E, 0x1D0F, 0x1D1A, 0x1D2B, 0x1DF5, 0x1E25, 0x2908, 0x2910, 0x24B9, 0x24CF, 0x252B, 0x2573, 0x260D, 0x263E, 0x26C5, 0x3927, 0x3985, 0x39D7, 0x39E8, 0x3A14, 0x3A32, 0x3A59, 0x3A64, 0x3A89, 0x3A8F, 0x3AA6, 0x3B89, 0x3B9B, 0x3CDB, 0x3F55, 0x0414, 0x044F, 0x045A, 0x0566, 0x05B7, 0x05F3, 0x062A, 0x065B, 0x06F7, 0x07EF, 0x027E, 0x02B9): # 0x0764
        # replace ld [MBC], a
        rom.patch(0x00, addr, ASM("ld [$2100], a"), ASM("call $00A0"))
    for addr in (0x3DA0, 0x3DAB, 0x3DB6, 0x3DC1, 0x3DCC, 0x3DD7, 0x3DE2, 0x3DED, 0x3DF8, 0x3E03, 0x3E0E, 0x3E29, 0x3E34, 0x3E6B):
        # replace callhl
        bank = rom.banks[0][addr + 4]
        rom.patch(0x00, addr, ASM("ld hl, $2100\nld [hl], $%02x" % (bank)), ASM("""
            push af
            ld   a, $%02X
            rst  $30
            pop  af
        """ % (bank)))
    for addr in (0x0836, 0x0847, 0x0858, 0x0865, 0x08D7, 0x08E6, 0x08F0, 0x08FB, 0x0905, 0x090F, 0x092F, 0x0979, 0x0983, 0x09C9, 0x09D4, 0x09DF, 0x09EA, 0x09F6, 0x0A48, 0x0A54, 0x0A6C, 0x0A78, 0x0A84, 0x0A90, 0x0AB6, 0x0AC7, 0x0AD3, 0x0AEB, 0x0AF7, 0x0B02, 0x0B41, 0x0F1A, 0x0F6A, 0x0FD0, 0x100A, 0x10CB, 0x1165, 0x128D, 0x134B, 0x1373, 0x138E, 0x14B4, 0x1819, 0x1828, 0x1A22, 0x1A2A, 0x1A39, 0x1A41, 0x20BF, 0x20C7, 0x20EC, 0x2156, 0x2178, 0x2234, 0x2291, 0x22B0, 0x22DD, 0x27F7, 0x2802, 0x29ED, 0x29F8, 0x2A07, 0x2BC2, 0x2E79, 0x3023, 0x30FC, 0x3109, 0x3111, 0x328E, 0x3296, 0x329E, 0x32CD, 0x37FE, 0x38D4, 0x38DC, 0x38FC, 0x1C00, 0x1CFF, 0x1D1E, 0x3942, 0x394D, 0x3965, 0x3970, 0x397B, 0x39CE, 0x3A0A, 0x3B18, 0x3B23, 0x3B2E, 0x3B39, 0x3B44, 0x3B4F, 0x3B5A, 0x3B65, 0x3B70, 0x3B7B, 0x3C69, 0x3D47, 0x0177, 0x018F, 0x019D, 0x01C2, 0x01CF, 0x0409, 0x0431, 0x043D, 0x0445, 0x04DA, 0x0530, 0x054B, 0x055B, 0x0622, 0x06A9, 0x07B0, 0x025C, 0x026E, 0x02AA):
        # replace callsb
        rom.patch(0x00, addr + 2, ASM("ld [$2100], a"), ASM("call $00A0"))
    for addr in (0x2319, 0x30EC, 0x3915, 0x391D, 0x1BC5, 0x236B, 0x23CA, 0x247D, 0x24AF, 0x27AF, 0x27BB):
        # replace jpsb
        rom.patch(0x00, addr + 2, ASM("ld [$2100], a"), ASM("call $00A0"))
    for addr in (0x0C34, 0x3E3F, 0x3E5A, 0x3BAA, 0x3BB5, 0x392F):
        # replace "ld hl, $2000; ld [hl], $XX"
        bank = rom.banks[0][addr + 4]
        rom.patch(0x00, addr, ASM("ld hl, $2100\nld [hl], $%02x" % (bank)), ASM("""
            push af
            ld   a, $%02X
            rst  $30
            pop  af
        """ % (bank)))

    # Do not switch SRAM bank, as this screw up the MBC1 selected ROM bank.
    for addr in (0x27D1,):
        rom.patch(0x00, addr, ASM("ld hl, $4000\nld [hl], $00"), "", fill_nop=True)

    rom.patch(0x00, 0x0147, "1B", "03")
    rom.patch(0x00, 0x0148, "05", "06")
    rom.patch(0x00, 0x0149, "03", "02")

    rom.patch(0x00, 0x1D12, 0x1D18, ASM("push hl\npop de\ncall $00D0"), fill_nop=True)
    rom.patch(0x00, 0x00D0, "00" * 0x20, ASM("""
        ld  hl, $FF51
        ld  [hl], b
        inc hl
        ld  [hl], c
        inc hl
        ld  [hl], d
        inc hl
        ld  [hl], e
        inc hl
        ld  [hl], $01
        ret
    """), fill_nop=True)
