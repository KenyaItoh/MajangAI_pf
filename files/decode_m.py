# 引数: m = 面子のID
# 戻り値:h = 面子の中身
def decode_m(m):
    kui = (m & 3)
    fuuro_label = 0
    # 順子
    if m & (1<<2):
        fuuro_label = 3
        t = (m & 0xFC00) >> 10
        r = t % 3
        t = int(t / 3)
        t = int(t / 7) * 9 + (t % 7)
        t *= 4
        h = [t + 4 * 0 + ((m & 0x0018) >> 3), t + 4 * 1 + ((m & 0x0060) >> 5), t + 4 * 2 + ((m & 0x0180) >> 7)]
        
        # 牌の並び替え
        if r == 1:
            h.insert(0, h[1])
            del(h[2])
        elif r == 2:
            h.insert(2, h[1])
            del(h[1])

    # 刻子
    elif m & (1<<3):
        fuuro_label = 1
        unused = (m & 0x0060) >> 5
        t = (m & 0xFE00) >> 9
        r = t % 3
        t = int(t / 3)
        t  *= 4
        h = [t, t, t]
        if unused == 0:
            h[0]  += 1;h[1]  += 2;h[2]  += 3
        elif unused == 1:
            h[0]  += 0;h[1]  += 2;h[2]  += 3
        elif unused == 2:
            h[0]  += 0;h[1]  += 1;h[2]  += 3
        elif unused == 3:
            h[0]  += 0;h[1]  += 1;h[2]  += 2
        # 牌の並び替え
        if r == 1:
            h.insert(0, h[1])
            del(h[2])
        elif r == 2:
            h.insert(2, h[1])
            del(h[1])

        if kui < 3:
            h.insert(2, h[1])
            del(h[1])
        elif kui < 2:
            h.insert(2, h[1])
            del(h[1])

    # 加槓
    elif m & (1<<4):
        fuuro_label = 5
        added = (m & 0x0060) >> 5
        t = (m & 0xFE00) >> 9
        r = t % 3
        t = int(t / 3)
        t *= 4
        h = [t, t, t]
        if added == 0:
            h[0]  += 1;h[1]  += 2;h[2]  += 3
        elif added == 1:
            h[0]  += 0;h[1]  += 2;h[2]  += 3
        elif added == 2:
            h[0]  += 0;h[1]  += 1;h[2]  += 3
        elif added == 3:
            h[0]  += 0;h[1]  += 1;h[2]  += 2
        # 牌の並び替え
        if r == 1:
            h.insert(0, h[1])
            del(h[2])
        elif r == 2:
            h.insert(2, h[1])
            del(h[1])
        
    # 北抜き
    elif m & (1<<5):
        return "未実装"

    # 暗槓, 明槓
    else:   
        hai0 = (m & 0xFF00) >> 8
        if not kui:
            hai0 = (hai0 & ~3) + 3 # 暗槓
            fuuro_label = 4
        else:
            fuuro_label = 2       
        t = int(hai0 / 4) * 4
        h = [t, t, t]
        unco = hai0 % 4
        if unco == 0:
            h[0] += 1;h[1] += 2;h[2] += 3
        elif unco == 1:
            h[0] += 0;h[1] += 2;h[2] += 3
        elif unco == 2:
            h[0] += 0;h[1] += 1;h[2] += 3
        elif unco == 3:
            h[0] += 0;h[1] += 1;h[2] += 2
        if kui==1:
            a = hai0;hai0 = h[2];h[2] = a
        if kui==2:
            a = hai0;hai0 = h[0];h[0] = a

    return fuuro_label, h


if __name__ == '__main__':  
    m = 57567
    h = decode_m(m)
    print(h)