raw_keys = ['0x243F6A88L,', '0x85A308D3L,', '0x13198A2EL,', '0x03707344L,', '0xA4093822L,', '0x299F31D0L,',
            '0x082EFA98L,', '0xEC4E6C89L,', '0x452821E6L,', '0x38D01377L,', '0xBE5466CFL,', '0x34E90C6CL,',
            '0xC0AC29B7L,', '0xC97C50DDL,', '0x3F84D5B5L,', '0xB5470917L,', '0x9216D5D9L,', '0x8979FB1BL,',
            '0x38D01377L,', '0xA4093822L,', '0xEC4E6C89L,', '0x243F6A88L,', '0x13198A2EL,', '0x85A308D3L,',
            '0x082EFA98L,', '0x85A308D3L,', '0xBE5466CFL,', '0x03707344L,', '0x243F6A88L,', '0x452821E6L,',
            '0x85A308D3L,', '0x38D01377L,']


def get_processed_keys():
    return [key[2:-2] for key in raw_keys]
